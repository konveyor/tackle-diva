/*
Copyright IBM Corporation 2021

Licensed under the Eclipse Public License 2.0, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

package io.tackle.diva;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.function.Supplier;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.SourceDirectoryTreeModule;
import com.ibm.wala.ipa.callgraph.AnalysisOptions;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ipa.callgraph.CallGraphStats;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.config.FileOfClasses;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.analysis.JPAAnalysis;
import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaSourceLoaderImpl;

public class Standalone {

    public static void main(String[] args) throws Exception {

        Options options = new Options();

        options.addOption("s", "source", true, "source path");
        options.addOption("c", "contexts", true, "contexts yaml file");

        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = null;
        try {
            cmd = parser.parse(options, args);
            if (!cmd.hasOption("source")) {
                throw new RuntimeException();
            }
        } catch (Exception e) {
            HelpFormatter hf = new HelpFormatter();
            hf.printHelp("[opts]", options);
            return;
        }
        Util.injectedCall(DivaIRGen.advices(), Standalone.class.getName() + ".run", cmd);
    }

    public static void run(CommandLine cmd) throws Exception {
        AnalysisScope scope = new JavaSourceAnalysisScope() {
            @Override
            public boolean isApplicationLoader(IClassLoader loader) {
                return loader.getReference() == ClassLoaderReference.Application
                        || loader.getReference() == JavaSourceAnalysisScope.SOURCE;
            }
        };
        addDefaultExclusions(scope);
        // add standard libraries to scope
        String[] stdlibs = Framework.loadStandardLib(scope);
        // add the source directory
        String[] sourceDirs = cmd.getOptionValue("source").split(":");
        for (String sourceDir : sourceDirs) {
            scope.addToScope(JavaSourceAnalysisScope.SOURCE, new SourceDirectoryTreeModule(new File(sourceDir)));
        }

        // build the class hierarchy
        IClassHierarchy cha = ClassHierarchyFactory.makeWithRoot(scope,
                new ECJClassLoaderFactory(scope.getExclusions()) {
                    @Override
                    protected JavaSourceLoaderImpl makeSourceLoader(ClassLoaderReference classLoaderReference,
                            IClassHierarchy cha, IClassLoader parent) {
                        return new DivaSourceLoaderImpl(classLoaderReference, parent, cha, stdlibs);
                    }
                });
        Util.LOGGER.info(cha.getNumberOfClasses() + " classes");
        Util.LOGGER.info(Warnings.asString());

        IClassLoader apploader = cha.getLoader(JavaSourceAnalysisScope.SOURCE);

        List<IMethod> entries = new ArrayList<>();
        entries.addAll(ServletAnalysis.getEntries(cha));
        entries.addAll(SpringBootAnalysis.getEntries(cha));

        List<IMethod> cgEntries = new ArrayList<>();
        cgEntries.addAll(entries);
        cgEntries.addAll(SpringBootAnalysis.getInits(cha));

        JPAAnalysis.getEntities(cha);

        CallGraph cg = gengraph(scope, cha, apploader, cgEntries);

        Framework fw = new Framework(cha, cg);

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                fw.recordContraint(new Context.EntryConstraint(n));
            }
        }
        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Context> contexts;
        if (!cmd.hasOption("contexts")) {
            contexts = Context.calculateDefaultContexts(fw);
        } else {
            contexts = Context.loadContexts(fw, cmd.getOptionValue("contexts"));
        }

        List<Object> res = new ArrayList<>();
        Report report = new Util.JsonReport(res);

        for (Context cxt : contexts) {
            CGNode entry = null;
            for (Context.Constraint c : cxt) {
                if (c instanceof Context.EntryConstraint) {
                    entry = ((Context.EntryConstraint) c).node();
                }
            }
            if (entry != null) {
                CGNode n = entry;
                report.add((Report.Named map) -> {
                    for (Context.Constraint c : cxt) {
                        c.report(map);
                    }
                    map.put("transactions", (Report txs) -> {
                        fw.calculateTransactions(n, cxt, txs);
                    });
                });
            }
        }

        try (Writer f = new FileWriter("transaction.json")) {
            f.write(Util.JSON_SERIALIZER.writeValueAsString(res));
        }
        try (Writer f = new FileWriter("transaction.yml")) {
            f.write(Util.YAML_SERIALIZER.writeValueAsString(res));
        }
    }

    public static CallGraph gengraph(AnalysisScope scope, IClassHierarchy cha, IClassLoader apploader,
            Collection<? extends IMethod> entries) throws IOException, CancelException {
        AnalysisOptions options = new AnalysisOptions();
        // CallGraphBuilder<InstanceKey> builder = Framework.rtaBuilder(cha, scope,
        // options, entries);
        Supplier<CallGraph> builder = Framework.chaCgBuilder(cha, options, entries);

        Util.LOGGER.info("building call graph...");
        // CallGraph cg = builder.makeCallGraph(options, null);
        CallGraph cg = builder.get();
        Util.LOGGER.info("done");
        Util.LOGGER.info(CallGraphStats.getStats(cg));
        // Util.dumpCallGraph(cg);
        return cg;
    }

    public static void addDefaultExclusions(AnalysisScope scope) throws UnsupportedEncodingException, IOException {
        scope.setExclusions(new FileOfClasses(new ByteArrayInputStream(EXCLUSIONS.getBytes("UTF-8"))));
    }

    private static final String EXCLUSIONS = "java\\/awt\\/.*\n" + "javax\\/awt\\/.*\n" + "javax\\/swing\\/.*\n"
            + "sun\\/.*\n" + /* "com\\/.*\n" + */ "jdk\\/.*\n" + "oracle\\/.*\n" + "apple\\/.*\n" + "netscape\\/.*\n"
            + "javafx\\/.*\n" + "org\\/w3c\\/.*\n" + "org\\/xml\\/.*\n" + "org\\/jcp\\/.*\n" + "org\\/ietf\\/.*\n"
            + "org\\/omg\\/.*\n" + "java\\/security\\/.*\n" + "java\\/beans\\/.*\n" + "java\\/time\\/.*\n"
            + "java\\/text\\/.*\n" + "java\\/net\\/.*\n" + "java\\/nio\\/.*\n" /* + "java\\/io\\/.*\n" */
            + "java\\/math\\/.*\n" + "java\\/applet\\/.*\n" + "java\\/rmi\\/.*\n" + "";

}

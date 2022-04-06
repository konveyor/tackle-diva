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
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Supplier;
import java.util.jar.JarFile;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.apache.commons.io.FileUtils;

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.BinaryDirectoryTreeModule;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.JarFileModule;
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

import io.tackle.diva.analysis.JDBCAnalysis;
import io.tackle.diva.analysis.JPAAnalysis;
import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaSourceLoaderImpl;
import io.tackle.diva.irgen.FilteredClassHierarchy;

public class Standalone {

    public static void main(String[] args) throws Exception {

        Options options = new Options();

        options.addOption("s", "source", true, "source path");
        options.addOption("b", "binary", true, "binary path");
        options.addOption("c", "contexts", true, "contexts yaml file");
        options.addOption("u", "usage", true, "enable usage analysis");

        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = null;
        try {
            cmd = parser.parse(options, args);
            if (!cmd.hasOption("source") && !cmd.hasOption("binary")) {
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
                return loader.getReference().equals(ClassLoaderReference.Application)
                        || loader.getReference().equals(JavaSourceAnalysisScope.SOURCE);
            }
        };
        addDefaultExclusions(scope);

        Path temp = Files.createTempDirectory("diva-temp");
        Util.LOGGER.info("tempdir=" + temp);

        // add standard libraries to scope
        String[] stdlibs = Framework.loadStandardLib(scope, temp);

        if (cmd.hasOption("source")) {
            // add the source directory

            String[] sourceDirs = cmd.getOptionValue("source").split(":");
            for (String sourceDir : sourceDirs) {
                scope.addToScope(JavaSourceAnalysisScope.SOURCE, new SourceDirectoryTreeModule(new File(sourceDir)));
            }

        } else if (cmd.hasOption("binary")) {

            List<String> classRoots = new ArrayList<>();
            List<String> jars = new ArrayList<>();

            String[] binaryFiles = cmd.getOptionValue("binary").split(":");

            for (String s : binaryFiles) {
                if (new File(s).isDirectory()) {
                    classRoots.add(s);
                } else if (s.endsWith(".ear") || s.endsWith(".war")) {
                    Framework.unpackArchives(s, temp.resolve("unpacked"), classRoots, jars);
                } else if (Framework.checkSpringBoot(s)) {
                    Framework.unpackArchives(s, temp.resolve("unpacked"), classRoots, jars);
                } else {
                    jars.add(s);
                }
            }

            for (String classRoot : classRoots) {
                scope.addToScope(ClassLoaderReference.Application, new BinaryDirectoryTreeModule(new File(classRoot)));
            }
            for (String jar : jars) {
                scope.addToScope(ClassLoaderReference.Application, new JarFileModule(new JarFile(jar)));
            }
        }

        FileUtils.forceDeleteOnExit(temp.toFile());

        DivaIRGen.init();

        // build the class hierarchy
        IClassHierarchy cha = ClassHierarchyFactory.makeWithRoot(scope,
                new ECJClassLoaderFactory(scope.getExclusions()) {
                    @Override
                    protected JavaSourceLoaderImpl makeSourceLoader(ClassLoaderReference classLoaderReference,
                            IClassHierarchy cha, IClassLoader parent) {
                        return new DivaSourceLoaderImpl(classLoaderReference, parent, cha, stdlibs);
                    }
                });
        Util.LOGGER.info("Done class hierarchy: " + cha.getNumberOfClasses() + " classes");
        Util.LOGGER.fine(Warnings.asString());

        Set<IClass> relevantClasses = new HashSet<>();
        Set<IClass> appClasses = new HashSet<>();
        Framework.relevantJarsAnalysis(cha, relevantClasses, appClasses,
                c -> JDBCAnalysis.checkRelevance(c) || JPAAnalysis.checkRelevance(c));

        IClassHierarchy filteredCha = new FilteredClassHierarchy(cha, appClasses::contains);
        IClassHierarchy relevantCha = new FilteredClassHierarchy(cha, relevantClasses::contains);

        List<IMethod> entries = new ArrayList<>();
        entries.addAll(ServletAnalysis.getEntries(filteredCha));
        entries.addAll(SpringBootAnalysis.getEntries(filteredCha));

        List<IMethod> cgEntries = new ArrayList<>();
        cgEntries.addAll(entries);
        cgEntries.addAll(SpringBootAnalysis.getInits(relevantCha));

        JPAAnalysis.getEntities(cha);

        if (entries.isEmpty()) {
            Util.LOGGER.info("No entry methods found");
            return;
        }

        CallGraph cg = gengraph(scope, relevantCha, cgEntries, relevantClasses);

        Framework fw = new Framework(cha, cg, cmd.hasOption("usage"));

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                fw.recordContraint(new Constraint.EntryConstraint(n));
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
            for (Constraint c : cxt) {
                if (c instanceof Constraint.EntryConstraint) {
                    entry = ((Constraint.EntryConstraint) c).node();
                }
            }
            if (entry != null) {
                CGNode n = entry;
                report.add((Report.Named map) -> {
                    for (Constraint c : cxt) {
                        c.report(map);
                    }
                    map.put(Report.TRANSACTIONS, (Report txs) -> {
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

    public static CallGraph gengraph(AnalysisScope scope, IClassHierarchy cha, Collection<? extends IMethod> entries,
            Set<IClass> relevantClasses) throws IOException, CancelException {
        AnalysisOptions options = new AnalysisOptions();
        // CallGraphBuilder<InstanceKey> builder = Framework.rtaBuilder(cha, scope,
        // options, entries);
        Supplier<CallGraph> builder = Framework.chaCgBuilder(cha, options, entries,
                m -> relevantClasses.contains(m.getDeclaringClass()));

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

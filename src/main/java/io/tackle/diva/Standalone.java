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
import java.util.Map;
import java.util.Map.Entry;
import java.util.function.Supplier;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
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
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.config.FileOfClasses;
import com.ibm.wala.util.strings.StringStuff;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.Context.Constraint;
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
                        return new DivaSourceLoaderImpl(classLoaderReference, parent, cha, false, classLoaderReference, stdlibs);
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

        CallGraph cg = gengraph(scope, cha, apploader, cgEntries);

        Framework fw = new Framework(cha, cg);

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                fw.recordContraint(new EntryConstraint(n));
            }
        }
        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Context> contexts;
        if (!cmd.hasOption("contexts")) {
            contexts = calculateDefaultContexts(fw);
        } else {
            contexts = loadContexts(fw, cmd.getOptionValue("contexts"));
        }

        List<Object> res = new ArrayList<>();
        Report report = new Util.JsonReport(res);

        for (Context cxt : contexts) {
            CGNode entry = null;
            for (Context.Constraint c : cxt) {
                if (c instanceof EntryConstraint) {
                    entry = ((EntryConstraint) c).node();
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

    public static List<Context> calculateDefaultContexts(Framework fw) throws IOException {
        // calculate cross product of constraint groups
        List<Context> result = new ArrayList<>();

        int[] counter = new int[fw.constraints.size()];
        List<Context.Constraint>[] cs = new List[fw.constraints.size()];

        int k = 0;
        for (List<Context.Constraint> c : fw.constraints.values()) {
            counter[k] = 0;
            cs[k] = c;
            k++;
        }

        outer: while (true) {
            Context cxt = new Context();

            for (k = 0; k < cs.length; k++) {
                cxt.add(cs[k].get(counter[k]));
            }

            result.add(cxt);

            counter[cs.length - 1] += 1;
            for (k = cs.length - 1; k >= 0; k--) {
                if (counter[k] < cs[k].size()) {
                    break;
                }
                if (k == 0)
                    break outer;
                counter[k] = 0;
                counter[k - 1] += 1;
            }
        }

        List<Object> json = new ArrayList<>();
        Report report = new Util.JsonReport(json);
        for (Context cxt : result) {
            report.add((Report.Named map) -> {
                for (Context.Constraint c : cxt) {
                    c.report(map);
                }
            });

        }
        try (Writer f = new FileWriter("contexts.yml")) {
            f.write(Util.YAML_SERIALIZER.writeValueAsString(json));
        }

        return result;
    }

    public static List<Context> loadContexts(Framework fw, String file)
            throws JsonParseException, JsonMappingException, IOException {

        List<Map<String, Map<String, List<String>>>> data = (List<Map<String, Map<String, List<String>>>>) Util.YAML_SERIALIZER
                .readValue(new File(file), Object.class);

        List<Context> result = new ArrayList<>();

        for (Map<String, Map<String, List<String>>> e : data) {
            Context cxt = new Context();
            for (Entry<String, Map<String, List<String>>> e2 : e.entrySet()) {
                for (Entry<String, List<String>> e3 : e2.getValue().entrySet()) {
                    for (Constraint c : fw.constraints.get(Pair.make(e2.getKey(), e3.getKey()))) {
                        if (e3.getValue().contains(c.value())) {
                            cxt.add(c);
                        }
                    }
                }
            }
            result.add(cxt);
        }

        return result;
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

    public static class EntryConstraint implements Context.Constraint {

        public EntryConstraint(CGNode node) {
            super();
            this.node = node;
        }

        CGNode node;

        @Override
        public String category() {
            return "entry";
        }

        @Override
        public String type() {
            return "methods";
        }

        @Override
        public String value() {
            IMethod method = node.getMethod();
            return StringStuff.jvmToBinaryName(method.getDeclaringClass().getName().toString()) + "."
                    + method.getName().toString();
        }

        public CGNode node() {
            return node;
        }
    }

}

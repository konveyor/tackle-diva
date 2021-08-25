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
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.function.Supplier;

import org.junit.Ignore;
import org.junit.Test;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.BinaryDirectoryTreeModule;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.SourceDirectoryTreeModule;
import com.ibm.wala.ipa.callgraph.AnalysisOptions;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ipa.callgraph.CallGraphStats;
import com.ibm.wala.ipa.callgraph.Entrypoint;
import com.ibm.wala.ipa.callgraph.impl.DefaultEntrypoint;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.config.FileOfClasses;
import com.ibm.wala.util.strings.StringStuff;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.Context.Constraint;
import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaSourceLoaderImpl;

public class DaytraderTest {

    public static void main(String[] args) throws Exception {
        // fromBinary();
        Util.injectedCall(DivaIRGen.advices(), DaytraderTest.class.getName() + ".fromSource");
    }

    @Test
    public void fromSourceTest() throws Exception {
        Util.injectedCall(DivaIRGen.advices(), DaytraderTest.class.getName() + ".fromSource");
    }

    @Ignore
    @Test
    public void fromBinaryTest() throws Exception {
        fromBinary();
    }

    public static void fromSource() throws Exception {
        long start = System.currentTimeMillis();
        // JavaSourceAnalysisEngine engine = new ECJJavaSourceAnalysisEngine();
        // EclipseSourceFileModule.createEclipseSourceFileModule(selectedIte

        // String[] sourceDirs = new String[] {
        // "/Users/akihiko/work/ocp/daytrader-example-webrepo/daytrader-webapp/daytrader-web/src/main/java/"
        // };
        String[] sourceDirs = new String[] { "../sample.daytrader7/daytrader-ee7-web/src/main/java/",
                "../sample.daytrader7/daytrader-ee7-ejb/src/main/java/" };
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
        System.out.println(cha.getNumberOfClasses() + " classes");
        System.out.println(Warnings.asString());

        checkCha(cha);

        IClassLoader apploader = cha.getLoader(JavaSourceAnalysisScope.SOURCE);

        IClass tradeServletAction = apploader.lookupClass(TypeName.string2TypeName(StringStuff
                .deployment2CanonicalTypeString("com.ibm.websphere.samples.daytrader.web.TradeServletAction")));
        IClass tradeAppServlet = apploader.lookupClass(TypeName.string2TypeName(
                StringStuff.deployment2CanonicalTypeString("com.ibm.websphere.samples.daytrader.web.TradeAppServlet")));

        List<IMethod> entries = new ArrayList<>();

        for (IMethod m : tradeAppServlet.getDeclaredMethods()) {
            if (m.getName().toString().equals("doGet") || m.getName().toString().equals("doPost")) {
                entries.add(m);
            }
        }

        CallGraph cg = gengraph(start, scope, cha, apploader, entries);

        doAnalysis(cha, entries, cg);
    }

    public static void fromBinary() throws Exception {

        long start = System.currentTimeMillis();

        String[] classDirs = new String[] { "../sample.daytrader7/daytrader-ee7-web/target/classes/",
                "../sample.daytrader7/daytrader-ee7-ejb/target/classes/" };
        AnalysisScope scope = AnalysisScope.createJavaAnalysisScope();
        // set exclusions. we use these exclusions as standard for handling JDK 8
        addDefaultExclusions(scope);
        String[] stdlibs = Framework.loadStandardLib(scope);
        // add the source directory
        for (String sourceDir : classDirs) {
            scope.addToScope(ClassLoaderReference.Application, new BinaryDirectoryTreeModule(new File(sourceDir)));
        }

        IClassHierarchy cha = ClassHierarchyFactory.makeWithRoot(scope);

        checkCha(cha);

        System.out.println(cha.getNumberOfClasses() + " classes");
        System.out.println(Warnings.asString());
        Warnings.clear();

        IClassLoader apploader = cha.getLoader(ClassLoaderReference.Application);

        IClass tradeServletAction = apploader.lookupClass(TypeName.string2TypeName(StringStuff
                .deployment2CanonicalTypeString("com.ibm.websphere.samples.daytrader.web.TradeServletAction")));

        IClass tradeAppServlet = apploader.lookupClass(TypeName.string2TypeName(
                StringStuff.deployment2CanonicalTypeString("com.ibm.websphere.samples.daytrader.web.TradeAppServlet")));

        List<IMethod> entries = new ArrayList<>();

        for (IMethod m : tradeAppServlet.getDeclaredMethods()) {
            if (m.getName().toString().equals("doGet") || m.getName().toString().equals("doPost")) {
                entries.add(m);
            }
        }

        CallGraph cg = gengraph(start, scope, cha, apploader, entries);

        doAnalysis(cha, entries, cg);

        // AnalysisOptions options = new AnalysisOptions();
        // Iterable<Entrypoint> entrypoints = entryClass != null ?
        // makePublicEntrypoints(scope, null, entryClass)
        // : com.ibm.wala.ipa.callgraph.impl.Util.makeMainEntrypoints(scope, cha,
        // mainClass);
        // options.setEntrypoints(entrypoints);
        // // you can dial down reflection handling if you like
        // // options.setReflectionOptions(ReflectionOptions.NONE);
        // AnalysisCache cache = new AnalysisCacheImpl();
        // // other builders can be constructed with different Util methods
        // // AnalysisCache cache = new
        // // AnalysisCacheImpl(AstIRFactory.makeDefaultFactory());
        //
        // CallGraphBuilder builder =
        // com.ibm.wala.ipa.callgraph.impl.Util.makeZeroOneContainerCFABuilder(options,
        // cache,
        // cha, scope);
        //
        // // CallGraphBuilder builder = Util.makeNCFABuilder(2, options, cache, cha,
        // // scope);
        // // CallGraphBuilder builder = Util.makeVanillaNCFABuilder(2, options, cache,
        // // cha, scope);
        // System.out.println("building call graph...");
        // CallGraph cg = builder.makeCallGraph(options, null);
        // long end = System.currentTimeMillis();
        // System.out.println("done");
        // System.out.println("took " + (end - start) + "ms");
        // System.out.println(CallGraphStats.getStats(cg));

    }

    private static Iterable<Entrypoint> makePublicEntrypoints(AnalysisScope scope, IClassHierarchy cha,
            String entryClass) {
        Collection<Entrypoint> result = new ArrayList<Entrypoint>();
        IClass klass = cha.lookupClass(TypeReference.findOrCreate(ClassLoaderReference.Application,
                StringStuff.deployment2CanonicalTypeString(entryClass)));
        for (IMethod m : klass.getDeclaredMethods()) {
            if (m.isPublic()) {
                result.add(new DefaultEntrypoint(m, cha));
            }
        }
        return result;
    }

    public static void checkCha(IClassHierarchy cha) {
        String mainClass = "org.apache.geronimo.daytrader.javaee6.web.TradeAppServlet";

        HashSet<String> packages = new HashSet<>();
        for (IClass c : cha) {
            String k = StringStuff.jvmToBinaryName(c.getName().toString());
            int j = k.indexOf('.');
            String p = k;
            if (j >= 0) {
                j = k.indexOf('.', j + 1) < 0 ? j : k.indexOf('.', j + 1);
                p = k.substring(0, j);
            }
            packages.add(p);
            // if (k.contains("daytrader")) {
            // if (k.contains("TradeServletAction")) {
            // System.out.println("HERE");
            // }
            // System.out.println(k);
            // }
            if (k.contains("unknown")) {
                System.out.println(k);
                TypeReference ref = TypeReference.findOrCreate(c.getClassLoader().getReference(), c.getName());
                System.out.println(cha.lookupClass(ref));
            }
            if (!k.contains(".") || k.contains("<")) {
                System.out.println(k + ": " + c);
            }
        }

        for (TypeReference c : cha.getUnresolvedClasses()) {
            String k = StringStuff.jvmToBinaryName(c.getName().toString());
            int j = k.indexOf('.');
            String p = k;
            if (j >= 0) {
                j = k.indexOf('.', j + 1) < 0 ? j : k.indexOf('.', j + 1);
                p = k.substring(0, j);
            }
            packages.add(p);
            if (k.contains("daytrader")) {
                System.out.println(k);
            }

        }
        System.out.println(packages);
    }

    public static CallGraph gengraph(long start, AnalysisScope scope, IClassHierarchy cha, IClassLoader apploader,
            Collection<? extends IMethod> entries) throws IOException, CancelException {
        AnalysisOptions options = new AnalysisOptions();
        // CallGraphBuilder<InstanceKey> builder = Framework.rtaBuilder(cha, scope,
        // options, entries);
        Supplier<CallGraph> builder = Framework.chaCgBuilder(cha, options, entries);

        System.out.println("building call graph...");
        // CallGraph cg = builder.makeCallGraph(options, null);
        CallGraph cg = builder.get();
        long end = System.currentTimeMillis();
        System.out.println("done");
        System.out.println("took " + (end - start) + "ms");
        System.out.println(CallGraphStats.getStats(cg));

        try (PrintWriter out = new PrintWriter(new FileWriter("res.dot"))) {
            out.println("digraph {");
            out.println("node[shape=plaintext]");
            out.println("rankdir=LR");

            for (CGNode src : cg) {
                if (!src.toString().contains("daytrader") && !src.toString().contains("sql"))
                    continue;
                out.println("n" + src.getGraphNodeId() + " [label=\"" + src.toString() + "\"]");
            }
            for (CGNode src : cg) {
                if (!src.toString().contains("daytrader") && !src.toString().contains("sql"))
                    continue;
                for (CGNode tgt : (Iterable<CGNode>) () -> cg.getSuccNodes(src)) {
                    if (!tgt.toString().contains("daytrader") && !tgt.toString().contains("sql"))
                        continue;
                    out.println("n" + src.getGraphNodeId() + " -> n" + tgt.getGraphNodeId());
                }
            }
            out.println("}");
        }
        return cg;
    }

    public static void doAnalysis(IClassHierarchy cha, List<IMethod> entries, CallGraph cg)
            throws IOException, JsonProcessingException {
        Framework fw = new Framework(cha, cg);

        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Object> res = new ArrayList<>();
        Report report = new Util.JsonReport(res);

        for (CGNode n : cg) {
            if (n.getMethod() == entries.get(0)) {
                for (Constraint c : fw.constraints.get(Pair.make("http-param", "action"))) {
                    report.add((Report.Named map) -> {
                        map.put("entry", n.getMethod().toString());
                        c.report(map);
                        map.put("transactions", (Report txs) -> {
                            fw.calculateTransactions(n, new Context(Collections.singleton(c)), txs);
                        });
                    });
                }
            }
        }

        try (Writer f = new FileWriter("transaction.json")) {
            f.write(Util.JSON_SERIALIZER.writeValueAsString(res));
        }
        try (Writer f = new FileWriter("transaction.yml")) {
            f.write(Util.YAML_SERIALIZER.writeValueAsString(res));
        }
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

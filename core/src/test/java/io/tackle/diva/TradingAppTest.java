package io.tackle.diva;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Supplier;

import org.apache.commons.io.FileUtils;
import org.junit.Test;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.IClass;
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
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.strings.StringStuff;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaSourceLoaderImpl;

public class TradingAppTest {

    public static void main(String[] args) throws Exception {
        // fromBinary();
        Util.injectedCall(DivaIRGen.advices(), TradingAppTest.class.getName() + ".fromSource");
    }

    @Test
    public void fromSourceTest() throws Exception {
        Util.injectedCall(DivaIRGen.advices(), TradingAppTest.class.getName() + ".fromSource");
    }

    public static void fromSource() throws Exception {
        long start = System.currentTimeMillis();

        String[] sourceDirs = new String[] { "../../trading-app" };
        AnalysisScope scope = new JavaSourceAnalysisScope() {
            @Override
            public boolean isApplicationLoader(IClassLoader loader) {
                return loader.getReference() == ClassLoaderReference.Application
                        || loader.getReference() == JavaSourceAnalysisScope.SOURCE;
            }
        };
        Standalone.addDefaultExclusions(scope);
        Path tmpDir = Paths.get(".", "tmp");

        // add standard libraries to scope
        String[] stdlibs = Framework.loadStandardLib(scope, tmpDir);
        // add the source directory
        for (String sourceDir : sourceDirs) {
            scope.addToScope(JavaSourceAnalysisScope.SOURCE, new SourceDirectoryTreeModule(new File(sourceDir)));
        }

        FileUtils.forceDeleteOnExit(tmpDir.toFile());

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
        System.out.println(cha.getNumberOfClasses() + " classes");
        System.out.println(Warnings.asString());

        checkCha(cha);

        IClassLoader apploader = cha.getLoader(JavaSourceAnalysisScope.SOURCE);

        Set<IMethod> entries = new LinkedHashSet<>();

        for (IClass c : cha) {
            if (c.getClassLoader().getReference().equals(ClassLoaderReference.Primordial))
                continue;
            for (IMethod m : c.getDeclaredMethods()) {
                if (c.getName().toString().endsWith("Controller") && m.getName() != Constants.theClinit
                        && m.getName() != Constants.theInit) {
                    entries.add(m);
                }
                if (m.getName() == Constants.theInit
                        && Util.any(Util.getAnnotations(m), a -> a.getType().getName() == Constants.LSpringAutowired)) {
                    entries.add(m);
                }
            }
        }

        CallGraph cg = gengraph(start, scope, cha, apploader, entries);

        doAnalysis(cha, entries, cg);
    }

    public static void checkCha(IClassHierarchy cha) {
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

        Util.dumpCallGraph(cg);

        return cg;
    }

    public static void doAnalysis(IClassHierarchy cha, Set<IMethod> entries, CallGraph cg)
            throws IOException, JsonProcessingException {
        Framework fw = new Framework(cha, cg);

        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Object> res = new ArrayList<>();
        Report report = new Util.JsonReport(res);

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                report.add((Report.Named map) -> {
                    map.put("entry", n.getMethod().toString());
                    map.put("transactions", (Report txs) -> {
                        fw.calculateTransactions(n, new Context(Collections.emptySet()), txs);
                    });
                });
            }
        }

        String cname = Thread.currentThread().getStackTrace()[1].getClassName().replace('.', '_');
        try (Writer f = new FileWriter("transaction-" + cname + ".json")) {
            f.write(Util.JSON_SERIALIZER.writeValueAsString(res));
        }
        try (Writer f = new FileWriter("transaction-" + cname + ".yml")) {
            f.write(Util.YAML_SERIALIZER.writeValueAsString(res));
        }
    }

}

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

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.net.URI;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.jar.JarFile;
import java.util.stream.Stream;

import org.apache.commons.io.FileUtils;

import com.ibm.wala.analysis.reflection.ReflectionContextInterpreter;
import com.ibm.wala.cast.ipa.callgraph.AstContextInsensitiveSSAContextInterpreter;
import com.ibm.wala.cast.ir.ssa.AstIRFactory;
import com.ibm.wala.cast.java.client.impl.ZeroCFABuilderFactory;
import com.ibm.wala.classLoader.BinaryDirectoryTreeModule;
import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.IMethod.SourcePosition;
import com.ibm.wala.ipa.callgraph.AnalysisCache;
import com.ibm.wala.ipa.callgraph.AnalysisCacheImpl;
import com.ibm.wala.ipa.callgraph.AnalysisOptions;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ipa.callgraph.CallGraphBuilder;
import com.ibm.wala.ipa.callgraph.ContextSelector;
import com.ibm.wala.ipa.callgraph.Entrypoint;
import com.ibm.wala.ipa.callgraph.cha.CHACallGraph;
import com.ibm.wala.ipa.callgraph.impl.ClassHierarchyClassTargetSelector;
import com.ibm.wala.ipa.callgraph.impl.ClassHierarchyMethodTargetSelector;
import com.ibm.wala.ipa.callgraph.impl.DefaultContextSelector;
import com.ibm.wala.ipa.callgraph.impl.DefaultEntrypoint;
import com.ibm.wala.ipa.callgraph.propagation.InstanceKey;
import com.ibm.wala.ipa.callgraph.propagation.SSAContextInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.cfa.DefaultSSAInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.cfa.DelegatingSSAContextInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.rta.BasicRTABuilder;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAOptions;
import com.ibm.wala.ssa.SSAPutInstruction;
import com.ibm.wala.ssa.SymbolTable;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.FieldReference;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.MutableIntSet;

import io.tackle.diva.analysis.JDBCAnalysis;
import io.tackle.diva.analysis.JPAAnalysis;
import io.tackle.diva.analysis.QuarkusAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.irgen.DivaPhantomClass;

public class Framework {

    public Framework(IClassHierarchy cha, CallGraph callgraph) {
        super();
        this.cha = cha;
        this.callgraph = callgraph;
    }

    IClassHierarchy cha;
    CallGraph callgraph;

    public CallGraph callgraph() {
        return callgraph;
    }

    public IClassHierarchy classHierarchy() {
        return cha;
    }

    public static String[] loadStandardLib(AnalysisScope scope) throws IOException {
        String javaVersion = System.getProperty("java.specification.version");
        String javaHome = System.getProperty("java.home");
        Util.LOGGER.info("java.specification.version=" + javaVersion);
        Util.LOGGER.info("java.home=" + javaHome);
        // Util.LOGGER.info("java.class.path=" + System.getProperty("java.class.path"));

        List<String> stdlibs = new ArrayList<>();
        if (javaVersion.equals("1.8")) {
            Path libdir = Paths.get(System.getProperty("java.home"), "lib");
            Files.list(libdir).forEach(path -> {
                if (path.toString().endsWith(".jar")) {
                    stdlibs.add(path.toString());
                }
            });
        } else {
            // deep copy files in jrt module to temp dir
            Path temp = Files.createTempDirectory("diva-temp");
            Util.LOGGER.info("tempdir=" + temp);
            Runtime.getRuntime().addShutdownHook(new Thread() {
                @Override
                public void run() {
                    try {
                        FileUtils.deleteDirectory(temp.toFile());
                    } catch (IOException e) {
                    }
                }
            });
            Path javaBase = FileSystems.getFileSystem(URI.create("jrt:/")).getPath("modules", "java.base");
            Path javaSql = FileSystems.getFileSystem(URI.create("jrt:/")).getPath("modules", "java.sql");
            Stream.concat(Files.walk(javaBase), Files.walk(javaSql)).forEach(path -> {
                if (Files.isDirectory(path))
                    return;
                Path copy = temp;
                for (int k = 2; k < path.getNameCount(); k++) {
                    copy = copy.resolve(path.getName(k).toString());
                }
                try {
                    Files.createDirectories(copy.getParent());
                    Files.copy(path, copy);
                } catch (IOException e) {
                }
            });
            stdlibs.add(temp.toString());
        }
        String[] res = new String[stdlibs.size()];

        for (int k = 0; k < res.length; k++) {
            String stdlib = stdlibs.get(k);
            res[k] = stdlib;
            if (stdlib.endsWith(".jar")) {
                scope.addToScope(ClassLoaderReference.Primordial, new JarFile(stdlib));
            } else {
                scope.addToScope(ClassLoaderReference.Primordial, new BinaryDirectoryTreeModule(new File(stdlib)));
            }
        }
        return res;
    }

    public static Supplier<CallGraph> chaCgBuilder(IClassHierarchy cha, AnalysisOptions options,
            Iterable<? extends IMethod> entries) {
        List<Entrypoint> entryPoints = new ArrayList<>();

        for (IMethod m : entries) {
            entryPoints.add(new DefaultEntrypoint(m, cha));
            for (int i = 0; i < m.getNumberOfParameters(); i++) {
                if (cha.lookupClass(m.getParameterType(i)) == null) {
                    System.out.println("adding: " + m.getParameterType(i));
                    cha.addClass(new DivaPhantomClass(m.getParameterType(i), cha));
                }
            }
        }

        options.setEntrypoints(entryPoints);
        SSAOptions ssaOptions = new SSAOptions();
        ssaOptions.setDefaultValues(SymbolTable::getDefaultValue);

        AnalysisCache cache = new AnalysisCacheImpl(AstIRFactory.makeDefaultFactory(), ssaOptions);

        CHACallGraph cg = new CHACallGraph(cha, true);

        try {
            Field cgCache = CHACallGraph.class.getDeclaredField("cache");
            cgCache.setAccessible(true);
            cgCache.set(cg, cache);

        } catch (ReflectiveOperationException | IllegalArgumentException e) {
            throw new RuntimeException(e);
        }

        cg.setInterpreter(
                new DelegatingSSAContextInterpreter(new AstContextInsensitiveSSAContextInterpreter(options, cache),
                        new DefaultSSAInterpreter(options, cache)));

        return () -> {
            try {
                cg.init(entryPoints);
                return cg;
            } catch (CancelException e) {
                return null;
            }
        };
    }

    public static CallGraphBuilder<InstanceKey> rtaBuilder(IClassHierarchy cha, AnalysisScope scope,
            AnalysisOptions options, Iterable<? extends IMethod> entries) {
        List<Entrypoint> entryPoints = new ArrayList<>();

        for (IMethod m : entries) {
            entryPoints.add(new DefaultEntrypoint(m, cha));
            for (int i = 0; i < m.getNumberOfParameters(); i++) {
                if (cha.lookupClass(m.getParameterType(i)) == null) {
                    System.out.println("adding: " + m.getParameterType(i));
                    cha.addClass(new DivaPhantomClass(m.getParameterType(i), cha));
                }
            }
        }

        options.setEntrypoints(entryPoints);

        // options.setSelector(new ClassHierarchyClassTargetSelector(cha) {
        //
        // @Override
        // public IClass getAllocatedTarget(CGNode caller, NewSiteReference site) {
        // IClass c = super.getAllocatedTarget(caller, site);
        // if (c != null)
        // return c;
        // return cha.lookupClass(site.getDeclaredType());
        // }
        // });
        // options.setSelector(new ClassHierarchyMethodTargetSelector(cha) {
        //
        // @Override
        // public IMethod getCalleeTarget(CGNode caller, CallSiteReference call, IClass
        // receiver) {
        // IMethod m = super.getCalleeTarget(caller, call, receiver);
        // if (caller.toString().contains("daytrader") ||
        // call.toString().contains("daytrader")) {
        // System.out.println(caller + ", " + call + ", " + receiver + " -> " + m);
        // }
        // return m;
        // }
        //
        // });
        options.setSelector(new ClassHierarchyClassTargetSelector(cha));
        options.setSelector(new ClassHierarchyMethodTargetSelector(cha));

        SSAOptions ssaOptions = new SSAOptions();
        ssaOptions.setDefaultValues(SymbolTable::getDefaultValue);
        // you can dial down reflection handling if you like
        // options.setReflectionOptions(ReflectionOptions.NONE);
        // AnalysisCache cache = new AnalysisCacheImpl();
        // other builders can be constructed with different Util methods
        // AnalysisCache cache = new
        // AnalysisCacheImpl(AstIRFactory.makeDefaultFactory());
        AnalysisCache cache = new AnalysisCacheImpl(AstIRFactory.makeDefaultFactory(), ssaOptions);

        // CallGraphBuilder builder =
        // com.ibm.wala.ipa.callgraph.impl.Util.makeZeroOneContainerCFABuilder(options,
        // cache,
        // cha, scope);
        // new AstJavaSSAPropagationCallGraphBuilder(doSellMethod, options, cache, new
        // DefaultPointerKeyFactory()) {
        // };
        // AstSSAPropagationCallGraphBuilder.makeDefaultContextInterpreters(SSAContextInterpreter,
        // AnalysisOptions, IClassHierarchy)
        // ---------------------------------------------------
        // CallGraphBuilder<InstanceKey> builder = new
        // ZeroCFABuilderFactory().make(options, cache, cha, scope);

        SSAContextInterpreter c = new DefaultSSAInterpreter(options, cache);
        c = new DelegatingSSAContextInterpreter(new AstContextInsensitiveSSAContextInterpreter(options, cache) {

            @Override
            public Iterator<FieldReference> iterateFieldsRead(CGNode node) {
                if (node.getIR() == null)
                    return Collections.emptyIterator();
                return Util
                        .map(Util.<SSAInstruction>filter(() -> node.getIR().iterateNormalInstructions(),
                                i -> i instanceof SSAGetInstruction), i -> ((SSAGetInstruction) i).getDeclaredField())
                        .iterator();
            }

            @Override
            public Iterator<FieldReference> iterateFieldsWritten(CGNode node) {
                if (node.getIR() == null)
                    return Collections.emptyIterator();
                return Util
                        .map(Util.<SSAInstruction>filter(() -> node.getIR().iterateNormalInstructions(),
                                i -> i instanceof SSAPutInstruction), i -> ((SSAPutInstruction) i).getDeclaredField())
                        .iterator();
            }

        }, c);
        c = new DelegatingSSAContextInterpreter(
                ReflectionContextInterpreter.createReflectionContextInterpreter(cha, options, cache), c);

        ContextSelector def = new DefaultContextSelector(options, cha);

        BasicRTABuilder builder = new BasicRTABuilder(cha, options, cache, def, c);

        return builder;
    }

    public static CallGraphBuilder<InstanceKey> cfaBuilder(IClassHierarchy cha, AnalysisScope scope,
            AnalysisOptions options, Iterable<? extends IMethod> entries) {
        List<Entrypoint> entryPoints = new ArrayList<>();

        for (IMethod m : entries) {
            entryPoints.add(new DefaultEntrypoint(m, cha));
            for (int i = 0; i < m.getNumberOfParameters(); i++) {
                if (cha.lookupClass(m.getParameterType(i)) == null) {
                    System.out.println("adding: " + m.getParameterType(i));
                    cha.addClass(new DivaPhantomClass(m.getParameterType(i), cha));
                }
            }
        }

        options.setEntrypoints(entryPoints);

        SSAOptions ssaOptions = new SSAOptions();
        ssaOptions.setDefaultValues(SymbolTable::getDefaultValue);

        AnalysisCache cache = new AnalysisCacheImpl(AstIRFactory.makeDefaultFactory(), ssaOptions);

        CallGraphBuilder<InstanceKey> builder = new ZeroCFABuilderFactory().make(options, cache, cha, scope);

        return builder;
    }

    public void traverse(CGNode entry, Trace.Visitor visitor) {
        traverse(entry, visitor, false);
    }

    public void traverse(CGNode entry, Trace.Visitor visitor, boolean pathSensitive) {

        MutableIntSet visited = null;
        if (!pathSensitive) {
            visited = new BitVectorIntSet();
        }
        Stack<Trace> stack = new Stack<>();
        Stack<Iterator<CallSiteReference>> iters = new Stack<>();

        stack.push(new Trace(entry, null));
        iters.push(entry.iterateCallSites());
        if (!pathSensitive) {
            visited.add(entry.getGraphNodeId());
        }
        visitor.visitNode(stack.peek());

        while (!stack.isEmpty()) {
            Trace trace = stack.peek();

            if (!iters.peek().hasNext()) {
                trace.setSite(null);
                visitor.visitExit(trace);
                stack.pop();
                iters.pop();
                continue;
            }
            CallSiteReference site = iters.peek().next();

            if (!trace.in(site))
                continue;

            trace.setSite(site);

            visitor.visitCallSite(trace);

            Set<CGNode> targets = callgraph.getPossibleTargets(trace.node(), site);
            Iterable<CGNode> ts = targets;

            if (targets.isEmpty())
                continue;

            if (targets.size() > 1) {
                // should be virtual
                SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
                IClass self = trace.inferType(this, instr.getUse(0));
                if (self != null) {
                    ts = Util.filter(targets, n -> {
                        IClass c = n.getMethod().getDeclaringClass();
                        return Util.any(self.isInterface() ? c.getAllImplementedInterfaces() : Util.superChain(c),
                                i -> i == self);
                    });
                } else {
                    Util.LOGGER.info("Failing to determine target for " + site);
                }
            }

            for (CGNode n : ts) {
                if (n.getMethod().getDeclaringClass().getName().toString().startsWith("Ljava/")) {
                    continue;
                }
                if (pathSensitive) {
                    if (Util.any(trace, t -> t.node.getGraphNodeId() == n.getGraphNodeId()))
                        continue;
                } else if (visited.contains(n.getGraphNodeId())) {
                    continue;
                } else {
                    visited.add(n.getGraphNodeId());
                }
                stack.push(new Trace(n, trace));
                iters.push(n.iterateCallSites());

                visitor.visitNode(stack.peek());
                // skip the rest of targets
                // @TODO: we may create a call-target constraint in such a case.
                break;
            }
        }
    }

    public Report report;
    public Report transaction;
    public int transactionId;

    public void reportOperation(Trace trace, Consumer<Report.Named> named) {
        if (transaction == null) {
            report.add((Report.Named map) -> {
                map.put("txid", transactionId++);
                map.put("transaction", (Report v) -> {
                    transaction = v;
                });
            });
        }
        transaction.add((Report.Named map) -> {
            map.put("stacktrace", trace, _trace -> (Report stacktrace) -> {
                for (Trace t : _trace.reversed()) {
                    IMethod m = t.node().getMethod();
                    SourcePosition p = null;
                    try {
                        p = m.getSourcePosition(t.site().getProgramCounter());
                    } catch (InvalidClassFileException | NullPointerException e) {
                    }
                    SourcePosition pos = p;
                    stacktrace.add((Report.Named site) -> {
                        site.put("method", m.toString());
                        site.put("file", m.getDeclaringClass().getSourceFileName());
                        site.put("position", "" + pos);
                    });
                }
            });
            named.accept(map);
        });
    }

    public void reportSqlStatement(Trace trace, String stmt) {
        reportOperation(trace, map -> map.put("sql", stmt));
    }

    public void reportTxBoundary() {
        if (transaction != null) {
            transaction = null;
        }
    }

    public boolean txStarted() {
        return transaction != null;
    }

    public void calculateTransactions(CGNode entry, Context cxt, Report report, Trace.Visitor visitor) {
        this.report = report;
        this.transactionId = 0;
        traverse(entry, visitor, true);
        if (txStarted()) {
            reportTxBoundary();
        }
    }

    public void calculateTransactions(CGNode entry, Context cxt, Report report) {
        calculateTransactions(entry, cxt, report,
                JDBCAnalysis.getTransactionAnalysis(this, cxt)
                        .with(SpringBootAnalysis.getTransactionAnalysis(this, cxt)
                                .with(JPAAnalysis.getTransactionAnalysis(this, cxt))));

    }

    public void recordContraint(Context.Constraint c) {
        Pair<String, String> key = Pair.make(c.category(), c.type());
        if (!constraints.containsKey(key)) {
            constraints.put(key, new ArrayList<>());
        }
        constraints.get(key).add(c);
    }

    public Map<Pair<String, String>, List<Context.Constraint>> constraints = new LinkedHashMap<>();

}

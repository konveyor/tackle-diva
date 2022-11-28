/*
Copyright IBM Corporation 2021

Licensed under the Apache Public License 2.0, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

package io.tackle.diva;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.Field;
import java.net.URI;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Logger;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ibm.wala.analysis.reflection.ReflectionContextInterpreter;
import com.ibm.wala.cast.ipa.callgraph.AstContextInsensitiveSSAContextInterpreter;
import com.ibm.wala.cast.ir.ssa.AstIRFactory;
import com.ibm.wala.cast.java.client.impl.ZeroCFABuilderFactory;
import com.ibm.wala.classLoader.BinaryDirectoryTreeModule;
import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.IMethod.SourcePosition;
import com.ibm.wala.classLoader.JarFileEntry;
import com.ibm.wala.classLoader.ModuleEntry;
import com.ibm.wala.classLoader.ShrikeClass;
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
import com.ibm.wala.ipa.callgraph.impl.Everywhere;
import com.ibm.wala.ipa.callgraph.impl.FakeRootMethod;
import com.ibm.wala.ipa.callgraph.propagation.InstanceKey;
import com.ibm.wala.ipa.callgraph.propagation.SSAContextInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.cfa.DefaultSSAInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.cfa.DelegatingSSAContextInterpreter;
import com.ibm.wala.ipa.callgraph.propagation.rta.BasicRTABuilder;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.ClassConstants;
import com.ibm.wala.shrikeCT.ConstantPoolParser;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.ssa.AuxiliaryCache;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.IRFactory;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSACache;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAOptions;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAPutInstruction;
import com.ibm.wala.ssa.SymbolTable;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.FieldReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.collections.HashMapFactory;
import com.ibm.wala.util.collections.MapUtil;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.intset.BimodalMutableIntSet;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntSet;
import com.ibm.wala.util.intset.MutableIntSet;
import com.ibm.wala.util.ref.CacheReference;
import com.ibm.wala.util.strings.Atom;

import io.tackle.diva.analysis.DispatchAnalysis;
import io.tackle.diva.analysis.JDBCAnalysis;
import io.tackle.diva.analysis.JPAAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.irgen.DivaPhantomClass;

public class Framework {

    private static final Logger LOGGER = Logger.getLogger(Framework.class.getName());

    public Framework(IClassHierarchy cha, CallGraph callgraph) {
        this(cha, callgraph, false);
    }

    public Framework(IClassHierarchy cha, CallGraph callgraph, boolean usageAnalysis) {
        super();
        this.cha = cha;
        this.callgraph = callgraph;
        this.usageAnalysis = usageAnalysis;
        reachabilityAnalysis();
    }

    IClassHierarchy cha;
    public CallGraph callgraph;
    public boolean usageAnalysis;

    public CallGraph callgraph() {
        return callgraph;
    }

    public IClassHierarchy classHierarchy() {
        return cha;
    }

    public static String[] loadStandardLib(AnalysisScope scope, Path workDir) throws IOException {
        String javaVersion = System.getProperty("java.specification.version");
        String javaHome = System.getProperty("java.home");
        LOGGER.info("java.specification.version=" + javaVersion);
        LOGGER.info("java.home=" + javaHome);
        // LOGGER.info("java.class.path=" + System.getProperty("java.class.path"));

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
            Path temp = workDir.resolve("jrt");
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

    public static HttpClient httpClient = HttpClientBuilder.create().build();

    public static boolean checkMavenCentral(String sha1, String name) {
        try {
            if (name.startsWith("log4j") || name.startsWith("slf4j")) {
                return true;
            }
            HttpGet request = new HttpGet(
                    "https://search.maven.org/solrsearch/select?q=1:" + sha1 + "&rows=20&wt=json");
            request.addHeader("content-type", "application/json");

            HttpResponse response = httpClient.execute(request);

            Map<String, Map<String, Object>> res = new ObjectMapper().readValue(response.getEntity().getContent(),
                    Map.class);
            if (!res.get("response").get("numFound").equals(0)) {
                return true;
            }
        } catch (Exception e) {
            LOGGER.info("Failed to query central: " + name);
        }
        return false;
    }

    public static final Pattern patternWar = Pattern.compile(".*\\.war");
    public static final Pattern patternJar = Pattern.compile(".*\\.jar");
    public static final Pattern patternClasses = Pattern.compile(".*/classes$");
    static final Pattern patternClass = Pattern.compile(".*/classes/(.*)\\.class$");
    static final Pattern patternXhtml = Pattern.compile(".*\\.xhtml$");

    public static boolean checkSpringBoot(String jarFile) throws IOException, FileNotFoundException {
        JarFile jar = new java.util.jar.JarFile(jarFile);
        return jar.getJarEntry("BOOT-INF") != null;
    }

    public static void unpackArchives(String jarFile, Path workDir, List<String> classRoots, List<String> jars)
            throws IOException, FileNotFoundException {

        JarFile jar = new java.util.jar.JarFile(jarFile);
        Enumeration<JarEntry> enumEntries = jar.entries();

        while (enumEntries.hasMoreElements()) {
            JarEntry entry = enumEntries.nextElement();
            File file = workDir.resolve(entry.getName()).toFile();
            String fileName = file.getAbsolutePath().toString();
            if (!file.exists()) {
                file.getParentFile().mkdirs();
            }

            boolean mj = patternJar.matcher(fileName).find();
            if (mj) {
                String sha1 = DigestUtils.sha1Hex(jar.getInputStream(entry));
                if (checkMavenCentral(sha1, file.getName())) {
                    LOGGER.info("skpping " + sha1 + " " + file.getName());
                    // System.out.println("inMemoryIdentifier.addMapping(\"" + sha1 + "\", \"" +
                    // file.getName() + "\");");
                } else {
                    jars.add(fileName);
                }
            }

            if (entry.isDirectory()) {
                boolean mcs = patternClasses.matcher(fileName).find();
                if (mcs) {
                    classRoots.add(fileName);
                }
                continue;
            }

            Files.copy(jar.getInputStream(entry), file.toPath(), StandardCopyOption.REPLACE_EXISTING);

            boolean mw = patternWar.matcher(fileName).find();
            if (mw) {
                String warname = entry.getName().substring(0, entry.getName().lastIndexOf("."));
                String newWorkDir = workDir + java.io.File.separator + warname;
                unpackArchives(fileName, workDir.resolve(warname), classRoots, jars);
            }
        }
        jar.close();

    }

    public static Set<IClass> relevantJarsAnalysis(IClassHierarchy cha, Set<IClass> relevantClasses,
            Set<IClass> applicationClasses, Predicate<IClass> relevanceTest) {

        Map<String, Set<IClass>> defines = new HashMap<>();
        Map<String, Set<IClass>> references = new HashMap<>();
        Map<String, Set<String>> deps = new HashMap<>();

        for (IClass c : cha) {
            if (c.getClassLoader().getReference().equals(ClassLoaderReference.Primordial)) {
                continue;
            }
            if (!(c instanceof ShrikeClass)) {
                relevantClasses.add(c);
                applicationClasses.add(c);
                continue;
            }
            ShrikeClass sc = (ShrikeClass) c;
            ModuleEntry m = sc.getModuleEntry();
            if (!(m instanceof JarFileEntry)) {
                relevantClasses.add(c);
                applicationClasses.add(c);
                continue;
            }

            String jarName = ((JarFileEntry) m).getJarFile().getName();

            if (!defines.containsKey(jarName)) {
                defines.put(jarName, new HashSet<>());
            }
            defines.get(jarName).add(c);

            ConstantPoolParser cp = sc.getReader().getCP();
            for (int k = 1; k < cp.getItemCount(); k++) {
                if (cp.getItemType(k) == ClassConstants.CONSTANT_Class) {
                    String cref;
                    try {
                        cref = cp.getCPClass(k);
                    } catch (Exception e) {
                        continue;
                    }
                    // if (cref.equals("java/sql/Connection")) {
                    // System.out.println(c);
                    // }
                    IClass c2 = c.getClassLoader().lookupClass(TypeName.findOrCreate("L" + cref));
                    if (c2 == null)
                        continue;

                    if (!references.containsKey(jarName)) {
                        references.put(jarName, new HashSet<>());
                    }
                    references.get(jarName).add(c2);
                }
            }
        }

        List<String> next = new ArrayList<>(references.keySet());

        while (!next.isEmpty()) {
            List<String> todo = next;
            next = new ArrayList<>();
            for (String j : todo) {
                if (!references.containsKey(j)) {
                    references.put(j, new HashSet<>());
                }
                Set<IClass> rs = references.get(j);
                Set<String> js = new HashSet<>();
                for (Map.Entry<String, Set<IClass>> e2 : defines.entrySet()) {
                    if (e2.getKey().equals(j))
                        continue;
                    if (Util.any(rs, v -> e2.getValue().contains(v))) {
                        js.add(e2.getKey());
                    }
                }
                if (js.isEmpty())
                    continue;
                boolean mod = false;
                for (String j2 : js) {
                    Set<IClass> rs2 = references.getOrDefault(j2, Collections.emptySet());
                    if (rs.containsAll(rs2))
                        continue;
                    rs.addAll(rs2);
                    mod = true;
                }
                if (mod)
                    next.add(j);
            }
        }

        Set<String> relevantJars = new HashSet<>();

        for (Map.Entry<String, Set<IClass>> e : references.entrySet()) {
            if (Util.any(e.getValue(), relevanceTest)) {
                relevantJars.add(e.getKey());
            }
        }

        LOGGER.info("Relevant jars: " + relevantJars);

        for (String jar : relevantJars) {
            relevantClasses.addAll(defines.getOrDefault(jar, Collections.emptySet()));
        }
        return relevantClasses;
    }

    public static Predicate<IMethod> isRelevantMethod = null;

    public static Supplier<CallGraph> chaCgBuilder(IClassHierarchy cha, AnalysisOptions options,
            Iterable<? extends IMethod> entries) {
        return chaCgBuilder(cha, options, entries,
                m -> !m.getDeclaringClass().getClassLoader().getReference().equals(ClassLoaderReference.Primordial));
    }

    public static Supplier<CallGraph> chaCgBuilder(IClassHierarchy cha, AnalysisOptions options,
            Iterable<? extends IMethod> entries, Predicate<IMethod> relevanceTest) {

        isRelevantMethod = relevanceTest;

        List<Entrypoint> entryPoints = new ArrayList<>();

        for (IMethod m : entries) {
            entryPoints.add(new DefaultEntrypoint(m, cha));
            for (int i = 0; i < m.getNumberOfParameters(); i++) {
                if (cha.lookupClass(m.getParameterType(i)) == null) {
                    LOGGER.fine("adding: " + m.getParameterType(i));
                    cha.addClass(new DivaPhantomClass(m.getParameterType(i), cha));
                }
            }
        }

        options.setEntrypoints(entryPoints);
        SSAOptions ssaOptions = new SSAOptions();
        ssaOptions.setDefaultValues(SymbolTable::getDefaultValue);

        IRFactory<IMethod> irFactory = AstIRFactory.makeDefaultFactory();
        AnalysisCache cache = new AnalysisCache(irFactory, ssaOptions,
                new SSACache(irFactory, null, new AuxiliaryCache()) {

                    private HashMap<Pair<IMethod, com.ibm.wala.ipa.callgraph.Context>, Map<SSAOptions, Object>> dictionary = HashMapFactory
                            .make();

                    @Override
                    public synchronized IR findOrCreateIR(IMethod m, com.ibm.wala.ipa.callgraph.Context c,
                            SSAOptions options) {
                        if (m == null) {
                            throw new IllegalArgumentException("m is null");
                        }
                        if (m.isAbstract() || m.isNative()) {
                            return null;
                        }

                        if (irFactory.contextIsIrrelevant(m)) {
                            c = Everywhere.EVERYWHERE;
                        }

                        IR ir = find(m, c, options);
                        if (ir == null) {
                            ir = irFactory.makeIR(m, c, options);
                            cache(m, c, options, ir);
                        }
                        return ir;
                    }

                    private void cache(IMethod m, com.ibm.wala.ipa.callgraph.Context c, SSAOptions options, IR ir) {
                        Pair<IMethod, com.ibm.wala.ipa.callgraph.Context> p = Pair.make(m, c);
                        Map<SSAOptions, Object> methodMap = MapUtil.findOrCreateMap(dictionary, p);
                        Object ref = CacheReference.make(ir);
                        methodMap.put(options, ref);
                    }

                    private IR find(IMethod m, com.ibm.wala.ipa.callgraph.Context c, SSAOptions options) {
                        Pair<IMethod, com.ibm.wala.ipa.callgraph.Context> p = Pair.make(m, c);
                        Map<SSAOptions, Object> methodMap = MapUtil.findOrCreateMap(dictionary, p);
                        Object ref = methodMap.get(options);
                        if (ref == null || CacheReference.get(ref) == null) {
                            return null;
                        } else {
                            return (IR) CacheReference.get(ref);
                        }
                    }

                    @Override
                    public void invalidateIR(IMethod method, com.ibm.wala.ipa.callgraph.Context c) {
                        dictionary.remove(Pair.make(method, c));
                    }

                });

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
                    LOGGER.fine("adding: " + m.getParameterType(i));
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
                    LOGGER.fine("adding: " + m.getParameterType(i));
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

    MutableIntSet[] reachability;

    public void reachabilityAnalysis() {
        LOGGER.info("Started: reachability analysis");

        reachability = new MutableIntSet[callgraph().getNumberOfNodes()];

        MutableIntSet[] backedges = new MutableIntSet[callgraph().getNumberOfNodes()];
        MutableIntSet todo = new BitVectorIntSet();

        for (CGNode n : callgraph()) {
            backedges[n.getGraphNodeId()] = new BimodalMutableIntSet();
            reachability[n.getGraphNodeId()] = new BimodalMutableIntSet();
        }

        for (CGNode n : callgraph()) {
            for (CallSiteReference site : (Iterable<CallSiteReference>) () -> n.iterateCallSites()) {
                String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
                if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/"))
                    continue;
                for (CGNode m : callgraph().getPossibleTargets(n, site)) {
                    if (reachability[n.getGraphNodeId()].add(m.getGraphNodeId())) {
                        todo.add(n.getGraphNodeId());
                    }
                    backedges[m.getGraphNodeId()].add(n.getGraphNodeId());
                }
            }
        }

        // Transitive closure algorithm -- faster than Warshall's algorithm?
        while (!todo.isEmpty()) {
            MutableIntSet next = new BitVectorIntSet();
            for (int j : Util.makeIterable(todo)) {
                for (int i : Util.makeIterable(backedges[j])) {
                    if (reachability[i].addAll(reachability[j])) {
                        next.add(i);
                    }
                }
            }
            todo = next;
        }
        LOGGER.info("Done: reachability analysis");
    }

    public boolean isReachable(CGNode from, CGNode to) {
        return from == to || reachability[from.getGraphNodeId()].contains(to.getGraphNodeId());
    }

    public int maxRecursion = 1;

    public void setMaxRecursion(int k) {
        maxRecursion = k;
    }

    public void traverse(CGNode entry, Trace.Visitor visitor) {
        traverse(new Trace(entry, null), visitor, false);
    }

    public static Atom CALL = Atom.findOrCreateUnicodeAtom("call");

    public void traverse(Trace trace0, Trace.Visitor visitor, boolean pathSensitive) {

        MutableIntSet visited = null;
        if (!pathSensitive) {
            visited = new BitVectorIntSet();
        }
        Stack<Trace> stack = new Stack<>();
        Stack<Iterator<?>> iters = new Stack<>();

        stack.push(trace0);
        CGNode entry = trace0.node();
        iters.push(entry.getMethod() instanceof FakeRootMethod ? entry.iterateCallSites()
                : entry.getIR().iterateAllInstructions());
        if (!pathSensitive) {
            visited.add(entry.getGraphNodeId());
        }
        visitor.visitNode(stack.peek());

        while (!stack.isEmpty()) {
            if (Thread.interrupted())
                throw new RuntimeException("Diva interrupted");

            Trace trace = stack.peek();

            if (!iters.peek().hasNext()) {
                trace = trace.updateSite(null);
                visitor.visitExit(trace);
                stack.pop();
                iters.pop();
                continue;
            }
            Object o = iters.peek().next();
            if (o == null)
                continue;
            CallSiteReference site;
            if (o instanceof SSAInstruction) {
                SSAInstruction instr = (SSAInstruction) o;
                if (instr instanceof SSAPhiInstruction)
                    continue;
                if (!trace.in(this, instr))
                    continue;
                visitor.visitInstruction(trace, instr);
                if (!(instr instanceof SSAAbstractInvokeInstruction))
                    continue;
                site = ((SSAAbstractInvokeInstruction) instr).getCallSite();
            } else if (o instanceof CallSiteReference) {
                site = (CallSiteReference) o;
            } else
                continue;

            trace = trace.updateSite(site);

            visitor.visitCallSite(trace);

            String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
            if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/")) {
                continue;
            }

            Trace targetTrace = null;
            if (trace.callLog() != null) {
                targetTrace = trace.callLog().getOrDefault(site, null);
            }
            if (targetTrace != null) {
                stack.push(targetTrace);
                iters.push(targetTrace.node().getIR().iterateAllInstructions());

            } else {
//                if (pathSensitive && site.getDeclaredTarget().getName().toString().equals("exec")) {
//                    System.out.println("BREAK HERE");
//                }
                Set<CGNode> targets = DispatchAnalysis.getFilteredTargets(this, trace, site, pathSensitive);

                if (targets.isEmpty())
                    continue;

                if (targets.size() > 1) {
                    LOGGER.fine("Failing to determine target for " + site);
                }

                for (CGNode n : targets) {
                    if (pathSensitive) {
                        if (Util.count(Util.filter(trace,
                                t -> t.node().getGraphNodeId() == n.getGraphNodeId())) >= maxRecursion)
                            continue;
                    } else if (visited.contains(n.getGraphNodeId())) {
                        continue;
                    } else {
                        visited.add(n.getGraphNodeId());
                    }

                    stack.push(new Trace(n, trace));
                    iters.push(n.getIR().iterateAllInstructions());

                    trace.logCall(stack.peek());

                    visitor.visitNode(stack.peek());

                    if (pathSensitive)
                        break;
                }
            }
        }
    }

    MutableIntSet relevance;

    public boolean isRelevant(CGNode from) {
        if (relevance == null)
            return true;
        if (relevance.contains(from.getGraphNodeId()))
            return true;
        IntSet reachable = reachability[from.getGraphNodeId()];
        if (reachable == null)
            return false;
        return reachable.containsAny(relevance);
    }

    public void relevanceAnalysis(Predicate<IClass>... tests) {
        relevance = new BitVectorIntSet();

        traverse(callgraph().getNode(0), new Trace.InstructionVisitor() {

            @Override
            public void visitInstruction(Trace trace, SSAInstruction instr) {
                if (!(instr instanceof SSAAbstractInvokeInstruction))
                    return;
                if (relevance.contains(trace.node().getGraphNodeId()))
                    return;
                TypeReference ref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget().getDeclaringClass();
                IClass c = cha.lookupClass(ref);
                if (c == null)
                    return;
                for (Predicate<IClass> t : tests) {
                    if (t.test(c)) {
                        relevance.add(trace.node().getGraphNodeId());
                        return;
                    }
                }
            }

        });

    }

    public Map<String, String> stringDictionary = new LinkedHashMap<>();

    public void populateStringDictionary(Map<String, String> dict) {
        stringDictionary.putAll(dict);
    }

    public Set<MethodReference> methodsTreatedAsIdentity = new LinkedHashSet<>();

    public void registerIdentityMethod(MethodReference mref) {
        methodsTreatedAsIdentity.add(mref);
    }

    public Report report;
    public Report transaction;
    public int transactionId;
    public int operationId;
    public Map<Trace, Integer> callSiteToOp;

    public void reportOperation(Trace trace, Consumer<Report.Named> named) {
        if (transaction == null) {
            report.add((Report.Named map) -> {
                map.put(Report.TXID, transactionId++);
                map.put(Report.TRANSACTION, (Report v) -> {
                    transaction = v;
                });
            });
        }
        transaction.add((Report.Named map) -> {
            if (trace.site() != null) {
                callSiteToOp.put(trace, operationId);
            }
            map.put(Report.OPID, operationId++);
            map.put(Report.STACKTRACE, trace, _trace -> (Report stacktrace) -> {
                for (Trace t : _trace.reversed()) {
                    IMethod m = t.node().getMethod();
                    SourcePosition p = null;
                    try {
                        p = m.getSourcePosition(t.site().getProgramCounter());
                    } catch (InvalidClassFileException | NullPointerException e) {
                    }
                    SourcePosition pos = p;
                    stacktrace.add((Report.Named site) -> {
                        site.put(Report.METHOD, m.toString());
                        site.put(Report.FILE, m.getDeclaringClass().getSourceFileName());
                        site.put(Report.POSITION, "" + pos);
                    });
                }
            });
            named.accept(map);
        });
    }

    public void reportSqlStatement(Trace trace, String stmt) {
        reportOperation(trace, map -> map.put(Report.SQL, stmt));
    }

    public void reportTxBoundary() {
        if (transaction != null) {
            transaction = null;
        }
    }

    public boolean txStarted() {
        return transaction != null;
    }

    public void calculateTransactionsWithTimeout(CGNode entry, Context cxt, Report report, Trace.Visitor visitor) {
        Thread current = Thread.currentThread();
        ExecutorService threadPool = Executors.newFixedThreadPool(1);
        Future<?> future = threadPool.submit(() -> {
            try {
                Thread.sleep(60000);
                current.interrupt();
            } catch (InterruptedException e) {
            }
        });
        try {
            calculateTransactions(entry, cxt, report, visitor);
        } finally {
            while (!future.isDone() && !future.cancel(true)) {
                try {
                    Thread.sleep(10); // seems like never reaching here
                } catch (InterruptedException e) {
                }
            }
            Thread.interrupted(); // assuming no interrupt afterwards
            threadPool.shutdown();
        }
    }

    public void calculateTransactions(CGNode entry, Context cxt, Report report, Trace.Visitor visitor) {
        this.report = report;
        this.transactionId = 0;
        this.operationId = 0;
        this.callSiteToOp = new HashMap<>();
        traverse(new Trace(entry, null), visitor, true);
        if (txStarted()) {
            reportTxBoundary();
        }
    }

    public void calculateTransactionsWithTimeout(CGNode entry, Context cxt, Report report) {
        calculateTransactionsWithTimeout(entry, cxt, report,
                JDBCAnalysis.getTransactionAnalysis(this, cxt).with(SpringBootAnalysis.getTransactionAnalysis(this, cxt)
                        .with(JPAAnalysis.getTransactionAnalysis(this, cxt))));
    }

    public void calculateTransactions(CGNode entry, Context cxt, Report report) {
        calculateTransactions(entry, cxt, report, JDBCAnalysis.getTransactionAnalysis(this, cxt).with(SpringBootAnalysis
                .getTransactionAnalysis(this, cxt).with(JPAAnalysis.getTransactionAnalysis(this, cxt))));

    }

    public void recordContraint(Constraint c) {
        Pair<String, String> key = Pair.make(c.category(), c.type());
        if (!constraints.containsKey(key)) {
            constraints.put(key, new ArrayList<>());
        }
        constraints.get(key).add(c);
    }

    public Map<Pair<String, String>, List<Constraint>> constraints = new LinkedHashMap<>();

}

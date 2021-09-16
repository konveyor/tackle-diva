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
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.logging.Logger;
import java.util.regex.Pattern;

import org.apache.commons.io.IOUtils;

import com.fasterxml.jackson.core.util.DefaultIndenter;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.types.annotations.Annotation;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.intset.BitVector;

import io.tackle.diva.irgen.DivaIRGen;
import net.bytebuddy.ByteBuddy;
import net.bytebuddy.asm.Advice;
import net.bytebuddy.dynamic.DynamicType.Builder;
import net.bytebuddy.matcher.ElementMatchers;

public class Util {

    static {
        System.setProperty("java.util.logging.SimpleFormatter.format", "%1$tF %1$tT %4$s %5$s%6$s%n");
    }

    public static final Logger LOGGER = Logger.getLogger("");

    public static String CLASS_DUMP_LOCATION = null;
    // public static String CLASS_DUMP_LOCATION = "./logs/akihiko/"
    public static String[] INJECTION_PACKAGES = new String[] { "com.ibm.wala", "org.eclipse.jdt", "io.tackle.diva" };
    public static String[] EXCLUSION_PACKAGES = new String[] { "io.tackle.diva.windup.model",
            "io.tackle.diva.windup.service" };
    public static Predicate<String> INJECTION_PREDICATE;
    public static Predicate<String> EXCLUSION_PREDICATE;
    public static ObjectWriter JSON_SERIALIZER;
    public static ObjectMapper YAML_SERIALIZER;

    static {
        String pat = null;
        for (String p : INJECTION_PACKAGES) {
            if (pat == null) {
                pat = "^" + p.replace(".", "\\.") + "\\..*";
            } else {
                pat += "|^" + p.replace(".", "\\.") + "\\..*";
            }
        }
        INJECTION_PREDICATE = Pattern.compile(pat).asPredicate();

        pat = null;
        for (String p : EXCLUSION_PACKAGES) {
            if (pat == null) {
                pat = "^" + p.replace(".", "\\.") + "\\..*";
            } else {
                pat += "|^" + p.replace(".", "\\.") + "\\..*";
            }
        }
        EXCLUSION_PREDICATE = Pattern.compile(pat).asPredicate();

        DefaultPrettyPrinter.Indenter indenter = new DefaultIndenter("  ", DefaultIndenter.SYS_LF);
        DefaultPrettyPrinter printer = new DefaultPrettyPrinter();
        printer.indentObjectsWith(indenter);
        printer.indentArraysWith(indenter);

        JSON_SERIALIZER = new ObjectMapper().writer(printer);

        YAML_SERIALIZER = new ObjectMapper(new YAMLFactory());

    }

    public static void directoryAssurance(String directory) {
        File dir = new File(directory);
        if (!dir.exists())
            dir.mkdirs();
    }

    public static List<Annotation> getAnnotations(IClass c) {
        List<Annotation> res = new ArrayList<>();
        Collection<Annotation> as = c.getAnnotations();
        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
            res.add(a);
        }
        as = DivaIRGen.annotations.get(c.getReference());
        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
            res.add(a);
        }
        return res;
    }

    public static List<Annotation> getAnnotations(IMethod m) {
        List<Annotation> res = new ArrayList<>();

        // String key = m.getDeclaringClass().getName() + " " + m.getName() + " " +
        // m.getDescriptor().toString();
        Collection<Annotation> as = DivaIRGen.annotations.get(m.getReference());
        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
            res.add(a);
        }
//        as = m.getAnnotations();
//        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
//            res.add(a);
//        }
        return res;
    }

    public static List<Annotation> getAnnotations(IMethod m, int param) {
        List<Annotation> res = new ArrayList<>();
        Collection<Annotation> as = DivaIRGen.annotations.get(Pair.make(m.getReference(), param));
        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
            res.add(a);
        }
        return res;
    }

    public static List<Annotation> getAnnotations(IField f) {
        List<Annotation> res = new ArrayList<>();
        // String key = f.getDeclaringClass().getName() + " " + f.getName();
        Collection<Annotation> as = DivaIRGen.annotations
                .get(Pair.make(f.getDeclaringClass().getReference(), f.getName()));
        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
            res.add(a);
        }
//        as = f.getAnnotations();
//        for (Annotation a : as == null ? Collections.<Annotation>emptySet() : as) {
//            res.add(a);
//        }
        return res;
    }

    public static void injectedCall(Map<String, Class<?>> injectors, String name, Object... args) throws Exception {

        Class klazz = Class.forName(name.substring(0, name.lastIndexOf('.')));
        String method = name.substring(name.lastIndexOf('.') + 1);

        Set<String> targetClasses = new HashSet<>();

        for (String target : injectors.keySet()) {
            String targetClass = target.substring(0, target.lastIndexOf('.'));
            targetClasses.add(targetClass);
        }

        ClassLoader delegate = klazz.getClassLoader();

        ClassLoader cl = new ClassLoader() {
            //
            // @Override
            // public InputStream getResourceAsStream(String name) {
            // // @TODO: do not hard code here
            // if (name.equals("wala.properties")) {
            // return new ReaderInputStream(
            // new StringReader("java_runtime_dir = " + System.getProperty("java.home")));
            // }
            // return super.getResourceAsStream(name);
            // }

            @Override
            protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {

                Class<?> c = delegate.loadClass(name);
                byte[] bytes;
                if (targetClasses.contains(name)) {
                    // TODO: can't we just define it without original class?
                    Builder<?> b = new ByteBuddy().redefine(c);
                    for (String target : injectors.keySet()) {
                        if (target.startsWith(name)) {
                            String targetMethod = target.substring(target.lastIndexOf('.') + 1);
                            b = b.visit(Advice.to(injectors.get(target))
                                    .on(targetMethod.equals("<init>") ? ElementMatchers.isConstructor()
                                            : ElementMatchers.isMethod().and(ElementMatchers.named(targetMethod))));
                        }
                    }
                    bytes = b.make().getBytes();
                    LOGGER.info("Instrumented: " + name);
                    if (CLASS_DUMP_LOCATION != null) {
                        try {
                            String path = CLASS_DUMP_LOCATION + "/" + name.replace('.', '/') + ".class";
                            Util.directoryAssurance(path.substring(0, path.lastIndexOf('/')));
                            FileOutputStream fos = new FileOutputStream(path);
                            fos.write(bytes);
                            fos.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }

                } else if (c.getClassLoader() == null || !INJECTION_PREDICATE.test(name)
                        || EXCLUSION_PREDICATE.test(name)) {
                    return c;
                } else {
                    String classAsPath = name.replace('.', '/') + ".class";
                    try {
                        bytes = IOUtils.toByteArray(c.getClassLoader().getResourceAsStream(classAsPath));
                    } catch (IOException e) {
                        return c;
                    }
                }
                return defineClass(name, bytes, 0, bytes.length);
            }

            @Override
            public URL getResource(String name) {
                return delegate.getResource(name);
            }

            @Override
            public InputStream getResourceAsStream(String name) {
                return delegate.getResourceAsStream(name);
            }

            @Override
            public Enumeration<URL> getResources(String name) throws IOException {
                return delegate.getResources(name);
            }
        };

        // ClassLoader loader = new MultipleParentClassLoader.Builder
        // ().append(Test2.class.getClassLoader()).build();

        Class c = Class.forName(klazz.getName(), false, cl);
        for (Method m : c.getDeclaredMethods()) {
            if (m.getName().equals(method)) {
                m.invoke(null, args);
                break;
            }
        }
    }

    public static void dumpCallGraph(CallGraph cg) throws IOException {
        BitVector seen = new BitVector();

        try (PrintWriter out = new PrintWriter(new FileWriter("cg.dot"))) {
            out.println("digraph {");
            out.println("node[shape=plaintext]");
            out.println("rankdir=LR");

            for (CGNode src : cg) {
                if (!seen.contains(src.getGraphNodeId())) {
                    seen.set(src.getGraphNodeId());
                    out.println("n" + src.getGraphNodeId() + " [label=\"" + src.toString() + "\"]");
                }
                for (CGNode tgt : (Iterable<CGNode>) () -> cg.getSuccNodes(src)) {
                    if (!seen.contains(tgt.getGraphNodeId())) {
                        seen.set(tgt.getGraphNodeId());
                        out.println("n" + tgt.getGraphNodeId() + " [label=\"" + tgt.toString() + "\"]");
                    }
                    out.println("n" + src.getGraphNodeId() + " -> n" + tgt.getGraphNodeId());
                }
            }
            out.println("}");
        }
    }

    public static Iterable<IClass> superChain(IClass c) {
        return () -> new Iterator<IClass>() {
            IClass p = c;

            @Override
            public boolean hasNext() {
                return p != null;
            }

            @Override
            public IClass next() {
                IClass c = p;
                p = c.getSuperclass();
                return c;
            }
        };
    }

    public static String truncate(Object o) {
        if (o == null) {
            return "null";
        }
        String s = String.join(" ", o.toString().split("[\\n\\s]+"));
        if (s.length() < 50) {
            return s;
        }
        return s.substring(0, 50) + "...";
    }

    public static <T> Iterable<T> makeIterable(T[] data) {
        return () -> new Iterator<T>() {
            int i = 0;

            @Override
            public boolean hasNext() {
                return i < data.length;
            }

            @Override
            public T next() {
                return hasNext() ? data[i++] : null;
            }
        };
    }

    public static <T> Iterable<T> filter(Iterable<T> data, Predicate<T> filter) {
        return () -> new Iterator<T>() {
            Iterator<T> i = data.iterator();
            T next;

            @Override
            public boolean hasNext() {
                if (next != null)
                    return true;
                while (i.hasNext()) {
                    next = i.next();
                    if (filter.test(next)) {
                        return true;
                    }
                }
                return false;
            }

            @Override
            public T next() {
                if (hasNext()) {
                    T r = next;
                    next = null;
                    return r;
                }
                return null;
            }
        };
    }

    public static <S, T> Iterable<T> map(Iterable<S> data, Function<S, T> map) {
        return () -> new Iterator<T>() {
            Iterator<S> i = data.iterator();
            T next;

            @Override
            public boolean hasNext() {
                return i.hasNext();
            }

            @Override
            public T next() {
                return map.apply(i.next());
            }
        };
    }

    public static <E> boolean any(Iterable<E> input, Predicate<E> f) {
        for (E e : input) {
            if (f.test(e)) {
                return true;
            }
        }
        return false;
    }

    public static <E> boolean all(Iterable<E> input, Predicate<E> f) {
        for (E e : input) {
            if (!f.test(e)) {
                return false;
            }
        }
        return true;
    }

    public static <T> T[] makeArray(Iterable<T> iter, Class<T> c) {
        List<T> temp = makeList(iter);
        T[] res = (T[]) Array.newInstance(c, temp.size());
        int i = 0;
        for (T t : temp) {
            res[i++] = t;
        }
        return res;
    }

    public static <T> List<T> makeList(Iterable<T> iter) {
        List<T> temp = new ArrayList<>();
        for (T v : iter) {
            temp.add(v);
        }
        return temp;
    }

    public static class Chain<T extends Chain<T>> implements Iterable<T> {
        protected T next;

        public Chain(T next) {
            this.next = next;
        }

        T reverse0() {
            T s = (T) this;
            T prev = null;
            while (s != null) {
                T next = s.next;
                s.next = prev;
                prev = s;
                s = next;
            }
            return prev;
        }

        public Iterable<T> reversed() {
            return () -> new Iterator<T>() {

                T last = reverse0();
                T current = last;

                @Override
                public boolean hasNext() {
                    return current != null;
                }

                @Override
                public T next() {
                    T c = current;
                    current = c.next;
                    if (current == null) {
                        last.reverse0();
                    }
                    return c;
                }

            };
        }

        @Override
        public Iterator<T> iterator() {
            return new Iterator<T>() {
                T current = (T) Chain.this;

                @Override
                public boolean hasNext() {
                    return current != null;
                }

                @Override
                public T next() {
                    T c = current;
                    current = c.next;
                    return c;
                }
            };
        }
    }

    public static class JsonReport implements Report {
        List<Object> list;

        public JsonReport(List<Object> list) {
            this.list = list;
        }

        @Override
        public void add(Named.Builder builder) {
            Map<String, Object> value = new LinkedHashMap<>();
            list.add(value);
            builder.build(new Named(value));
        }

        @Override
        public void add(Report.Builder builder) {
            List<Object> value = new ArrayList<>();
            list.add(value);
            builder.build(new JsonReport(value));
        }

        @Override
        public void add(String data) {
            list.add(data);
        }

        public static class Named implements Report.Named {
            Map<String, Object> map;

            public Named(Map<String, Object> map) {
                this.map = map;
            }

            @Override
            public void putPrimitive(String key, Object value) {
                map.put(key, value);
            }

            @Override
            public void put(String key, Named.Builder builder) {
                Map<String, Object> value;
                if (!map.containsKey(key)) {
                    value = new LinkedHashMap<>();
                    map.put(key, value);
                } else {
                    value = (Map) map.get(key);
                }
                builder.build(new Named(value));
            }

            @Override
            public void put(String key, Report.Builder builder) {
                List<Object> value;
                if (!map.containsKey(key)) {
                    value = new ArrayList<>();
                    map.put(key, value);
                } else {
                    value = (List) map.get(key);
                }
                builder.build(new JsonReport(value));
            }
        }
    }

    public static abstract class LazyReport implements Report, Consumer<Report.Builder> {

        Report delegate;

        @Override
        public void add(Report.Named.Builder builder) {
            if (delegate == null) {
                accept(r -> {
                    delegate = r;
                });
            }
            delegate.add(builder);
        }

        @Override
        public void add(Builder builder) {
            if (delegate == null) {
                accept(r -> {
                    delegate = r;
                });
            }
            delegate.add(builder);
        }

        @Override
        public void add(String data) {
            if (delegate == null) {
                accept(r -> {
                    delegate = r;
                });
            }
            delegate.add(data);
        }

    }

}

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

import static io.tackle.diva.Util.LOGGER;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;

import org.eclipse.core.runtime.NullProgressMonitor;
import org.eclipse.jdt.core.IJavaElement;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTNode;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.AnonymousClassDeclaration;
import org.eclipse.jdt.core.dom.ArrayInitializer;
import org.eclipse.jdt.core.dom.BodyDeclaration;
import org.eclipse.jdt.core.dom.ClassInstanceCreation;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.Expression;
import org.eclipse.jdt.core.dom.ExpressionMethodReference;
import org.eclipse.jdt.core.dom.FieldDeclaration;
import org.eclipse.jdt.core.dom.FileASTRequestor;
import org.eclipse.jdt.core.dom.IAnnotationBinding;
import org.eclipse.jdt.core.dom.IBinding;
import org.eclipse.jdt.core.dom.IMethodBinding;
import org.eclipse.jdt.core.dom.IPackageBinding;
import org.eclipse.jdt.core.dom.ITypeBinding;
import org.eclipse.jdt.core.dom.IVariableBinding;
import org.eclipse.jdt.core.dom.ImportDeclaration;
import org.eclipse.jdt.core.dom.LambdaExpression;
import org.eclipse.jdt.core.dom.MemberValuePair;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.MethodInvocation;
import org.eclipse.jdt.core.dom.Name;
import org.eclipse.jdt.core.dom.NormalAnnotation;
import org.eclipse.jdt.core.dom.QualifiedName;
import org.eclipse.jdt.core.dom.SimpleName;
import org.eclipse.jdt.core.dom.SimpleType;
import org.eclipse.jdt.core.dom.SingleMemberAnnotation;
import org.eclipse.jdt.core.dom.SuperMethodInvocation;
import org.eclipse.jdt.core.dom.TryStatement;
import org.eclipse.jdt.core.dom.Type;
import org.eclipse.jdt.core.dom.TypeDeclaration;
import org.eclipse.jdt.core.dom.VariableDeclarationExpression;
import org.eclipse.jdt.core.dom.VariableDeclarationFragment;

import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.Java2IRTranslator;
import com.ibm.wala.cast.java.translator.SourceModuleTranslator;
import com.ibm.wala.cast.java.translator.jdt.JDT2CAstUtils;
import com.ibm.wala.cast.java.translator.jdt.JDTJava2CAstTranslator;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJSourceModuleTranslator;
import com.ibm.wala.cast.loader.AstMethod;
import com.ibm.wala.cast.tree.CAst;
import com.ibm.wala.cast.tree.CAstNode;
import com.ibm.wala.cast.tree.CAstQualifier;
import com.ibm.wala.cast.tree.CAstSourcePositionMap.Position;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.ModuleEntry;
import com.ibm.wala.classLoader.PhantomClass;
import com.ibm.wala.classLoader.SourceFileModule;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.AnnotationsReader;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.Selector;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.types.annotations.Annotation;
import com.ibm.wala.util.collections.HashMapFactory;
import com.ibm.wala.util.strings.StringStuff;

import net.bytebuddy.asm.Advice;
import net.bytebuddy.implementation.bytecode.assign.Assigner.Typing;

public class DivaIRGen {

    public static JavaSourceLoaderImpl makeNewSourceLoader(String[] sourceDirs, String[] stdlibs,
            ClassLoaderReference classLoaderReference, IClassHierarchy cha, IClassLoader parent) {
        return new ECJSourceLoaderImpl(classLoaderReference, parent, cha, false) {

            Map<String, ModuleEntry> sourceMap = HashMapFactory.make();
            int countdown = sourceDirs.length;

            public void addClass(IClass c) {
                loadedClasses.put(c.getName(), c);
            }

            @Override
            protected SourceModuleTranslator getTranslator() {

                return new ECJSourceModuleTranslator(cha.getScope(), this, false) {

                    @Override
                    public void loadAllSources(Set<ModuleEntry> modules) {

                        for (ModuleEntry m : modules) {
                            if (m.isSourceFile()) {
                                SourceFileModule s = (SourceFileModule) m;
                                sourceMap.put(s.getAbsolutePath(), s);
                            }
                        }

                        if (--countdown > 0)
                            return;

                        String[] sourceFiles = sourceMap.keySet().toArray(new String[0]);

                        @SuppressWarnings("deprecation")
                        final ASTParser parser = ASTParser.newParser(AST.JLS8);
                        parser.setResolveBindings(true);
                        parser.setBindingsRecovery(true); // recover
                        parser.setStatementsRecovery(true); // recover
                        parser.setEnvironment(stdlibs, sourceDirs, null, true);
                        Hashtable<String, String> options = JavaCore.getOptions();
                        options.put(JavaCore.COMPILER_SOURCE, "1.8");
                        options.put(JavaCore.COMPILER_CODEGEN_TARGET_PLATFORM, "1.8");
                        parser.setCompilerOptions(options);

                        Map<String, CompilationUnit> units = new LinkedHashMap<>();

                        parser.createASTs(sourceFiles, null, new String[0], new FileASTRequestor() {
                            @Override
                            public void acceptAST(String source, CompilationUnit unit) {
                                units.put(source, unit);
                            }
                        }, new NullProgressMonitor());

                        recoverBindings(parser, units, cha);

                        for (String source : units.keySet()) {
                            CompilationUnit unit = units.get(source);
                            try {
                                JDTJava2CAstTranslator<Position> jdt2cast = makeCAstTranslator(unit, source);
                                final Java2IRTranslator java2ir = makeIRTranslator();
                                java2ir.translate(sourceMap.get(source), jdt2cast.translateToCAst());
                                LOGGER.info("Done wala IR: " + source);
                            } catch (Throwable e) {
                                LOGGER.info(e.getMessage());
                                ;
                                for (StackTraceElement s : e.getStackTrace()) {
                                    LOGGER.info(s.toString());
                                }
                                LOGGER.info("Failed wala IR: " + source + ", reason: " + e.getMessage());
                            }

                        }
                        if (knownAsClasses != null) {
                            for (String klazz : knownAsClasses) {
                                TypeName t = TypeName
                                        .string2TypeName(StringStuff.deployment2CanonicalTypeString(klazz));
                                if (lookupClass(t) == null) {
                                    TypeReference classRef = TypeReference.findOrCreate(ClassLoaderReference.Extension,
                                            t);
                                    addClass(new DivaPhantomClass(classRef, cha));
                                }
                            }
                        }
                        if (knownAsInterfaces != null) {
                            for (String klazz : knownAsInterfaces) {
                                TypeName t = TypeName
                                        .string2TypeName(StringStuff.deployment2CanonicalTypeString(klazz));
                                if (lookupClass(t) == null) {
                                    TypeReference classRef = TypeReference.findOrCreate(ClassLoaderReference.Extension,
                                            t);
                                    addClass(new DivaPhantomClass(classRef, cha, true));
                                }
                            }
                        }
                    }
                };
            }
        };
    }

    public static void recoverBindings(ASTParser parser, Map<String, CompilationUnit> units, IClassHierarchy cha) {

        for (String source : units.keySet()) {
            CompilationUnit unit = units.get(source);

            for (ImportDeclaration imp : (List<ImportDeclaration>) unit.imports()) {
                if (imp.isOnDemand())
                    continue;
                if (imp.isStatic())
                    continue;
                QualifiedName qname = (QualifiedName) imp.getName();
                imports.put(qname.getName().toString(), qname.toString());
            }
        }

        for (String source : units.keySet()) {
            CompilationUnit unit = units.get(source);

            wellKnownType = unit.getAST()::resolveWellKnownType;

            unit.accept(new ASTVisitor() {

                @Override
                public boolean visit(MethodInvocation node) {
                    IMethodBinding binding = node.resolveMethodBinding();
                    if (binding == null) {
                        binding = findOrCreatePhantomMethod(node);
                    }
                    return true;
                }

                @Override
                public boolean visit(SuperMethodInvocation node) {
                    IMethodBinding binding = node.resolveMethodBinding();
                    if (binding == null) {
                        binding = findOrCreatePhantomMethod(node);
                    }
                    return true;
                }

                @Override
                public boolean visit(ClassInstanceCreation node) {
                    // System.out.println(node);
                    IMethodBinding binding = node.resolveConstructorBinding();
                    if (binding == null) {
                        binding = findOrCreatePhantomMethod(node);
                    }
                    if (knownAsClasses == null) {
                        knownAsClasses = new HashSet();
                    }
                    String name = binding.getDeclaringClass().getBinaryName();
                    knownAsClasses.add(name);
                    return true;
                }

                @Override
                public boolean visit(SimpleName node) {
                    IBinding binding = node.resolveBinding();
                    if (binding == null) {
                        LOGGER.info(node + "->" + binding);
                    }
                    return true;
                }

                @Override
                public boolean visit(TryStatement node) {
                    // handle try-with-resources
                    List<Expression> resources = node.resources();
                    if (resources == null || resources.isEmpty()) {
                        return true;
                    }
                    for (Expression exp : resources) {
                        if (!(exp instanceof VariableDeclarationExpression)) {
                            continue;
                        }
                        for (VariableDeclarationFragment var : (List<VariableDeclarationFragment>) ((VariableDeclarationExpression) exp)
                                .fragments()) {
                            ITypeBinding klazz = var.resolveBinding().getType();
                            if (klazz.isRecovered()) {
                                findOrCreateCloseable(klazz);
                            }
                        }
                    }
                    return super.visit(node);
                }

                @Override
                public boolean visit(TypeDeclaration node) {
                    Type sup = node.getSuperclassType();
                    if (sup != null) {
                        String superName = sup.resolveBinding().getBinaryName();
                        if (knownAsClasses == null) {
                            knownAsClasses = new HashSet();
                        }
                        knownAsClasses.add(superName);
                    }
                    List<Type> ifaces = node.superInterfaceTypes();
                    for (Type i : ifaces) {
                        String ifaceName = i.resolveBinding().getBinaryName();
                        if (knownAsInterfaces == null) {
                            knownAsInterfaces = new HashSet();
                        }
                        knownAsInterfaces.add(ifaceName);
                    }
                    ITypeBinding t = node.resolveBinding();
                    if (t != null) {
                        String name = StringStuff.deployment2CanonicalTypeString(t.getBinaryName());
                        processAnnotations(cha, node, name);
                    }
                    return true;
                }

                @Override
                public boolean visit(AnonymousClassDeclaration node) {
                    ITypeBinding t = node.resolveBinding();
                    ITypeBinding sup = t.getSuperclass();
                    if (sup != null) {
                        String superName = sup.getBinaryName();
                        if (knownAsClasses == null) {
                            knownAsClasses = new HashSet();
                        }
                        knownAsClasses.add(superName);
                    }
                    return true;
                }

                @Override
                public boolean visit(MethodDeclaration node) {
                    IMethodBinding binding = node.resolveBinding();
                    if (binding != null) {
                        String name = methodSignature(binding.getDeclaringClass(), binding.getName(),
                                binding.getParameterTypes(), binding.getReturnType());
                        processAnnotations(cha, node, name);
                    }
                    return true;
                }

                @Override
                public boolean visit(FieldDeclaration node) {
                    ASTNode enclosing = node.getParent();
                    if (enclosing instanceof TypeDeclaration) {
                        ITypeBinding klazz = ((TypeDeclaration) enclosing).resolveBinding();
                        if (klazz == null) {
                            return true;
                        }
                        VariableDeclarationFragment vdecl = (VariableDeclarationFragment) node.fragments().get(0);
                        String name = StringStuff.deployment2CanonicalTypeString(klazz.getBinaryName()) + " "
                                + vdecl.getName().toString();
                        processAnnotations(cha, node, name);
                    }
                    return true;
                }

            });
            LOGGER.info("Done binding: " + source);
        }

    }

    public static Map<String, List<Annotation>> annotations;

    public static void processAnnotations(IClassHierarchy cha, BodyDeclaration node, String name) {
        for (ASTNode prop : (List<ASTNode>) node.modifiers()) {
            if (prop instanceof org.eclipse.jdt.core.dom.Annotation) {
                org.eclipse.jdt.core.dom.Annotation annot = (org.eclipse.jdt.core.dom.Annotation) prop;
                String annotType = StringStuff.deployment2CanonicalTypeString(
                        annot.resolveAnnotationBinding().getAnnotationType().getBinaryName().toString());
                Map<String, AnnotationsReader.ElementValue> namedParams = new LinkedHashMap<>();
                if (annot instanceof NormalAnnotation) {
                    NormalAnnotation a1 = (NormalAnnotation) annot;
                    for (MemberValuePair kv : (List<MemberValuePair>) a1.values()) {
                        AnnotationsReader.ElementValue ev = null;
                        Object v = kv.getValue().resolveConstantExpressionValue();
                        if (v != null) {
                            ev = new AnnotationsReader.ConstantElementValue(v);
                        } else if (v == null && kv.getValue() instanceof ArrayInitializer) {
                            ArrayInitializer i = (ArrayInitializer) kv.getValue();
                            AnnotationsReader.ElementValue[] vs = new AnnotationsReader.ElementValue[i.expressions()
                                    .size()];
                            int k = 0;
                            for (Expression e : (List<Expression>) i.expressions()) {
                                vs[k] = new AnnotationsReader.ConstantElementValue(i.expressions().get(k));
                            }
                            ev = new AnnotationsReader.ArrayElementValue(vs);
                        }
                        namedParams.put(kv.getName().toString(), ev);
                        // System.out.println("HERE:" + name + "/" + kv.getName().toString() + "=" + v);
                    }
                } else if (annot instanceof SingleMemberAnnotation) {
                    SingleMemberAnnotation a2 = (SingleMemberAnnotation) annot;
                    Expression e = a2.getValue();
                    Object v = e.resolveConstantExpressionValue();
                    AnnotationsReader.ElementValue ev = new AnnotationsReader.ConstantElementValue(v);
                    namedParams.put("value", ev);
                }
                IClass c = cha.getLoader(ClassLoaderReference.Extension).lookupClass(TypeName.findOrCreate(annotType));
                TypeReference t1 = c != null ? c.getReference()
                        : TypeReference.findOrCreate(ClassLoaderReference.Extension, annotType);
                Annotation a = Annotation.makeWithNamed(t1, namedParams);
                if (annotations == null) {
                    annotations = new LinkedHashMap<>();
                }
                if (!annotations.containsKey(name)) {
                    annotations.put(name, new ArrayList<>());
                }
                annotations.get(name).add(a);

            }
        }
    }

    // public static void processAnnotations(IBinding binding) {
    // String name = null;
    // if (binding instanceof ITypeBinding) {
    // name = StringStuff.deployment2CanonicalTypeString(((ITypeBinding)
    // binding).getBinaryName().toString());
    // }
    // if (binding.getAnnotations().length == 0)
    // return;
    // List<Annotation> res = new ArrayList<>();
    // for (IAnnotationBinding a : binding.getAnnotations()) {
    // ITypeBinding t = a.getAnnotationType();
    // for (IMemberValuePairBinding p : a.getDeclaredMemberValuePairs()) {
    // System.out.println(t.getBinaryName() + ":" + p.getKey() + "->" +
    // p.getValue());
    // }
    // }
    //
    // }

    public static class DoMethodBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.This MethodInvocation node,
                @Advice.Return(readOnly = false) IMethodBinding binding) {
            if (binding == null) {
                binding = findOrCreatePhantomMethod(node);
            }
        }
    }

    public static class DoSuperMethodBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.This SuperMethodInvocation node,
                @Advice.Return(readOnly = false) IMethodBinding binding) {
            if (binding == null) {
                binding = findOrCreatePhantomMethod(node);
            }
        }
    }

    public static class DoClassInstanceCreationBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.This ClassInstanceCreation node,
                @Advice.Return(readOnly = false) IMethodBinding binding) {
            if (binding == null) {
                binding = findOrCreatePhantomMethod(node);
            }
        }
    }

    public static class DoName {
        @Advice.OnMethodExit
        public static void exit(@Advice.This Name node, @Advice.Return(readOnly = false) IBinding binding) {
            if (binding == null) {
                binding = findOrCreateUnknownPhantomType(node.toString());
            } else if (binding.isRecovered()) {
                String key = binding.getKey();
                if (key.startsWith("Recovered#typeBindingL")) {
                    key = key.substring("Recovered#typeBindingL".length());
                    key = key.substring(0, key.lastIndexOf(';'));
                    if (Character.isUpperCase(key.charAt(0))) {
                        binding = findOrCreateUnknownPhantomType(key);
                    }
                }
            }
        }
    }

    public static class DoType {
        @Advice.OnMethodExit
        public static void exit(@Advice.This Type node, @Advice.Return(readOnly = false) ITypeBinding binding) {
            if (node instanceof SimpleType && (binding == null || isBroken(binding))) {
                binding = findOrCreateUnknownPhantomType(((SimpleType) node).getName().toString());
            }
        }
    }

    public static class DoVariableBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.Return(readOnly = false) ITypeBinding binding) {
            ITypeBinding b = binding.isParameterizedType() ? binding.getErasure() : binding;
            if (isBroken(b)) {
                binding = findOrCreateUnknownPhantomType(b);
            }
        }
    }

    public static class DoExpressionTypeBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.This Expression node, @Advice.Return(readOnly = false) ITypeBinding binding) {
            if (binding == null) {
                binding = findOrCreateType(node, false);
            }
        }
    }

    public static class DoGetSuperClass {
        @Advice.OnMethodExit
        public static void exit(@Advice.This ITypeBinding type, @Advice.Return(readOnly = false) ITypeBinding binding) {
            if (binding != null) {
                ITypeBinding b = binding.isParameterizedType() ? binding.getErasure() : binding;
                if (b.isRecovered()) {
                    if (isBroken(b)) {
                        b = findOrCreateUnknownPhantomType(b);
                        binding = b;
                    }
                    findOrCreateDefaultCtor(b);
                }
            }
        }
    }

    public static class DoLocalTypeBinding {
        @Advice.OnMethodExit
        public static void exit(@Advice.This(typing = Typing.DYNAMIC) ITypeBinding type,
                @Advice.Return(readOnly = false) String name) {
            if (name == null) {
                String key = type.getKey();
                name = StringStuff.jvmToBinaryName(key);
            }
        }
    }

    public static class DoOverrides {
        @Advice.OnMethodEnter(skipOn = Advice.OnNonDefaultValue.class)
        public static boolean enter(@Advice.Argument(0) IMethodBinding other) {
            return !other.getClass().getName().equals("org.eclipse.jdt.core.dom.MethodBinding");
        }

        @Advice.OnMethodExit
        public static void exit(@Advice.Enter boolean skip, @Advice.This(typing = Typing.DYNAMIC) IMethodBinding type,
                @Advice.Argument(0) IMethodBinding other, @Advice.Return(readOnly = false) boolean binding) {
            if (skip) {
                binding = type.getName().equals(other.getName())
                        && JDT2CAstUtils.sameErasedSignatureAndReturnType(type, other);
            }
        }
    }

    public static class DoGetParameterTypes {
        @Advice.OnMethodExit
        public static void exit(@Advice.Return(readOnly = true) ITypeBinding[] parameterTypes) {
            for (int k = 0; k < parameterTypes.length; k++) {
                ITypeBinding binding = parameterTypes[k];
                ITypeBinding b = binding.isParameterizedType() ? binding.getErasure() : binding;
                if (isBroken(b)) {
                    parameterTypes[k] = findOrCreateUnknownPhantomType(b);
                }
            }
        }
    }

    public static class DoGetTypeBinding {
        @Advice.OnMethodExit
        public static void enter(@Advice.Return(readOnly = false) ITypeBinding binding) {
            if (binding != null) {
                ITypeBinding b = binding.isParameterizedType() ? binding.getErasure() : binding;
                if (isBroken(b)) {
                    binding = findOrCreateUnknownPhantomType(b);
                }
            }
        }
    }

    public static class DoShrikeCTParse {
        @Advice.OnMethodEnter
        public static void enter(@Advice.Argument(0) byte[] bytes) {
            if (bytes[7] > 57) {
                // accepting openjdk15 (majorVersion = 59)
                bytes[7] = 57;
            }
        }
    }

//    public static class DoGetDirectInterfaces {
//        @Advice.OnMethodExit(onThrowable = AssertionError.class)
//        public static void exit(@Advice.Thrown(readOnly = false) AssertionError e) {
//            e = null;
//        }
//    }

    // public static class DoGetAnnotationType {
    // @Advice.OnMethodExit
    // public static void exit(
    // @Advice.Return(readOnly = false) ReferenceBinding typeBinding) {
    // if (typeBinding != null) {
    // typeBinding.tagBits &= ~TagBits.HasMissingType;
    // }
    // }
    // }

    public static class DoJDT2CastVisitNode {

        @Advice.OnMethodEnter(skipOn = Advice.OnNonDefaultValue.class)
        public static boolean enter(@Advice.Argument(value = 0) ASTNode n) {
            if (n instanceof ExpressionMethodReference) {
                Util.LOGGER.info(n.toString());
                return true;
            } else if (n instanceof LambdaExpression) {
                Util.LOGGER.info(n.toString());
                return true;
            }
            return false;
        }

        @Advice.OnMethodExit
        public static void exit(@Advice.Enter boolean skip, @Advice.FieldValue("fFactory") CAst fFactory,
                @Advice.Return(readOnly = false) CAstNode res) {
            if (skip) {
                Util.LOGGER.info("replaced with ??");
                res = fFactory.makeConstant("??");
            }
        }
    }

    @SuppressWarnings("serial")
    public static Map<String, Class<?>> advices() {
        return (new HashMap<String, Class<?>>() {
            {
                put("org.eclipse.jdt.core.dom.MethodInvocation.resolveMethodBinding", DoMethodBinding.class);
                put("org.eclipse.jdt.core.dom.SuperMethodInvocation.resolveMethodBinding", DoSuperMethodBinding.class);
                put("org.eclipse.jdt.core.dom.ClassInstanceCreation.resolveConstructorBinding",
                        DoClassInstanceCreationBinding.class);
                put("org.eclipse.jdt.core.dom.Name.resolveBinding", DoName.class);
                put("org.eclipse.jdt.core.dom.Type.resolveBinding", DoType.class);
                put("org.eclipse.jdt.core.dom.VariableBinding.getType", DoVariableBinding.class);
                put("org.eclipse.jdt.core.dom.Expression.resolveTypeBinding", DoExpressionTypeBinding.class);
                put("org.eclipse.jdt.core.dom.TypeBinding.getSuperclass", DoGetSuperClass.class);
                put("org.eclipse.jdt.core.dom.TypeBinding$LocalTypeBinding.getBinaryName", DoLocalTypeBinding.class);
                put("org.eclipse.jdt.core.dom.MethodBinding.overrides", DoOverrides.class);
                put("org.eclipse.jdt.core.dom.MethodBinding.getParameterTypes", DoGetParameterTypes.class);
                put("org.eclipse.jdt.core.dom.DefaultBindingResolver.getTypeBinding", DoGetTypeBinding.class);
                put("com.ibm.wala.shrikeCT.ClassReader.<init>", DoShrikeCTParse.class);
                // put("com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl$JavaClass.getDirectInterfaces",
                // DoGetDirectInterfaces.class);
                put("com.ibm.wala.cast.java.translator.jdt.JDTJava2CAstTranslator.visitNode",
                        DoJDT2CastVisitNode.class);
            }
        });
    }

    public static Function<String, ITypeBinding> wellKnownType;

    public static Map<String, String> imports = new HashMap<>();

    public static Map<String, ITypeBinding> phantomTypes;
    public static Map<Object, IMethodBinding> phantomMethods;
    public static Set<String> knownAsClasses;
    public static Set<String> knownAsInterfaces;

    public static ITypeBinding findOrCreateUnknownPhantomType(ITypeBinding b) {
        // System.out.println(b + " name=" + b.getName() + " binary=" +
        // b.getBinaryName() + " key=" + b.getKey());
        if (b.isParameterizedType()) {
            b = b.getErasure();
        }
        if (b.getBinaryName() != null && b.getBinaryName().contains(".")) {
            return findOrCreatePhantomType(b.getBinaryName());
        }
        return findOrCreateUnknownPhantomType(b.getName());
    }

    public static ITypeBinding findOrCreateUnknownPhantomType(String name) {
        if (imports.containsKey(name)) {
            return findOrCreatePhantomType(imports.get(name));
        }
        return findOrCreatePhantomType("unknown." + name);
    }

    public static ITypeBinding findOrCreatePhantomType(String name) {
        if (phantomTypes == null) {
            phantomTypes = new HashMap<>();
        }
        if (phantomTypes.containsKey(name)) {
            return phantomTypes.get(name);
        }

        ITypeBinding[] emptyTypes = new ITypeBinding[0];
        String key = "PHANTOM:" + StringStuff.deployment2CanonicalTypeString(name);

        Object[] lazyData = new Object[2];

        ITypeBinding binding = new ITypeBinding() {

            @Override
            public IAnnotationBinding[] getAnnotations() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public int getKind() {
                return TYPE;
            }

            @Override
            public boolean isDeprecated() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isRecovered() {
                return true;
            }

            @Override
            public boolean isSynthetic() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public IJavaElement getJavaElement() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public String getKey() {
                return key;
            }

            @Override
            public boolean isEqualTo(IBinding binding) {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public ITypeBinding createArrayType(int dimension) {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public String getBinaryName() {
                return name;
            }

            @Override
            public ITypeBinding getBound() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding getGenericTypeOfWildcardType() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public int getRank() {
                // TODO Auto-generated method stub
                return 0;
            }

            @Override
            public ITypeBinding getComponentType() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public IVariableBinding[] getDeclaredFields() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public IMethodBinding[] getDeclaredMethods() {
                if (lazyData[0] == null) {
                    List<IMethodBinding> list = new ArrayList<>();
                    for (IMethodBinding binding : phantomMethods.values()) {
                        if (binding.getDeclaringClass() == this) {
                            list.add(binding);
                        }
                    }
                    lazyData[0] = list.toArray(new IMethodBinding[list.size()]);
                }
                return (IMethodBinding[]) lazyData[0];
            }

            @Override
            public int getDeclaredModifiers() {
                // TODO Auto-generated method stub
                return 0;
            }

            @Override
            public ITypeBinding[] getDeclaredTypes() {
                // TODO Auto-generated method stub
                return emptyTypes;
            }

            @Override
            public ITypeBinding getDeclaringClass() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public IMethodBinding getDeclaringMethod() {
                return null;
            }

            @Override
            public IBinding getDeclaringMember() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public int getDimensions() {
                // TODO Auto-generated method stub
                return 0;
            }

            @Override
            public ITypeBinding getElementType() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding getErasure() {
                return (ITypeBinding) lazyData[1];
            }

            @Override
            public IMethodBinding getFunctionalInterfaceMethod() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding[] getInterfaces() {
                // TODO Auto-generated method stub
                return emptyTypes;
            }

            @Override
            public int getModifiers() {
                // TODO Auto-generated method stub
                return 0;
            }

            @Override
            public String getName() {
                // TODO Auto-generated method stub
                return name;
            }

            @Override
            public IPackageBinding getPackage() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public String getQualifiedName() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding getSuperclass() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public IAnnotationBinding[] getTypeAnnotations() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding[] getTypeArguments() {
                // TODO Auto-generated method stub
                return emptyTypes;
            }

            @Override
            public ITypeBinding[] getTypeBounds() {
                // TODO Auto-generated method stub
                return emptyTypes;
            }

            @Override
            public ITypeBinding getTypeDeclaration() {
                return (ITypeBinding) lazyData[1];
            }

            @Override
            public ITypeBinding[] getTypeParameters() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding getWildcard() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public boolean isAnnotation() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isAnonymous() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isArray() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isAssignmentCompatible(ITypeBinding variableType) {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isCapture() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isCastCompatible(ITypeBinding type) {
                return true;
            }

            @Override
            public boolean isClass() {
                return knownAsClasses.contains(name);
            }

            @Override
            public boolean isEnum() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isFromSource() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isGenericType() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isInterface() {
                return !knownAsClasses.contains(name);
            }

            @Override
            public boolean isIntersectionType() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isLocal() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isMember() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isNested() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isNullType() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isParameterizedType() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isPrimitive() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isRawType() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isSubTypeCompatible(ITypeBinding type) {
                return true;
            }

            @Override
            public boolean isTopLevel() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isTypeVariable() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isUpperbound() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isWildcardType() {
                // TODO Auto-generated method stub
                return false;
            }

        };
        lazyData[1] = binding;
        phantomTypes.put(name, binding);
        return binding;
    }

    public static ITypeBinding findOrCreateType(Expression exp) {
        return findOrCreateType(exp, true);
    }

    public static boolean isBroken(ITypeBinding type) {
        return type.isRecovered() && !type.getKey().startsWith("PHANTOM:");
    }

    public static ITypeBinding findOrCreateType(Expression exp, boolean resolve) {
        if (exp == null) {
            return findOrCreatePhantomType("unknown.Unknown");
        }
        ITypeBinding expType = resolve ? exp.resolveTypeBinding() : null;
        if (expType == null) {
            if (exp instanceof SimpleName) {
                return findOrCreateUnknownPhantomType(exp.toString());
            }
        } else if (isBroken(expType)) {
            return findOrCreateUnknownPhantomType(expType);
        } else {
            return expType;
        }
        return findOrCreatePhantomType("unknown.Unknown");
    }

    public static IMethodBinding findOrCreatePhantomMethod(Expression node) {

        if (phantomMethods == null) {
            phantomMethods = new IdentityHashMap<>();
        }
        if (phantomMethods.containsKey(node)) {
            return phantomMethods.get(node);
        }

        Expression exp = null;
        List<Expression> arguments = null;
        ITypeBinding klazz = null;
        String name = null;
        boolean isCtor = false;

        if (node instanceof MethodInvocation) {
            MethodInvocation method = (MethodInvocation) node;
            name = method.getName().toString();
            exp = method.getExpression();
            arguments = method.arguments();
            klazz = findOrCreateType(exp);

        } else if (node instanceof SuperMethodInvocation) {

            SuperMethodInvocation method = (SuperMethodInvocation) node;
            name = method.getName().toString();
            arguments = method.arguments();
            klazz = findOrCreatePhantomType("unknown.Unknown");

        } else if (node instanceof ClassInstanceCreation) {

            ClassInstanceCreation method = (ClassInstanceCreation) node;
            name = "<init>";
            arguments = method.arguments();
            isCtor = true;
            Type type = method.getType();
            klazz = type.resolveBinding();
            if (type instanceof SimpleType && (klazz == null || klazz.isRecovered())) {
                klazz = findOrCreateUnknownPhantomType(((SimpleType) type).getName().toString());
            }
        }

        List<ITypeBinding> list = new ArrayList();
        for (Expression arg : arguments) {
            list.add(findOrCreateType(arg));
        }
        ITypeBinding[] params = list.toArray(new ITypeBinding[list.size()]);

        ITypeBinding returnType = isCtor ? klazz : node.resolveTypeBinding();
        if (returnType == null) {
            returnType = findOrCreatePhantomType("unknown.Unknown");
        }

        IMethodBinding binding;
        if (!isCtor || arguments.size() > 0) {
            binding = findOrCreatePhantomMethod0(klazz, name, params, returnType, isCtor);
        } else {
            binding = findOrCreateDefaultCtor(klazz);
        }
        phantomMethods.put(node, binding);
        return binding;
    }

    public static IMethodBinding findOrCreateDefaultCtor(ITypeBinding klazz) {
        if (phantomMethods == null) {
            phantomMethods = new IdentityHashMap<>();
        }
        String key = (klazz.getName() + ".<init>()").intern();
        if (phantomMethods.containsKey(key)) {
            return phantomMethods.get(key);
        }
        IMethodBinding binding = findOrCreatePhantomMethod0(klazz, "<init>", new ITypeBinding[0], klazz, true);
        phantomMethods.put(key, binding);
        return binding;
    }

    public static IMethodBinding findOrCreateCloseable(ITypeBinding klazz) {
        if (phantomMethods == null) {
            phantomMethods = new IdentityHashMap<>();
        }
        String key = (klazz.getName() + ".close()").intern();
        if (phantomMethods.containsKey(key)) {
            return phantomMethods.get(key);
        }
        IMethodBinding binding = findOrCreatePhantomMethod0(klazz, "close", new ITypeBinding[0],
                wellKnownType.apply("void"), true);
        phantomMethods.put(key, binding);
        return binding;
    }

    public static IMethodBinding findOrCreatePhantomMethod0(ITypeBinding klazz, String name, ITypeBinding[] params,
            ITypeBinding returnType, boolean isCtor) {
        ITypeBinding[] exceptionTypes = new ITypeBinding[0];

        String key = "PHANTOM:" + methodSignature(klazz, name, params, returnType);

        Object[] lazyData = new Object[1];

        IMethodBinding binding = new IMethodBinding() {

            @Override
            public IAnnotationBinding[] getAnnotations() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public int getKind() {
                return METHOD;
            }

            @Override
            public int getModifiers() {
                // TODO Auto-generated method stub
                return 0;
            }

            @Override
            public boolean isDeprecated() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isRecovered() {
                return true;
            }

            @Override
            public boolean isSynthetic() {
                return false;
            }

            @Override
            public IJavaElement getJavaElement() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public String getKey() {
                return key;
            }

            @Override
            public boolean isEqualTo(IBinding binding) {
                return false;
            }

            @Override
            public boolean isConstructor() {
                return isCtor;
            }

            @Override
            public boolean isDefaultConstructor() {
                return false;
            }

            @Override
            public String getName() {
                return name;
            }

            @Override
            public ITypeBinding getDeclaringClass() {
                return klazz;
            }

            @Override
            public IBinding getDeclaringMember() {
                // TODO Auto-generated method stub
                return klazz;
            }

            @Override
            public Object getDefaultValue() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public IAnnotationBinding[] getParameterAnnotations(int paramIndex) {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public ITypeBinding[] getParameterTypes() {
                return params;
            }

            @Override
            public ITypeBinding getDeclaredReceiverType() {
                return klazz;
            }

            @Override
            public ITypeBinding getReturnType() {
                return returnType;
            }

            @Override
            public ITypeBinding[] getExceptionTypes() {
                return exceptionTypes;
            }

            @Override
            public ITypeBinding[] getTypeParameters() {
                // TODO Auto-generated method stub
                return null;
            }

            @Override
            public boolean isAnnotationMember() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isGenericMethod() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isParameterizedMethod() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public ITypeBinding[] getTypeArguments() {
                return params;
            }

            @Override
            public IMethodBinding getMethodDeclaration() {
                return (IMethodBinding) lazyData[0];
            }

            @Override
            public boolean isRawMethod() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isSubsignature(IMethodBinding otherMethod) {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean isVarargs() {
                // TODO Auto-generated method stub
                return false;
            }

            @Override
            public boolean overrides(IMethodBinding method) {
                // TODO Auto-generated method stub
                return false;
            }
        };
        lazyData[0] = binding;
        return binding;
    }

    public static String methodSignature(ITypeBinding klazz, String name, ITypeBinding[] params,
            ITypeBinding returnType) {
        String k = StringStuff.deployment2CanonicalTypeString(klazz.getBinaryName());
        k += " " + name + " (";
        for (ITypeBinding p : params) {
            k += p.isPrimitive() ? p.getBinaryName()
                    : StringStuff.deployment2CanonicalTypeString(p.getBinaryName()) + ";";
        }
        k += ")" + (returnType.isPrimitive() ? returnType.getBinaryName()
                : StringStuff.deployment2CanonicalTypeString(returnType.getBinaryName()) + ";");
        return k;
    }

    public static class DivaPhantomClass extends PhantomClass {
        public TypeReference classRef;
        public IClassHierarchy cha;
        public boolean isInterface;

        public DivaPhantomClass(TypeReference classRef, IClassHierarchy cha) {
            this(classRef, cha, false);
        }

        public DivaPhantomClass(TypeReference classRef, IClassHierarchy cha, boolean isInterface) {
            super(classRef, cha);
            this.classRef = classRef;
            this.cha = cha;
            this.isInterface = isInterface;
        }

        @Override
        public Collection<IField> getDeclaredInstanceFields() {
            return Collections.EMPTY_SET;
        }

        @Override
        public Collection<IMethod> getDeclaredMethods() {
            return Collections.EMPTY_SET;
        }

        @Override
        public IMethod getClassInitializer() {
            return getMethod(Selector.make("<clinit>()V"));
        }

        @Override
        public boolean isInterface() {
            return isInterface;
        }

        @Override
        public IMethod getMethod(Selector selector) {
            // AT: workaround ..
            // if (selector.getName().toString().equals("finalize"))
            // return null;
            TypeName[] params = selector.getDescriptor().getParameters();

            Collection<CAstQualifier> qualifiers = Collections.EMPTY_SET;
            Collection<Annotation> annotations = Collections.EMPTY_SET;
            MethodReference methodRef = MethodReference.findOrCreate(classRef, selector);

            return new AstMethod(DivaPhantomClass.this, qualifiers, methodRef, annotations) {

                @Override
                public boolean isAbstract() {
                    return true;
                }

                @Override
                public boolean isStatic() {
                    return false;
                }

                @Override
                public IClassHierarchy getClassHierarchy() {
                    return cha;
                }

                @Override
                public boolean hasLocalVariableTable() {
                    return false;
                }

                @Override
                public TypeReference getParameterType(int i) {
                    return TypeReference.findOrCreate(ClassLoaderReference.Extension, params[i]);
                }

                @Override
                public String getLocalVariableName(int bcIndex, int localNumber) {
                    return null;
                }

                @Override
                public TypeReference[] getDeclaredExceptions()
                        throws InvalidClassFileException, UnsupportedOperationException {
                    return null;
                }

                @Override
                public LexicalParent[] getParents() {
                    return null;
                }

                @Override
                public int getNumberOfParameters() {
                    return params == null ? 0 : params.length;
                }

            };
        }
    }

}

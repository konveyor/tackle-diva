package io.tackle.diva.irgen;

import java.util.Collection;
import java.util.Collections;

import com.ibm.wala.cast.loader.AstMethod;
import com.ibm.wala.cast.loader.AstMethod.LexicalParent;
import com.ibm.wala.cast.tree.CAstQualifier;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.PhantomClass;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.Selector;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.types.annotations.Annotation;

public class DivaPhantomClass extends PhantomClass {
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
        if (selector.getName().toString().equals("<clinit>"))
            return null;
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
package io.tackle.diva.irgen;

import java.util.Collection;
import java.util.Iterator;
import java.util.Set;
import java.util.Spliterator;
import java.util.function.Consumer;
import java.util.function.Predicate;

import com.ibm.wala.classLoader.ClassLoaderFactory;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.FieldReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.Selector;
import com.ibm.wala.types.TypeReference;

public class FilteredClassHierarchy implements IClassHierarchy {

    IClassHierarchy delegate;
    Predicate<IClass> filter;

    public FilteredClassHierarchy(IClassHierarchy delegate, Predicate<IClass> filter) {
        this.delegate = delegate;
        this.filter = filter;
    }

    @Override
    public Iterator<IClass> iterator() {
        return new Iterator<IClass>() {
            Iterator<IClass> i = delegate.iterator();
            IClass next;

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
            public IClass next() {
                if (hasNext()) {
                    IClass r = next;
                    next = null;
                    return r;
                }
                return null;
            }
        };
    }

    @Override
    public ClassLoaderFactory getFactory() {
        return delegate.getFactory();
    }

    @Override
    public AnalysisScope getScope() {
        return delegate.getScope();
    }

    @Override
    public IClassLoader[] getLoaders() {
        return delegate.getLoaders();
    }

    @Override
    public IClassLoader getLoader(ClassLoaderReference loaderRef) {
        return delegate.getLoader(loaderRef);
    }

    @Override
    public boolean addClass(IClass klass) {
        return delegate.addClass(klass);
    }

    @Override
    public int getNumberOfClasses() {
        return delegate.getNumberOfClasses();
    }

    @Override
    public boolean isRootClass(IClass c) {
        return delegate.isRootClass(c);
    }

    @Override
    public IClass getRootClass() {
        return delegate.getRootClass();
    }

    @Override
    public int getNumber(IClass c) {
        return delegate.getNumber(c);
    }

    @Override
    public Set<TypeReference> getUnresolvedClasses() {
        return delegate.getUnresolvedClasses();
    }

    @Override
    public Set<IMethod> getPossibleTargets(MethodReference ref) {
        return delegate.getPossibleTargets(ref);
    }

    @Override
    public void forEach(Consumer<? super IClass> action) {
        delegate.forEach(action);
    }

    @Override
    public Set<IMethod> getPossibleTargets(IClass receiverClass, MethodReference ref) {
        return delegate.getPossibleTargets(receiverClass, ref);
    }

    @Override
    public IMethod resolveMethod(MethodReference m) {
        return delegate.resolveMethod(m);
    }

    @Override
    public Spliterator<IClass> spliterator() {
        return delegate.spliterator();
    }

    @Override
    public IField resolveField(FieldReference f) {
        return delegate.resolveField(f);
    }

    @Override
    public IField resolveField(IClass klass, FieldReference f) {
        return delegate.resolveField(klass, f);
    }

    @Override
    public IMethod resolveMethod(IClass receiverClass, Selector selector) {
        return delegate.resolveMethod(receiverClass, selector);
    }

    @Override
    public IClass lookupClass(TypeReference A) {
        return delegate.lookupClass(A);
    }

    @Override
    public boolean isInterface(TypeReference type) {
        return delegate.isInterface(type);
    }

    @Override
    public IClass getLeastCommonSuperclass(IClass A, IClass B) {
        return delegate.getLeastCommonSuperclass(A, B);
    }

    @Override
    public TypeReference getLeastCommonSuperclass(TypeReference A, TypeReference B) {
        return delegate.getLeastCommonSuperclass(A, B);
    }

    @Override
    public boolean isSubclassOf(IClass c, IClass T) {
        return delegate.isSubclassOf(c, T);
    }

    @Override
    public boolean implementsInterface(IClass c, IClass i) {
        return delegate.implementsInterface(c, i);
    }

    @Override
    public Collection<IClass> computeSubClasses(TypeReference type) {
        return delegate.computeSubClasses(type);
    }

    @Override
    public Collection<TypeReference> getJavaLangErrorTypes() {
        return delegate.getJavaLangErrorTypes();
    }

    @Override
    public Collection<TypeReference> getJavaLangRuntimeExceptionTypes() {
        return delegate.getJavaLangRuntimeExceptionTypes();
    }

    @Override
    public Set<IClass> getImplementors(TypeReference type) {
        return delegate.getImplementors(type);
    }

    @Override
    public int getNumberOfImmediateSubclasses(IClass klass) {
        return delegate.getNumberOfImmediateSubclasses(klass);
    }

    @Override
    public Collection<IClass> getImmediateSubclasses(IClass klass) {
        return delegate.getImmediateSubclasses(klass);
    }

    @Override
    public boolean isAssignableFrom(IClass c1, IClass c2) {
        return delegate.isAssignableFrom(c1, c2);
    }

}

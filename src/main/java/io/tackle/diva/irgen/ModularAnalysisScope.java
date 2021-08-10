package io.tackle.diva.irgen;

import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.JavaLanguage;
import com.ibm.wala.classLoader.Language;
import com.ibm.wala.classLoader.Module;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.strings.Atom;

public class ModularAnalysisScope extends AnalysisScope {

    public ModularAnalysisScope() {
        this(Collections.singleton(Language.JAVA));
    }

    public ModularAnalysisScope(Set<JavaLanguage> languages) {
        super(languages);
        initCoreForJava();
    }

    Set<ClassLoaderReference> moduleRefs = new LinkedHashSet<>();

    public ClassLoaderReference addModuleLoader(String name, Module module, ClassLoaderReference parent) {
        ClassLoaderReference clref = new ClassLoaderReference(Atom.findOrCreateAsciiAtom("Source:" + name),
                Atom.findOrCreateAsciiAtom("Java"), parent);
        loadersByName.put(clref.getName(), clref);
        addToScope(clref, module);
        moduleRefs.add(clref);
        return clref;
    }

    public Set<ClassLoaderReference> moduleLoaderRefs() {
        return moduleRefs;
    }

    @Override
    public boolean isApplicationLoader(IClassLoader loader) {
        ClassLoaderReference clref = loader.getReference();
        return clref == ClassLoaderReference.Application || moduleRefs.contains(clref);
    }

}

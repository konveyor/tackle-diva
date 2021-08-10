package io.tackle.diva.irgen;

import java.util.Collection;
import java.util.Map;
import java.util.Set;

import com.ibm.wala.cast.java.translator.SourceModuleTranslator;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJSourceModuleTranslator;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.Module;
import com.ibm.wala.classLoader.ModuleEntry;
import com.ibm.wala.classLoader.SourceDirectoryTreeModule;
import com.ibm.wala.classLoader.SourceFileModule;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.collections.HashMapFactory;

public class DivaSourceLoaderImpl extends ECJSourceLoaderImpl {
    private final ClassLoaderReference classLoaderReference;
    private final String[] stdlibs;
    Map<String, ModuleEntry> sourceMap = HashMapFactory.make();
    int countdown;
    String[] srcDirs;

    public DivaSourceLoaderImpl(ClassLoaderReference loaderRef, IClassLoader parent, IClassHierarchy cha, boolean dump,
            ClassLoaderReference classLoaderReference, String[] stdlibs) {
        super(loaderRef, parent, cha, dump);
        this.classLoaderReference = classLoaderReference;
        this.stdlibs = stdlibs;
        Collection<Module> modules = cha.getScope().getModules(classLoaderReference);
        countdown = modules.size();
        srcDirs = new String[modules.size()];
        int k = 0;
        for (Module m : modules) {
            srcDirs[k++] = ((SourceDirectoryTreeModule) m).getPath();
        }
    }

    @Override
    protected SourceModuleTranslator getTranslator() {

        return new ECJSourceModuleTranslator(cha.getScope(), this, false) {

            @Override
            public void loadAllSources(Set<ModuleEntry> srcFiles) {

                for (ModuleEntry m : srcFiles) {
                    if (m.isSourceFile()) {
                        SourceFileModule s = (SourceFileModule) m;
                        sourceMap.put(s.getAbsolutePath(), s);
                    }
                }

                if (--countdown > 0)
                    return;

                DivaIRGen irgen = new DivaIRGen(DivaSourceLoaderImpl.this, c -> loadedClasses.put(c.getName(), c));
                irgen.genIR(cha, sourceMap, stdlibs, srcDirs, this::makeCAstTranslator, this::makeIRTranslator);
            }

        };
    }
}
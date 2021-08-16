package io.tackle.diva.irgen;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
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
    private final String[] stdlibs;
    Map<String, ModuleEntry> sourceMap = HashMapFactory.make();
    int countdown;
    String[] jdtDirs;

    public DivaSourceLoaderImpl(ClassLoaderReference loaderRef, IClassLoader parent, IClassHierarchy cha,
            String[] stdlibs) {
        super(loaderRef, parent, cha, false);
        this.stdlibs = stdlibs;
        countdown = cha.getScope().getModules(loaderRef).size();

        ClassLoaderReference clref = loaderRef;
        List<String> jdtDirList = new ArrayList<>();
        while (clref != ClassLoaderReference.Application) {
            Collection<Module> modules = cha.getScope().getModules(clref);
            for (Module m : modules) {
                jdtDirList.add(((SourceDirectoryTreeModule) m).getPath());
            }
            clref = clref.getParent();
        }
        jdtDirs = jdtDirList.toArray(new String[jdtDirList.size()]);
    }

    @Override
    protected SourceModuleTranslator getTranslator() {

        return new ECJSourceModuleTranslator(cha.getScope(), this, false) {

            @Override
            public void loadAllSources(Set<ModuleEntry> sourceFiles) {

                for (ModuleEntry m : sourceFiles) {
                    if (m.isSourceFile()) {
                        SourceFileModule s = (SourceFileModule) m;
                        sourceMap.put(s.getAbsolutePath(), s);
                    }
                }

                if (--countdown > 0)
                    return;

                DivaIRGen irgen = new DivaIRGen(DivaSourceLoaderImpl.this, c -> loadedClasses.put(c.getName(), c));
                irgen.genIR(cha, sourceMap, stdlibs, jdtDirs, this::makeCAstTranslator,
                        this::makeIRTranslator);
            }

        };
    }
}
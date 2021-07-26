package io.tackle.diva.windup;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.jboss.windup.config.GraphRewrite;
import org.jboss.windup.config.operation.GraphOperation;
import org.jboss.windup.graph.model.WindupConfigurationModel;
import org.jboss.windup.graph.model.resource.FileModel;
import org.jboss.windup.graph.service.WindupConfigurationService;
import org.ocpsoft.rewrite.context.EvaluationContext;

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.SourceDirectoryTreeModule;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.strings.StringStuff;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.Context;
import io.tackle.diva.DivaIRGen;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
import io.tackle.diva.Standalone;
import io.tackle.diva.Standalone.EntryConstraint;
import io.tackle.diva.Util;
import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.windup.model.DivaConstraintModel;
import io.tackle.diva.windup.model.DivaContextModel;
import io.tackle.diva.windup.model.DivaEntryMethodModel;
import io.tackle.diva.windup.model.DivaRequestParamModel;
import io.tackle.diva.windup.service.DivaEntryMethodService;
import io.tackle.diva.windup.service.GetOrCreateGraphService;

public class DivaLauncher extends GraphOperation {
    @Override
    public void perform(GraphRewrite event, EvaluationContext context) {
        try {
            Util.injectedCall(DivaIRGen.advices(), DivaLauncher.class.getName() + ".launch", event, context);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void launch(Object arg0, Object arg1) throws Exception {
        GraphRewrite event = (GraphRewrite) arg0;
        EvaluationContext context = (EvaluationContext) arg1;

        WindupConfigurationModel cfg = WindupConfigurationService.getConfigurationModel(event.getGraphContext());

        String[] sourceDirs = new String[cfg.getInputPaths().size()];
        int k = 0;
        for (FileModel file : cfg.getInputPaths()) {
            sourceDirs[k++] = file.getFilePath();
            Util.LOGGER.info(file.getFilePath());
            Util.LOGGER.info(file.getFileName());
            Util.LOGGER.info(file.toPrettyString());
        }

        AnalysisScope scope = new JavaSourceAnalysisScope() {
            @Override
            public boolean isApplicationLoader(IClassLoader loader) {
                return loader.getReference() == ClassLoaderReference.Application
                        || loader.getReference() == JavaSourceAnalysisScope.SOURCE;
            }
        };
        // add standard libraries to scope
        String[] stdlibs = Framework.loadStandardLib(scope);

        for (String sourceDir : sourceDirs) {
            scope.addToScope(JavaSourceAnalysisScope.SOURCE, new SourceDirectoryTreeModule(new File(sourceDir)));
        }

        // build the class hierarchy
        IClassHierarchy cha = ClassHierarchyFactory.makeWithRoot(scope,
                new ECJClassLoaderFactory(scope.getExclusions()) {
                    @Override
                    protected JavaSourceLoaderImpl makeSourceLoader(ClassLoaderReference classLoaderReference,
                            IClassHierarchy cha, IClassLoader parent) {
                        return DivaIRGen.makeNewSourceLoader(sourceDirs, stdlibs, classLoaderReference, cha, parent);
                    }
                });
        Util.LOGGER.info(cha.getNumberOfClasses() + " classes");
        Util.LOGGER.info(Warnings.asString());

        IClassLoader apploader = cha.getLoader(JavaSourceAnalysisScope.SOURCE);

        List<IMethod> entries = new ArrayList<>();
        entries.addAll(ServletAnalysis.getEntries(cha));
        entries.addAll(SpringBootAnalysis.getEntries(cha));

        List<IMethod> cgEntries = new ArrayList<>();
        cgEntries.addAll(entries);
        cgEntries.addAll(SpringBootAnalysis.getInits(cha));

        CallGraph cg = Standalone.gengraph(scope, cha, apploader, cgEntries);

        Framework fw = new Framework(cha, cg);

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                fw.recordContraint(new EntryConstraint(n));
            }
        }
        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Context> contexts = Standalone.calculateDefaultContexts(fw);
        // List<Context> contexts = Standalone.loadContexts(fw,
        // "/Users/aki/git/tackle-diva/dt-contexts.yml");

        JanusGraphReport<DivaContextModel> report = new JanusGraphReport<>(event.getGraphContext(),
                DivaContextModel.class);

        DivaEntryMethodService entryMethodService = new DivaEntryMethodService(event.getGraphContext());
        GetOrCreateGraphService<DivaRequestParamModel> requestParamService = new GetOrCreateGraphService<>(
                event.getGraphContext(), DivaRequestParamModel.class);

        for (Context cxt : contexts) {
            CGNode entry = null;
            for (Context.Constraint c : cxt) {
                if (c instanceof EntryConstraint) {
                    entry = ((EntryConstraint) c).node();
                }
            }
            if (entry != null) {
                CGNode n = entry;
                fw.calculateTransactions(entry, cxt, new Util.LazyReport(() -> {
                    Report[] delegate = new Report[] { null };
                    report.add((Report.Named map) -> {
                        map.put("constraints", (Report r) -> {
                            JanusGraphReport<DivaConstraintModel> cs = (JanusGraphReport<DivaConstraintModel>) r;
                            for (Context.Constraint c : cxt) {
                                if (c.category().equals("entry")) {
                                    IMethod m = ((Standalone.EntryConstraint) c).node().getMethod();
                                    DivaEntryMethodModel model = entryMethodService.getOrCreate(
                                            StringStuff.jvmToBinaryName(m.getDeclaringClass().getName().toString()),
                                            m.getName().toString());
                                    cs.add(model);
                                } else if (c.category().equals("http-param")) {
                                    DivaRequestParamModel model = requestParamService.getOrCreate(
                                            DivaRequestParamModel.PARAM_NAME, c.type(),
                                            DivaRequestParamModel.PARAM_VALUE, c.value());
                                    cs.add(model);
                                }
                            }
                        });
                        map.put("transactions", (Report txs) -> {
                            delegate[0] = txs;
                        });
                    });
                    return delegate[0];
                }));
            }
        }

        Util.LOGGER.info("DONE");
    }
}

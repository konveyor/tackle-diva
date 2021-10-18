package io.tackle.diva.windup;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Stack;
import java.util.function.Function;
import java.util.function.Supplier;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.jboss.windup.config.GraphRewrite;
import org.jboss.windup.config.operation.GraphOperation;
import org.jboss.windup.graph.GraphContext;
import org.jboss.windup.graph.model.ProjectDependencyModel;
import org.jboss.windup.graph.model.ProjectModel;
import org.jboss.windup.graph.model.WindupConfigurationModel;
import org.jboss.windup.graph.model.WindupFrame;
import org.jboss.windup.graph.model.resource.FileModel;
import org.jboss.windup.graph.model.resource.SourceFileModel;
import org.jboss.windup.graph.service.FileService;
import org.jboss.windup.graph.service.GraphService;
import org.jboss.windup.graph.service.WindupConfigurationService;
import org.jboss.windup.rules.apps.java.model.JavaClassModel;
import org.jboss.windup.rules.apps.java.model.JavaMethodModel;
import org.jboss.windup.rules.apps.java.model.PropertiesModel;
import org.jboss.windup.rules.apps.java.model.project.MavenProjectModel;
import org.ocpsoft.rewrite.context.EvaluationContext;

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.cast.java.loader.JavaSourceLoaderImpl;
import com.ibm.wala.cast.java.translator.jdt.ecj.ECJClassLoaderFactory;
import com.ibm.wala.classLoader.ClassLoaderFactory;
import com.ibm.wala.classLoader.ClassLoaderFactoryImpl;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.SourceDirectoryTreeModule;
import com.ibm.wala.ipa.callgraph.AnalysisOptions;
import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.AnnotationsReader.ConstantElementValue;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.annotations.Annotation;
import com.ibm.wala.util.strings.StringStuff;
import com.ibm.wala.util.warnings.Warnings;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Context.EntryConstraint;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;
import io.tackle.diva.analysis.JDBCAnalysis;
import io.tackle.diva.analysis.JPAAnalysis;
import io.tackle.diva.analysis.QuarkusAnalysis;
import io.tackle.diva.analysis.ServletAnalysis;
import io.tackle.diva.analysis.SpringBootAnalysis;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaSourceLoaderImpl;
import io.tackle.diva.irgen.ModularAnalysisScope;
import io.tackle.diva.windup.model.DivaAppModel;
import io.tackle.diva.windup.model.DivaConstraintModel;
import io.tackle.diva.windup.model.DivaContextModel;
import io.tackle.diva.windup.model.DivaEndpointModel;
import io.tackle.diva.windup.model.DivaEntryMethodModel;
import io.tackle.diva.windup.model.DivaRequestParamModel;
import io.tackle.diva.windup.model.DivaRestApiModel;
import io.tackle.diva.windup.model.DivaRestCallOpModel;
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

        List<? extends ProjectModel> projects = event.getGraphContext().getQuery(ProjectModel.class)
                .traverse(g -> g.filter(
                        __.out(ProjectModel.PROJECT_MODEL_TO_FILE).has(WindupFrame.TYPE_PROP, SourceFileModel.TYPE)))
                .toList(ProjectModel.class);
        List<? extends ProjectModel> notMaven = Util
                .makeList(Util.filter(projects, p -> !(p instanceof MavenProjectModel)));

        AnalysisScope scope;
        String[] stdlibs;
        ClassLoaderFactory clf;

        if (!projects.isEmpty() && notMaven.isEmpty()) {

            ModularAnalysisScope mods = new ModularAnalysisScope();
            scope = mods;
            stdlibs = Framework.loadStandardLib(mods);

            // For now, assume each p in projects has at-most-1 depending
            // p'. Partly due to wala's tree-not-dag class loaders (and class lookup
            // redundantly defined both in cha and loader-impl.)

            for (ProjectModel p : projects) {
                Util.LOGGER.info("Project: " + p.toPrettyString());

                Stack<ProjectModel> todo = new Stack<>();
                todo.push(p);

                while (true) {
                    List<ProjectModel> deps = Util.makeList(
                            Util.filter(Util.map(p.getDependencies(), ProjectDependencyModel::getProjectModel),
                                    projects::contains));
                    if (deps.isEmpty())
                        break;
                    p = deps.get(0);
                    todo.push(p);
                }
                ClassLoaderReference parent = ClassLoaderReference.Application;
                while (!todo.isEmpty()) {
                    p = todo.pop();
                    File f = new File(p.getRootFileModel().getFilePath() + "/src/main/java");
                    if (f.exists()) {
                        parent = mods.findOrCreateModuleLoader(p.getName(), new SourceDirectoryTreeModule(f), parent);
                    }
                }
            }

            clf = new ClassLoaderFactoryImpl(scope.getExclusions()) {
                @Override
                protected IClassLoader makeNewClassLoader(ClassLoaderReference classLoaderReference,
                        IClassHierarchy cha, IClassLoader parent, AnalysisScope unused) throws IOException {
                    if (mods.moduleLoaderRefs().contains(classLoaderReference)) {
                        IClassLoader cl = new DivaSourceLoaderImpl(classLoaderReference, parent, cha, stdlibs);
                        cl.init(mods.getModules(classLoaderReference));
                        return cl;
                    } else {
                        return super.makeNewClassLoader(classLoaderReference, cha, parent, scope);
                    }
                }
            };
        } else {
            WindupConfigurationModel cfg = WindupConfigurationService.getConfigurationModel(event.getGraphContext());
            List<String> sourceDirs = Util.makeList(Util.map(cfg.getInputPaths(), FileModel::getFilePath));
            Util.LOGGER.info("Using root source dirs: " + sourceDirs + " due to non-maven projects: " + notMaven);
            scope = new JavaSourceAnalysisScope() {
                @Override
                public boolean isApplicationLoader(IClassLoader loader) {
                    return loader.getReference() == ClassLoaderReference.Application
                            || loader.getReference() == JavaSourceAnalysisScope.SOURCE;
                }
            };
            // add standard libraries to scope
            stdlibs = Framework.loadStandardLib(scope);

            for (String sourceDir : sourceDirs) {
                scope.addToScope(JavaSourceAnalysisScope.SOURCE, new SourceDirectoryTreeModule(new File(sourceDir)));
            }
            clf = new ECJClassLoaderFactory(scope.getExclusions()) {
                @Override
                protected JavaSourceLoaderImpl makeSourceLoader(ClassLoaderReference classLoaderReference,
                        IClassHierarchy cha, IClassLoader parent) {
                    return new DivaSourceLoaderImpl(classLoaderReference, parent, cha, stdlibs);
                }
            };
        }

        DivaIRGen.init();
 
        // build the class hierarchy
        IClassHierarchy cha = ClassHierarchyFactory.makeWithRoot(scope, clf);
        Util.LOGGER.info(cha.getNumberOfClasses() + " classes");
        Util.LOGGER.info(Warnings.asString());

        List<IMethod> entries = new ArrayList<>();
        entries.addAll(ServletAnalysis.getEntries(cha));
        entries.addAll(SpringBootAnalysis.getEntries(cha));
        entries.addAll(QuarkusAnalysis.getEntries(cha));

        List<IMethod> cgEntries = new ArrayList<>();
        cgEntries.addAll(entries);
        cgEntries.addAll(SpringBootAnalysis.getInits(cha));

        JPAAnalysis.getEntities(cha);

        AnalysisOptions options = new AnalysisOptions();
        Supplier<CallGraph> builder = Framework.chaCgBuilder(cha, options, cgEntries);

        Util.LOGGER.info("building call graph...");
        CallGraph cg = builder.get();

        Framework fw = new Framework(cha, cg);

        for (CGNode n : cg) {
            if (entries.contains(n.getMethod())) {
                fw.recordContraint(new Context.EntryConstraint(n));
            }
        }
        fw.traverse(cg.getNode(0), ServletAnalysis.getContextualAnalysis(fw));

        List<Context> contexts = Context.calculateDefaultContexts(fw);
        // List<Context> contexts = Context.loadContexts(fw,
        // "/Users/aki/git/tackle-diva/dt-contexts.yml");

        JanusGraphReport<DivaContextModel> report = new JanusGraphReport<>(event.getGraphContext(),
                DivaContextModel.class);

        DivaEntryMethodService entryMethodService = new DivaEntryMethodService(event.getGraphContext());
        GetOrCreateGraphService<DivaRequestParamModel> requestParamService = new GetOrCreateGraphService<>(
                event.getGraphContext(), DivaRequestParamModel.class);

        for (Context cxt : contexts) {

            try {
                CGNode entry = null;
                for (Context.Constraint c : cxt) {
                    if (c instanceof Context.EntryConstraint) {
                        entry = ((Context.EntryConstraint) c).node();
                    }
                }
                if (entry != null) {
                    CGNode n = entry;
                    Trace.Visitor txAnalysis = JDBCAnalysis.getTransactionAnalysis(fw, cxt)
                            .with(SpringBootAnalysis.getTransactionAnalysis(fw, cxt)
                                    .with(JPAAnalysis.getTransactionAnalysis(fw, cxt)
                                            .with(QuarkusAnalysis.getTransactionAnalysis(fw, cxt))));

                    fw.calculateTransactions(entry, cxt, new Util.LazyReport() {
                        @Override
                        public void accept(Report.Builder txs) {
                            report.add((Report.Named map) -> {
                                map.put("constraints", (Report r) -> {
                                    JanusGraphReport<DivaConstraintModel> cs = (JanusGraphReport<DivaConstraintModel>) r;
                                    for (Context.Constraint c : cxt) {
                                        if (c.category().equals("entry")) {
                                            IMethod m = ((EntryConstraint) c).node().getMethod();
                                            DivaEntryMethodModel model = entryMethodService.getOrCreate(
                                                    StringStuff.jvmToBinaryName(
                                                            m.getDeclaringClass().getName().toString()),
                                                    m.getName().toString());
                                            for (Annotation a : Util.getAnnotations(m)) {
                                                // fill rest api if any
                                                if (a.getType().getName() == Constants.LJavaxWsRsGET) {
                                                    model.setHttpMethod("GET");
                                                } else if (a.getType().getName() == Constants.LJavaxWsRsPOST) {
                                                    model.setHttpMethod("POST");
                                                } else if (a.getType().getName() == Constants.LJavaxWsRsPATCH) {
                                                    model.setHttpMethod("PATCH");
                                                } else if (a.getType().getName() == Constants.LJavaxWsRsDELETE) {
                                                    model.setHttpMethod("DELETE");
                                                }
                                                if (a.getType().getName() == Constants.LJavaxWsRsPath) {
                                                    model.setUrlPath(DivaLauncher.stripBraces(((ConstantElementValue) a
                                                            .getNamedArguments().get("value")).val.toString()));
                                                }
                                                // @TODO. @WebServlet("/app")
                                            }
                                            cs.add(model);

                                        } else if (c.category().equals("http-param")) {
                                            DivaRequestParamModel model = requestParamService.getOrCreate(
                                                    DivaRequestParamModel.PARAM_NAME, c.type(),
                                                    DivaRequestParamModel.PARAM_VALUE, c.value());
                                            cs.add(model);
                                        }
                                    }
                                });
                                map.put("transactions", txs);
                            });
                        }
                    }, txAnalysis);
                }
                event.getGraphContext().getGraph().tx().commit();
            } catch (RuntimeException e) {
                event.getGraphContext().getGraph().tx().rollback();
            }
        }

        endpointResolution(event.getGraphContext(), projects);

        Util.LOGGER.info("DONE");
    }

    public static String stripBraces(String s) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            b.append(s.charAt(i));
            if (s.charAt(i) == '{') {
                for (; s.charAt(i) != '}'; i++)
                    ;
                b.append('}');
            }
        }
        return b.toString();
    }

    public static void endpointResolution(GraphContext gc, List<? extends ProjectModel> projects) {

        // 1) obtaining project -> application.properties mapping

        Map<String, Properties> appProps = new LinkedHashMap<>();
        FileService files = new FileService(gc);
        for (ProjectModel p : projects) {
            String targetPath = Paths.get(p.getRootFileModel().getFilePath())
                    .resolve("src/main/resources/application.properties").toString();
            PropertiesModel file = (PropertiesModel) files.findByPath(targetPath);
            if (file != null) {
                try {
                    appProps.put(p.getName(), file.getProperties());
                } catch (IOException e) {
                }
            }
        }

        Function<ProjectModel, DivaAppModel> toApp = p -> {
            DivaAppModel app;
            if (p instanceof DivaAppModel) {
                app = (DivaAppModel) p;
            } else {
                app = GraphService.addTypeToModel(gc, p, DivaAppModel.class);
                if (appProps.containsKey(p.getName())) {
                    String datasource = (String) appProps.get(p.getName()).getOrDefault("quarkus.datasource.jdbc.url",
                            null);
                    if (datasource != null) {
                        app.setDatasource(datasource);
                    }
                }
            }
            return app;
        };

        // 2) checking docker-compose.yml for hostname resolution for each project

        for (FileModel dockerComposeYaml : gc.getQuery(FileModel.class)
                .traverse(g -> g.has(FileModel.FILE_NAME, "docker-compose.yml")).toList(FileModel.class)) {
            try {
                Object o = Util.YAML_SERIALIZER.readValue(new File(dockerComposeYaml.getFilePath()), Object.class);
                for (Map.Entry<String, Map<String, Map<String, String>>> e : ((Map<String, Map<String, Map<String, Map<String, String>>>>) o)
                        .get("services").entrySet()) {
                    String targetPath = null;
                    if (e.getValue().getOrDefault("build", Collections.EMPTY_MAP).containsKey("dockerfile")) {
                        targetPath = Paths.get(dockerComposeYaml.getParentFile().getFilePath())
                                .resolve(e.getValue().get("build").get("dockerfile")).toFile().getCanonicalPath();

                    } else if (e.getValue().getOrDefault("build", Collections.EMPTY_MAP).containsKey("context")) {
                        targetPath = Paths.get(dockerComposeYaml.getParentFile().getFilePath())
                                .resolve(e.getValue().get("build").get("context")).toFile().getCanonicalPath();
                    }
                    if (targetPath != null) {
                        String thePath = targetPath;
                        List<? extends ProjectModel> ps = gc.getQuery(FileModel.class)
                                .traverse(
                                        g -> g.has(FileModel.FILE_PATH, thePath).in(ProjectModel.PROJECT_MODEL_TO_FILE))
                                .toList(ProjectModel.class);
                        for (ProjectModel p : ps) {
                            DivaAppModel app = toApp.apply(p);
                            app.setEndpointName(e.getKey());
                        }
                    }
                }
            } catch (IOException e1) {
            }
        }

        // 3) Attaching list of contexts to each app-model

        for (DivaContextModel cxt : gc.findAll(DivaContextModel.class)) {
            ProjectModel p = cxt
                    .traverse(g -> g.out(DivaContextModel.CONSTRAINTS).in(JavaClassModel.JAVA_METHOD)
                            .out(JavaClassModel.ORIGINAL_SOURCE).in(ProjectModel.PROJECT_MODEL_TO_FILE))
                    .next(ProjectModel.class);
            if (p != null) {
                DivaAppModel app = toApp.apply(p);
                app.addContext(cxt);
            }
        }

        // 4) Mapping each rest-call operation to its endpoint

        for (DivaRestCallOpModel call : gc.findAll(DivaRestCallOpModel.class)) {
            if (call.getMethod() == null)
                continue;
            JavaMethodModel meth = call.getMethod();
            JavaClassModel cls = meth.getJavaClass();
            List<? extends ProjectModel> ps = cls
                    .traverse(g -> g.out(JavaClassModel.ORIGINAL_SOURCE).in(ProjectModel.PROJECT_MODEL_TO_FILE))
                    .toList(ProjectModel.class);
            if (ps.isEmpty())
                continue;
            Properties props = appProps.getOrDefault(ps.get(0).getName(), null);
            if (props == null)
                continue;
            // org.apache.geronimo.daytrader.javaee6.accounts.service.PortfoliosRemoteCallService/mp-rest/url=http://daytrader-portfolios:8080/
            URL url;
            try {
                url = new URL((String) props.getOrDefault(cls.getQualifiedName() + "/mp-rest/url", null));
            } catch (RuntimeException | MalformedURLException e) {
                continue;
            }
            DivaAppModel app = gc.getQuery(DivaAppModel.class)
                    .traverse(g -> g.has(DivaEndpointModel.ENDPOINT_NAME, url.getHost())).next(DivaAppModel.class);
            if (app != null) {
                call.setEndpoint(app);
                List<? extends DivaEntryMethodModel> ms = app
                        .traverse(g -> g.out(DivaAppModel.CONTEXTS).out(DivaContextModel.CONSTRAINTS)
                                .has(DivaRestApiModel.URL_PATH, call.getUrlPath())
                                .has(DivaRestApiModel.HTTP_MEHOD, call.getHttpMethod()))
                        .toList(DivaEntryMethodModel.class);
                for (DivaEntryMethodModel m : ms) {
                    call.setEndpointMethod(m);
                    break;
                }

            }
        }

    }

}

package io.tackle.diva.windup;

import java.util.function.Consumer;
import java.util.function.Function;

import org.jboss.windup.graph.GraphContext;
import org.jboss.windup.graph.model.WindupVertexFrame;
import org.jboss.windup.graph.service.GraphService;
import org.jboss.windup.rules.apps.java.model.JavaClassModel;
import org.jboss.windup.rules.apps.java.model.JavaMethodModel;
import org.jboss.windup.rules.apps.java.service.JavaClassService;
import org.jboss.windup.rules.apps.java.service.JavaMethodService;

import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.IMethod.SourcePosition;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.util.strings.StringStuff;

import io.tackle.diva.Report;
import io.tackle.diva.Trace;
import io.tackle.diva.windup.model.DivaConstraintModel;
import io.tackle.diva.windup.model.DivaContextModel;
import io.tackle.diva.windup.model.DivaOpModel;
import io.tackle.diva.windup.model.DivaRestCallOpModel;
import io.tackle.diva.windup.model.DivaSqlOpModel;
import io.tackle.diva.windup.model.DivaStackTraceModel;
import io.tackle.diva.windup.model.DivaTxModel;
import io.tackle.diva.windup.service.DivaStackTraceService;

public class JanusGraphReport<T extends WindupVertexFrame> implements Report {

    GraphService<T> service = null;
    GraphContext gc;
    Consumer<T> addEdge = null;

    public JanusGraphReport(GraphContext context, Class<T> model) {
        this(context, model, null);
    }

    public JanusGraphReport(GraphContext context, Class<T> model, Consumer<T> addEdge) {
        this.gc = context;
        this.service = new GraphService<T>(context, model);
        this.addEdge = addEdge;
    }

    @Override
    public void add(Named.Builder builder) {
        T model = service.create();
        if (addEdge != null) {
            addEdge.accept(model);
        }
        builder.build(new Named<>(gc, model));
    }

    public void add(T model) {
        if (addEdge != null) {
            addEdge.accept(model);
        }
    }

    @Override
    public void add(Builder builder) {
        // TODO Auto-generated method stub

    }

    @Override
    public void add(String data) {
        // TODO Auto-generated method stub

    }

    public static class Named<T extends WindupVertexFrame> implements Report.Named {

        GraphContext gc;
        T model;

        public Named(GraphContext context, T model) {
            this.gc = context;
            this.model = model;
        }

        @Override
        public void putPrimitive(String key, Object value) {
            if (model instanceof DivaTxModel && key.equals("txid")) {
                ((DivaTxModel) model).setTxid((int) value);

            } else if (model instanceof DivaOpModel && key.equals("sql")) {
                DivaSqlOpModel m = GraphService.addTypeToModel(gc, model, DivaSqlOpModel.class);
                this.model = (T) m;
                m.setSql((String) value);

            } else if (model instanceof DivaRestCallOpModel && key.equals("http-method")) {
                ((DivaRestCallOpModel) model).setHttpMethod((String) value);

            } else if (model instanceof DivaRestCallOpModel && key.equals("url-path")) {
                ((DivaRestCallOpModel) model).setUrlPath(DivaLauncher.stripBraces((String) value));
            }
        }

        @Override
        public void put(String key, Builder builder) {
            if (model instanceof DivaOpModel && key.equals("rest-call")) {
                DivaRestCallOpModel m = GraphService.addTypeToModel(gc, model, DivaRestCallOpModel.class);
                this.model = (T) m;
                builder.build(new Named<DivaRestCallOpModel>(gc, m));
            }
        }

        @Override
        public void put(String key, io.tackle.diva.Report.Builder builder) {
            if (model instanceof DivaContextModel && key.equals("constraints")) {
                builder.build(new JanusGraphReport<>(gc, DivaConstraintModel.class,
                        ((DivaContextModel) model)::addConstraint));

            } else if (model instanceof DivaContextModel && key.equals("transactions")) {
                builder.build(
                        new JanusGraphReport<>(gc, DivaTxModel.class, ((DivaContextModel) model)::addTransaction));

            } else if (model instanceof DivaTxModel && key.equals("transaction")) {
                int[] counter = new int[] { 0 };
                builder.build(new JanusGraphReport<>(gc, DivaOpModel.class, op -> {
                    op.setOrdinal(counter[0]++);
                    ((DivaTxModel) model).addOp(op);
                }));
            }
        }

        @Override
        public <S> void put(String key, S data, Function<S, Report.Builder> fun) {
            if (model instanceof DivaOpModel && key.equals("stacktrace")) {
                DivaStackTraceService service = new DivaStackTraceService(gc);
                JavaClassService classService = new JavaClassService(gc);
                JavaMethodService methodService = new JavaMethodService(gc);
                DivaStackTraceModel parent = null;
                DivaStackTraceModel current = null;
                for (Trace t : ((Trace) data).reversed()) {
                    IMethod m = t.node().getMethod();
                    SourcePosition p = null;
                    try {
                        p = m.getSourcePosition(t.site().getProgramCounter());

                    } catch (InvalidClassFileException | NullPointerException e) {
                    }
                    JavaClassModel classModel = classService
                            .create(StringStuff.jvmToBinaryName(m.getDeclaringClass().getName().toString()));
                    JavaMethodModel methodModel = methodService.createJavaMethod(classModel, m.getName().toString());
                    classModel.addJavaMethod(methodModel);
                    if (p != null) {
                        current = service.getOrCreate(m.getDeclaringClass().getSourceFileName(), p.getFirstLine(),
                                p.getFirstCol(), p.getLastOffset() - p.getFirstOffset(), parent, methodModel);

                    } else {
                        current = service.create();
                        service.setFilePath(current, m.getDeclaringClass().getSourceFileName());
                        current.setMethod(methodModel);
                        if (parent != null) {
                            current.setParent(parent);
                        }
                    }
                    parent = current;
                }
                ((DivaOpModel) model).setStackTrace(current);
                if (((Trace) data).site() != null) {
                    MethodReference mref = ((Trace) data).site().getDeclaredTarget();
                    JavaClassModel classModel = classService
                            .create(StringStuff.jvmToBinaryName(mref.getDeclaringClass().getName().toString()));
                    JavaMethodModel methodModel = methodService.createJavaMethod(classModel, mref.getName().toString());
                    classModel.addJavaMethod(methodModel);
                    ((DivaOpModel) model).setMethod(methodModel);

                }
            } else {
                put(key, fun.apply(data));
            }
        }
    }

}

package io.tackle.diva.windup.service;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.jboss.windup.graph.GraphContext;
import org.jboss.windup.graph.service.GraphService;
import org.jboss.windup.rules.apps.java.model.JavaClassModel;
import org.jboss.windup.rules.apps.java.model.JavaMethodModel;
import org.jboss.windup.rules.apps.java.service.JavaClassService;
import org.jboss.windup.rules.apps.java.service.JavaMethodService;

import io.tackle.diva.windup.model.DivaEntryMethodModel;

public class DivaEntryMethodService extends GraphService<DivaEntryMethodModel> {

    public JavaClassService classService;
    public JavaMethodService methodService;

    public DivaEntryMethodService(GraphContext context) {
        super(context, DivaEntryMethodModel.class);
        classService = new JavaClassService(context);
        methodService = new JavaMethodService(context);
    }

    public DivaEntryMethodModel getOrCreate(String methodName, String className) {
        JavaClassModel classModel = classService.create(className);
        JavaMethodModel methodModel = methodService.createJavaMethod(classModel, methodName, new JavaClassModel[] {});
        GraphTraversal<?, ?> traversal = getQuery().getRawTraversal()
                .filter(__.out(DivaEntryMethodModel.METHOD).is(methodModel));
        DivaEntryMethodModel model = getUnique(traversal);
        if (model == null) {
            model = create();
            model.setMethod(methodModel);
        }
        return model;
    }

}

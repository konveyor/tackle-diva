package io.tackle.diva.windup.service;

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

    public DivaEntryMethodModel getOrCreate(String className, String methodName) {
        JavaClassModel classModel = classService.create(className);
        for (JavaMethodModel methodModel : classModel.getJavaMethods()) {
            if (methodModel.getMethodName().equals(methodName)) {
                if (methodModel instanceof DivaEntryMethodModel) {
                    return (DivaEntryMethodModel) methodModel;
                } else {
                    return addTypeToModel(methodModel);
                }
            }
        }
        DivaEntryMethodModel model = addTypeToModel(
                methodService.createJavaMethod(classModel, methodName, new JavaClassModel[] {}));
        classModel.addJavaMethod(model);
        return model;
    }

}

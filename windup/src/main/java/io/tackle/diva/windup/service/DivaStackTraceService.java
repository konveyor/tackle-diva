package io.tackle.diva.windup.service;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.jboss.windup.graph.GraphContext;
import org.jboss.windup.graph.model.FileLocationModel;
import org.jboss.windup.graph.model.FileReferenceModel;
import org.jboss.windup.graph.model.resource.FileModel;
import org.jboss.windup.graph.service.FileService;
import org.jboss.windup.graph.service.GraphService;

import io.tackle.diva.windup.model.DivaStackTraceModel;

public class DivaStackTraceService extends GraphService<DivaStackTraceModel> {

    FileService fileService;

    public DivaStackTraceService(GraphContext context) {
        super(context, DivaStackTraceModel.class);
        fileService = new FileService(context);
    }

    public void setFilePath(DivaStackTraceModel model, String filePath) {
        model.setFile(fileService.createByFilePath(filePath));
    }

    public DivaStackTraceModel getOrCreate(String filePath, int lineNumber, int columnNumber, int length,
            DivaStackTraceModel parent) {
        GraphTraversal<?, ?> traversal = getQuery().getRawTraversal().has(FileLocationModel.COLUMN_NUMBER, columnNumber)
                .has(FileLocationModel.LINE_NUMBER, lineNumber).has(FileLocationModel.LENGTH, length)
                .filter(__.out(FileReferenceModel.FILE_MODEL).has(FileModel.FILE_PATH, filePath));
        if (parent == null) {
            traversal = traversal.not(__.out(DivaStackTraceModel.PARENT));
        } else {
            traversal = traversal.filter(__.out(DivaStackTraceModel.PARENT).is(parent));
        }
        DivaStackTraceModel model = getUnique(traversal);
        if (model == null) {
            model = create();
            model.setColumnNumber(columnNumber);
            model.setLineNumber(lineNumber);
            model.setLength(length);
            setFilePath(model, filePath);
            if (parent != null) {
                model.setParent(parent);
            }
        }
        return model;
    }

}

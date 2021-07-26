package io.tackle.diva.windup;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.janusgraph.core.EdgeLabel;
import org.janusgraph.core.VertexLabel;
import org.janusgraph.core.schema.JanusGraphManagement;
import org.jboss.windup.config.GraphRewrite;
import org.jboss.windup.config.operation.GraphOperation;
import org.jboss.windup.graph.GraphContext;
import org.ocpsoft.rewrite.context.EvaluationContext;

public class BackupJanusGraph extends GraphOperation {

    @Override
    public void perform(GraphRewrite event, EvaluationContext context) {
        
        GraphContext graph = event.getGraphContext();
        
        try {
            graph.commit();
            graph.close();

            File sourceDirectory = graph.getGraphDirectory().toFile();
            File destinationDirectory = new File("janusgraph-backup/");
            FileUtils.copyDirectory(sourceDirectory, destinationDirectory);

        } catch (IOException e) {
            throw new RuntimeException(e);

        } finally {
            graph.load();

        }
    }

}

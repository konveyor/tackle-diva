package io.tackle.diva.windup.model;

import org.apache.tinkerpop.gremlin.structure.Direction;
import org.jboss.windup.graph.Adjacency;
import org.jboss.windup.graph.model.TypeValue;
import org.jboss.windup.graph.model.WindupVertexFrame;

@TypeValue(DivaOpModel.TYPE)
public interface DivaOpModel extends WindupVertexFrame {

    String TYPE = "DivaOpModel";
    String STACKTRACE = "stacktrace";

    @Adjacency(label = STACKTRACE, direction = Direction.OUT)
    DivaStackTraceModel getStackTrace();
    
    @Adjacency(label = STACKTRACE, direction = Direction.OUT)
    void setStackTrace(DivaStackTraceModel model);
}

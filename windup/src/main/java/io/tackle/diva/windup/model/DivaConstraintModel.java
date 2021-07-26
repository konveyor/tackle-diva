package io.tackle.diva.windup.model;

import org.jboss.windup.graph.model.TypeValue;
import org.jboss.windup.graph.model.WindupVertexFrame;

@TypeValue(DivaConstraintModel.TYPE)
public interface DivaConstraintModel extends WindupVertexFrame {

    String TYPE = "DivaConstraintModel";

}

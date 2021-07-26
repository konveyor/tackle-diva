package io.tackle.diva.windup.model;

import org.apache.tinkerpop.gremlin.structure.Direction;
import org.jboss.windup.graph.Adjacency;
import org.jboss.windup.graph.model.TypeValue;
import org.jboss.windup.rules.apps.java.model.JavaMethodModel;

@TypeValue(DivaEntryMethodModel.TYPE)
public interface DivaEntryMethodModel extends DivaConstraintModel {

    String TYPE = "DivaMethodEntryModel";
    String METHOD = "method";

    @Adjacency(label = METHOD, direction = Direction.OUT)
    JavaMethodModel getMethod();
    
    @Adjacency(label = METHOD, direction = Direction.OUT)
    void setMethod(JavaMethodModel method);

}

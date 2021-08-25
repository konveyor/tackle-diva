package io.tackle.diva.windup.model;

import org.apache.tinkerpop.gremlin.structure.Direction;
import org.jboss.windup.graph.Adjacency;
import org.jboss.windup.graph.model.TypeValue;
import org.jboss.windup.rules.apps.java.model.JavaMethodModel;

@TypeValue(DivaRestCallOpModel.TYPE)
public interface DivaRestCallOpModel extends DivaOpModel, DivaRestApiModel {
    String TYPE = "DivaRestCallOpModel";
    String ENDPOINT = "endpoint";
    String ENDPOINT_METHOD = "endpointMethod";

    @Adjacency(label = ENDPOINT, direction = Direction.OUT)
    DivaEndpointModel getEndpoint();

    @Adjacency(label = ENDPOINT, direction = Direction.OUT)
    void setEndpoint(DivaEndpointModel app);

    @Adjacency(label = ENDPOINT_METHOD, direction = Direction.OUT)
    JavaMethodModel getEndpointMethod();

    @Adjacency(label = ENDPOINT_METHOD, direction = Direction.OUT)
    void setEndpointMethod(JavaMethodModel m);
}

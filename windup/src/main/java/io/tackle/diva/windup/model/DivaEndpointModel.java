package io.tackle.diva.windup.model;

import org.jboss.windup.graph.Property;
import org.jboss.windup.graph.model.TypeValue;
import org.jboss.windup.graph.model.WindupVertexFrame;

@TypeValue(DivaEndpointModel.TYPE)
public interface DivaEndpointModel extends WindupVertexFrame {

    String TYPE = "DivaEndpointModel";
    String ENDPOINT_NAME = "endpointName";

    @Property(ENDPOINT_NAME)
    String getEndpointName();

    @Property(ENDPOINT_NAME)
    void setEndpointName(String endpointName);

}

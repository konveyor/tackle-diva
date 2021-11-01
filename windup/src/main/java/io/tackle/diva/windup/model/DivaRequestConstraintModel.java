package io.tackle.diva.windup.model;

import org.jboss.windup.graph.model.TypeValue;

@TypeValue(DivaRequestConstraintModel.TYPE)
public interface DivaRequestConstraintModel extends DivaRequestParamModel, DivaConstraintModel {

    String TYPE = "DivaRequestConstraintModel";

}

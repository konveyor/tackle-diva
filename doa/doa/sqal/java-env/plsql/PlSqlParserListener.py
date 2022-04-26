# Generated from plsql/PlSqlParser.g4 by ANTLR 4.10
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PlSqlParser import PlSqlParser
else:
    from PlSqlParser import PlSqlParser

# This class defines a complete listener for a parse tree produced by PlSqlParser.
class PlSqlParserListener(ParseTreeListener):

    # Enter a parse tree produced by PlSqlParser#sql_script.
    def enterSql_script(self, ctx:PlSqlParser.Sql_scriptContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sql_script.
    def exitSql_script(self, ctx:PlSqlParser.Sql_scriptContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unit_statement.
    def enterUnit_statement(self, ctx:PlSqlParser.Unit_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unit_statement.
    def exitUnit_statement(self, ctx:PlSqlParser.Unit_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_function.
    def enterDrop_function(self, ctx:PlSqlParser.Drop_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_function.
    def exitDrop_function(self, ctx:PlSqlParser.Drop_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_function.
    def enterAlter_function(self, ctx:PlSqlParser.Alter_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_function.
    def exitAlter_function(self, ctx:PlSqlParser.Alter_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_function_body.
    def enterCreate_function_body(self, ctx:PlSqlParser.Create_function_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_function_body.
    def exitCreate_function_body(self, ctx:PlSqlParser.Create_function_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parallel_enable_clause.
    def enterParallel_enable_clause(self, ctx:PlSqlParser.Parallel_enable_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parallel_enable_clause.
    def exitParallel_enable_clause(self, ctx:PlSqlParser.Parallel_enable_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_by_clause.
    def enterPartition_by_clause(self, ctx:PlSqlParser.Partition_by_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_by_clause.
    def exitPartition_by_clause(self, ctx:PlSqlParser.Partition_by_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#result_cache_clause.
    def enterResult_cache_clause(self, ctx:PlSqlParser.Result_cache_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#result_cache_clause.
    def exitResult_cache_clause(self, ctx:PlSqlParser.Result_cache_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#relies_on_part.
    def enterRelies_on_part(self, ctx:PlSqlParser.Relies_on_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#relies_on_part.
    def exitRelies_on_part(self, ctx:PlSqlParser.Relies_on_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#streaming_clause.
    def enterStreaming_clause(self, ctx:PlSqlParser.Streaming_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#streaming_clause.
    def exitStreaming_clause(self, ctx:PlSqlParser.Streaming_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_package.
    def enterDrop_package(self, ctx:PlSqlParser.Drop_packageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_package.
    def exitDrop_package(self, ctx:PlSqlParser.Drop_packageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_package.
    def enterAlter_package(self, ctx:PlSqlParser.Alter_packageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_package.
    def exitAlter_package(self, ctx:PlSqlParser.Alter_packageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_package.
    def enterCreate_package(self, ctx:PlSqlParser.Create_packageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_package.
    def exitCreate_package(self, ctx:PlSqlParser.Create_packageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_package_body.
    def enterCreate_package_body(self, ctx:PlSqlParser.Create_package_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_package_body.
    def exitCreate_package_body(self, ctx:PlSqlParser.Create_package_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#package_obj_spec.
    def enterPackage_obj_spec(self, ctx:PlSqlParser.Package_obj_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#package_obj_spec.
    def exitPackage_obj_spec(self, ctx:PlSqlParser.Package_obj_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#procedure_spec.
    def enterProcedure_spec(self, ctx:PlSqlParser.Procedure_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#procedure_spec.
    def exitProcedure_spec(self, ctx:PlSqlParser.Procedure_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_spec.
    def enterFunction_spec(self, ctx:PlSqlParser.Function_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_spec.
    def exitFunction_spec(self, ctx:PlSqlParser.Function_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#package_obj_body.
    def enterPackage_obj_body(self, ctx:PlSqlParser.Package_obj_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#package_obj_body.
    def exitPackage_obj_body(self, ctx:PlSqlParser.Package_obj_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_procedure.
    def enterDrop_procedure(self, ctx:PlSqlParser.Drop_procedureContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_procedure.
    def exitDrop_procedure(self, ctx:PlSqlParser.Drop_procedureContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_procedure.
    def enterAlter_procedure(self, ctx:PlSqlParser.Alter_procedureContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_procedure.
    def exitAlter_procedure(self, ctx:PlSqlParser.Alter_procedureContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_body.
    def enterFunction_body(self, ctx:PlSqlParser.Function_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_body.
    def exitFunction_body(self, ctx:PlSqlParser.Function_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#procedure_body.
    def enterProcedure_body(self, ctx:PlSqlParser.Procedure_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#procedure_body.
    def exitProcedure_body(self, ctx:PlSqlParser.Procedure_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_procedure_body.
    def enterCreate_procedure_body(self, ctx:PlSqlParser.Create_procedure_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_procedure_body.
    def exitCreate_procedure_body(self, ctx:PlSqlParser.Create_procedure_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_trigger.
    def enterDrop_trigger(self, ctx:PlSqlParser.Drop_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_trigger.
    def exitDrop_trigger(self, ctx:PlSqlParser.Drop_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_trigger.
    def enterAlter_trigger(self, ctx:PlSqlParser.Alter_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_trigger.
    def exitAlter_trigger(self, ctx:PlSqlParser.Alter_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_trigger.
    def enterCreate_trigger(self, ctx:PlSqlParser.Create_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_trigger.
    def exitCreate_trigger(self, ctx:PlSqlParser.Create_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trigger_follows_clause.
    def enterTrigger_follows_clause(self, ctx:PlSqlParser.Trigger_follows_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trigger_follows_clause.
    def exitTrigger_follows_clause(self, ctx:PlSqlParser.Trigger_follows_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trigger_when_clause.
    def enterTrigger_when_clause(self, ctx:PlSqlParser.Trigger_when_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trigger_when_clause.
    def exitTrigger_when_clause(self, ctx:PlSqlParser.Trigger_when_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#simple_dml_trigger.
    def enterSimple_dml_trigger(self, ctx:PlSqlParser.Simple_dml_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#simple_dml_trigger.
    def exitSimple_dml_trigger(self, ctx:PlSqlParser.Simple_dml_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#for_each_row.
    def enterFor_each_row(self, ctx:PlSqlParser.For_each_rowContext):
        pass

    # Exit a parse tree produced by PlSqlParser#for_each_row.
    def exitFor_each_row(self, ctx:PlSqlParser.For_each_rowContext):
        pass


    # Enter a parse tree produced by PlSqlParser#compound_dml_trigger.
    def enterCompound_dml_trigger(self, ctx:PlSqlParser.Compound_dml_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#compound_dml_trigger.
    def exitCompound_dml_trigger(self, ctx:PlSqlParser.Compound_dml_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#non_dml_trigger.
    def enterNon_dml_trigger(self, ctx:PlSqlParser.Non_dml_triggerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#non_dml_trigger.
    def exitNon_dml_trigger(self, ctx:PlSqlParser.Non_dml_triggerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trigger_body.
    def enterTrigger_body(self, ctx:PlSqlParser.Trigger_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trigger_body.
    def exitTrigger_body(self, ctx:PlSqlParser.Trigger_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#routine_clause.
    def enterRoutine_clause(self, ctx:PlSqlParser.Routine_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#routine_clause.
    def exitRoutine_clause(self, ctx:PlSqlParser.Routine_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#compound_trigger_block.
    def enterCompound_trigger_block(self, ctx:PlSqlParser.Compound_trigger_blockContext):
        pass

    # Exit a parse tree produced by PlSqlParser#compound_trigger_block.
    def exitCompound_trigger_block(self, ctx:PlSqlParser.Compound_trigger_blockContext):
        pass


    # Enter a parse tree produced by PlSqlParser#timing_point_section.
    def enterTiming_point_section(self, ctx:PlSqlParser.Timing_point_sectionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#timing_point_section.
    def exitTiming_point_section(self, ctx:PlSqlParser.Timing_point_sectionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#non_dml_event.
    def enterNon_dml_event(self, ctx:PlSqlParser.Non_dml_eventContext):
        pass

    # Exit a parse tree produced by PlSqlParser#non_dml_event.
    def exitNon_dml_event(self, ctx:PlSqlParser.Non_dml_eventContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dml_event_clause.
    def enterDml_event_clause(self, ctx:PlSqlParser.Dml_event_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dml_event_clause.
    def exitDml_event_clause(self, ctx:PlSqlParser.Dml_event_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dml_event_element.
    def enterDml_event_element(self, ctx:PlSqlParser.Dml_event_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dml_event_element.
    def exitDml_event_element(self, ctx:PlSqlParser.Dml_event_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dml_event_nested_clause.
    def enterDml_event_nested_clause(self, ctx:PlSqlParser.Dml_event_nested_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dml_event_nested_clause.
    def exitDml_event_nested_clause(self, ctx:PlSqlParser.Dml_event_nested_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#referencing_clause.
    def enterReferencing_clause(self, ctx:PlSqlParser.Referencing_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#referencing_clause.
    def exitReferencing_clause(self, ctx:PlSqlParser.Referencing_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#referencing_element.
    def enterReferencing_element(self, ctx:PlSqlParser.Referencing_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#referencing_element.
    def exitReferencing_element(self, ctx:PlSqlParser.Referencing_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_type.
    def enterDrop_type(self, ctx:PlSqlParser.Drop_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_type.
    def exitDrop_type(self, ctx:PlSqlParser.Drop_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_type.
    def enterAlter_type(self, ctx:PlSqlParser.Alter_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_type.
    def exitAlter_type(self, ctx:PlSqlParser.Alter_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#compile_type_clause.
    def enterCompile_type_clause(self, ctx:PlSqlParser.Compile_type_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#compile_type_clause.
    def exitCompile_type_clause(self, ctx:PlSqlParser.Compile_type_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#replace_type_clause.
    def enterReplace_type_clause(self, ctx:PlSqlParser.Replace_type_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#replace_type_clause.
    def exitReplace_type_clause(self, ctx:PlSqlParser.Replace_type_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_method_spec.
    def enterAlter_method_spec(self, ctx:PlSqlParser.Alter_method_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_method_spec.
    def exitAlter_method_spec(self, ctx:PlSqlParser.Alter_method_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_method_element.
    def enterAlter_method_element(self, ctx:PlSqlParser.Alter_method_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_method_element.
    def exitAlter_method_element(self, ctx:PlSqlParser.Alter_method_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_attribute_definition.
    def enterAlter_attribute_definition(self, ctx:PlSqlParser.Alter_attribute_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_attribute_definition.
    def exitAlter_attribute_definition(self, ctx:PlSqlParser.Alter_attribute_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#attribute_definition.
    def enterAttribute_definition(self, ctx:PlSqlParser.Attribute_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#attribute_definition.
    def exitAttribute_definition(self, ctx:PlSqlParser.Attribute_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_collection_clauses.
    def enterAlter_collection_clauses(self, ctx:PlSqlParser.Alter_collection_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_collection_clauses.
    def exitAlter_collection_clauses(self, ctx:PlSqlParser.Alter_collection_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dependent_handling_clause.
    def enterDependent_handling_clause(self, ctx:PlSqlParser.Dependent_handling_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dependent_handling_clause.
    def exitDependent_handling_clause(self, ctx:PlSqlParser.Dependent_handling_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dependent_exceptions_part.
    def enterDependent_exceptions_part(self, ctx:PlSqlParser.Dependent_exceptions_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dependent_exceptions_part.
    def exitDependent_exceptions_part(self, ctx:PlSqlParser.Dependent_exceptions_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_type.
    def enterCreate_type(self, ctx:PlSqlParser.Create_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_type.
    def exitCreate_type(self, ctx:PlSqlParser.Create_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_definition.
    def enterType_definition(self, ctx:PlSqlParser.Type_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_definition.
    def exitType_definition(self, ctx:PlSqlParser.Type_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_type_def.
    def enterObject_type_def(self, ctx:PlSqlParser.Object_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_type_def.
    def exitObject_type_def(self, ctx:PlSqlParser.Object_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_as_part.
    def enterObject_as_part(self, ctx:PlSqlParser.Object_as_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_as_part.
    def exitObject_as_part(self, ctx:PlSqlParser.Object_as_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_under_part.
    def enterObject_under_part(self, ctx:PlSqlParser.Object_under_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_under_part.
    def exitObject_under_part(self, ctx:PlSqlParser.Object_under_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#nested_table_type_def.
    def enterNested_table_type_def(self, ctx:PlSqlParser.Nested_table_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#nested_table_type_def.
    def exitNested_table_type_def(self, ctx:PlSqlParser.Nested_table_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sqlj_object_type.
    def enterSqlj_object_type(self, ctx:PlSqlParser.Sqlj_object_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sqlj_object_type.
    def exitSqlj_object_type(self, ctx:PlSqlParser.Sqlj_object_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_body.
    def enterType_body(self, ctx:PlSqlParser.Type_bodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_body.
    def exitType_body(self, ctx:PlSqlParser.Type_bodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_body_elements.
    def enterType_body_elements(self, ctx:PlSqlParser.Type_body_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_body_elements.
    def exitType_body_elements(self, ctx:PlSqlParser.Type_body_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#map_order_func_declaration.
    def enterMap_order_func_declaration(self, ctx:PlSqlParser.Map_order_func_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#map_order_func_declaration.
    def exitMap_order_func_declaration(self, ctx:PlSqlParser.Map_order_func_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subprog_decl_in_type.
    def enterSubprog_decl_in_type(self, ctx:PlSqlParser.Subprog_decl_in_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subprog_decl_in_type.
    def exitSubprog_decl_in_type(self, ctx:PlSqlParser.Subprog_decl_in_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#proc_decl_in_type.
    def enterProc_decl_in_type(self, ctx:PlSqlParser.Proc_decl_in_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#proc_decl_in_type.
    def exitProc_decl_in_type(self, ctx:PlSqlParser.Proc_decl_in_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#func_decl_in_type.
    def enterFunc_decl_in_type(self, ctx:PlSqlParser.Func_decl_in_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#func_decl_in_type.
    def exitFunc_decl_in_type(self, ctx:PlSqlParser.Func_decl_in_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constructor_declaration.
    def enterConstructor_declaration(self, ctx:PlSqlParser.Constructor_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constructor_declaration.
    def exitConstructor_declaration(self, ctx:PlSqlParser.Constructor_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modifier_clause.
    def enterModifier_clause(self, ctx:PlSqlParser.Modifier_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modifier_clause.
    def exitModifier_clause(self, ctx:PlSqlParser.Modifier_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_member_spec.
    def enterObject_member_spec(self, ctx:PlSqlParser.Object_member_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_member_spec.
    def exitObject_member_spec(self, ctx:PlSqlParser.Object_member_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sqlj_object_type_attr.
    def enterSqlj_object_type_attr(self, ctx:PlSqlParser.Sqlj_object_type_attrContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sqlj_object_type_attr.
    def exitSqlj_object_type_attr(self, ctx:PlSqlParser.Sqlj_object_type_attrContext):
        pass


    # Enter a parse tree produced by PlSqlParser#element_spec.
    def enterElement_spec(self, ctx:PlSqlParser.Element_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#element_spec.
    def exitElement_spec(self, ctx:PlSqlParser.Element_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#element_spec_options.
    def enterElement_spec_options(self, ctx:PlSqlParser.Element_spec_optionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#element_spec_options.
    def exitElement_spec_options(self, ctx:PlSqlParser.Element_spec_optionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subprogram_spec.
    def enterSubprogram_spec(self, ctx:PlSqlParser.Subprogram_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subprogram_spec.
    def exitSubprogram_spec(self, ctx:PlSqlParser.Subprogram_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#overriding_subprogram_spec.
    def enterOverriding_subprogram_spec(self, ctx:PlSqlParser.Overriding_subprogram_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#overriding_subprogram_spec.
    def exitOverriding_subprogram_spec(self, ctx:PlSqlParser.Overriding_subprogram_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#overriding_function_spec.
    def enterOverriding_function_spec(self, ctx:PlSqlParser.Overriding_function_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#overriding_function_spec.
    def exitOverriding_function_spec(self, ctx:PlSqlParser.Overriding_function_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_procedure_spec.
    def enterType_procedure_spec(self, ctx:PlSqlParser.Type_procedure_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_procedure_spec.
    def exitType_procedure_spec(self, ctx:PlSqlParser.Type_procedure_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_function_spec.
    def enterType_function_spec(self, ctx:PlSqlParser.Type_function_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_function_spec.
    def exitType_function_spec(self, ctx:PlSqlParser.Type_function_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constructor_spec.
    def enterConstructor_spec(self, ctx:PlSqlParser.Constructor_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constructor_spec.
    def exitConstructor_spec(self, ctx:PlSqlParser.Constructor_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#map_order_function_spec.
    def enterMap_order_function_spec(self, ctx:PlSqlParser.Map_order_function_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#map_order_function_spec.
    def exitMap_order_function_spec(self, ctx:PlSqlParser.Map_order_function_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pragma_clause.
    def enterPragma_clause(self, ctx:PlSqlParser.Pragma_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pragma_clause.
    def exitPragma_clause(self, ctx:PlSqlParser.Pragma_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pragma_elements.
    def enterPragma_elements(self, ctx:PlSqlParser.Pragma_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pragma_elements.
    def exitPragma_elements(self, ctx:PlSqlParser.Pragma_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_elements_parameter.
    def enterType_elements_parameter(self, ctx:PlSqlParser.Type_elements_parameterContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_elements_parameter.
    def exitType_elements_parameter(self, ctx:PlSqlParser.Type_elements_parameterContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_sequence.
    def enterDrop_sequence(self, ctx:PlSqlParser.Drop_sequenceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_sequence.
    def exitDrop_sequence(self, ctx:PlSqlParser.Drop_sequenceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_sequence.
    def enterAlter_sequence(self, ctx:PlSqlParser.Alter_sequenceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_sequence.
    def exitAlter_sequence(self, ctx:PlSqlParser.Alter_sequenceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_session.
    def enterAlter_session(self, ctx:PlSqlParser.Alter_sessionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_session.
    def exitAlter_session(self, ctx:PlSqlParser.Alter_sessionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_session_set_clause.
    def enterAlter_session_set_clause(self, ctx:PlSqlParser.Alter_session_set_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_session_set_clause.
    def exitAlter_session_set_clause(self, ctx:PlSqlParser.Alter_session_set_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_sequence.
    def enterCreate_sequence(self, ctx:PlSqlParser.Create_sequenceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_sequence.
    def exitCreate_sequence(self, ctx:PlSqlParser.Create_sequenceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sequence_spec.
    def enterSequence_spec(self, ctx:PlSqlParser.Sequence_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sequence_spec.
    def exitSequence_spec(self, ctx:PlSqlParser.Sequence_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sequence_start_clause.
    def enterSequence_start_clause(self, ctx:PlSqlParser.Sequence_start_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sequence_start_clause.
    def exitSequence_start_clause(self, ctx:PlSqlParser.Sequence_start_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_index.
    def enterCreate_index(self, ctx:PlSqlParser.Create_indexContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_index.
    def exitCreate_index(self, ctx:PlSqlParser.Create_indexContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cluster_index_clause.
    def enterCluster_index_clause(self, ctx:PlSqlParser.Cluster_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cluster_index_clause.
    def exitCluster_index_clause(self, ctx:PlSqlParser.Cluster_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cluster_name.
    def enterCluster_name(self, ctx:PlSqlParser.Cluster_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cluster_name.
    def exitCluster_name(self, ctx:PlSqlParser.Cluster_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_index_clause.
    def enterTable_index_clause(self, ctx:PlSqlParser.Table_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_index_clause.
    def exitTable_index_clause(self, ctx:PlSqlParser.Table_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#bitmap_join_index_clause.
    def enterBitmap_join_index_clause(self, ctx:PlSqlParser.Bitmap_join_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#bitmap_join_index_clause.
    def exitBitmap_join_index_clause(self, ctx:PlSqlParser.Bitmap_join_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_expr.
    def enterIndex_expr(self, ctx:PlSqlParser.Index_exprContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_expr.
    def exitIndex_expr(self, ctx:PlSqlParser.Index_exprContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_properties.
    def enterIndex_properties(self, ctx:PlSqlParser.Index_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_properties.
    def exitIndex_properties(self, ctx:PlSqlParser.Index_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#domain_index_clause.
    def enterDomain_index_clause(self, ctx:PlSqlParser.Domain_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#domain_index_clause.
    def exitDomain_index_clause(self, ctx:PlSqlParser.Domain_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#local_domain_index_clause.
    def enterLocal_domain_index_clause(self, ctx:PlSqlParser.Local_domain_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#local_domain_index_clause.
    def exitLocal_domain_index_clause(self, ctx:PlSqlParser.Local_domain_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlindex_clause.
    def enterXmlindex_clause(self, ctx:PlSqlParser.Xmlindex_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlindex_clause.
    def exitXmlindex_clause(self, ctx:PlSqlParser.Xmlindex_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#local_xmlindex_clause.
    def enterLocal_xmlindex_clause(self, ctx:PlSqlParser.Local_xmlindex_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#local_xmlindex_clause.
    def exitLocal_xmlindex_clause(self, ctx:PlSqlParser.Local_xmlindex_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#global_partitioned_index.
    def enterGlobal_partitioned_index(self, ctx:PlSqlParser.Global_partitioned_indexContext):
        pass

    # Exit a parse tree produced by PlSqlParser#global_partitioned_index.
    def exitGlobal_partitioned_index(self, ctx:PlSqlParser.Global_partitioned_indexContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_partitioning_clause.
    def enterIndex_partitioning_clause(self, ctx:PlSqlParser.Index_partitioning_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_partitioning_clause.
    def exitIndex_partitioning_clause(self, ctx:PlSqlParser.Index_partitioning_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#local_partitioned_index.
    def enterLocal_partitioned_index(self, ctx:PlSqlParser.Local_partitioned_indexContext):
        pass

    # Exit a parse tree produced by PlSqlParser#local_partitioned_index.
    def exitLocal_partitioned_index(self, ctx:PlSqlParser.Local_partitioned_indexContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_range_partitioned_table.
    def enterOn_range_partitioned_table(self, ctx:PlSqlParser.On_range_partitioned_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_range_partitioned_table.
    def exitOn_range_partitioned_table(self, ctx:PlSqlParser.On_range_partitioned_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_list_partitioned_table.
    def enterOn_list_partitioned_table(self, ctx:PlSqlParser.On_list_partitioned_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_list_partitioned_table.
    def exitOn_list_partitioned_table(self, ctx:PlSqlParser.On_list_partitioned_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partitioned_table.
    def enterPartitioned_table(self, ctx:PlSqlParser.Partitioned_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partitioned_table.
    def exitPartitioned_table(self, ctx:PlSqlParser.Partitioned_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_hash_partitioned_table.
    def enterOn_hash_partitioned_table(self, ctx:PlSqlParser.On_hash_partitioned_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_hash_partitioned_table.
    def exitOn_hash_partitioned_table(self, ctx:PlSqlParser.On_hash_partitioned_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_hash_partitioned_clause.
    def enterOn_hash_partitioned_clause(self, ctx:PlSqlParser.On_hash_partitioned_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_hash_partitioned_clause.
    def exitOn_hash_partitioned_clause(self, ctx:PlSqlParser.On_hash_partitioned_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_comp_partitioned_table.
    def enterOn_comp_partitioned_table(self, ctx:PlSqlParser.On_comp_partitioned_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_comp_partitioned_table.
    def exitOn_comp_partitioned_table(self, ctx:PlSqlParser.On_comp_partitioned_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_comp_partitioned_clause.
    def enterOn_comp_partitioned_clause(self, ctx:PlSqlParser.On_comp_partitioned_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_comp_partitioned_clause.
    def exitOn_comp_partitioned_clause(self, ctx:PlSqlParser.On_comp_partitioned_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_subpartition_clause.
    def enterIndex_subpartition_clause(self, ctx:PlSqlParser.Index_subpartition_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_subpartition_clause.
    def exitIndex_subpartition_clause(self, ctx:PlSqlParser.Index_subpartition_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_subpartition_subclause.
    def enterIndex_subpartition_subclause(self, ctx:PlSqlParser.Index_subpartition_subclauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_subpartition_subclause.
    def exitIndex_subpartition_subclause(self, ctx:PlSqlParser.Index_subpartition_subclauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#odci_parameters.
    def enterOdci_parameters(self, ctx:PlSqlParser.Odci_parametersContext):
        pass

    # Exit a parse tree produced by PlSqlParser#odci_parameters.
    def exitOdci_parameters(self, ctx:PlSqlParser.Odci_parametersContext):
        pass


    # Enter a parse tree produced by PlSqlParser#indextype.
    def enterIndextype(self, ctx:PlSqlParser.IndextypeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#indextype.
    def exitIndextype(self, ctx:PlSqlParser.IndextypeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_index.
    def enterAlter_index(self, ctx:PlSqlParser.Alter_indexContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_index.
    def exitAlter_index(self, ctx:PlSqlParser.Alter_indexContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_index_ops_set1.
    def enterAlter_index_ops_set1(self, ctx:PlSqlParser.Alter_index_ops_set1Context):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_index_ops_set1.
    def exitAlter_index_ops_set1(self, ctx:PlSqlParser.Alter_index_ops_set1Context):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_index_ops_set2.
    def enterAlter_index_ops_set2(self, ctx:PlSqlParser.Alter_index_ops_set2Context):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_index_ops_set2.
    def exitAlter_index_ops_set2(self, ctx:PlSqlParser.Alter_index_ops_set2Context):
        pass


    # Enter a parse tree produced by PlSqlParser#visible_or_invisible.
    def enterVisible_or_invisible(self, ctx:PlSqlParser.Visible_or_invisibleContext):
        pass

    # Exit a parse tree produced by PlSqlParser#visible_or_invisible.
    def exitVisible_or_invisible(self, ctx:PlSqlParser.Visible_or_invisibleContext):
        pass


    # Enter a parse tree produced by PlSqlParser#monitoring_nomonitoring.
    def enterMonitoring_nomonitoring(self, ctx:PlSqlParser.Monitoring_nomonitoringContext):
        pass

    # Exit a parse tree produced by PlSqlParser#monitoring_nomonitoring.
    def exitMonitoring_nomonitoring(self, ctx:PlSqlParser.Monitoring_nomonitoringContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rebuild_clause.
    def enterRebuild_clause(self, ctx:PlSqlParser.Rebuild_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rebuild_clause.
    def exitRebuild_clause(self, ctx:PlSqlParser.Rebuild_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_index_partitioning.
    def enterAlter_index_partitioning(self, ctx:PlSqlParser.Alter_index_partitioningContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_index_partitioning.
    def exitAlter_index_partitioning(self, ctx:PlSqlParser.Alter_index_partitioningContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_index_default_attrs.
    def enterModify_index_default_attrs(self, ctx:PlSqlParser.Modify_index_default_attrsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_index_default_attrs.
    def exitModify_index_default_attrs(self, ctx:PlSqlParser.Modify_index_default_attrsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_hash_index_partition.
    def enterAdd_hash_index_partition(self, ctx:PlSqlParser.Add_hash_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_hash_index_partition.
    def exitAdd_hash_index_partition(self, ctx:PlSqlParser.Add_hash_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#coalesce_index_partition.
    def enterCoalesce_index_partition(self, ctx:PlSqlParser.Coalesce_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#coalesce_index_partition.
    def exitCoalesce_index_partition(self, ctx:PlSqlParser.Coalesce_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_index_partition.
    def enterModify_index_partition(self, ctx:PlSqlParser.Modify_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_index_partition.
    def exitModify_index_partition(self, ctx:PlSqlParser.Modify_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_index_partitions_ops.
    def enterModify_index_partitions_ops(self, ctx:PlSqlParser.Modify_index_partitions_opsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_index_partitions_ops.
    def exitModify_index_partitions_ops(self, ctx:PlSqlParser.Modify_index_partitions_opsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rename_index_partition.
    def enterRename_index_partition(self, ctx:PlSqlParser.Rename_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rename_index_partition.
    def exitRename_index_partition(self, ctx:PlSqlParser.Rename_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_index_partition.
    def enterDrop_index_partition(self, ctx:PlSqlParser.Drop_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_index_partition.
    def exitDrop_index_partition(self, ctx:PlSqlParser.Drop_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#split_index_partition.
    def enterSplit_index_partition(self, ctx:PlSqlParser.Split_index_partitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#split_index_partition.
    def exitSplit_index_partition(self, ctx:PlSqlParser.Split_index_partitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_partition_description.
    def enterIndex_partition_description(self, ctx:PlSqlParser.Index_partition_descriptionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_partition_description.
    def exitIndex_partition_description(self, ctx:PlSqlParser.Index_partition_descriptionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_index_subpartition.
    def enterModify_index_subpartition(self, ctx:PlSqlParser.Modify_index_subpartitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_index_subpartition.
    def exitModify_index_subpartition(self, ctx:PlSqlParser.Modify_index_subpartitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_name_old.
    def enterPartition_name_old(self, ctx:PlSqlParser.Partition_name_oldContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_name_old.
    def exitPartition_name_old(self, ctx:PlSqlParser.Partition_name_oldContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_partition_name.
    def enterNew_partition_name(self, ctx:PlSqlParser.New_partition_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_partition_name.
    def exitNew_partition_name(self, ctx:PlSqlParser.New_partition_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_index_name.
    def enterNew_index_name(self, ctx:PlSqlParser.New_index_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_index_name.
    def exitNew_index_name(self, ctx:PlSqlParser.New_index_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_user.
    def enterCreate_user(self, ctx:PlSqlParser.Create_userContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_user.
    def exitCreate_user(self, ctx:PlSqlParser.Create_userContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_user.
    def enterAlter_user(self, ctx:PlSqlParser.Alter_userContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_user.
    def exitAlter_user(self, ctx:PlSqlParser.Alter_userContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_identified_by.
    def enterAlter_identified_by(self, ctx:PlSqlParser.Alter_identified_byContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_identified_by.
    def exitAlter_identified_by(self, ctx:PlSqlParser.Alter_identified_byContext):
        pass


    # Enter a parse tree produced by PlSqlParser#identified_by.
    def enterIdentified_by(self, ctx:PlSqlParser.Identified_byContext):
        pass

    # Exit a parse tree produced by PlSqlParser#identified_by.
    def exitIdentified_by(self, ctx:PlSqlParser.Identified_byContext):
        pass


    # Enter a parse tree produced by PlSqlParser#identified_other_clause.
    def enterIdentified_other_clause(self, ctx:PlSqlParser.Identified_other_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#identified_other_clause.
    def exitIdentified_other_clause(self, ctx:PlSqlParser.Identified_other_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#user_tablespace_clause.
    def enterUser_tablespace_clause(self, ctx:PlSqlParser.User_tablespace_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#user_tablespace_clause.
    def exitUser_tablespace_clause(self, ctx:PlSqlParser.User_tablespace_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#quota_clause.
    def enterQuota_clause(self, ctx:PlSqlParser.Quota_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#quota_clause.
    def exitQuota_clause(self, ctx:PlSqlParser.Quota_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#profile_clause.
    def enterProfile_clause(self, ctx:PlSqlParser.Profile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#profile_clause.
    def exitProfile_clause(self, ctx:PlSqlParser.Profile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#role_clause.
    def enterRole_clause(self, ctx:PlSqlParser.Role_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#role_clause.
    def exitRole_clause(self, ctx:PlSqlParser.Role_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#user_default_role_clause.
    def enterUser_default_role_clause(self, ctx:PlSqlParser.User_default_role_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#user_default_role_clause.
    def exitUser_default_role_clause(self, ctx:PlSqlParser.User_default_role_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#password_expire_clause.
    def enterPassword_expire_clause(self, ctx:PlSqlParser.Password_expire_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#password_expire_clause.
    def exitPassword_expire_clause(self, ctx:PlSqlParser.Password_expire_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#user_lock_clause.
    def enterUser_lock_clause(self, ctx:PlSqlParser.User_lock_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#user_lock_clause.
    def exitUser_lock_clause(self, ctx:PlSqlParser.User_lock_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#user_editions_clause.
    def enterUser_editions_clause(self, ctx:PlSqlParser.User_editions_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#user_editions_clause.
    def exitUser_editions_clause(self, ctx:PlSqlParser.User_editions_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_user_editions_clause.
    def enterAlter_user_editions_clause(self, ctx:PlSqlParser.Alter_user_editions_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_user_editions_clause.
    def exitAlter_user_editions_clause(self, ctx:PlSqlParser.Alter_user_editions_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#proxy_clause.
    def enterProxy_clause(self, ctx:PlSqlParser.Proxy_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#proxy_clause.
    def exitProxy_clause(self, ctx:PlSqlParser.Proxy_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#container_names.
    def enterContainer_names(self, ctx:PlSqlParser.Container_namesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#container_names.
    def exitContainer_names(self, ctx:PlSqlParser.Container_namesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#set_container_data.
    def enterSet_container_data(self, ctx:PlSqlParser.Set_container_dataContext):
        pass

    # Exit a parse tree produced by PlSqlParser#set_container_data.
    def exitSet_container_data(self, ctx:PlSqlParser.Set_container_dataContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_rem_container_data.
    def enterAdd_rem_container_data(self, ctx:PlSqlParser.Add_rem_container_dataContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_rem_container_data.
    def exitAdd_rem_container_data(self, ctx:PlSqlParser.Add_rem_container_dataContext):
        pass


    # Enter a parse tree produced by PlSqlParser#container_data_clause.
    def enterContainer_data_clause(self, ctx:PlSqlParser.Container_data_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#container_data_clause.
    def exitContainer_data_clause(self, ctx:PlSqlParser.Container_data_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#analyze.
    def enterAnalyze(self, ctx:PlSqlParser.AnalyzeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#analyze.
    def exitAnalyze(self, ctx:PlSqlParser.AnalyzeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_extention_clause.
    def enterPartition_extention_clause(self, ctx:PlSqlParser.Partition_extention_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_extention_clause.
    def exitPartition_extention_clause(self, ctx:PlSqlParser.Partition_extention_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#validation_clauses.
    def enterValidation_clauses(self, ctx:PlSqlParser.Validation_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#validation_clauses.
    def exitValidation_clauses(self, ctx:PlSqlParser.Validation_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#online_or_offline.
    def enterOnline_or_offline(self, ctx:PlSqlParser.Online_or_offlineContext):
        pass

    # Exit a parse tree produced by PlSqlParser#online_or_offline.
    def exitOnline_or_offline(self, ctx:PlSqlParser.Online_or_offlineContext):
        pass


    # Enter a parse tree produced by PlSqlParser#into_clause1.
    def enterInto_clause1(self, ctx:PlSqlParser.Into_clause1Context):
        pass

    # Exit a parse tree produced by PlSqlParser#into_clause1.
    def exitInto_clause1(self, ctx:PlSqlParser.Into_clause1Context):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_key_value.
    def enterPartition_key_value(self, ctx:PlSqlParser.Partition_key_valueContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_key_value.
    def exitPartition_key_value(self, ctx:PlSqlParser.Partition_key_valueContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_key_value.
    def enterSubpartition_key_value(self, ctx:PlSqlParser.Subpartition_key_valueContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_key_value.
    def exitSubpartition_key_value(self, ctx:PlSqlParser.Subpartition_key_valueContext):
        pass


    # Enter a parse tree produced by PlSqlParser#associate_statistics.
    def enterAssociate_statistics(self, ctx:PlSqlParser.Associate_statisticsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#associate_statistics.
    def exitAssociate_statistics(self, ctx:PlSqlParser.Associate_statisticsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_association.
    def enterColumn_association(self, ctx:PlSqlParser.Column_associationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_association.
    def exitColumn_association(self, ctx:PlSqlParser.Column_associationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_association.
    def enterFunction_association(self, ctx:PlSqlParser.Function_associationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_association.
    def exitFunction_association(self, ctx:PlSqlParser.Function_associationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#indextype_name.
    def enterIndextype_name(self, ctx:PlSqlParser.Indextype_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#indextype_name.
    def exitIndextype_name(self, ctx:PlSqlParser.Indextype_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#using_statistics_type.
    def enterUsing_statistics_type(self, ctx:PlSqlParser.Using_statistics_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#using_statistics_type.
    def exitUsing_statistics_type(self, ctx:PlSqlParser.Using_statistics_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#statistics_type_name.
    def enterStatistics_type_name(self, ctx:PlSqlParser.Statistics_type_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#statistics_type_name.
    def exitStatistics_type_name(self, ctx:PlSqlParser.Statistics_type_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#default_cost_clause.
    def enterDefault_cost_clause(self, ctx:PlSqlParser.Default_cost_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#default_cost_clause.
    def exitDefault_cost_clause(self, ctx:PlSqlParser.Default_cost_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cpu_cost.
    def enterCpu_cost(self, ctx:PlSqlParser.Cpu_costContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cpu_cost.
    def exitCpu_cost(self, ctx:PlSqlParser.Cpu_costContext):
        pass


    # Enter a parse tree produced by PlSqlParser#io_cost.
    def enterIo_cost(self, ctx:PlSqlParser.Io_costContext):
        pass

    # Exit a parse tree produced by PlSqlParser#io_cost.
    def exitIo_cost(self, ctx:PlSqlParser.Io_costContext):
        pass


    # Enter a parse tree produced by PlSqlParser#network_cost.
    def enterNetwork_cost(self, ctx:PlSqlParser.Network_costContext):
        pass

    # Exit a parse tree produced by PlSqlParser#network_cost.
    def exitNetwork_cost(self, ctx:PlSqlParser.Network_costContext):
        pass


    # Enter a parse tree produced by PlSqlParser#default_selectivity_clause.
    def enterDefault_selectivity_clause(self, ctx:PlSqlParser.Default_selectivity_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#default_selectivity_clause.
    def exitDefault_selectivity_clause(self, ctx:PlSqlParser.Default_selectivity_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#default_selectivity.
    def enterDefault_selectivity(self, ctx:PlSqlParser.Default_selectivityContext):
        pass

    # Exit a parse tree produced by PlSqlParser#default_selectivity.
    def exitDefault_selectivity(self, ctx:PlSqlParser.Default_selectivityContext):
        pass


    # Enter a parse tree produced by PlSqlParser#storage_table_clause.
    def enterStorage_table_clause(self, ctx:PlSqlParser.Storage_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#storage_table_clause.
    def exitStorage_table_clause(self, ctx:PlSqlParser.Storage_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unified_auditing.
    def enterUnified_auditing(self, ctx:PlSqlParser.Unified_auditingContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unified_auditing.
    def exitUnified_auditing(self, ctx:PlSqlParser.Unified_auditingContext):
        pass


    # Enter a parse tree produced by PlSqlParser#policy_name.
    def enterPolicy_name(self, ctx:PlSqlParser.Policy_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#policy_name.
    def exitPolicy_name(self, ctx:PlSqlParser.Policy_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_traditional.
    def enterAudit_traditional(self, ctx:PlSqlParser.Audit_traditionalContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_traditional.
    def exitAudit_traditional(self, ctx:PlSqlParser.Audit_traditionalContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_direct_path.
    def enterAudit_direct_path(self, ctx:PlSqlParser.Audit_direct_pathContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_direct_path.
    def exitAudit_direct_path(self, ctx:PlSqlParser.Audit_direct_pathContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_container_clause.
    def enterAudit_container_clause(self, ctx:PlSqlParser.Audit_container_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_container_clause.
    def exitAudit_container_clause(self, ctx:PlSqlParser.Audit_container_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_operation_clause.
    def enterAudit_operation_clause(self, ctx:PlSqlParser.Audit_operation_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_operation_clause.
    def exitAudit_operation_clause(self, ctx:PlSqlParser.Audit_operation_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#auditing_by_clause.
    def enterAuditing_by_clause(self, ctx:PlSqlParser.Auditing_by_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#auditing_by_clause.
    def exitAuditing_by_clause(self, ctx:PlSqlParser.Auditing_by_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_user.
    def enterAudit_user(self, ctx:PlSqlParser.Audit_userContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_user.
    def exitAudit_user(self, ctx:PlSqlParser.Audit_userContext):
        pass


    # Enter a parse tree produced by PlSqlParser#audit_schema_object_clause.
    def enterAudit_schema_object_clause(self, ctx:PlSqlParser.Audit_schema_object_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#audit_schema_object_clause.
    def exitAudit_schema_object_clause(self, ctx:PlSqlParser.Audit_schema_object_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sql_operation.
    def enterSql_operation(self, ctx:PlSqlParser.Sql_operationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sql_operation.
    def exitSql_operation(self, ctx:PlSqlParser.Sql_operationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#auditing_on_clause.
    def enterAuditing_on_clause(self, ctx:PlSqlParser.Auditing_on_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#auditing_on_clause.
    def exitAuditing_on_clause(self, ctx:PlSqlParser.Auditing_on_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_name.
    def enterModel_name(self, ctx:PlSqlParser.Model_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_name.
    def exitModel_name(self, ctx:PlSqlParser.Model_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_name.
    def enterObject_name(self, ctx:PlSqlParser.Object_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_name.
    def exitObject_name(self, ctx:PlSqlParser.Object_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#profile_name.
    def enterProfile_name(self, ctx:PlSqlParser.Profile_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#profile_name.
    def exitProfile_name(self, ctx:PlSqlParser.Profile_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sql_statement_shortcut.
    def enterSql_statement_shortcut(self, ctx:PlSqlParser.Sql_statement_shortcutContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sql_statement_shortcut.
    def exitSql_statement_shortcut(self, ctx:PlSqlParser.Sql_statement_shortcutContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_index.
    def enterDrop_index(self, ctx:PlSqlParser.Drop_indexContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_index.
    def exitDrop_index(self, ctx:PlSqlParser.Drop_indexContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rename_object.
    def enterRename_object(self, ctx:PlSqlParser.Rename_objectContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rename_object.
    def exitRename_object(self, ctx:PlSqlParser.Rename_objectContext):
        pass


    # Enter a parse tree produced by PlSqlParser#grant_statement.
    def enterGrant_statement(self, ctx:PlSqlParser.Grant_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#grant_statement.
    def exitGrant_statement(self, ctx:PlSqlParser.Grant_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#container_clause.
    def enterContainer_clause(self, ctx:PlSqlParser.Container_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#container_clause.
    def exitContainer_clause(self, ctx:PlSqlParser.Container_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_directory.
    def enterCreate_directory(self, ctx:PlSqlParser.Create_directoryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_directory.
    def exitCreate_directory(self, ctx:PlSqlParser.Create_directoryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#directory_name.
    def enterDirectory_name(self, ctx:PlSqlParser.Directory_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#directory_name.
    def exitDirectory_name(self, ctx:PlSqlParser.Directory_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#directory_path.
    def enterDirectory_path(self, ctx:PlSqlParser.Directory_pathContext):
        pass

    # Exit a parse tree produced by PlSqlParser#directory_path.
    def exitDirectory_path(self, ctx:PlSqlParser.Directory_pathContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_library.
    def enterAlter_library(self, ctx:PlSqlParser.Alter_libraryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_library.
    def exitAlter_library(self, ctx:PlSqlParser.Alter_libraryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#library_editionable.
    def enterLibrary_editionable(self, ctx:PlSqlParser.Library_editionableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#library_editionable.
    def exitLibrary_editionable(self, ctx:PlSqlParser.Library_editionableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#library_debug.
    def enterLibrary_debug(self, ctx:PlSqlParser.Library_debugContext):
        pass

    # Exit a parse tree produced by PlSqlParser#library_debug.
    def exitLibrary_debug(self, ctx:PlSqlParser.Library_debugContext):
        pass


    # Enter a parse tree produced by PlSqlParser#compiler_parameters_clause.
    def enterCompiler_parameters_clause(self, ctx:PlSqlParser.Compiler_parameters_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#compiler_parameters_clause.
    def exitCompiler_parameters_clause(self, ctx:PlSqlParser.Compiler_parameters_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parameter_value.
    def enterParameter_value(self, ctx:PlSqlParser.Parameter_valueContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parameter_value.
    def exitParameter_value(self, ctx:PlSqlParser.Parameter_valueContext):
        pass


    # Enter a parse tree produced by PlSqlParser#library_name.
    def enterLibrary_name(self, ctx:PlSqlParser.Library_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#library_name.
    def exitLibrary_name(self, ctx:PlSqlParser.Library_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_view.
    def enterAlter_view(self, ctx:PlSqlParser.Alter_viewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_view.
    def exitAlter_view(self, ctx:PlSqlParser.Alter_viewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_view_editionable.
    def enterAlter_view_editionable(self, ctx:PlSqlParser.Alter_view_editionableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_view_editionable.
    def exitAlter_view_editionable(self, ctx:PlSqlParser.Alter_view_editionableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_view.
    def enterCreate_view(self, ctx:PlSqlParser.Create_viewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_view.
    def exitCreate_view(self, ctx:PlSqlParser.Create_viewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#view_options.
    def enterView_options(self, ctx:PlSqlParser.View_optionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#view_options.
    def exitView_options(self, ctx:PlSqlParser.View_optionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#view_alias_constraint.
    def enterView_alias_constraint(self, ctx:PlSqlParser.View_alias_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#view_alias_constraint.
    def exitView_alias_constraint(self, ctx:PlSqlParser.View_alias_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_view_clause.
    def enterObject_view_clause(self, ctx:PlSqlParser.Object_view_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_view_clause.
    def exitObject_view_clause(self, ctx:PlSqlParser.Object_view_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#inline_constraint.
    def enterInline_constraint(self, ctx:PlSqlParser.Inline_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#inline_constraint.
    def exitInline_constraint(self, ctx:PlSqlParser.Inline_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#inline_ref_constraint.
    def enterInline_ref_constraint(self, ctx:PlSqlParser.Inline_ref_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#inline_ref_constraint.
    def exitInline_ref_constraint(self, ctx:PlSqlParser.Inline_ref_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#out_of_line_ref_constraint.
    def enterOut_of_line_ref_constraint(self, ctx:PlSqlParser.Out_of_line_ref_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#out_of_line_ref_constraint.
    def exitOut_of_line_ref_constraint(self, ctx:PlSqlParser.Out_of_line_ref_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#out_of_line_constraint.
    def enterOut_of_line_constraint(self, ctx:PlSqlParser.Out_of_line_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#out_of_line_constraint.
    def exitOut_of_line_constraint(self, ctx:PlSqlParser.Out_of_line_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constraint_state.
    def enterConstraint_state(self, ctx:PlSqlParser.Constraint_stateContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constraint_state.
    def exitConstraint_state(self, ctx:PlSqlParser.Constraint_stateContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_tablespace.
    def enterAlter_tablespace(self, ctx:PlSqlParser.Alter_tablespaceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_tablespace.
    def exitAlter_tablespace(self, ctx:PlSqlParser.Alter_tablespaceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datafile_tempfile_clauses.
    def enterDatafile_tempfile_clauses(self, ctx:PlSqlParser.Datafile_tempfile_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datafile_tempfile_clauses.
    def exitDatafile_tempfile_clauses(self, ctx:PlSqlParser.Datafile_tempfile_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_logging_clauses.
    def enterTablespace_logging_clauses(self, ctx:PlSqlParser.Tablespace_logging_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_logging_clauses.
    def exitTablespace_logging_clauses(self, ctx:PlSqlParser.Tablespace_logging_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_group_clause.
    def enterTablespace_group_clause(self, ctx:PlSqlParser.Tablespace_group_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_group_clause.
    def exitTablespace_group_clause(self, ctx:PlSqlParser.Tablespace_group_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_group_name.
    def enterTablespace_group_name(self, ctx:PlSqlParser.Tablespace_group_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_group_name.
    def exitTablespace_group_name(self, ctx:PlSqlParser.Tablespace_group_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_state_clauses.
    def enterTablespace_state_clauses(self, ctx:PlSqlParser.Tablespace_state_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_state_clauses.
    def exitTablespace_state_clauses(self, ctx:PlSqlParser.Tablespace_state_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#flashback_mode_clause.
    def enterFlashback_mode_clause(self, ctx:PlSqlParser.Flashback_mode_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#flashback_mode_clause.
    def exitFlashback_mode_clause(self, ctx:PlSqlParser.Flashback_mode_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_tablespace_name.
    def enterNew_tablespace_name(self, ctx:PlSqlParser.New_tablespace_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_tablespace_name.
    def exitNew_tablespace_name(self, ctx:PlSqlParser.New_tablespace_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_tablespace.
    def enterCreate_tablespace(self, ctx:PlSqlParser.Create_tablespaceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_tablespace.
    def exitCreate_tablespace(self, ctx:PlSqlParser.Create_tablespaceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#permanent_tablespace_clause.
    def enterPermanent_tablespace_clause(self, ctx:PlSqlParser.Permanent_tablespace_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#permanent_tablespace_clause.
    def exitPermanent_tablespace_clause(self, ctx:PlSqlParser.Permanent_tablespace_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_encryption_spec.
    def enterTablespace_encryption_spec(self, ctx:PlSqlParser.Tablespace_encryption_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_encryption_spec.
    def exitTablespace_encryption_spec(self, ctx:PlSqlParser.Tablespace_encryption_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#logging_clause.
    def enterLogging_clause(self, ctx:PlSqlParser.Logging_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#logging_clause.
    def exitLogging_clause(self, ctx:PlSqlParser.Logging_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#extent_management_clause.
    def enterExtent_management_clause(self, ctx:PlSqlParser.Extent_management_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#extent_management_clause.
    def exitExtent_management_clause(self, ctx:PlSqlParser.Extent_management_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#segment_management_clause.
    def enterSegment_management_clause(self, ctx:PlSqlParser.Segment_management_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#segment_management_clause.
    def exitSegment_management_clause(self, ctx:PlSqlParser.Segment_management_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#temporary_tablespace_clause.
    def enterTemporary_tablespace_clause(self, ctx:PlSqlParser.Temporary_tablespace_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#temporary_tablespace_clause.
    def exitTemporary_tablespace_clause(self, ctx:PlSqlParser.Temporary_tablespace_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#undo_tablespace_clause.
    def enterUndo_tablespace_clause(self, ctx:PlSqlParser.Undo_tablespace_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#undo_tablespace_clause.
    def exitUndo_tablespace_clause(self, ctx:PlSqlParser.Undo_tablespace_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace_retention_clause.
    def enterTablespace_retention_clause(self, ctx:PlSqlParser.Tablespace_retention_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace_retention_clause.
    def exitTablespace_retention_clause(self, ctx:PlSqlParser.Tablespace_retention_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datafile_specification.
    def enterDatafile_specification(self, ctx:PlSqlParser.Datafile_specificationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datafile_specification.
    def exitDatafile_specification(self, ctx:PlSqlParser.Datafile_specificationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tempfile_specification.
    def enterTempfile_specification(self, ctx:PlSqlParser.Tempfile_specificationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tempfile_specification.
    def exitTempfile_specification(self, ctx:PlSqlParser.Tempfile_specificationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datafile_tempfile_spec.
    def enterDatafile_tempfile_spec(self, ctx:PlSqlParser.Datafile_tempfile_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datafile_tempfile_spec.
    def exitDatafile_tempfile_spec(self, ctx:PlSqlParser.Datafile_tempfile_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#redo_log_file_spec.
    def enterRedo_log_file_spec(self, ctx:PlSqlParser.Redo_log_file_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#redo_log_file_spec.
    def exitRedo_log_file_spec(self, ctx:PlSqlParser.Redo_log_file_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#autoextend_clause.
    def enterAutoextend_clause(self, ctx:PlSqlParser.Autoextend_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#autoextend_clause.
    def exitAutoextend_clause(self, ctx:PlSqlParser.Autoextend_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#maxsize_clause.
    def enterMaxsize_clause(self, ctx:PlSqlParser.Maxsize_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#maxsize_clause.
    def exitMaxsize_clause(self, ctx:PlSqlParser.Maxsize_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#build_clause.
    def enterBuild_clause(self, ctx:PlSqlParser.Build_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#build_clause.
    def exitBuild_clause(self, ctx:PlSqlParser.Build_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parallel_clause.
    def enterParallel_clause(self, ctx:PlSqlParser.Parallel_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parallel_clause.
    def exitParallel_clause(self, ctx:PlSqlParser.Parallel_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_materialized_view.
    def enterAlter_materialized_view(self, ctx:PlSqlParser.Alter_materialized_viewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_materialized_view.
    def exitAlter_materialized_view(self, ctx:PlSqlParser.Alter_materialized_viewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_mv_option1.
    def enterAlter_mv_option1(self, ctx:PlSqlParser.Alter_mv_option1Context):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_mv_option1.
    def exitAlter_mv_option1(self, ctx:PlSqlParser.Alter_mv_option1Context):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_mv_refresh.
    def enterAlter_mv_refresh(self, ctx:PlSqlParser.Alter_mv_refreshContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_mv_refresh.
    def exitAlter_mv_refresh(self, ctx:PlSqlParser.Alter_mv_refreshContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rollback_segment.
    def enterRollback_segment(self, ctx:PlSqlParser.Rollback_segmentContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rollback_segment.
    def exitRollback_segment(self, ctx:PlSqlParser.Rollback_segmentContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_mv_column_clause.
    def enterModify_mv_column_clause(self, ctx:PlSqlParser.Modify_mv_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_mv_column_clause.
    def exitModify_mv_column_clause(self, ctx:PlSqlParser.Modify_mv_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_materialized_view_log.
    def enterAlter_materialized_view_log(self, ctx:PlSqlParser.Alter_materialized_view_logContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_materialized_view_log.
    def exitAlter_materialized_view_log(self, ctx:PlSqlParser.Alter_materialized_view_logContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_mv_log_column_clause.
    def enterAdd_mv_log_column_clause(self, ctx:PlSqlParser.Add_mv_log_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_mv_log_column_clause.
    def exitAdd_mv_log_column_clause(self, ctx:PlSqlParser.Add_mv_log_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#move_mv_log_clause.
    def enterMove_mv_log_clause(self, ctx:PlSqlParser.Move_mv_log_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#move_mv_log_clause.
    def exitMove_mv_log_clause(self, ctx:PlSqlParser.Move_mv_log_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#mv_log_augmentation.
    def enterMv_log_augmentation(self, ctx:PlSqlParser.Mv_log_augmentationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#mv_log_augmentation.
    def exitMv_log_augmentation(self, ctx:PlSqlParser.Mv_log_augmentationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datetime_expr.
    def enterDatetime_expr(self, ctx:PlSqlParser.Datetime_exprContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datetime_expr.
    def exitDatetime_expr(self, ctx:PlSqlParser.Datetime_exprContext):
        pass


    # Enter a parse tree produced by PlSqlParser#interval_expr.
    def enterInterval_expr(self, ctx:PlSqlParser.Interval_exprContext):
        pass

    # Exit a parse tree produced by PlSqlParser#interval_expr.
    def exitInterval_expr(self, ctx:PlSqlParser.Interval_exprContext):
        pass


    # Enter a parse tree produced by PlSqlParser#synchronous_or_asynchronous.
    def enterSynchronous_or_asynchronous(self, ctx:PlSqlParser.Synchronous_or_asynchronousContext):
        pass

    # Exit a parse tree produced by PlSqlParser#synchronous_or_asynchronous.
    def exitSynchronous_or_asynchronous(self, ctx:PlSqlParser.Synchronous_or_asynchronousContext):
        pass


    # Enter a parse tree produced by PlSqlParser#including_or_excluding.
    def enterIncluding_or_excluding(self, ctx:PlSqlParser.Including_or_excludingContext):
        pass

    # Exit a parse tree produced by PlSqlParser#including_or_excluding.
    def exitIncluding_or_excluding(self, ctx:PlSqlParser.Including_or_excludingContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_materialized_view_log.
    def enterCreate_materialized_view_log(self, ctx:PlSqlParser.Create_materialized_view_logContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_materialized_view_log.
    def exitCreate_materialized_view_log(self, ctx:PlSqlParser.Create_materialized_view_logContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_values_clause.
    def enterNew_values_clause(self, ctx:PlSqlParser.New_values_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_values_clause.
    def exitNew_values_clause(self, ctx:PlSqlParser.New_values_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#mv_log_purge_clause.
    def enterMv_log_purge_clause(self, ctx:PlSqlParser.Mv_log_purge_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#mv_log_purge_clause.
    def exitMv_log_purge_clause(self, ctx:PlSqlParser.Mv_log_purge_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_materialized_view.
    def enterCreate_materialized_view(self, ctx:PlSqlParser.Create_materialized_viewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_materialized_view.
    def exitCreate_materialized_view(self, ctx:PlSqlParser.Create_materialized_viewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_mv_refresh.
    def enterCreate_mv_refresh(self, ctx:PlSqlParser.Create_mv_refreshContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_mv_refresh.
    def exitCreate_mv_refresh(self, ctx:PlSqlParser.Create_mv_refreshContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_context.
    def enterCreate_context(self, ctx:PlSqlParser.Create_contextContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_context.
    def exitCreate_context(self, ctx:PlSqlParser.Create_contextContext):
        pass


    # Enter a parse tree produced by PlSqlParser#oracle_namespace.
    def enterOracle_namespace(self, ctx:PlSqlParser.Oracle_namespaceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#oracle_namespace.
    def exitOracle_namespace(self, ctx:PlSqlParser.Oracle_namespaceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_cluster.
    def enterCreate_cluster(self, ctx:PlSqlParser.Create_clusterContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_cluster.
    def exitCreate_cluster(self, ctx:PlSqlParser.Create_clusterContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_table.
    def enterCreate_table(self, ctx:PlSqlParser.Create_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_table.
    def exitCreate_table(self, ctx:PlSqlParser.Create_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmltype_table.
    def enterXmltype_table(self, ctx:PlSqlParser.Xmltype_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmltype_table.
    def exitXmltype_table(self, ctx:PlSqlParser.Xmltype_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmltype_virtual_columns.
    def enterXmltype_virtual_columns(self, ctx:PlSqlParser.Xmltype_virtual_columnsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmltype_virtual_columns.
    def exitXmltype_virtual_columns(self, ctx:PlSqlParser.Xmltype_virtual_columnsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmltype_column_properties.
    def enterXmltype_column_properties(self, ctx:PlSqlParser.Xmltype_column_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmltype_column_properties.
    def exitXmltype_column_properties(self, ctx:PlSqlParser.Xmltype_column_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmltype_storage.
    def enterXmltype_storage(self, ctx:PlSqlParser.Xmltype_storageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmltype_storage.
    def exitXmltype_storage(self, ctx:PlSqlParser.Xmltype_storageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlschema_spec.
    def enterXmlschema_spec(self, ctx:PlSqlParser.Xmlschema_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlschema_spec.
    def exitXmlschema_spec(self, ctx:PlSqlParser.Xmlschema_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_table.
    def enterObject_table(self, ctx:PlSqlParser.Object_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_table.
    def exitObject_table(self, ctx:PlSqlParser.Object_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#oid_index_clause.
    def enterOid_index_clause(self, ctx:PlSqlParser.Oid_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#oid_index_clause.
    def exitOid_index_clause(self, ctx:PlSqlParser.Oid_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#oid_clause.
    def enterOid_clause(self, ctx:PlSqlParser.Oid_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#oid_clause.
    def exitOid_clause(self, ctx:PlSqlParser.Oid_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_properties.
    def enterObject_properties(self, ctx:PlSqlParser.Object_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_properties.
    def exitObject_properties(self, ctx:PlSqlParser.Object_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_table_substitution.
    def enterObject_table_substitution(self, ctx:PlSqlParser.Object_table_substitutionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_table_substitution.
    def exitObject_table_substitution(self, ctx:PlSqlParser.Object_table_substitutionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#relational_table.
    def enterRelational_table(self, ctx:PlSqlParser.Relational_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#relational_table.
    def exitRelational_table(self, ctx:PlSqlParser.Relational_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#relational_property.
    def enterRelational_property(self, ctx:PlSqlParser.Relational_propertyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#relational_property.
    def exitRelational_property(self, ctx:PlSqlParser.Relational_propertyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_partitioning_clauses.
    def enterTable_partitioning_clauses(self, ctx:PlSqlParser.Table_partitioning_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_partitioning_clauses.
    def exitTable_partitioning_clauses(self, ctx:PlSqlParser.Table_partitioning_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#range_partitions.
    def enterRange_partitions(self, ctx:PlSqlParser.Range_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#range_partitions.
    def exitRange_partitions(self, ctx:PlSqlParser.Range_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#list_partitions.
    def enterList_partitions(self, ctx:PlSqlParser.List_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#list_partitions.
    def exitList_partitions(self, ctx:PlSqlParser.List_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hash_partitions.
    def enterHash_partitions(self, ctx:PlSqlParser.Hash_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hash_partitions.
    def exitHash_partitions(self, ctx:PlSqlParser.Hash_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#individual_hash_partitions.
    def enterIndividual_hash_partitions(self, ctx:PlSqlParser.Individual_hash_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#individual_hash_partitions.
    def exitIndividual_hash_partitions(self, ctx:PlSqlParser.Individual_hash_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hash_partitions_by_quantity.
    def enterHash_partitions_by_quantity(self, ctx:PlSqlParser.Hash_partitions_by_quantityContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hash_partitions_by_quantity.
    def exitHash_partitions_by_quantity(self, ctx:PlSqlParser.Hash_partitions_by_quantityContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hash_partition_quantity.
    def enterHash_partition_quantity(self, ctx:PlSqlParser.Hash_partition_quantityContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hash_partition_quantity.
    def exitHash_partition_quantity(self, ctx:PlSqlParser.Hash_partition_quantityContext):
        pass


    # Enter a parse tree produced by PlSqlParser#composite_range_partitions.
    def enterComposite_range_partitions(self, ctx:PlSqlParser.Composite_range_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#composite_range_partitions.
    def exitComposite_range_partitions(self, ctx:PlSqlParser.Composite_range_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#composite_list_partitions.
    def enterComposite_list_partitions(self, ctx:PlSqlParser.Composite_list_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#composite_list_partitions.
    def exitComposite_list_partitions(self, ctx:PlSqlParser.Composite_list_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#composite_hash_partitions.
    def enterComposite_hash_partitions(self, ctx:PlSqlParser.Composite_hash_partitionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#composite_hash_partitions.
    def exitComposite_hash_partitions(self, ctx:PlSqlParser.Composite_hash_partitionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#reference_partitioning.
    def enterReference_partitioning(self, ctx:PlSqlParser.Reference_partitioningContext):
        pass

    # Exit a parse tree produced by PlSqlParser#reference_partitioning.
    def exitReference_partitioning(self, ctx:PlSqlParser.Reference_partitioningContext):
        pass


    # Enter a parse tree produced by PlSqlParser#reference_partition_desc.
    def enterReference_partition_desc(self, ctx:PlSqlParser.Reference_partition_descContext):
        pass

    # Exit a parse tree produced by PlSqlParser#reference_partition_desc.
    def exitReference_partition_desc(self, ctx:PlSqlParser.Reference_partition_descContext):
        pass


    # Enter a parse tree produced by PlSqlParser#system_partitioning.
    def enterSystem_partitioning(self, ctx:PlSqlParser.System_partitioningContext):
        pass

    # Exit a parse tree produced by PlSqlParser#system_partitioning.
    def exitSystem_partitioning(self, ctx:PlSqlParser.System_partitioningContext):
        pass


    # Enter a parse tree produced by PlSqlParser#range_partition_desc.
    def enterRange_partition_desc(self, ctx:PlSqlParser.Range_partition_descContext):
        pass

    # Exit a parse tree produced by PlSqlParser#range_partition_desc.
    def exitRange_partition_desc(self, ctx:PlSqlParser.Range_partition_descContext):
        pass


    # Enter a parse tree produced by PlSqlParser#list_partition_desc.
    def enterList_partition_desc(self, ctx:PlSqlParser.List_partition_descContext):
        pass

    # Exit a parse tree produced by PlSqlParser#list_partition_desc.
    def exitList_partition_desc(self, ctx:PlSqlParser.List_partition_descContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_template.
    def enterSubpartition_template(self, ctx:PlSqlParser.Subpartition_templateContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_template.
    def exitSubpartition_template(self, ctx:PlSqlParser.Subpartition_templateContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hash_subpartition_quantity.
    def enterHash_subpartition_quantity(self, ctx:PlSqlParser.Hash_subpartition_quantityContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hash_subpartition_quantity.
    def exitHash_subpartition_quantity(self, ctx:PlSqlParser.Hash_subpartition_quantityContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_by_range.
    def enterSubpartition_by_range(self, ctx:PlSqlParser.Subpartition_by_rangeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_by_range.
    def exitSubpartition_by_range(self, ctx:PlSqlParser.Subpartition_by_rangeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_by_list.
    def enterSubpartition_by_list(self, ctx:PlSqlParser.Subpartition_by_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_by_list.
    def exitSubpartition_by_list(self, ctx:PlSqlParser.Subpartition_by_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_by_hash.
    def enterSubpartition_by_hash(self, ctx:PlSqlParser.Subpartition_by_hashContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_by_hash.
    def exitSubpartition_by_hash(self, ctx:PlSqlParser.Subpartition_by_hashContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subpartition_name.
    def enterSubpartition_name(self, ctx:PlSqlParser.Subpartition_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subpartition_name.
    def exitSubpartition_name(self, ctx:PlSqlParser.Subpartition_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#range_subpartition_desc.
    def enterRange_subpartition_desc(self, ctx:PlSqlParser.Range_subpartition_descContext):
        pass

    # Exit a parse tree produced by PlSqlParser#range_subpartition_desc.
    def exitRange_subpartition_desc(self, ctx:PlSqlParser.Range_subpartition_descContext):
        pass


    # Enter a parse tree produced by PlSqlParser#list_subpartition_desc.
    def enterList_subpartition_desc(self, ctx:PlSqlParser.List_subpartition_descContext):
        pass

    # Exit a parse tree produced by PlSqlParser#list_subpartition_desc.
    def exitList_subpartition_desc(self, ctx:PlSqlParser.List_subpartition_descContext):
        pass


    # Enter a parse tree produced by PlSqlParser#individual_hash_subparts.
    def enterIndividual_hash_subparts(self, ctx:PlSqlParser.Individual_hash_subpartsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#individual_hash_subparts.
    def exitIndividual_hash_subparts(self, ctx:PlSqlParser.Individual_hash_subpartsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hash_subparts_by_quantity.
    def enterHash_subparts_by_quantity(self, ctx:PlSqlParser.Hash_subparts_by_quantityContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hash_subparts_by_quantity.
    def exitHash_subparts_by_quantity(self, ctx:PlSqlParser.Hash_subparts_by_quantityContext):
        pass


    # Enter a parse tree produced by PlSqlParser#range_values_clause.
    def enterRange_values_clause(self, ctx:PlSqlParser.Range_values_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#range_values_clause.
    def exitRange_values_clause(self, ctx:PlSqlParser.Range_values_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#list_values_clause.
    def enterList_values_clause(self, ctx:PlSqlParser.List_values_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#list_values_clause.
    def exitList_values_clause(self, ctx:PlSqlParser.List_values_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_partition_description.
    def enterTable_partition_description(self, ctx:PlSqlParser.Table_partition_descriptionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_partition_description.
    def exitTable_partition_description(self, ctx:PlSqlParser.Table_partition_descriptionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partitioning_storage_clause.
    def enterPartitioning_storage_clause(self, ctx:PlSqlParser.Partitioning_storage_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partitioning_storage_clause.
    def exitPartitioning_storage_clause(self, ctx:PlSqlParser.Partitioning_storage_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_partitioning_storage.
    def enterLob_partitioning_storage(self, ctx:PlSqlParser.Lob_partitioning_storageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_partitioning_storage.
    def exitLob_partitioning_storage(self, ctx:PlSqlParser.Lob_partitioning_storageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datatype_null_enable.
    def enterDatatype_null_enable(self, ctx:PlSqlParser.Datatype_null_enableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datatype_null_enable.
    def exitDatatype_null_enable(self, ctx:PlSqlParser.Datatype_null_enableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#size_clause.
    def enterSize_clause(self, ctx:PlSqlParser.Size_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#size_clause.
    def exitSize_clause(self, ctx:PlSqlParser.Size_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_compression.
    def enterTable_compression(self, ctx:PlSqlParser.Table_compressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_compression.
    def exitTable_compression(self, ctx:PlSqlParser.Table_compressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#physical_attributes_clause.
    def enterPhysical_attributes_clause(self, ctx:PlSqlParser.Physical_attributes_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#physical_attributes_clause.
    def exitPhysical_attributes_clause(self, ctx:PlSqlParser.Physical_attributes_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#storage_clause.
    def enterStorage_clause(self, ctx:PlSqlParser.Storage_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#storage_clause.
    def exitStorage_clause(self, ctx:PlSqlParser.Storage_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#deferred_segment_creation.
    def enterDeferred_segment_creation(self, ctx:PlSqlParser.Deferred_segment_creationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#deferred_segment_creation.
    def exitDeferred_segment_creation(self, ctx:PlSqlParser.Deferred_segment_creationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#segment_attributes_clause.
    def enterSegment_attributes_clause(self, ctx:PlSqlParser.Segment_attributes_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#segment_attributes_clause.
    def exitSegment_attributes_clause(self, ctx:PlSqlParser.Segment_attributes_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#physical_properties.
    def enterPhysical_properties(self, ctx:PlSqlParser.Physical_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#physical_properties.
    def exitPhysical_properties(self, ctx:PlSqlParser.Physical_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#row_movement_clause.
    def enterRow_movement_clause(self, ctx:PlSqlParser.Row_movement_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#row_movement_clause.
    def exitRow_movement_clause(self, ctx:PlSqlParser.Row_movement_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#flashback_archive_clause.
    def enterFlashback_archive_clause(self, ctx:PlSqlParser.Flashback_archive_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#flashback_archive_clause.
    def exitFlashback_archive_clause(self, ctx:PlSqlParser.Flashback_archive_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#log_grp.
    def enterLog_grp(self, ctx:PlSqlParser.Log_grpContext):
        pass

    # Exit a parse tree produced by PlSqlParser#log_grp.
    def exitLog_grp(self, ctx:PlSqlParser.Log_grpContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_table_logging.
    def enterSupplemental_table_logging(self, ctx:PlSqlParser.Supplemental_table_loggingContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_table_logging.
    def exitSupplemental_table_logging(self, ctx:PlSqlParser.Supplemental_table_loggingContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_log_grp_clause.
    def enterSupplemental_log_grp_clause(self, ctx:PlSqlParser.Supplemental_log_grp_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_log_grp_clause.
    def exitSupplemental_log_grp_clause(self, ctx:PlSqlParser.Supplemental_log_grp_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_id_key_clause.
    def enterSupplemental_id_key_clause(self, ctx:PlSqlParser.Supplemental_id_key_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_id_key_clause.
    def exitSupplemental_id_key_clause(self, ctx:PlSqlParser.Supplemental_id_key_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#allocate_extent_clause.
    def enterAllocate_extent_clause(self, ctx:PlSqlParser.Allocate_extent_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#allocate_extent_clause.
    def exitAllocate_extent_clause(self, ctx:PlSqlParser.Allocate_extent_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#deallocate_unused_clause.
    def enterDeallocate_unused_clause(self, ctx:PlSqlParser.Deallocate_unused_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#deallocate_unused_clause.
    def exitDeallocate_unused_clause(self, ctx:PlSqlParser.Deallocate_unused_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#shrink_clause.
    def enterShrink_clause(self, ctx:PlSqlParser.Shrink_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#shrink_clause.
    def exitShrink_clause(self, ctx:PlSqlParser.Shrink_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#records_per_block_clause.
    def enterRecords_per_block_clause(self, ctx:PlSqlParser.Records_per_block_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#records_per_block_clause.
    def exitRecords_per_block_clause(self, ctx:PlSqlParser.Records_per_block_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#upgrade_table_clause.
    def enterUpgrade_table_clause(self, ctx:PlSqlParser.Upgrade_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#upgrade_table_clause.
    def exitUpgrade_table_clause(self, ctx:PlSqlParser.Upgrade_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#truncate_table.
    def enterTruncate_table(self, ctx:PlSqlParser.Truncate_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#truncate_table.
    def exitTruncate_table(self, ctx:PlSqlParser.Truncate_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_table.
    def enterDrop_table(self, ctx:PlSqlParser.Drop_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_table.
    def exitDrop_table(self, ctx:PlSqlParser.Drop_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_view.
    def enterDrop_view(self, ctx:PlSqlParser.Drop_viewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_view.
    def exitDrop_view(self, ctx:PlSqlParser.Drop_viewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#comment_on_column.
    def enterComment_on_column(self, ctx:PlSqlParser.Comment_on_columnContext):
        pass

    # Exit a parse tree produced by PlSqlParser#comment_on_column.
    def exitComment_on_column(self, ctx:PlSqlParser.Comment_on_columnContext):
        pass


    # Enter a parse tree produced by PlSqlParser#enable_or_disable.
    def enterEnable_or_disable(self, ctx:PlSqlParser.Enable_or_disableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#enable_or_disable.
    def exitEnable_or_disable(self, ctx:PlSqlParser.Enable_or_disableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#allow_or_disallow.
    def enterAllow_or_disallow(self, ctx:PlSqlParser.Allow_or_disallowContext):
        pass

    # Exit a parse tree produced by PlSqlParser#allow_or_disallow.
    def exitAllow_or_disallow(self, ctx:PlSqlParser.Allow_or_disallowContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_synonym.
    def enterCreate_synonym(self, ctx:PlSqlParser.Create_synonymContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_synonym.
    def exitCreate_synonym(self, ctx:PlSqlParser.Create_synonymContext):
        pass


    # Enter a parse tree produced by PlSqlParser#comment_on_table.
    def enterComment_on_table(self, ctx:PlSqlParser.Comment_on_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#comment_on_table.
    def exitComment_on_table(self, ctx:PlSqlParser.Comment_on_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_cluster.
    def enterAlter_cluster(self, ctx:PlSqlParser.Alter_clusterContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_cluster.
    def exitAlter_cluster(self, ctx:PlSqlParser.Alter_clusterContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cache_or_nocache.
    def enterCache_or_nocache(self, ctx:PlSqlParser.Cache_or_nocacheContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cache_or_nocache.
    def exitCache_or_nocache(self, ctx:PlSqlParser.Cache_or_nocacheContext):
        pass


    # Enter a parse tree produced by PlSqlParser#database_name.
    def enterDatabase_name(self, ctx:PlSqlParser.Database_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#database_name.
    def exitDatabase_name(self, ctx:PlSqlParser.Database_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_database.
    def enterAlter_database(self, ctx:PlSqlParser.Alter_databaseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_database.
    def exitAlter_database(self, ctx:PlSqlParser.Alter_databaseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#startup_clauses.
    def enterStartup_clauses(self, ctx:PlSqlParser.Startup_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#startup_clauses.
    def exitStartup_clauses(self, ctx:PlSqlParser.Startup_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#resetlogs_or_noresetlogs.
    def enterResetlogs_or_noresetlogs(self, ctx:PlSqlParser.Resetlogs_or_noresetlogsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#resetlogs_or_noresetlogs.
    def exitResetlogs_or_noresetlogs(self, ctx:PlSqlParser.Resetlogs_or_noresetlogsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#upgrade_or_downgrade.
    def enterUpgrade_or_downgrade(self, ctx:PlSqlParser.Upgrade_or_downgradeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#upgrade_or_downgrade.
    def exitUpgrade_or_downgrade(self, ctx:PlSqlParser.Upgrade_or_downgradeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#recovery_clauses.
    def enterRecovery_clauses(self, ctx:PlSqlParser.Recovery_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#recovery_clauses.
    def exitRecovery_clauses(self, ctx:PlSqlParser.Recovery_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#begin_or_end.
    def enterBegin_or_end(self, ctx:PlSqlParser.Begin_or_endContext):
        pass

    # Exit a parse tree produced by PlSqlParser#begin_or_end.
    def exitBegin_or_end(self, ctx:PlSqlParser.Begin_or_endContext):
        pass


    # Enter a parse tree produced by PlSqlParser#general_recovery.
    def enterGeneral_recovery(self, ctx:PlSqlParser.General_recoveryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#general_recovery.
    def exitGeneral_recovery(self, ctx:PlSqlParser.General_recoveryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#full_database_recovery.
    def enterFull_database_recovery(self, ctx:PlSqlParser.Full_database_recoveryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#full_database_recovery.
    def exitFull_database_recovery(self, ctx:PlSqlParser.Full_database_recoveryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partial_database_recovery.
    def enterPartial_database_recovery(self, ctx:PlSqlParser.Partial_database_recoveryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partial_database_recovery.
    def exitPartial_database_recovery(self, ctx:PlSqlParser.Partial_database_recoveryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partial_database_recovery_10g.
    def enterPartial_database_recovery_10g(self, ctx:PlSqlParser.Partial_database_recovery_10gContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partial_database_recovery_10g.
    def exitPartial_database_recovery_10g(self, ctx:PlSqlParser.Partial_database_recovery_10gContext):
        pass


    # Enter a parse tree produced by PlSqlParser#managed_standby_recovery.
    def enterManaged_standby_recovery(self, ctx:PlSqlParser.Managed_standby_recoveryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#managed_standby_recovery.
    def exitManaged_standby_recovery(self, ctx:PlSqlParser.Managed_standby_recoveryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#db_name.
    def enterDb_name(self, ctx:PlSqlParser.Db_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#db_name.
    def exitDb_name(self, ctx:PlSqlParser.Db_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#database_file_clauses.
    def enterDatabase_file_clauses(self, ctx:PlSqlParser.Database_file_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#database_file_clauses.
    def exitDatabase_file_clauses(self, ctx:PlSqlParser.Database_file_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#create_datafile_clause.
    def enterCreate_datafile_clause(self, ctx:PlSqlParser.Create_datafile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#create_datafile_clause.
    def exitCreate_datafile_clause(self, ctx:PlSqlParser.Create_datafile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_datafile_clause.
    def enterAlter_datafile_clause(self, ctx:PlSqlParser.Alter_datafile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_datafile_clause.
    def exitAlter_datafile_clause(self, ctx:PlSqlParser.Alter_datafile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_tempfile_clause.
    def enterAlter_tempfile_clause(self, ctx:PlSqlParser.Alter_tempfile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_tempfile_clause.
    def exitAlter_tempfile_clause(self, ctx:PlSqlParser.Alter_tempfile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#logfile_clauses.
    def enterLogfile_clauses(self, ctx:PlSqlParser.Logfile_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#logfile_clauses.
    def exitLogfile_clauses(self, ctx:PlSqlParser.Logfile_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_logfile_clauses.
    def enterAdd_logfile_clauses(self, ctx:PlSqlParser.Add_logfile_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_logfile_clauses.
    def exitAdd_logfile_clauses(self, ctx:PlSqlParser.Add_logfile_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#log_file_group.
    def enterLog_file_group(self, ctx:PlSqlParser.Log_file_groupContext):
        pass

    # Exit a parse tree produced by PlSqlParser#log_file_group.
    def exitLog_file_group(self, ctx:PlSqlParser.Log_file_groupContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_logfile_clauses.
    def enterDrop_logfile_clauses(self, ctx:PlSqlParser.Drop_logfile_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_logfile_clauses.
    def exitDrop_logfile_clauses(self, ctx:PlSqlParser.Drop_logfile_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#switch_logfile_clause.
    def enterSwitch_logfile_clause(self, ctx:PlSqlParser.Switch_logfile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#switch_logfile_clause.
    def exitSwitch_logfile_clause(self, ctx:PlSqlParser.Switch_logfile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_db_logging.
    def enterSupplemental_db_logging(self, ctx:PlSqlParser.Supplemental_db_loggingContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_db_logging.
    def exitSupplemental_db_logging(self, ctx:PlSqlParser.Supplemental_db_loggingContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_or_drop.
    def enterAdd_or_drop(self, ctx:PlSqlParser.Add_or_dropContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_or_drop.
    def exitAdd_or_drop(self, ctx:PlSqlParser.Add_or_dropContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_plsql_clause.
    def enterSupplemental_plsql_clause(self, ctx:PlSqlParser.Supplemental_plsql_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_plsql_clause.
    def exitSupplemental_plsql_clause(self, ctx:PlSqlParser.Supplemental_plsql_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#logfile_descriptor.
    def enterLogfile_descriptor(self, ctx:PlSqlParser.Logfile_descriptorContext):
        pass

    # Exit a parse tree produced by PlSqlParser#logfile_descriptor.
    def exitLogfile_descriptor(self, ctx:PlSqlParser.Logfile_descriptorContext):
        pass


    # Enter a parse tree produced by PlSqlParser#controlfile_clauses.
    def enterControlfile_clauses(self, ctx:PlSqlParser.Controlfile_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#controlfile_clauses.
    def exitControlfile_clauses(self, ctx:PlSqlParser.Controlfile_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trace_file_clause.
    def enterTrace_file_clause(self, ctx:PlSqlParser.Trace_file_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trace_file_clause.
    def exitTrace_file_clause(self, ctx:PlSqlParser.Trace_file_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#standby_database_clauses.
    def enterStandby_database_clauses(self, ctx:PlSqlParser.Standby_database_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#standby_database_clauses.
    def exitStandby_database_clauses(self, ctx:PlSqlParser.Standby_database_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#activate_standby_db_clause.
    def enterActivate_standby_db_clause(self, ctx:PlSqlParser.Activate_standby_db_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#activate_standby_db_clause.
    def exitActivate_standby_db_clause(self, ctx:PlSqlParser.Activate_standby_db_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#maximize_standby_db_clause.
    def enterMaximize_standby_db_clause(self, ctx:PlSqlParser.Maximize_standby_db_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#maximize_standby_db_clause.
    def exitMaximize_standby_db_clause(self, ctx:PlSqlParser.Maximize_standby_db_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#register_logfile_clause.
    def enterRegister_logfile_clause(self, ctx:PlSqlParser.Register_logfile_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#register_logfile_clause.
    def exitRegister_logfile_clause(self, ctx:PlSqlParser.Register_logfile_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#commit_switchover_clause.
    def enterCommit_switchover_clause(self, ctx:PlSqlParser.Commit_switchover_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#commit_switchover_clause.
    def exitCommit_switchover_clause(self, ctx:PlSqlParser.Commit_switchover_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#start_standby_clause.
    def enterStart_standby_clause(self, ctx:PlSqlParser.Start_standby_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#start_standby_clause.
    def exitStart_standby_clause(self, ctx:PlSqlParser.Start_standby_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#stop_standby_clause.
    def enterStop_standby_clause(self, ctx:PlSqlParser.Stop_standby_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#stop_standby_clause.
    def exitStop_standby_clause(self, ctx:PlSqlParser.Stop_standby_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#convert_database_clause.
    def enterConvert_database_clause(self, ctx:PlSqlParser.Convert_database_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#convert_database_clause.
    def exitConvert_database_clause(self, ctx:PlSqlParser.Convert_database_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#default_settings_clause.
    def enterDefault_settings_clause(self, ctx:PlSqlParser.Default_settings_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#default_settings_clause.
    def exitDefault_settings_clause(self, ctx:PlSqlParser.Default_settings_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#set_time_zone_clause.
    def enterSet_time_zone_clause(self, ctx:PlSqlParser.Set_time_zone_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#set_time_zone_clause.
    def exitSet_time_zone_clause(self, ctx:PlSqlParser.Set_time_zone_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#instance_clauses.
    def enterInstance_clauses(self, ctx:PlSqlParser.Instance_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#instance_clauses.
    def exitInstance_clauses(self, ctx:PlSqlParser.Instance_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#security_clause.
    def enterSecurity_clause(self, ctx:PlSqlParser.Security_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#security_clause.
    def exitSecurity_clause(self, ctx:PlSqlParser.Security_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#domain.
    def enterDomain(self, ctx:PlSqlParser.DomainContext):
        pass

    # Exit a parse tree produced by PlSqlParser#domain.
    def exitDomain(self, ctx:PlSqlParser.DomainContext):
        pass


    # Enter a parse tree produced by PlSqlParser#database.
    def enterDatabase(self, ctx:PlSqlParser.DatabaseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#database.
    def exitDatabase(self, ctx:PlSqlParser.DatabaseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#edition_name.
    def enterEdition_name(self, ctx:PlSqlParser.Edition_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#edition_name.
    def exitEdition_name(self, ctx:PlSqlParser.Edition_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#filenumber.
    def enterFilenumber(self, ctx:PlSqlParser.FilenumberContext):
        pass

    # Exit a parse tree produced by PlSqlParser#filenumber.
    def exitFilenumber(self, ctx:PlSqlParser.FilenumberContext):
        pass


    # Enter a parse tree produced by PlSqlParser#filename.
    def enterFilename(self, ctx:PlSqlParser.FilenameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#filename.
    def exitFilename(self, ctx:PlSqlParser.FilenameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_table.
    def enterAlter_table(self, ctx:PlSqlParser.Alter_tableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_table.
    def exitAlter_table(self, ctx:PlSqlParser.Alter_tableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_table_properties.
    def enterAlter_table_properties(self, ctx:PlSqlParser.Alter_table_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_table_properties.
    def exitAlter_table_properties(self, ctx:PlSqlParser.Alter_table_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_table_properties_1.
    def enterAlter_table_properties_1(self, ctx:PlSqlParser.Alter_table_properties_1Context):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_table_properties_1.
    def exitAlter_table_properties_1(self, ctx:PlSqlParser.Alter_table_properties_1Context):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_iot_clauses.
    def enterAlter_iot_clauses(self, ctx:PlSqlParser.Alter_iot_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_iot_clauses.
    def exitAlter_iot_clauses(self, ctx:PlSqlParser.Alter_iot_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_mapping_table_clause.
    def enterAlter_mapping_table_clause(self, ctx:PlSqlParser.Alter_mapping_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_mapping_table_clause.
    def exitAlter_mapping_table_clause(self, ctx:PlSqlParser.Alter_mapping_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_overflow_clause.
    def enterAlter_overflow_clause(self, ctx:PlSqlParser.Alter_overflow_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_overflow_clause.
    def exitAlter_overflow_clause(self, ctx:PlSqlParser.Alter_overflow_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_overflow_clause.
    def enterAdd_overflow_clause(self, ctx:PlSqlParser.Add_overflow_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_overflow_clause.
    def exitAdd_overflow_clause(self, ctx:PlSqlParser.Add_overflow_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#enable_disable_clause.
    def enterEnable_disable_clause(self, ctx:PlSqlParser.Enable_disable_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#enable_disable_clause.
    def exitEnable_disable_clause(self, ctx:PlSqlParser.Enable_disable_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#using_index_clause.
    def enterUsing_index_clause(self, ctx:PlSqlParser.Using_index_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#using_index_clause.
    def exitUsing_index_clause(self, ctx:PlSqlParser.Using_index_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_attributes.
    def enterIndex_attributes(self, ctx:PlSqlParser.Index_attributesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_attributes.
    def exitIndex_attributes(self, ctx:PlSqlParser.Index_attributesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sort_or_nosort.
    def enterSort_or_nosort(self, ctx:PlSqlParser.Sort_or_nosortContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sort_or_nosort.
    def exitSort_or_nosort(self, ctx:PlSqlParser.Sort_or_nosortContext):
        pass


    # Enter a parse tree produced by PlSqlParser#exceptions_clause.
    def enterExceptions_clause(self, ctx:PlSqlParser.Exceptions_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#exceptions_clause.
    def exitExceptions_clause(self, ctx:PlSqlParser.Exceptions_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#move_table_clause.
    def enterMove_table_clause(self, ctx:PlSqlParser.Move_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#move_table_clause.
    def exitMove_table_clause(self, ctx:PlSqlParser.Move_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_org_table_clause.
    def enterIndex_org_table_clause(self, ctx:PlSqlParser.Index_org_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_org_table_clause.
    def exitIndex_org_table_clause(self, ctx:PlSqlParser.Index_org_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#mapping_table_clause.
    def enterMapping_table_clause(self, ctx:PlSqlParser.Mapping_table_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#mapping_table_clause.
    def exitMapping_table_clause(self, ctx:PlSqlParser.Mapping_table_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#key_compression.
    def enterKey_compression(self, ctx:PlSqlParser.Key_compressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#key_compression.
    def exitKey_compression(self, ctx:PlSqlParser.Key_compressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_org_overflow_clause.
    def enterIndex_org_overflow_clause(self, ctx:PlSqlParser.Index_org_overflow_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_org_overflow_clause.
    def exitIndex_org_overflow_clause(self, ctx:PlSqlParser.Index_org_overflow_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_clauses.
    def enterColumn_clauses(self, ctx:PlSqlParser.Column_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_clauses.
    def exitColumn_clauses(self, ctx:PlSqlParser.Column_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_collection_retrieval.
    def enterModify_collection_retrieval(self, ctx:PlSqlParser.Modify_collection_retrievalContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_collection_retrieval.
    def exitModify_collection_retrieval(self, ctx:PlSqlParser.Modify_collection_retrievalContext):
        pass


    # Enter a parse tree produced by PlSqlParser#collection_item.
    def enterCollection_item(self, ctx:PlSqlParser.Collection_itemContext):
        pass

    # Exit a parse tree produced by PlSqlParser#collection_item.
    def exitCollection_item(self, ctx:PlSqlParser.Collection_itemContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rename_column_clause.
    def enterRename_column_clause(self, ctx:PlSqlParser.Rename_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rename_column_clause.
    def exitRename_column_clause(self, ctx:PlSqlParser.Rename_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#old_column_name.
    def enterOld_column_name(self, ctx:PlSqlParser.Old_column_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#old_column_name.
    def exitOld_column_name(self, ctx:PlSqlParser.Old_column_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_column_name.
    def enterNew_column_name(self, ctx:PlSqlParser.New_column_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_column_name.
    def exitNew_column_name(self, ctx:PlSqlParser.New_column_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_modify_drop_column_clauses.
    def enterAdd_modify_drop_column_clauses(self, ctx:PlSqlParser.Add_modify_drop_column_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_modify_drop_column_clauses.
    def exitAdd_modify_drop_column_clauses(self, ctx:PlSqlParser.Add_modify_drop_column_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_column_clause.
    def enterDrop_column_clause(self, ctx:PlSqlParser.Drop_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_column_clause.
    def exitDrop_column_clause(self, ctx:PlSqlParser.Drop_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_column_clauses.
    def enterModify_column_clauses(self, ctx:PlSqlParser.Modify_column_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_column_clauses.
    def exitModify_column_clauses(self, ctx:PlSqlParser.Modify_column_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_col_properties.
    def enterModify_col_properties(self, ctx:PlSqlParser.Modify_col_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_col_properties.
    def exitModify_col_properties(self, ctx:PlSqlParser.Modify_col_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_col_substitutable.
    def enterModify_col_substitutable(self, ctx:PlSqlParser.Modify_col_substitutableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_col_substitutable.
    def exitModify_col_substitutable(self, ctx:PlSqlParser.Modify_col_substitutableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_column_clause.
    def enterAdd_column_clause(self, ctx:PlSqlParser.Add_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_column_clause.
    def exitAdd_column_clause(self, ctx:PlSqlParser.Add_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#alter_varray_col_properties.
    def enterAlter_varray_col_properties(self, ctx:PlSqlParser.Alter_varray_col_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#alter_varray_col_properties.
    def exitAlter_varray_col_properties(self, ctx:PlSqlParser.Alter_varray_col_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#varray_col_properties.
    def enterVarray_col_properties(self, ctx:PlSqlParser.Varray_col_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#varray_col_properties.
    def exitVarray_col_properties(self, ctx:PlSqlParser.Varray_col_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#varray_storage_clause.
    def enterVarray_storage_clause(self, ctx:PlSqlParser.Varray_storage_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#varray_storage_clause.
    def exitVarray_storage_clause(self, ctx:PlSqlParser.Varray_storage_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_segname.
    def enterLob_segname(self, ctx:PlSqlParser.Lob_segnameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_segname.
    def exitLob_segname(self, ctx:PlSqlParser.Lob_segnameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_item.
    def enterLob_item(self, ctx:PlSqlParser.Lob_itemContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_item.
    def exitLob_item(self, ctx:PlSqlParser.Lob_itemContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_storage_parameters.
    def enterLob_storage_parameters(self, ctx:PlSqlParser.Lob_storage_parametersContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_storage_parameters.
    def exitLob_storage_parameters(self, ctx:PlSqlParser.Lob_storage_parametersContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_storage_clause.
    def enterLob_storage_clause(self, ctx:PlSqlParser.Lob_storage_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_storage_clause.
    def exitLob_storage_clause(self, ctx:PlSqlParser.Lob_storage_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_lob_storage_clause.
    def enterModify_lob_storage_clause(self, ctx:PlSqlParser.Modify_lob_storage_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_lob_storage_clause.
    def exitModify_lob_storage_clause(self, ctx:PlSqlParser.Modify_lob_storage_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#modify_lob_parameters.
    def enterModify_lob_parameters(self, ctx:PlSqlParser.Modify_lob_parametersContext):
        pass

    # Exit a parse tree produced by PlSqlParser#modify_lob_parameters.
    def exitModify_lob_parameters(self, ctx:PlSqlParser.Modify_lob_parametersContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_parameters.
    def enterLob_parameters(self, ctx:PlSqlParser.Lob_parametersContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_parameters.
    def exitLob_parameters(self, ctx:PlSqlParser.Lob_parametersContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_deduplicate_clause.
    def enterLob_deduplicate_clause(self, ctx:PlSqlParser.Lob_deduplicate_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_deduplicate_clause.
    def exitLob_deduplicate_clause(self, ctx:PlSqlParser.Lob_deduplicate_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_compression_clause.
    def enterLob_compression_clause(self, ctx:PlSqlParser.Lob_compression_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_compression_clause.
    def exitLob_compression_clause(self, ctx:PlSqlParser.Lob_compression_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lob_retention_clause.
    def enterLob_retention_clause(self, ctx:PlSqlParser.Lob_retention_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lob_retention_clause.
    def exitLob_retention_clause(self, ctx:PlSqlParser.Lob_retention_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#encryption_spec.
    def enterEncryption_spec(self, ctx:PlSqlParser.Encryption_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#encryption_spec.
    def exitEncryption_spec(self, ctx:PlSqlParser.Encryption_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tablespace.
    def enterTablespace(self, ctx:PlSqlParser.TablespaceContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tablespace.
    def exitTablespace(self, ctx:PlSqlParser.TablespaceContext):
        pass


    # Enter a parse tree produced by PlSqlParser#varray_item.
    def enterVarray_item(self, ctx:PlSqlParser.Varray_itemContext):
        pass

    # Exit a parse tree produced by PlSqlParser#varray_item.
    def exitVarray_item(self, ctx:PlSqlParser.Varray_itemContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_properties.
    def enterColumn_properties(self, ctx:PlSqlParser.Column_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_properties.
    def exitColumn_properties(self, ctx:PlSqlParser.Column_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#period_definition.
    def enterPeriod_definition(self, ctx:PlSqlParser.Period_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#period_definition.
    def exitPeriod_definition(self, ctx:PlSqlParser.Period_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#start_time_column.
    def enterStart_time_column(self, ctx:PlSqlParser.Start_time_columnContext):
        pass

    # Exit a parse tree produced by PlSqlParser#start_time_column.
    def exitStart_time_column(self, ctx:PlSqlParser.Start_time_columnContext):
        pass


    # Enter a parse tree produced by PlSqlParser#end_time_column.
    def enterEnd_time_column(self, ctx:PlSqlParser.End_time_columnContext):
        pass

    # Exit a parse tree produced by PlSqlParser#end_time_column.
    def exitEnd_time_column(self, ctx:PlSqlParser.End_time_columnContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_definition.
    def enterColumn_definition(self, ctx:PlSqlParser.Column_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_definition.
    def exitColumn_definition(self, ctx:PlSqlParser.Column_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#virtual_column_definition.
    def enterVirtual_column_definition(self, ctx:PlSqlParser.Virtual_column_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#virtual_column_definition.
    def exitVirtual_column_definition(self, ctx:PlSqlParser.Virtual_column_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#autogenerated_sequence_definition.
    def enterAutogenerated_sequence_definition(self, ctx:PlSqlParser.Autogenerated_sequence_definitionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#autogenerated_sequence_definition.
    def exitAutogenerated_sequence_definition(self, ctx:PlSqlParser.Autogenerated_sequence_definitionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#out_of_line_part_storage.
    def enterOut_of_line_part_storage(self, ctx:PlSqlParser.Out_of_line_part_storageContext):
        pass

    # Exit a parse tree produced by PlSqlParser#out_of_line_part_storage.
    def exitOut_of_line_part_storage(self, ctx:PlSqlParser.Out_of_line_part_storageContext):
        pass


    # Enter a parse tree produced by PlSqlParser#nested_table_col_properties.
    def enterNested_table_col_properties(self, ctx:PlSqlParser.Nested_table_col_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#nested_table_col_properties.
    def exitNested_table_col_properties(self, ctx:PlSqlParser.Nested_table_col_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#nested_item.
    def enterNested_item(self, ctx:PlSqlParser.Nested_itemContext):
        pass

    # Exit a parse tree produced by PlSqlParser#nested_item.
    def exitNested_item(self, ctx:PlSqlParser.Nested_itemContext):
        pass


    # Enter a parse tree produced by PlSqlParser#substitutable_column_clause.
    def enterSubstitutable_column_clause(self, ctx:PlSqlParser.Substitutable_column_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#substitutable_column_clause.
    def exitSubstitutable_column_clause(self, ctx:PlSqlParser.Substitutable_column_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_name.
    def enterPartition_name(self, ctx:PlSqlParser.Partition_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_name.
    def exitPartition_name(self, ctx:PlSqlParser.Partition_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#supplemental_logging_props.
    def enterSupplemental_logging_props(self, ctx:PlSqlParser.Supplemental_logging_propsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#supplemental_logging_props.
    def exitSupplemental_logging_props(self, ctx:PlSqlParser.Supplemental_logging_propsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_or_attribute.
    def enterColumn_or_attribute(self, ctx:PlSqlParser.Column_or_attributeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_or_attribute.
    def exitColumn_or_attribute(self, ctx:PlSqlParser.Column_or_attributeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_type_col_properties.
    def enterObject_type_col_properties(self, ctx:PlSqlParser.Object_type_col_propertiesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_type_col_properties.
    def exitObject_type_col_properties(self, ctx:PlSqlParser.Object_type_col_propertiesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constraint_clauses.
    def enterConstraint_clauses(self, ctx:PlSqlParser.Constraint_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constraint_clauses.
    def exitConstraint_clauses(self, ctx:PlSqlParser.Constraint_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#old_constraint_name.
    def enterOld_constraint_name(self, ctx:PlSqlParser.Old_constraint_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#old_constraint_name.
    def exitOld_constraint_name(self, ctx:PlSqlParser.Old_constraint_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#new_constraint_name.
    def enterNew_constraint_name(self, ctx:PlSqlParser.New_constraint_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#new_constraint_name.
    def exitNew_constraint_name(self, ctx:PlSqlParser.New_constraint_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_constraint_clause.
    def enterDrop_constraint_clause(self, ctx:PlSqlParser.Drop_constraint_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_constraint_clause.
    def exitDrop_constraint_clause(self, ctx:PlSqlParser.Drop_constraint_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_primary_key_or_unique_or_generic_clause.
    def enterDrop_primary_key_or_unique_or_generic_clause(self, ctx:PlSqlParser.Drop_primary_key_or_unique_or_generic_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_primary_key_or_unique_or_generic_clause.
    def exitDrop_primary_key_or_unique_or_generic_clause(self, ctx:PlSqlParser.Drop_primary_key_or_unique_or_generic_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_constraint.
    def enterAdd_constraint(self, ctx:PlSqlParser.Add_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_constraint.
    def exitAdd_constraint(self, ctx:PlSqlParser.Add_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#add_constraint_clause.
    def enterAdd_constraint_clause(self, ctx:PlSqlParser.Add_constraint_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#add_constraint_clause.
    def exitAdd_constraint_clause(self, ctx:PlSqlParser.Add_constraint_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#check_constraint.
    def enterCheck_constraint(self, ctx:PlSqlParser.Check_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#check_constraint.
    def exitCheck_constraint(self, ctx:PlSqlParser.Check_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#drop_constraint.
    def enterDrop_constraint(self, ctx:PlSqlParser.Drop_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#drop_constraint.
    def exitDrop_constraint(self, ctx:PlSqlParser.Drop_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#enable_constraint.
    def enterEnable_constraint(self, ctx:PlSqlParser.Enable_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#enable_constraint.
    def exitEnable_constraint(self, ctx:PlSqlParser.Enable_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#disable_constraint.
    def enterDisable_constraint(self, ctx:PlSqlParser.Disable_constraintContext):
        pass

    # Exit a parse tree produced by PlSqlParser#disable_constraint.
    def exitDisable_constraint(self, ctx:PlSqlParser.Disable_constraintContext):
        pass


    # Enter a parse tree produced by PlSqlParser#foreign_key_clause.
    def enterForeign_key_clause(self, ctx:PlSqlParser.Foreign_key_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#foreign_key_clause.
    def exitForeign_key_clause(self, ctx:PlSqlParser.Foreign_key_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#references_clause.
    def enterReferences_clause(self, ctx:PlSqlParser.References_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#references_clause.
    def exitReferences_clause(self, ctx:PlSqlParser.References_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#on_delete_clause.
    def enterOn_delete_clause(self, ctx:PlSqlParser.On_delete_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#on_delete_clause.
    def exitOn_delete_clause(self, ctx:PlSqlParser.On_delete_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unique_key_clause.
    def enterUnique_key_clause(self, ctx:PlSqlParser.Unique_key_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unique_key_clause.
    def exitUnique_key_clause(self, ctx:PlSqlParser.Unique_key_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#primary_key_clause.
    def enterPrimary_key_clause(self, ctx:PlSqlParser.Primary_key_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#primary_key_clause.
    def exitPrimary_key_clause(self, ctx:PlSqlParser.Primary_key_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#anonymous_block.
    def enterAnonymous_block(self, ctx:PlSqlParser.Anonymous_blockContext):
        pass

    # Exit a parse tree produced by PlSqlParser#anonymous_block.
    def exitAnonymous_block(self, ctx:PlSqlParser.Anonymous_blockContext):
        pass


    # Enter a parse tree produced by PlSqlParser#invoker_rights_clause.
    def enterInvoker_rights_clause(self, ctx:PlSqlParser.Invoker_rights_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#invoker_rights_clause.
    def exitInvoker_rights_clause(self, ctx:PlSqlParser.Invoker_rights_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#call_spec.
    def enterCall_spec(self, ctx:PlSqlParser.Call_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#call_spec.
    def exitCall_spec(self, ctx:PlSqlParser.Call_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#java_spec.
    def enterJava_spec(self, ctx:PlSqlParser.Java_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#java_spec.
    def exitJava_spec(self, ctx:PlSqlParser.Java_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#c_spec.
    def enterC_spec(self, ctx:PlSqlParser.C_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#c_spec.
    def exitC_spec(self, ctx:PlSqlParser.C_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#c_agent_in_clause.
    def enterC_agent_in_clause(self, ctx:PlSqlParser.C_agent_in_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#c_agent_in_clause.
    def exitC_agent_in_clause(self, ctx:PlSqlParser.C_agent_in_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#c_parameters_clause.
    def enterC_parameters_clause(self, ctx:PlSqlParser.C_parameters_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#c_parameters_clause.
    def exitC_parameters_clause(self, ctx:PlSqlParser.C_parameters_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parameter.
    def enterParameter(self, ctx:PlSqlParser.ParameterContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parameter.
    def exitParameter(self, ctx:PlSqlParser.ParameterContext):
        pass


    # Enter a parse tree produced by PlSqlParser#default_value_part.
    def enterDefault_value_part(self, ctx:PlSqlParser.Default_value_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#default_value_part.
    def exitDefault_value_part(self, ctx:PlSqlParser.Default_value_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#seq_of_declare_specs.
    def enterSeq_of_declare_specs(self, ctx:PlSqlParser.Seq_of_declare_specsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#seq_of_declare_specs.
    def exitSeq_of_declare_specs(self, ctx:PlSqlParser.Seq_of_declare_specsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#declare_spec.
    def enterDeclare_spec(self, ctx:PlSqlParser.Declare_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#declare_spec.
    def exitDeclare_spec(self, ctx:PlSqlParser.Declare_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#variable_declaration.
    def enterVariable_declaration(self, ctx:PlSqlParser.Variable_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#variable_declaration.
    def exitVariable_declaration(self, ctx:PlSqlParser.Variable_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subtype_declaration.
    def enterSubtype_declaration(self, ctx:PlSqlParser.Subtype_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subtype_declaration.
    def exitSubtype_declaration(self, ctx:PlSqlParser.Subtype_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cursor_declaration.
    def enterCursor_declaration(self, ctx:PlSqlParser.Cursor_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cursor_declaration.
    def exitCursor_declaration(self, ctx:PlSqlParser.Cursor_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parameter_spec.
    def enterParameter_spec(self, ctx:PlSqlParser.Parameter_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parameter_spec.
    def exitParameter_spec(self, ctx:PlSqlParser.Parameter_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#exception_declaration.
    def enterException_declaration(self, ctx:PlSqlParser.Exception_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#exception_declaration.
    def exitException_declaration(self, ctx:PlSqlParser.Exception_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pragma_declaration.
    def enterPragma_declaration(self, ctx:PlSqlParser.Pragma_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pragma_declaration.
    def exitPragma_declaration(self, ctx:PlSqlParser.Pragma_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#record_type_def.
    def enterRecord_type_def(self, ctx:PlSqlParser.Record_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#record_type_def.
    def exitRecord_type_def(self, ctx:PlSqlParser.Record_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#field_spec.
    def enterField_spec(self, ctx:PlSqlParser.Field_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#field_spec.
    def exitField_spec(self, ctx:PlSqlParser.Field_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#ref_cursor_type_def.
    def enterRef_cursor_type_def(self, ctx:PlSqlParser.Ref_cursor_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#ref_cursor_type_def.
    def exitRef_cursor_type_def(self, ctx:PlSqlParser.Ref_cursor_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_declaration.
    def enterType_declaration(self, ctx:PlSqlParser.Type_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_declaration.
    def exitType_declaration(self, ctx:PlSqlParser.Type_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_type_def.
    def enterTable_type_def(self, ctx:PlSqlParser.Table_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_type_def.
    def exitTable_type_def(self, ctx:PlSqlParser.Table_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_indexed_by_part.
    def enterTable_indexed_by_part(self, ctx:PlSqlParser.Table_indexed_by_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_indexed_by_part.
    def exitTable_indexed_by_part(self, ctx:PlSqlParser.Table_indexed_by_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#varray_type_def.
    def enterVarray_type_def(self, ctx:PlSqlParser.Varray_type_defContext):
        pass

    # Exit a parse tree produced by PlSqlParser#varray_type_def.
    def exitVarray_type_def(self, ctx:PlSqlParser.Varray_type_defContext):
        pass


    # Enter a parse tree produced by PlSqlParser#seq_of_statements.
    def enterSeq_of_statements(self, ctx:PlSqlParser.Seq_of_statementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#seq_of_statements.
    def exitSeq_of_statements(self, ctx:PlSqlParser.Seq_of_statementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#label_declaration.
    def enterLabel_declaration(self, ctx:PlSqlParser.Label_declarationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#label_declaration.
    def exitLabel_declaration(self, ctx:PlSqlParser.Label_declarationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#statement.
    def enterStatement(self, ctx:PlSqlParser.StatementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#statement.
    def exitStatement(self, ctx:PlSqlParser.StatementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#swallow_to_semi.
    def enterSwallow_to_semi(self, ctx:PlSqlParser.Swallow_to_semiContext):
        pass

    # Exit a parse tree produced by PlSqlParser#swallow_to_semi.
    def exitSwallow_to_semi(self, ctx:PlSqlParser.Swallow_to_semiContext):
        pass


    # Enter a parse tree produced by PlSqlParser#assignment_statement.
    def enterAssignment_statement(self, ctx:PlSqlParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#assignment_statement.
    def exitAssignment_statement(self, ctx:PlSqlParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#continue_statement.
    def enterContinue_statement(self, ctx:PlSqlParser.Continue_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#continue_statement.
    def exitContinue_statement(self, ctx:PlSqlParser.Continue_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#exit_statement.
    def enterExit_statement(self, ctx:PlSqlParser.Exit_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#exit_statement.
    def exitExit_statement(self, ctx:PlSqlParser.Exit_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#goto_statement.
    def enterGoto_statement(self, ctx:PlSqlParser.Goto_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#goto_statement.
    def exitGoto_statement(self, ctx:PlSqlParser.Goto_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#if_statement.
    def enterIf_statement(self, ctx:PlSqlParser.If_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#if_statement.
    def exitIf_statement(self, ctx:PlSqlParser.If_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#elsif_part.
    def enterElsif_part(self, ctx:PlSqlParser.Elsif_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#elsif_part.
    def exitElsif_part(self, ctx:PlSqlParser.Elsif_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#else_part.
    def enterElse_part(self, ctx:PlSqlParser.Else_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#else_part.
    def exitElse_part(self, ctx:PlSqlParser.Else_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#loop_statement.
    def enterLoop_statement(self, ctx:PlSqlParser.Loop_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#loop_statement.
    def exitLoop_statement(self, ctx:PlSqlParser.Loop_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cursor_loop_param.
    def enterCursor_loop_param(self, ctx:PlSqlParser.Cursor_loop_paramContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cursor_loop_param.
    def exitCursor_loop_param(self, ctx:PlSqlParser.Cursor_loop_paramContext):
        pass


    # Enter a parse tree produced by PlSqlParser#forall_statement.
    def enterForall_statement(self, ctx:PlSqlParser.Forall_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#forall_statement.
    def exitForall_statement(self, ctx:PlSqlParser.Forall_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#bounds_clause.
    def enterBounds_clause(self, ctx:PlSqlParser.Bounds_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#bounds_clause.
    def exitBounds_clause(self, ctx:PlSqlParser.Bounds_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#between_bound.
    def enterBetween_bound(self, ctx:PlSqlParser.Between_boundContext):
        pass

    # Exit a parse tree produced by PlSqlParser#between_bound.
    def exitBetween_bound(self, ctx:PlSqlParser.Between_boundContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lower_bound.
    def enterLower_bound(self, ctx:PlSqlParser.Lower_boundContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lower_bound.
    def exitLower_bound(self, ctx:PlSqlParser.Lower_boundContext):
        pass


    # Enter a parse tree produced by PlSqlParser#upper_bound.
    def enterUpper_bound(self, ctx:PlSqlParser.Upper_boundContext):
        pass

    # Exit a parse tree produced by PlSqlParser#upper_bound.
    def exitUpper_bound(self, ctx:PlSqlParser.Upper_boundContext):
        pass


    # Enter a parse tree produced by PlSqlParser#null_statement.
    def enterNull_statement(self, ctx:PlSqlParser.Null_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#null_statement.
    def exitNull_statement(self, ctx:PlSqlParser.Null_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#raise_statement.
    def enterRaise_statement(self, ctx:PlSqlParser.Raise_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#raise_statement.
    def exitRaise_statement(self, ctx:PlSqlParser.Raise_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#return_statement.
    def enterReturn_statement(self, ctx:PlSqlParser.Return_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#return_statement.
    def exitReturn_statement(self, ctx:PlSqlParser.Return_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_call.
    def enterFunction_call(self, ctx:PlSqlParser.Function_callContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_call.
    def exitFunction_call(self, ctx:PlSqlParser.Function_callContext):
        pass


    # Enter a parse tree produced by PlSqlParser#procedure_call.
    def enterProcedure_call(self, ctx:PlSqlParser.Procedure_callContext):
        pass

    # Exit a parse tree produced by PlSqlParser#procedure_call.
    def exitProcedure_call(self, ctx:PlSqlParser.Procedure_callContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pipe_row_statement.
    def enterPipe_row_statement(self, ctx:PlSqlParser.Pipe_row_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pipe_row_statement.
    def exitPipe_row_statement(self, ctx:PlSqlParser.Pipe_row_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#body.
    def enterBody(self, ctx:PlSqlParser.BodyContext):
        pass

    # Exit a parse tree produced by PlSqlParser#body.
    def exitBody(self, ctx:PlSqlParser.BodyContext):
        pass


    # Enter a parse tree produced by PlSqlParser#exception_handler.
    def enterException_handler(self, ctx:PlSqlParser.Exception_handlerContext):
        pass

    # Exit a parse tree produced by PlSqlParser#exception_handler.
    def exitException_handler(self, ctx:PlSqlParser.Exception_handlerContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trigger_block.
    def enterTrigger_block(self, ctx:PlSqlParser.Trigger_blockContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trigger_block.
    def exitTrigger_block(self, ctx:PlSqlParser.Trigger_blockContext):
        pass


    # Enter a parse tree produced by PlSqlParser#block.
    def enterBlock(self, ctx:PlSqlParser.BlockContext):
        pass

    # Exit a parse tree produced by PlSqlParser#block.
    def exitBlock(self, ctx:PlSqlParser.BlockContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sql_statement.
    def enterSql_statement(self, ctx:PlSqlParser.Sql_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sql_statement.
    def exitSql_statement(self, ctx:PlSqlParser.Sql_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#execute_immediate.
    def enterExecute_immediate(self, ctx:PlSqlParser.Execute_immediateContext):
        pass

    # Exit a parse tree produced by PlSqlParser#execute_immediate.
    def exitExecute_immediate(self, ctx:PlSqlParser.Execute_immediateContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dynamic_returning_clause.
    def enterDynamic_returning_clause(self, ctx:PlSqlParser.Dynamic_returning_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dynamic_returning_clause.
    def exitDynamic_returning_clause(self, ctx:PlSqlParser.Dynamic_returning_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#data_manipulation_language_statements.
    def enterData_manipulation_language_statements(self, ctx:PlSqlParser.Data_manipulation_language_statementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#data_manipulation_language_statements.
    def exitData_manipulation_language_statements(self, ctx:PlSqlParser.Data_manipulation_language_statementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cursor_manipulation_statements.
    def enterCursor_manipulation_statements(self, ctx:PlSqlParser.Cursor_manipulation_statementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cursor_manipulation_statements.
    def exitCursor_manipulation_statements(self, ctx:PlSqlParser.Cursor_manipulation_statementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#close_statement.
    def enterClose_statement(self, ctx:PlSqlParser.Close_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#close_statement.
    def exitClose_statement(self, ctx:PlSqlParser.Close_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#open_statement.
    def enterOpen_statement(self, ctx:PlSqlParser.Open_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#open_statement.
    def exitOpen_statement(self, ctx:PlSqlParser.Open_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#fetch_statement.
    def enterFetch_statement(self, ctx:PlSqlParser.Fetch_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#fetch_statement.
    def exitFetch_statement(self, ctx:PlSqlParser.Fetch_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#open_for_statement.
    def enterOpen_for_statement(self, ctx:PlSqlParser.Open_for_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#open_for_statement.
    def exitOpen_for_statement(self, ctx:PlSqlParser.Open_for_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#transaction_control_statements.
    def enterTransaction_control_statements(self, ctx:PlSqlParser.Transaction_control_statementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#transaction_control_statements.
    def exitTransaction_control_statements(self, ctx:PlSqlParser.Transaction_control_statementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#set_transaction_command.
    def enterSet_transaction_command(self, ctx:PlSqlParser.Set_transaction_commandContext):
        pass

    # Exit a parse tree produced by PlSqlParser#set_transaction_command.
    def exitSet_transaction_command(self, ctx:PlSqlParser.Set_transaction_commandContext):
        pass


    # Enter a parse tree produced by PlSqlParser#set_constraint_command.
    def enterSet_constraint_command(self, ctx:PlSqlParser.Set_constraint_commandContext):
        pass

    # Exit a parse tree produced by PlSqlParser#set_constraint_command.
    def exitSet_constraint_command(self, ctx:PlSqlParser.Set_constraint_commandContext):
        pass


    # Enter a parse tree produced by PlSqlParser#commit_statement.
    def enterCommit_statement(self, ctx:PlSqlParser.Commit_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#commit_statement.
    def exitCommit_statement(self, ctx:PlSqlParser.Commit_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#write_clause.
    def enterWrite_clause(self, ctx:PlSqlParser.Write_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#write_clause.
    def exitWrite_clause(self, ctx:PlSqlParser.Write_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rollback_statement.
    def enterRollback_statement(self, ctx:PlSqlParser.Rollback_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rollback_statement.
    def exitRollback_statement(self, ctx:PlSqlParser.Rollback_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#savepoint_statement.
    def enterSavepoint_statement(self, ctx:PlSqlParser.Savepoint_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#savepoint_statement.
    def exitSavepoint_statement(self, ctx:PlSqlParser.Savepoint_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#explain_statement.
    def enterExplain_statement(self, ctx:PlSqlParser.Explain_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#explain_statement.
    def exitExplain_statement(self, ctx:PlSqlParser.Explain_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#select_only_statement.
    def enterSelect_only_statement(self, ctx:PlSqlParser.Select_only_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#select_only_statement.
    def exitSelect_only_statement(self, ctx:PlSqlParser.Select_only_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#select_statement.
    def enterSelect_statement(self, ctx:PlSqlParser.Select_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#select_statement.
    def exitSelect_statement(self, ctx:PlSqlParser.Select_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subquery_factoring_clause.
    def enterSubquery_factoring_clause(self, ctx:PlSqlParser.Subquery_factoring_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subquery_factoring_clause.
    def exitSubquery_factoring_clause(self, ctx:PlSqlParser.Subquery_factoring_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#factoring_element.
    def enterFactoring_element(self, ctx:PlSqlParser.Factoring_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#factoring_element.
    def exitFactoring_element(self, ctx:PlSqlParser.Factoring_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#search_clause.
    def enterSearch_clause(self, ctx:PlSqlParser.Search_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#search_clause.
    def exitSearch_clause(self, ctx:PlSqlParser.Search_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cycle_clause.
    def enterCycle_clause(self, ctx:PlSqlParser.Cycle_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cycle_clause.
    def exitCycle_clause(self, ctx:PlSqlParser.Cycle_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subquery.
    def enterSubquery(self, ctx:PlSqlParser.SubqueryContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subquery.
    def exitSubquery(self, ctx:PlSqlParser.SubqueryContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subquery_basic_elements.
    def enterSubquery_basic_elements(self, ctx:PlSqlParser.Subquery_basic_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subquery_basic_elements.
    def exitSubquery_basic_elements(self, ctx:PlSqlParser.Subquery_basic_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subquery_operation_part.
    def enterSubquery_operation_part(self, ctx:PlSqlParser.Subquery_operation_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subquery_operation_part.
    def exitSubquery_operation_part(self, ctx:PlSqlParser.Subquery_operation_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#query_block.
    def enterQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        pass

    # Exit a parse tree produced by PlSqlParser#query_block.
    def exitQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        pass


    # Enter a parse tree produced by PlSqlParser#selected_list.
    def enterSelected_list(self, ctx:PlSqlParser.Selected_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#selected_list.
    def exitSelected_list(self, ctx:PlSqlParser.Selected_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#from_clause.
    def enterFrom_clause(self, ctx:PlSqlParser.From_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#from_clause.
    def exitFrom_clause(self, ctx:PlSqlParser.From_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#select_list_elements.
    def enterSelect_list_elements(self, ctx:PlSqlParser.Select_list_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#select_list_elements.
    def exitSelect_list_elements(self, ctx:PlSqlParser.Select_list_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref_list.
    def enterTable_ref_list(self, ctx:PlSqlParser.Table_ref_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref_list.
    def exitTable_ref_list(self, ctx:PlSqlParser.Table_ref_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref.
    def enterTable_ref(self, ctx:PlSqlParser.Table_refContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref.
    def exitTable_ref(self, ctx:PlSqlParser.Table_refContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref_aux.
    def enterTable_ref_aux(self, ctx:PlSqlParser.Table_ref_auxContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref_aux.
    def exitTable_ref_aux(self, ctx:PlSqlParser.Table_ref_auxContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref_aux_internal_one.
    def enterTable_ref_aux_internal_one(self, ctx:PlSqlParser.Table_ref_aux_internal_oneContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref_aux_internal_one.
    def exitTable_ref_aux_internal_one(self, ctx:PlSqlParser.Table_ref_aux_internal_oneContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref_aux_internal_two.
    def enterTable_ref_aux_internal_two(self, ctx:PlSqlParser.Table_ref_aux_internal_twoContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref_aux_internal_two.
    def exitTable_ref_aux_internal_two(self, ctx:PlSqlParser.Table_ref_aux_internal_twoContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_ref_aux_internal_three.
    def enterTable_ref_aux_internal_three(self, ctx:PlSqlParser.Table_ref_aux_internal_threeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_ref_aux_internal_three.
    def exitTable_ref_aux_internal_three(self, ctx:PlSqlParser.Table_ref_aux_internal_threeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#join_clause.
    def enterJoin_clause(self, ctx:PlSqlParser.Join_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#join_clause.
    def exitJoin_clause(self, ctx:PlSqlParser.Join_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#join_on_part.
    def enterJoin_on_part(self, ctx:PlSqlParser.Join_on_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#join_on_part.
    def exitJoin_on_part(self, ctx:PlSqlParser.Join_on_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#join_using_part.
    def enterJoin_using_part(self, ctx:PlSqlParser.Join_using_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#join_using_part.
    def exitJoin_using_part(self, ctx:PlSqlParser.Join_using_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#outer_join_type.
    def enterOuter_join_type(self, ctx:PlSqlParser.Outer_join_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#outer_join_type.
    def exitOuter_join_type(self, ctx:PlSqlParser.Outer_join_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#query_partition_clause.
    def enterQuery_partition_clause(self, ctx:PlSqlParser.Query_partition_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#query_partition_clause.
    def exitQuery_partition_clause(self, ctx:PlSqlParser.Query_partition_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#flashback_query_clause.
    def enterFlashback_query_clause(self, ctx:PlSqlParser.Flashback_query_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#flashback_query_clause.
    def exitFlashback_query_clause(self, ctx:PlSqlParser.Flashback_query_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_clause.
    def enterPivot_clause(self, ctx:PlSqlParser.Pivot_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_clause.
    def exitPivot_clause(self, ctx:PlSqlParser.Pivot_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_element.
    def enterPivot_element(self, ctx:PlSqlParser.Pivot_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_element.
    def exitPivot_element(self, ctx:PlSqlParser.Pivot_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_for_clause.
    def enterPivot_for_clause(self, ctx:PlSqlParser.Pivot_for_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_for_clause.
    def exitPivot_for_clause(self, ctx:PlSqlParser.Pivot_for_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_in_clause.
    def enterPivot_in_clause(self, ctx:PlSqlParser.Pivot_in_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_in_clause.
    def exitPivot_in_clause(self, ctx:PlSqlParser.Pivot_in_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_in_clause_element.
    def enterPivot_in_clause_element(self, ctx:PlSqlParser.Pivot_in_clause_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_in_clause_element.
    def exitPivot_in_clause_element(self, ctx:PlSqlParser.Pivot_in_clause_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#pivot_in_clause_elements.
    def enterPivot_in_clause_elements(self, ctx:PlSqlParser.Pivot_in_clause_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#pivot_in_clause_elements.
    def exitPivot_in_clause_elements(self, ctx:PlSqlParser.Pivot_in_clause_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unpivot_clause.
    def enterUnpivot_clause(self, ctx:PlSqlParser.Unpivot_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unpivot_clause.
    def exitUnpivot_clause(self, ctx:PlSqlParser.Unpivot_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unpivot_in_clause.
    def enterUnpivot_in_clause(self, ctx:PlSqlParser.Unpivot_in_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unpivot_in_clause.
    def exitUnpivot_in_clause(self, ctx:PlSqlParser.Unpivot_in_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unpivot_in_elements.
    def enterUnpivot_in_elements(self, ctx:PlSqlParser.Unpivot_in_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unpivot_in_elements.
    def exitUnpivot_in_elements(self, ctx:PlSqlParser.Unpivot_in_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#hierarchical_query_clause.
    def enterHierarchical_query_clause(self, ctx:PlSqlParser.Hierarchical_query_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#hierarchical_query_clause.
    def exitHierarchical_query_clause(self, ctx:PlSqlParser.Hierarchical_query_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#start_part.
    def enterStart_part(self, ctx:PlSqlParser.Start_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#start_part.
    def exitStart_part(self, ctx:PlSqlParser.Start_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#group_by_clause.
    def enterGroup_by_clause(self, ctx:PlSqlParser.Group_by_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#group_by_clause.
    def exitGroup_by_clause(self, ctx:PlSqlParser.Group_by_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#group_by_elements.
    def enterGroup_by_elements(self, ctx:PlSqlParser.Group_by_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#group_by_elements.
    def exitGroup_by_elements(self, ctx:PlSqlParser.Group_by_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rollup_cube_clause.
    def enterRollup_cube_clause(self, ctx:PlSqlParser.Rollup_cube_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rollup_cube_clause.
    def exitRollup_cube_clause(self, ctx:PlSqlParser.Rollup_cube_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#grouping_sets_clause.
    def enterGrouping_sets_clause(self, ctx:PlSqlParser.Grouping_sets_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#grouping_sets_clause.
    def exitGrouping_sets_clause(self, ctx:PlSqlParser.Grouping_sets_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#grouping_sets_elements.
    def enterGrouping_sets_elements(self, ctx:PlSqlParser.Grouping_sets_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#grouping_sets_elements.
    def exitGrouping_sets_elements(self, ctx:PlSqlParser.Grouping_sets_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#having_clause.
    def enterHaving_clause(self, ctx:PlSqlParser.Having_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#having_clause.
    def exitHaving_clause(self, ctx:PlSqlParser.Having_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_clause.
    def enterModel_clause(self, ctx:PlSqlParser.Model_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_clause.
    def exitModel_clause(self, ctx:PlSqlParser.Model_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cell_reference_options.
    def enterCell_reference_options(self, ctx:PlSqlParser.Cell_reference_optionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cell_reference_options.
    def exitCell_reference_options(self, ctx:PlSqlParser.Cell_reference_optionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#return_rows_clause.
    def enterReturn_rows_clause(self, ctx:PlSqlParser.Return_rows_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#return_rows_clause.
    def exitReturn_rows_clause(self, ctx:PlSqlParser.Return_rows_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#reference_model.
    def enterReference_model(self, ctx:PlSqlParser.Reference_modelContext):
        pass

    # Exit a parse tree produced by PlSqlParser#reference_model.
    def exitReference_model(self, ctx:PlSqlParser.Reference_modelContext):
        pass


    # Enter a parse tree produced by PlSqlParser#main_model.
    def enterMain_model(self, ctx:PlSqlParser.Main_modelContext):
        pass

    # Exit a parse tree produced by PlSqlParser#main_model.
    def exitMain_model(self, ctx:PlSqlParser.Main_modelContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_column_clauses.
    def enterModel_column_clauses(self, ctx:PlSqlParser.Model_column_clausesContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_column_clauses.
    def exitModel_column_clauses(self, ctx:PlSqlParser.Model_column_clausesContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_column_partition_part.
    def enterModel_column_partition_part(self, ctx:PlSqlParser.Model_column_partition_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_column_partition_part.
    def exitModel_column_partition_part(self, ctx:PlSqlParser.Model_column_partition_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_column_list.
    def enterModel_column_list(self, ctx:PlSqlParser.Model_column_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_column_list.
    def exitModel_column_list(self, ctx:PlSqlParser.Model_column_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_column.
    def enterModel_column(self, ctx:PlSqlParser.Model_columnContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_column.
    def exitModel_column(self, ctx:PlSqlParser.Model_columnContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_rules_clause.
    def enterModel_rules_clause(self, ctx:PlSqlParser.Model_rules_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_rules_clause.
    def exitModel_rules_clause(self, ctx:PlSqlParser.Model_rules_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_rules_part.
    def enterModel_rules_part(self, ctx:PlSqlParser.Model_rules_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_rules_part.
    def exitModel_rules_part(self, ctx:PlSqlParser.Model_rules_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_rules_element.
    def enterModel_rules_element(self, ctx:PlSqlParser.Model_rules_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_rules_element.
    def exitModel_rules_element(self, ctx:PlSqlParser.Model_rules_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cell_assignment.
    def enterCell_assignment(self, ctx:PlSqlParser.Cell_assignmentContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cell_assignment.
    def exitCell_assignment(self, ctx:PlSqlParser.Cell_assignmentContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_iterate_clause.
    def enterModel_iterate_clause(self, ctx:PlSqlParser.Model_iterate_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_iterate_clause.
    def exitModel_iterate_clause(self, ctx:PlSqlParser.Model_iterate_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#until_part.
    def enterUntil_part(self, ctx:PlSqlParser.Until_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#until_part.
    def exitUntil_part(self, ctx:PlSqlParser.Until_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#order_by_clause.
    def enterOrder_by_clause(self, ctx:PlSqlParser.Order_by_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#order_by_clause.
    def exitOrder_by_clause(self, ctx:PlSqlParser.Order_by_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#order_by_elements.
    def enterOrder_by_elements(self, ctx:PlSqlParser.Order_by_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#order_by_elements.
    def exitOrder_by_elements(self, ctx:PlSqlParser.Order_by_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#offset_clause.
    def enterOffset_clause(self, ctx:PlSqlParser.Offset_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#offset_clause.
    def exitOffset_clause(self, ctx:PlSqlParser.Offset_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#fetch_clause.
    def enterFetch_clause(self, ctx:PlSqlParser.Fetch_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#fetch_clause.
    def exitFetch_clause(self, ctx:PlSqlParser.Fetch_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#for_update_clause.
    def enterFor_update_clause(self, ctx:PlSqlParser.For_update_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#for_update_clause.
    def exitFor_update_clause(self, ctx:PlSqlParser.For_update_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#for_update_of_part.
    def enterFor_update_of_part(self, ctx:PlSqlParser.For_update_of_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#for_update_of_part.
    def exitFor_update_of_part(self, ctx:PlSqlParser.For_update_of_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#for_update_options.
    def enterFor_update_options(self, ctx:PlSqlParser.For_update_optionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#for_update_options.
    def exitFor_update_options(self, ctx:PlSqlParser.For_update_optionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#update_statement.
    def enterUpdate_statement(self, ctx:PlSqlParser.Update_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#update_statement.
    def exitUpdate_statement(self, ctx:PlSqlParser.Update_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#update_set_clause.
    def enterUpdate_set_clause(self, ctx:PlSqlParser.Update_set_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#update_set_clause.
    def exitUpdate_set_clause(self, ctx:PlSqlParser.Update_set_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_based_update_set_clause.
    def enterColumn_based_update_set_clause(self, ctx:PlSqlParser.Column_based_update_set_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_based_update_set_clause.
    def exitColumn_based_update_set_clause(self, ctx:PlSqlParser.Column_based_update_set_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#delete_statement.
    def enterDelete_statement(self, ctx:PlSqlParser.Delete_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#delete_statement.
    def exitDelete_statement(self, ctx:PlSqlParser.Delete_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#insert_statement.
    def enterInsert_statement(self, ctx:PlSqlParser.Insert_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#insert_statement.
    def exitInsert_statement(self, ctx:PlSqlParser.Insert_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#single_table_insert.
    def enterSingle_table_insert(self, ctx:PlSqlParser.Single_table_insertContext):
        pass

    # Exit a parse tree produced by PlSqlParser#single_table_insert.
    def exitSingle_table_insert(self, ctx:PlSqlParser.Single_table_insertContext):
        pass


    # Enter a parse tree produced by PlSqlParser#multi_table_insert.
    def enterMulti_table_insert(self, ctx:PlSqlParser.Multi_table_insertContext):
        pass

    # Exit a parse tree produced by PlSqlParser#multi_table_insert.
    def exitMulti_table_insert(self, ctx:PlSqlParser.Multi_table_insertContext):
        pass


    # Enter a parse tree produced by PlSqlParser#multi_table_element.
    def enterMulti_table_element(self, ctx:PlSqlParser.Multi_table_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#multi_table_element.
    def exitMulti_table_element(self, ctx:PlSqlParser.Multi_table_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#conditional_insert_clause.
    def enterConditional_insert_clause(self, ctx:PlSqlParser.Conditional_insert_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#conditional_insert_clause.
    def exitConditional_insert_clause(self, ctx:PlSqlParser.Conditional_insert_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#conditional_insert_when_part.
    def enterConditional_insert_when_part(self, ctx:PlSqlParser.Conditional_insert_when_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#conditional_insert_when_part.
    def exitConditional_insert_when_part(self, ctx:PlSqlParser.Conditional_insert_when_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#conditional_insert_else_part.
    def enterConditional_insert_else_part(self, ctx:PlSqlParser.Conditional_insert_else_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#conditional_insert_else_part.
    def exitConditional_insert_else_part(self, ctx:PlSqlParser.Conditional_insert_else_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#insert_into_clause.
    def enterInsert_into_clause(self, ctx:PlSqlParser.Insert_into_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#insert_into_clause.
    def exitInsert_into_clause(self, ctx:PlSqlParser.Insert_into_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#values_clause.
    def enterValues_clause(self, ctx:PlSqlParser.Values_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#values_clause.
    def exitValues_clause(self, ctx:PlSqlParser.Values_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#merge_statement.
    def enterMerge_statement(self, ctx:PlSqlParser.Merge_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#merge_statement.
    def exitMerge_statement(self, ctx:PlSqlParser.Merge_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#merge_update_clause.
    def enterMerge_update_clause(self, ctx:PlSqlParser.Merge_update_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#merge_update_clause.
    def exitMerge_update_clause(self, ctx:PlSqlParser.Merge_update_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#merge_element.
    def enterMerge_element(self, ctx:PlSqlParser.Merge_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#merge_element.
    def exitMerge_element(self, ctx:PlSqlParser.Merge_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#merge_update_delete_part.
    def enterMerge_update_delete_part(self, ctx:PlSqlParser.Merge_update_delete_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#merge_update_delete_part.
    def exitMerge_update_delete_part(self, ctx:PlSqlParser.Merge_update_delete_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#merge_insert_clause.
    def enterMerge_insert_clause(self, ctx:PlSqlParser.Merge_insert_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#merge_insert_clause.
    def exitMerge_insert_clause(self, ctx:PlSqlParser.Merge_insert_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#selected_tableview.
    def enterSelected_tableview(self, ctx:PlSqlParser.Selected_tableviewContext):
        pass

    # Exit a parse tree produced by PlSqlParser#selected_tableview.
    def exitSelected_tableview(self, ctx:PlSqlParser.Selected_tableviewContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lock_table_statement.
    def enterLock_table_statement(self, ctx:PlSqlParser.Lock_table_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lock_table_statement.
    def exitLock_table_statement(self, ctx:PlSqlParser.Lock_table_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#wait_nowait_part.
    def enterWait_nowait_part(self, ctx:PlSqlParser.Wait_nowait_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#wait_nowait_part.
    def exitWait_nowait_part(self, ctx:PlSqlParser.Wait_nowait_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lock_table_element.
    def enterLock_table_element(self, ctx:PlSqlParser.Lock_table_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lock_table_element.
    def exitLock_table_element(self, ctx:PlSqlParser.Lock_table_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#lock_mode.
    def enterLock_mode(self, ctx:PlSqlParser.Lock_modeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#lock_mode.
    def exitLock_mode(self, ctx:PlSqlParser.Lock_modeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#general_table_ref.
    def enterGeneral_table_ref(self, ctx:PlSqlParser.General_table_refContext):
        pass

    # Exit a parse tree produced by PlSqlParser#general_table_ref.
    def exitGeneral_table_ref(self, ctx:PlSqlParser.General_table_refContext):
        pass


    # Enter a parse tree produced by PlSqlParser#static_returning_clause.
    def enterStatic_returning_clause(self, ctx:PlSqlParser.Static_returning_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#static_returning_clause.
    def exitStatic_returning_clause(self, ctx:PlSqlParser.Static_returning_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#error_logging_clause.
    def enterError_logging_clause(self, ctx:PlSqlParser.Error_logging_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#error_logging_clause.
    def exitError_logging_clause(self, ctx:PlSqlParser.Error_logging_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#error_logging_into_part.
    def enterError_logging_into_part(self, ctx:PlSqlParser.Error_logging_into_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#error_logging_into_part.
    def exitError_logging_into_part(self, ctx:PlSqlParser.Error_logging_into_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#error_logging_reject_part.
    def enterError_logging_reject_part(self, ctx:PlSqlParser.Error_logging_reject_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#error_logging_reject_part.
    def exitError_logging_reject_part(self, ctx:PlSqlParser.Error_logging_reject_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dml_table_expression_clause.
    def enterDml_table_expression_clause(self, ctx:PlSqlParser.Dml_table_expression_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dml_table_expression_clause.
    def exitDml_table_expression_clause(self, ctx:PlSqlParser.Dml_table_expression_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_collection_expression.
    def enterTable_collection_expression(self, ctx:PlSqlParser.Table_collection_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_collection_expression.
    def exitTable_collection_expression(self, ctx:PlSqlParser.Table_collection_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#subquery_restriction_clause.
    def enterSubquery_restriction_clause(self, ctx:PlSqlParser.Subquery_restriction_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#subquery_restriction_clause.
    def exitSubquery_restriction_clause(self, ctx:PlSqlParser.Subquery_restriction_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sample_clause.
    def enterSample_clause(self, ctx:PlSqlParser.Sample_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sample_clause.
    def exitSample_clause(self, ctx:PlSqlParser.Sample_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#seed_part.
    def enterSeed_part(self, ctx:PlSqlParser.Seed_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#seed_part.
    def exitSeed_part(self, ctx:PlSqlParser.Seed_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#condition.
    def enterCondition(self, ctx:PlSqlParser.ConditionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#condition.
    def exitCondition(self, ctx:PlSqlParser.ConditionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#expressions.
    def enterExpressions(self, ctx:PlSqlParser.ExpressionsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#expressions.
    def exitExpressions(self, ctx:PlSqlParser.ExpressionsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#expression.
    def enterExpression(self, ctx:PlSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#expression.
    def exitExpression(self, ctx:PlSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cursor_expression.
    def enterCursor_expression(self, ctx:PlSqlParser.Cursor_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cursor_expression.
    def exitCursor_expression(self, ctx:PlSqlParser.Cursor_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#logical_expression.
    def enterLogical_expression(self, ctx:PlSqlParser.Logical_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#logical_expression.
    def exitLogical_expression(self, ctx:PlSqlParser.Logical_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unary_logical_expression.
    def enterUnary_logical_expression(self, ctx:PlSqlParser.Unary_logical_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unary_logical_expression.
    def exitUnary_logical_expression(self, ctx:PlSqlParser.Unary_logical_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#logical_operation.
    def enterLogical_operation(self, ctx:PlSqlParser.Logical_operationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#logical_operation.
    def exitLogical_operation(self, ctx:PlSqlParser.Logical_operationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#multiset_expression.
    def enterMultiset_expression(self, ctx:PlSqlParser.Multiset_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#multiset_expression.
    def exitMultiset_expression(self, ctx:PlSqlParser.Multiset_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#relational_expression.
    def enterRelational_expression(self, ctx:PlSqlParser.Relational_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#relational_expression.
    def exitRelational_expression(self, ctx:PlSqlParser.Relational_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#compound_expression.
    def enterCompound_expression(self, ctx:PlSqlParser.Compound_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#compound_expression.
    def exitCompound_expression(self, ctx:PlSqlParser.Compound_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#relational_operator.
    def enterRelational_operator(self, ctx:PlSqlParser.Relational_operatorContext):
        pass

    # Exit a parse tree produced by PlSqlParser#relational_operator.
    def exitRelational_operator(self, ctx:PlSqlParser.Relational_operatorContext):
        pass


    # Enter a parse tree produced by PlSqlParser#in_elements.
    def enterIn_elements(self, ctx:PlSqlParser.In_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#in_elements.
    def exitIn_elements(self, ctx:PlSqlParser.In_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#between_elements.
    def enterBetween_elements(self, ctx:PlSqlParser.Between_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#between_elements.
    def exitBetween_elements(self, ctx:PlSqlParser.Between_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#concatenation.
    def enterConcatenation(self, ctx:PlSqlParser.ConcatenationContext):
        pass

    # Exit a parse tree produced by PlSqlParser#concatenation.
    def exitConcatenation(self, ctx:PlSqlParser.ConcatenationContext):
        pass


    # Enter a parse tree produced by PlSqlParser#interval_expression.
    def enterInterval_expression(self, ctx:PlSqlParser.Interval_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#interval_expression.
    def exitInterval_expression(self, ctx:PlSqlParser.Interval_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_expression.
    def enterModel_expression(self, ctx:PlSqlParser.Model_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_expression.
    def exitModel_expression(self, ctx:PlSqlParser.Model_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#model_expression_element.
    def enterModel_expression_element(self, ctx:PlSqlParser.Model_expression_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#model_expression_element.
    def exitModel_expression_element(self, ctx:PlSqlParser.Model_expression_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#single_column_for_loop.
    def enterSingle_column_for_loop(self, ctx:PlSqlParser.Single_column_for_loopContext):
        pass

    # Exit a parse tree produced by PlSqlParser#single_column_for_loop.
    def exitSingle_column_for_loop(self, ctx:PlSqlParser.Single_column_for_loopContext):
        pass


    # Enter a parse tree produced by PlSqlParser#multi_column_for_loop.
    def enterMulti_column_for_loop(self, ctx:PlSqlParser.Multi_column_for_loopContext):
        pass

    # Exit a parse tree produced by PlSqlParser#multi_column_for_loop.
    def exitMulti_column_for_loop(self, ctx:PlSqlParser.Multi_column_for_loopContext):
        pass


    # Enter a parse tree produced by PlSqlParser#unary_expression.
    def enterUnary_expression(self, ctx:PlSqlParser.Unary_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#unary_expression.
    def exitUnary_expression(self, ctx:PlSqlParser.Unary_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#case_statement.
    def enterCase_statement(self, ctx:PlSqlParser.Case_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#case_statement.
    def exitCase_statement(self, ctx:PlSqlParser.Case_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#simple_case_statement.
    def enterSimple_case_statement(self, ctx:PlSqlParser.Simple_case_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#simple_case_statement.
    def exitSimple_case_statement(self, ctx:PlSqlParser.Simple_case_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#simple_case_when_part.
    def enterSimple_case_when_part(self, ctx:PlSqlParser.Simple_case_when_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#simple_case_when_part.
    def exitSimple_case_when_part(self, ctx:PlSqlParser.Simple_case_when_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#searched_case_statement.
    def enterSearched_case_statement(self, ctx:PlSqlParser.Searched_case_statementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#searched_case_statement.
    def exitSearched_case_statement(self, ctx:PlSqlParser.Searched_case_statementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#searched_case_when_part.
    def enterSearched_case_when_part(self, ctx:PlSqlParser.Searched_case_when_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#searched_case_when_part.
    def exitSearched_case_when_part(self, ctx:PlSqlParser.Searched_case_when_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#case_else_part.
    def enterCase_else_part(self, ctx:PlSqlParser.Case_else_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#case_else_part.
    def exitCase_else_part(self, ctx:PlSqlParser.Case_else_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#atom.
    def enterAtom(self, ctx:PlSqlParser.AtomContext):
        pass

    # Exit a parse tree produced by PlSqlParser#atom.
    def exitAtom(self, ctx:PlSqlParser.AtomContext):
        pass


    # Enter a parse tree produced by PlSqlParser#quantified_expression.
    def enterQuantified_expression(self, ctx:PlSqlParser.Quantified_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#quantified_expression.
    def exitQuantified_expression(self, ctx:PlSqlParser.Quantified_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#string_function.
    def enterString_function(self, ctx:PlSqlParser.String_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#string_function.
    def exitString_function(self, ctx:PlSqlParser.String_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#standard_function.
    def enterStandard_function(self, ctx:PlSqlParser.Standard_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#standard_function.
    def exitStandard_function(self, ctx:PlSqlParser.Standard_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#literal.
    def enterLiteral(self, ctx:PlSqlParser.LiteralContext):
        pass

    # Exit a parse tree produced by PlSqlParser#literal.
    def exitLiteral(self, ctx:PlSqlParser.LiteralContext):
        pass


    # Enter a parse tree produced by PlSqlParser#numeric_function_wrapper.
    def enterNumeric_function_wrapper(self, ctx:PlSqlParser.Numeric_function_wrapperContext):
        pass

    # Exit a parse tree produced by PlSqlParser#numeric_function_wrapper.
    def exitNumeric_function_wrapper(self, ctx:PlSqlParser.Numeric_function_wrapperContext):
        pass


    # Enter a parse tree produced by PlSqlParser#numeric_function.
    def enterNumeric_function(self, ctx:PlSqlParser.Numeric_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#numeric_function.
    def exitNumeric_function(self, ctx:PlSqlParser.Numeric_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#other_function.
    def enterOther_function(self, ctx:PlSqlParser.Other_functionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#other_function.
    def exitOther_function(self, ctx:PlSqlParser.Other_functionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#over_clause_keyword.
    def enterOver_clause_keyword(self, ctx:PlSqlParser.Over_clause_keywordContext):
        pass

    # Exit a parse tree produced by PlSqlParser#over_clause_keyword.
    def exitOver_clause_keyword(self, ctx:PlSqlParser.Over_clause_keywordContext):
        pass


    # Enter a parse tree produced by PlSqlParser#within_or_over_clause_keyword.
    def enterWithin_or_over_clause_keyword(self, ctx:PlSqlParser.Within_or_over_clause_keywordContext):
        pass

    # Exit a parse tree produced by PlSqlParser#within_or_over_clause_keyword.
    def exitWithin_or_over_clause_keyword(self, ctx:PlSqlParser.Within_or_over_clause_keywordContext):
        pass


    # Enter a parse tree produced by PlSqlParser#standard_prediction_function_keyword.
    def enterStandard_prediction_function_keyword(self, ctx:PlSqlParser.Standard_prediction_function_keywordContext):
        pass

    # Exit a parse tree produced by PlSqlParser#standard_prediction_function_keyword.
    def exitStandard_prediction_function_keyword(self, ctx:PlSqlParser.Standard_prediction_function_keywordContext):
        pass


    # Enter a parse tree produced by PlSqlParser#over_clause.
    def enterOver_clause(self, ctx:PlSqlParser.Over_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#over_clause.
    def exitOver_clause(self, ctx:PlSqlParser.Over_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#windowing_clause.
    def enterWindowing_clause(self, ctx:PlSqlParser.Windowing_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#windowing_clause.
    def exitWindowing_clause(self, ctx:PlSqlParser.Windowing_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#windowing_type.
    def enterWindowing_type(self, ctx:PlSqlParser.Windowing_typeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#windowing_type.
    def exitWindowing_type(self, ctx:PlSqlParser.Windowing_typeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#windowing_elements.
    def enterWindowing_elements(self, ctx:PlSqlParser.Windowing_elementsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#windowing_elements.
    def exitWindowing_elements(self, ctx:PlSqlParser.Windowing_elementsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#using_clause.
    def enterUsing_clause(self, ctx:PlSqlParser.Using_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#using_clause.
    def exitUsing_clause(self, ctx:PlSqlParser.Using_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#using_element.
    def enterUsing_element(self, ctx:PlSqlParser.Using_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#using_element.
    def exitUsing_element(self, ctx:PlSqlParser.Using_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#collect_order_by_part.
    def enterCollect_order_by_part(self, ctx:PlSqlParser.Collect_order_by_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#collect_order_by_part.
    def exitCollect_order_by_part(self, ctx:PlSqlParser.Collect_order_by_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#within_or_over_part.
    def enterWithin_or_over_part(self, ctx:PlSqlParser.Within_or_over_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#within_or_over_part.
    def exitWithin_or_over_part(self, ctx:PlSqlParser.Within_or_over_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cost_matrix_clause.
    def enterCost_matrix_clause(self, ctx:PlSqlParser.Cost_matrix_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cost_matrix_clause.
    def exitCost_matrix_clause(self, ctx:PlSqlParser.Cost_matrix_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_passing_clause.
    def enterXml_passing_clause(self, ctx:PlSqlParser.Xml_passing_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_passing_clause.
    def exitXml_passing_clause(self, ctx:PlSqlParser.Xml_passing_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_attributes_clause.
    def enterXml_attributes_clause(self, ctx:PlSqlParser.Xml_attributes_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_attributes_clause.
    def exitXml_attributes_clause(self, ctx:PlSqlParser.Xml_attributes_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_namespaces_clause.
    def enterXml_namespaces_clause(self, ctx:PlSqlParser.Xml_namespaces_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_namespaces_clause.
    def exitXml_namespaces_clause(self, ctx:PlSqlParser.Xml_namespaces_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_table_column.
    def enterXml_table_column(self, ctx:PlSqlParser.Xml_table_columnContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_table_column.
    def exitXml_table_column(self, ctx:PlSqlParser.Xml_table_columnContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_general_default_part.
    def enterXml_general_default_part(self, ctx:PlSqlParser.Xml_general_default_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_general_default_part.
    def exitXml_general_default_part(self, ctx:PlSqlParser.Xml_general_default_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_multiuse_expression_element.
    def enterXml_multiuse_expression_element(self, ctx:PlSqlParser.Xml_multiuse_expression_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_multiuse_expression_element.
    def exitXml_multiuse_expression_element(self, ctx:PlSqlParser.Xml_multiuse_expression_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlroot_param_version_part.
    def enterXmlroot_param_version_part(self, ctx:PlSqlParser.Xmlroot_param_version_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlroot_param_version_part.
    def exitXmlroot_param_version_part(self, ctx:PlSqlParser.Xmlroot_param_version_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlroot_param_standalone_part.
    def enterXmlroot_param_standalone_part(self, ctx:PlSqlParser.Xmlroot_param_standalone_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlroot_param_standalone_part.
    def exitXmlroot_param_standalone_part(self, ctx:PlSqlParser.Xmlroot_param_standalone_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlserialize_param_enconding_part.
    def enterXmlserialize_param_enconding_part(self, ctx:PlSqlParser.Xmlserialize_param_enconding_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlserialize_param_enconding_part.
    def exitXmlserialize_param_enconding_part(self, ctx:PlSqlParser.Xmlserialize_param_enconding_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlserialize_param_version_part.
    def enterXmlserialize_param_version_part(self, ctx:PlSqlParser.Xmlserialize_param_version_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlserialize_param_version_part.
    def exitXmlserialize_param_version_part(self, ctx:PlSqlParser.Xmlserialize_param_version_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmlserialize_param_ident_part.
    def enterXmlserialize_param_ident_part(self, ctx:PlSqlParser.Xmlserialize_param_ident_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmlserialize_param_ident_part.
    def exitXmlserialize_param_ident_part(self, ctx:PlSqlParser.Xmlserialize_param_ident_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sql_plus_command.
    def enterSql_plus_command(self, ctx:PlSqlParser.Sql_plus_commandContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sql_plus_command.
    def exitSql_plus_command(self, ctx:PlSqlParser.Sql_plus_commandContext):
        pass


    # Enter a parse tree produced by PlSqlParser#whenever_command.
    def enterWhenever_command(self, ctx:PlSqlParser.Whenever_commandContext):
        pass

    # Exit a parse tree produced by PlSqlParser#whenever_command.
    def exitWhenever_command(self, ctx:PlSqlParser.Whenever_commandContext):
        pass


    # Enter a parse tree produced by PlSqlParser#set_command.
    def enterSet_command(self, ctx:PlSqlParser.Set_commandContext):
        pass

    # Exit a parse tree produced by PlSqlParser#set_command.
    def exitSet_command(self, ctx:PlSqlParser.Set_commandContext):
        pass


    # Enter a parse tree produced by PlSqlParser#partition_extension_clause.
    def enterPartition_extension_clause(self, ctx:PlSqlParser.Partition_extension_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#partition_extension_clause.
    def exitPartition_extension_clause(self, ctx:PlSqlParser.Partition_extension_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_alias.
    def enterColumn_alias(self, ctx:PlSqlParser.Column_aliasContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_alias.
    def exitColumn_alias(self, ctx:PlSqlParser.Column_aliasContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_alias.
    def enterTable_alias(self, ctx:PlSqlParser.Table_aliasContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_alias.
    def exitTable_alias(self, ctx:PlSqlParser.Table_aliasContext):
        pass


    # Enter a parse tree produced by PlSqlParser#where_clause.
    def enterWhere_clause(self, ctx:PlSqlParser.Where_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#where_clause.
    def exitWhere_clause(self, ctx:PlSqlParser.Where_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#into_clause.
    def enterInto_clause(self, ctx:PlSqlParser.Into_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#into_clause.
    def exitInto_clause(self, ctx:PlSqlParser.Into_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xml_column_name.
    def enterXml_column_name(self, ctx:PlSqlParser.Xml_column_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xml_column_name.
    def exitXml_column_name(self, ctx:PlSqlParser.Xml_column_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cost_class_name.
    def enterCost_class_name(self, ctx:PlSqlParser.Cost_class_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cost_class_name.
    def exitCost_class_name(self, ctx:PlSqlParser.Cost_class_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#attribute_name.
    def enterAttribute_name(self, ctx:PlSqlParser.Attribute_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#attribute_name.
    def exitAttribute_name(self, ctx:PlSqlParser.Attribute_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#savepoint_name.
    def enterSavepoint_name(self, ctx:PlSqlParser.Savepoint_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#savepoint_name.
    def exitSavepoint_name(self, ctx:PlSqlParser.Savepoint_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#rollback_segment_name.
    def enterRollback_segment_name(self, ctx:PlSqlParser.Rollback_segment_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#rollback_segment_name.
    def exitRollback_segment_name(self, ctx:PlSqlParser.Rollback_segment_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_var_name.
    def enterTable_var_name(self, ctx:PlSqlParser.Table_var_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_var_name.
    def exitTable_var_name(self, ctx:PlSqlParser.Table_var_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#schema_name.
    def enterSchema_name(self, ctx:PlSqlParser.Schema_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#schema_name.
    def exitSchema_name(self, ctx:PlSqlParser.Schema_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#routine_name.
    def enterRoutine_name(self, ctx:PlSqlParser.Routine_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#routine_name.
    def exitRoutine_name(self, ctx:PlSqlParser.Routine_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#package_name.
    def enterPackage_name(self, ctx:PlSqlParser.Package_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#package_name.
    def exitPackage_name(self, ctx:PlSqlParser.Package_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#implementation_type_name.
    def enterImplementation_type_name(self, ctx:PlSqlParser.Implementation_type_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#implementation_type_name.
    def exitImplementation_type_name(self, ctx:PlSqlParser.Implementation_type_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#parameter_name.
    def enterParameter_name(self, ctx:PlSqlParser.Parameter_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#parameter_name.
    def exitParameter_name(self, ctx:PlSqlParser.Parameter_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#reference_model_name.
    def enterReference_model_name(self, ctx:PlSqlParser.Reference_model_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#reference_model_name.
    def exitReference_model_name(self, ctx:PlSqlParser.Reference_model_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#main_model_name.
    def enterMain_model_name(self, ctx:PlSqlParser.Main_model_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#main_model_name.
    def exitMain_model_name(self, ctx:PlSqlParser.Main_model_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#container_tableview_name.
    def enterContainer_tableview_name(self, ctx:PlSqlParser.Container_tableview_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#container_tableview_name.
    def exitContainer_tableview_name(self, ctx:PlSqlParser.Container_tableview_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#aggregate_function_name.
    def enterAggregate_function_name(self, ctx:PlSqlParser.Aggregate_function_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#aggregate_function_name.
    def exitAggregate_function_name(self, ctx:PlSqlParser.Aggregate_function_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#query_name.
    def enterQuery_name(self, ctx:PlSqlParser.Query_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#query_name.
    def exitQuery_name(self, ctx:PlSqlParser.Query_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#grantee_name.
    def enterGrantee_name(self, ctx:PlSqlParser.Grantee_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#grantee_name.
    def exitGrantee_name(self, ctx:PlSqlParser.Grantee_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#role_name.
    def enterRole_name(self, ctx:PlSqlParser.Role_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#role_name.
    def exitRole_name(self, ctx:PlSqlParser.Role_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constraint_name.
    def enterConstraint_name(self, ctx:PlSqlParser.Constraint_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constraint_name.
    def exitConstraint_name(self, ctx:PlSqlParser.Constraint_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#label_name.
    def enterLabel_name(self, ctx:PlSqlParser.Label_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#label_name.
    def exitLabel_name(self, ctx:PlSqlParser.Label_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_name.
    def enterType_name(self, ctx:PlSqlParser.Type_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_name.
    def exitType_name(self, ctx:PlSqlParser.Type_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#sequence_name.
    def enterSequence_name(self, ctx:PlSqlParser.Sequence_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#sequence_name.
    def exitSequence_name(self, ctx:PlSqlParser.Sequence_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#exception_name.
    def enterException_name(self, ctx:PlSqlParser.Exception_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#exception_name.
    def exitException_name(self, ctx:PlSqlParser.Exception_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_name.
    def enterFunction_name(self, ctx:PlSqlParser.Function_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_name.
    def exitFunction_name(self, ctx:PlSqlParser.Function_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#procedure_name.
    def enterProcedure_name(self, ctx:PlSqlParser.Procedure_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#procedure_name.
    def exitProcedure_name(self, ctx:PlSqlParser.Procedure_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#trigger_name.
    def enterTrigger_name(self, ctx:PlSqlParser.Trigger_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#trigger_name.
    def exitTrigger_name(self, ctx:PlSqlParser.Trigger_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#variable_name.
    def enterVariable_name(self, ctx:PlSqlParser.Variable_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#variable_name.
    def exitVariable_name(self, ctx:PlSqlParser.Variable_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#index_name.
    def enterIndex_name(self, ctx:PlSqlParser.Index_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#index_name.
    def exitIndex_name(self, ctx:PlSqlParser.Index_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#cursor_name.
    def enterCursor_name(self, ctx:PlSqlParser.Cursor_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#cursor_name.
    def exitCursor_name(self, ctx:PlSqlParser.Cursor_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#record_name.
    def enterRecord_name(self, ctx:PlSqlParser.Record_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#record_name.
    def exitRecord_name(self, ctx:PlSqlParser.Record_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#collection_name.
    def enterCollection_name(self, ctx:PlSqlParser.Collection_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#collection_name.
    def exitCollection_name(self, ctx:PlSqlParser.Collection_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#link_name.
    def enterLink_name(self, ctx:PlSqlParser.Link_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#link_name.
    def exitLink_name(self, ctx:PlSqlParser.Link_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_name.
    def enterColumn_name(self, ctx:PlSqlParser.Column_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_name.
    def exitColumn_name(self, ctx:PlSqlParser.Column_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#tableview_name.
    def enterTableview_name(self, ctx:PlSqlParser.Tableview_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#tableview_name.
    def exitTableview_name(self, ctx:PlSqlParser.Tableview_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#xmltable.
    def enterXmltable(self, ctx:PlSqlParser.XmltableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#xmltable.
    def exitXmltable(self, ctx:PlSqlParser.XmltableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#char_set_name.
    def enterChar_set_name(self, ctx:PlSqlParser.Char_set_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#char_set_name.
    def exitChar_set_name(self, ctx:PlSqlParser.Char_set_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#synonym_name.
    def enterSynonym_name(self, ctx:PlSqlParser.Synonym_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#synonym_name.
    def exitSynonym_name(self, ctx:PlSqlParser.Synonym_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#schema_object_name.
    def enterSchema_object_name(self, ctx:PlSqlParser.Schema_object_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#schema_object_name.
    def exitSchema_object_name(self, ctx:PlSqlParser.Schema_object_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#dir_object_name.
    def enterDir_object_name(self, ctx:PlSqlParser.Dir_object_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#dir_object_name.
    def exitDir_object_name(self, ctx:PlSqlParser.Dir_object_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#user_object_name.
    def enterUser_object_name(self, ctx:PlSqlParser.User_object_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#user_object_name.
    def exitUser_object_name(self, ctx:PlSqlParser.User_object_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#grant_object_name.
    def enterGrant_object_name(self, ctx:PlSqlParser.Grant_object_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#grant_object_name.
    def exitGrant_object_name(self, ctx:PlSqlParser.Grant_object_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#column_list.
    def enterColumn_list(self, ctx:PlSqlParser.Column_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#column_list.
    def exitColumn_list(self, ctx:PlSqlParser.Column_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#paren_column_list.
    def enterParen_column_list(self, ctx:PlSqlParser.Paren_column_listContext):
        pass

    # Exit a parse tree produced by PlSqlParser#paren_column_list.
    def exitParen_column_list(self, ctx:PlSqlParser.Paren_column_listContext):
        pass


    # Enter a parse tree produced by PlSqlParser#keep_clause.
    def enterKeep_clause(self, ctx:PlSqlParser.Keep_clauseContext):
        pass

    # Exit a parse tree produced by PlSqlParser#keep_clause.
    def exitKeep_clause(self, ctx:PlSqlParser.Keep_clauseContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_argument.
    def enterFunction_argument(self, ctx:PlSqlParser.Function_argumentContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_argument.
    def exitFunction_argument(self, ctx:PlSqlParser.Function_argumentContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_argument_analytic.
    def enterFunction_argument_analytic(self, ctx:PlSqlParser.Function_argument_analyticContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_argument_analytic.
    def exitFunction_argument_analytic(self, ctx:PlSqlParser.Function_argument_analyticContext):
        pass


    # Enter a parse tree produced by PlSqlParser#function_argument_modeling.
    def enterFunction_argument_modeling(self, ctx:PlSqlParser.Function_argument_modelingContext):
        pass

    # Exit a parse tree produced by PlSqlParser#function_argument_modeling.
    def exitFunction_argument_modeling(self, ctx:PlSqlParser.Function_argument_modelingContext):
        pass


    # Enter a parse tree produced by PlSqlParser#respect_or_ignore_nulls.
    def enterRespect_or_ignore_nulls(self, ctx:PlSqlParser.Respect_or_ignore_nullsContext):
        pass

    # Exit a parse tree produced by PlSqlParser#respect_or_ignore_nulls.
    def exitRespect_or_ignore_nulls(self, ctx:PlSqlParser.Respect_or_ignore_nullsContext):
        pass


    # Enter a parse tree produced by PlSqlParser#argument.
    def enterArgument(self, ctx:PlSqlParser.ArgumentContext):
        pass

    # Exit a parse tree produced by PlSqlParser#argument.
    def exitArgument(self, ctx:PlSqlParser.ArgumentContext):
        pass


    # Enter a parse tree produced by PlSqlParser#type_spec.
    def enterType_spec(self, ctx:PlSqlParser.Type_specContext):
        pass

    # Exit a parse tree produced by PlSqlParser#type_spec.
    def exitType_spec(self, ctx:PlSqlParser.Type_specContext):
        pass


    # Enter a parse tree produced by PlSqlParser#datatype.
    def enterDatatype(self, ctx:PlSqlParser.DatatypeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#datatype.
    def exitDatatype(self, ctx:PlSqlParser.DatatypeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#precision_part.
    def enterPrecision_part(self, ctx:PlSqlParser.Precision_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#precision_part.
    def exitPrecision_part(self, ctx:PlSqlParser.Precision_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#native_datatype_element.
    def enterNative_datatype_element(self, ctx:PlSqlParser.Native_datatype_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#native_datatype_element.
    def exitNative_datatype_element(self, ctx:PlSqlParser.Native_datatype_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#bind_variable.
    def enterBind_variable(self, ctx:PlSqlParser.Bind_variableContext):
        pass

    # Exit a parse tree produced by PlSqlParser#bind_variable.
    def exitBind_variable(self, ctx:PlSqlParser.Bind_variableContext):
        pass


    # Enter a parse tree produced by PlSqlParser#general_element.
    def enterGeneral_element(self, ctx:PlSqlParser.General_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#general_element.
    def exitGeneral_element(self, ctx:PlSqlParser.General_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#general_element_part.
    def enterGeneral_element_part(self, ctx:PlSqlParser.General_element_partContext):
        pass

    # Exit a parse tree produced by PlSqlParser#general_element_part.
    def exitGeneral_element_part(self, ctx:PlSqlParser.General_element_partContext):
        pass


    # Enter a parse tree produced by PlSqlParser#table_element.
    def enterTable_element(self, ctx:PlSqlParser.Table_elementContext):
        pass

    # Exit a parse tree produced by PlSqlParser#table_element.
    def exitTable_element(self, ctx:PlSqlParser.Table_elementContext):
        pass


    # Enter a parse tree produced by PlSqlParser#object_privilege.
    def enterObject_privilege(self, ctx:PlSqlParser.Object_privilegeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#object_privilege.
    def exitObject_privilege(self, ctx:PlSqlParser.Object_privilegeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#system_privilege.
    def enterSystem_privilege(self, ctx:PlSqlParser.System_privilegeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#system_privilege.
    def exitSystem_privilege(self, ctx:PlSqlParser.System_privilegeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#constant.
    def enterConstant(self, ctx:PlSqlParser.ConstantContext):
        pass

    # Exit a parse tree produced by PlSqlParser#constant.
    def exitConstant(self, ctx:PlSqlParser.ConstantContext):
        pass


    # Enter a parse tree produced by PlSqlParser#numeric.
    def enterNumeric(self, ctx:PlSqlParser.NumericContext):
        pass

    # Exit a parse tree produced by PlSqlParser#numeric.
    def exitNumeric(self, ctx:PlSqlParser.NumericContext):
        pass


    # Enter a parse tree produced by PlSqlParser#numeric_negative.
    def enterNumeric_negative(self, ctx:PlSqlParser.Numeric_negativeContext):
        pass

    # Exit a parse tree produced by PlSqlParser#numeric_negative.
    def exitNumeric_negative(self, ctx:PlSqlParser.Numeric_negativeContext):
        pass


    # Enter a parse tree produced by PlSqlParser#quoted_string.
    def enterQuoted_string(self, ctx:PlSqlParser.Quoted_stringContext):
        pass

    # Exit a parse tree produced by PlSqlParser#quoted_string.
    def exitQuoted_string(self, ctx:PlSqlParser.Quoted_stringContext):
        pass


    # Enter a parse tree produced by PlSqlParser#identifier.
    def enterIdentifier(self, ctx:PlSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by PlSqlParser#identifier.
    def exitIdentifier(self, ctx:PlSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by PlSqlParser#id_expression.
    def enterId_expression(self, ctx:PlSqlParser.Id_expressionContext):
        pass

    # Exit a parse tree produced by PlSqlParser#id_expression.
    def exitId_expression(self, ctx:PlSqlParser.Id_expressionContext):
        pass


    # Enter a parse tree produced by PlSqlParser#outer_join_sign.
    def enterOuter_join_sign(self, ctx:PlSqlParser.Outer_join_signContext):
        pass

    # Exit a parse tree produced by PlSqlParser#outer_join_sign.
    def exitOuter_join_sign(self, ctx:PlSqlParser.Outer_join_signContext):
        pass


    # Enter a parse tree produced by PlSqlParser#regular_id.
    def enterRegular_id(self, ctx:PlSqlParser.Regular_idContext):
        pass

    # Exit a parse tree produced by PlSqlParser#regular_id.
    def exitRegular_id(self, ctx:PlSqlParser.Regular_idContext):
        pass


    # Enter a parse tree produced by PlSqlParser#non_reserved_keywords_in_12c.
    def enterNon_reserved_keywords_in_12c(self, ctx:PlSqlParser.Non_reserved_keywords_in_12cContext):
        pass

    # Exit a parse tree produced by PlSqlParser#non_reserved_keywords_in_12c.
    def exitNon_reserved_keywords_in_12c(self, ctx:PlSqlParser.Non_reserved_keywords_in_12cContext):
        pass


    # Enter a parse tree produced by PlSqlParser#non_reserved_keywords_pre12c.
    def enterNon_reserved_keywords_pre12c(self, ctx:PlSqlParser.Non_reserved_keywords_pre12cContext):
        pass

    # Exit a parse tree produced by PlSqlParser#non_reserved_keywords_pre12c.
    def exitNon_reserved_keywords_pre12c(self, ctx:PlSqlParser.Non_reserved_keywords_pre12cContext):
        pass


    # Enter a parse tree produced by PlSqlParser#string_function_name.
    def enterString_function_name(self, ctx:PlSqlParser.String_function_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#string_function_name.
    def exitString_function_name(self, ctx:PlSqlParser.String_function_nameContext):
        pass


    # Enter a parse tree produced by PlSqlParser#numeric_function_name.
    def enterNumeric_function_name(self, ctx:PlSqlParser.Numeric_function_nameContext):
        pass

    # Exit a parse tree produced by PlSqlParser#numeric_function_name.
    def exitNumeric_function_name(self, ctx:PlSqlParser.Numeric_function_nameContext):
        pass



del PlSqlParser
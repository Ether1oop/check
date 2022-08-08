import FunctionDefinition
import SolidityUnit


def emitAdd_AfterTransfer(contract_node):
    function_list = FunctionDefinition.retrieveTransferFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event after transaction")
            print("\tLocation: function " + function_node['name'])


def emitAdd_AfterApprove(contract_node):
    function_list = FunctionDefinition.retrieveApproveFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event after authorizing")
            print("\tLocation: function " + function_node['name'])



def emitAdd_AfterConstruct(contract_node):
    function_list = FunctionDefinition.retrieveConstructorFromContract(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            print("Advice: Please insert event in constructor to record the owner")
            print("\tLocation: function " + function_node['name'])



def emitChangeParameter_Gas(contract_node):
    # Get all global variables
    state_variable_list = SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node)
    state_typeName_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(state_variable_list)

    function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
    for function_node in function_list:
        if not FunctionDefinition.IsContainedEmitStatement(function_node):
            continue
        function_name = function_node['name']
        # Get all temp variable
        temp_variable_list = FunctionDefinition.getVariableDeclarationStatementFromFunctionDefinition(function_node)
        temp_typename_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(temp_variable_list)
        temp_typename_list.extend(FunctionDefinition.getParameterVariableFromFunctionDefinition(function_node))
        # Get all variable in emit
        emit_statement_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
        emit_variableName_list = FunctionDefinition.getAllVariableFromEmitStatementList(emit_statement_list)
        # ����ÿһ����emit�еı����������������ʱ�����У�������ȫ�ֱ����У��ͱ�ʾ��Ҫ�����޸�
        for emit_node in emit_variableName_list:
            for variable in emit_node:
                if variable not in temp_typename_list and variable in state_typeName_list:
                    print("Advice: you can use temporary variables instead of global variables to reduce about 800 gas when emit something")
                    print("\tLocation:  function " + function_name)






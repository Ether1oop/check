import FunctionDefinition


def emitAdd_AfterTransfer(function_node):
    if not FunctionDefinition.IsContainedEmitStatement(function_node):
        print("Advice: Please insert event after transaction")


def emitAdd_AfterApprove(function_node):
    if not FunctionDefinition.IsContainedEmitStatement(function_node):
        print("Advice: Please insert event after authorizing")


def emitAdd_AfterConstruct(function_node):
    if not FunctionDefinition.IsContainedEmitStatement(function_node):
        print("Advice: Please insert event in constructor to record the owner")


def emitChangeParameter_Gas(contract_node):

    state_variable_list = FunctionDefinition.getStateVariableDeclarationFromContractDefinition(contract_node)
    state_name_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(state_variable_list)


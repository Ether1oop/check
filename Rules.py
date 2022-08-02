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
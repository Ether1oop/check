import handleFunctionDefinition


def emitAdd_AfterTransfer(function_node):
    if not handleFunctionDefinition.IsContainedEmitStatement(function_node):
        print("Advice: Please insert event after transaction")



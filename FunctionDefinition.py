import SolidityUnit


def retrieveTransferFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if item['name'].find("transfer") != -1 or item['stateMutability'] == 'payable':
                function_list.append(item)
    return function_list


def IsContainedEmitStatement(function_node):
    result = getEmitStatementFromFunctionDefinition(function_node)
    if len(result) == 0:
        return False
    else:
        return True


def retrieveApproveFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if "approv" in item['name'] or "Approv" in item['name']:
                function_list.append(item)
    return function_list


def retrieveConstructorFromContract(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            if item['name'] == 'constructor':
                function_list.append(item)
    return function_list


def getAllStateVariableDeclarationFromContractDefinition(contract_list):
    state_list = []
    for contract_node in contract_list:
        state_list.append(SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node))
    return state_list


def getNameTypeFromStateVariableDeclaration(state_node):
    name = state_node['variables'][0]['name']
    # typeName = state_node['variables'][0]['typeName']['name']
    # return [name,typeName]
    return name


def getAllNameTypeFromStateVariableDeclaration(state_list):
    nameType = []
    for item in state_list:
        nameType.append(getNameTypeFromStateVariableDeclaration(item))
    return nameType


def getEmitStatementFromFunctionDefinition(function_node):
    nodes = function_node['body']['statements']
    emit_statements = []
    for item in nodes:
        if item['type'] == 'EmitStatement':
            emit_statements.append(item)
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] is not None:
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None:
                nodes.extend(item['FalseBody']['statements'])
    return emit_statements


def getVariablesFromEmitStatement(emit_statement):
    variable_list = emit_statement['eventCall']['arguments']
    result = []
    for item in variable_list:
        if item['type'] == 'Identifier':
            result.append(item['name'])
        # elif item['type'] == 'FunctionCall':

    return result


def getAllVariableFromEmitStatementList(emit_statement_list):
    result = []
    for item in emit_statement_list:
        result.append(getVariablesFromEmitStatement(item))
    return result


def getVariableDeclarationStatementFromFunctionDefinition(function_node):
    nodes = function_node['body']['statements']
    variable_statements = []
    for item in nodes:
        if item['type'] == 'VariableDeclarationStatement':
            variable_statements.append(item)
        elif item['type'] == 'IfStatement':
            if item['TrueBody'] is not None:
                nodes.extend(item['TrueBody']['statements'])
            elif item['FalseBody'] is not None:
                nodes.extend(item['FalseBody']['statements'])
    return variable_statements


def getParameterVariableFromFunctionDefinition(function_node):
    parameters_list = function_node['parameters']['parameters']
    result = []
    for item in parameters_list:
        if item['type'] == 'Parameter':
            result.append(item['name'])
    return result


def retrieveTransferFromContract(contract_list):
    function_list = []
    for contract_node in contract_list:
        for item in contract_node['subNodes']:
            if item['type'] == 'FunctionDefinition':
                if item['name'].find("transfer") != -1 or item['stateMutability'] == 'payable':
                    function_list.append(item)
    return function_list


def IsContainedEmitStatement(function_node):
    statements = function_node['body']['statements']
    for item in statements:
        if item['type'] == "EmitStatement":
            return True
    return False


def retrieveApproveFromContract(contract_list):
    function_list = []
    for contract_node in contract_list:
        for item in contract_node['subNodes']:
            if item['type'] == 'FunctionDefinition':
                if "approv" in item['name'] or "Approv" in item['name']:
                    function_list.append(item)
    return function_list


def retrieveConstructorFromContract(contract_list):
    function_list = []
    for contract_node in contract_list:
        for item in contract_node['subNodes']:
            if item['type'] == 'FunctionDefinition':
                if item['name'] == 'constructor':
                    function_list.append(item)
    return function_list


def getStateVariableDeclarationFromContractDefinition(contract_node):
    state_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'StateVariableDeclaration':
            state_list.append(item)
    return state_list


def getAllStateVariableDeclarationFromContractDefinition(contract_list):
    state_list = []
    for contract_node in contract_list:
        state_list.append(getStateVariableDeclarationFromContractDefinition(contract_node))
    return state_list


def getNameTypeFromStateVariableDeclaration(state_node):
    name = state_node['variables'][0]['name']
    typeName = state_node['variables'][0]['typeName']['name']
    return [name,typeName]


def getAllNameTypeFromStateVariableDeclaration(state_list):
    nameType = []
    for item in state_list:
        nameType.append(getNameTypeFromStateVariableDeclaration(item))
    return nameType


def getAllEmitStatementFromBlock(block):
    nodes = block['statements']
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

# def getAllEmitStatementFromIfStatement(if_statement):




def getAllEmitStatementFromFunctionDefinition(function_node):
    statements = function_node['body']['statements']




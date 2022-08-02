

def getPragmaDirective(source_unit):
    pragma_list = []
    for child in source_unit['children']:
        if child['type'] == "PragmaDirective":
            pragma_list.append(child)
    return pragma_list


def getImportDirective(source_unit):
    import_list = []
    for child in source_unit['children']:
        if child['type'] == 'ImportDirective':
            import_list.append(child)
    return import_list


def getContractDefinition(source_unit):
    contract_list = []
    for child in source_unit['children']:
        if child['type'] == 'ContractDefinition':
            contract_list.append(child)
    return contract_list


def getFunctionDefinitionFromContractDefinition(contract_node):
    function_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'FunctionDefinition':
            function_list.append(item)
    return function_list


def getStateVariableDeclarationFromContractDefinition(contract_node):
    state_list = []
    for item in contract_node['subNodes']:
        if item['type'] == 'StateVariableDeclaration':
            state_list.append(item)
    return state_list


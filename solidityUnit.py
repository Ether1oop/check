

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

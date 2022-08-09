import os

import solidity_parser
import queue


def solidity_parse(path):
    try:
        source_unit = solidity_parser.parse_file(path)
        return source_unit
    except:
        print("parse error!\t" + path)


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


def repairNewPath(absolute_path, path):
    if './' not in path:
        return path

    path_list = path.split("/")
    absolute_path_list = absolute_path.split("/")
    absolute_path_list.pop()
    for i in range(0, len(path_list)):
        item = path_list[i]
        if item == "..":
            absolute_path_list.pop()
        elif item == ".":
            continue
        else:
            break
    result = "/".join(absolute_path_list) + "/" + "/".join(path_list[i:])
    return result


def getAllPathFromImportDirective(absolute_path, import_list):
    relative_path_list = queue.Queue()
    absolute_path_list = []
    for import_node in import_list:
        relative_path_list.put(import_node['path'])

    while relative_path_list.qsize() > 0:
        path_item = repairNewPath(absolute_path, relative_path_list.get())
        absolute_path_list.append(path_item)
        if not os.path.exists(path_item):
            continue
        source_unit = solidity_parse(path_item)
        if source_unit is None:
            continue
        import_list = getImportDirective(source_unit)
        for import_node in import_list:
            relative_path_list.put(import_node['path'])

    return absolute_path_list


def IsContainedERC20OrERC2771Context(path_list):
    for item in path_list:
        if "@openzeppelin" in item:
            if "ERC20.sol" in item or "ERC2771Context.sol" in item or "Context.sol" in item:
                return True

    return False

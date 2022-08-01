def retrieveAllFunctionNameFromContract(contract_list):
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



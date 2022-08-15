import json
import queue

import FunctionDefinition
import Rules
import SolidityUnit
import os
import tkinter.filedialog

# if __name__ == '__main__':
    # absolute_path = tkinter.filedialog.askopenfilename(title="choose file", filetypes=[('solidity files', '.sol')])
    # source_unit = SolidityUnit.solidity_parse(absolute_path)
    # contract_list = SolidityUnit.getContractDefinition(source_unit)
    # Rules.emitChangeParameter_MetaTransaction(absolute_path, source_unit)
    #
    # for contract_node in contract_list:
    #     Rules.emitAdd_AfterTransfer(contract_node)
    #     Rules.emitAdd_AfterApprove(contract_node)
    #     Rules.emitAdd_AfterConstruct(contract_node)
    #     Rules.emitChangeParameter_Gas(contract_node)
    #     Rules.emitChangeParameter_Version(contract_node)
    #     Rules.emitSwapOrder(contract_node)

def getRepositoriesNameList():
    repositories_list = []
    repositories_path = "/home/yantong/Code/SolidityWorm/Repositories"
    file_list = os.listdir(repositories_path)
    file_list.sort(key=lambda x:int(x[:-4]))

    for i in range(50,100):
        file_node = file_list[i]
        with open(repositories_path + "/" + file_node,"r") as file:
            jsonStr = json.loads(file.read())
        repositories_list.append(jsonStr['full_name'].replace("/"," "))

    return repositories_list


def getAllAbsolutePathOfSolidityFiles(repository_path):
    absolute_path_list = []
    for filepath,dirnames,filenames in os.walk(repository_path):
        for file in filenames:
            absolute_path = os.path.join(filepath,file)
            if os.path.splitext(absolute_path)[-1] == '.sol':
                absolute_path_list.append(absolute_path)
    return absolute_path_list


def test_getAllEventDefinitionFromImportDirective(absolute_path, import_list):
    relative_path_list = []
    event_list = []
    for import_node in import_list:
        relative_path_list.append(import_node['path'])

    for i in range(0,len(relative_path_list)):

        path_item = SolidityUnit.repairNewPath(absolute_path, relative_path_list[i])
        if not os.path.exists(path_item):
            continue
        source_unit = SolidityUnit.solidity_parse(path_item)
        if source_unit is None:
            continue
        contract_list = SolidityUnit.getContractDefinition(source_unit)
        for contract_node in contract_list:
            event_list.extend(SolidityUnit.getEventDefinitionFromContractDefinition(contract_node))

        import_list = SolidityUnit.getImportDirective(source_unit)
        for import_node in import_list:
            if import_node not in relative_path_list:
                relative_path_list.append(import_node['path'])

    return event_list


def IsContainedEmitStatement(contract_list):
    for contract_node in contract_list:
        function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
        for function_node in function_list:
            if FunctionDefinition.IsContainedEmitStatement(function_node) :
                return True

    return False


def test_emitSwapOrder(absolute_path_node):
    num = 0
    source_unit = SolidityUnit.solidity_parse(absolute_path_node)

    if source_unit is None:
        return 0

    contract_list = SolidityUnit.getContractDefinition(source_unit)

    if not IsContainedEmitStatement(contract_list):
        return 0

    #取得其import信息，并编译，取得所有event定义
    event_list = test_getAllEventDefinitionFromImportDirective(absolute_path_node,SolidityUnit.getImportDirective(source_unit))

    for contract_node in contract_list:
        event_list.extend(SolidityUnit.getEventDefinitionFromContractDefinition(contract_node))

    event_content_list = SolidityUnit.getAllVariableFromEventDefinition(event_list)

    if len(event_content_list) == 0:
        return 0

    for contract_node in contract_list:
        function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
        for function_node in function_list:
            emit_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
            if len(emit_list) == 0:
                continue

            for emit_node in emit_list:
                emit_name = emit_node['eventCall']['expression']['name']
                parameter = []
                for item in emit_node['eventCall']['arguments']:
                    if item['type'] == 'Identifier':
                        parameter.append(item['name'])
                    elif item['type'] == 'MemberAccess':
                        parameter.append(item['memberName'])
                event = SolidityUnit.getEventDefinitionFromList(emit_name, event_content_list)
                if event is None:
                    continue
                if SolidityUnit.IsOrderError(parameter, event):
                    # print("Advice: The order of variables recorded in emit should be consistent with the event definition")
                    # print("\tLocation: function " + function_node['name'])
                    num += 1
    return num


def _test_emitSwapOrder(absolute_path_node):
    result = set()
    source_unit = SolidityUnit.solidity_parse(absolute_path_node)

    if source_unit is None:
        return 0

    contract_list = SolidityUnit.getContractDefinition(source_unit)

    if not IsContainedEmitStatement(contract_list):
        return 0

    #取得其import信息，并编译，取得所有event定义
    event_list = test_getAllEventDefinitionFromImportDirective(absolute_path_node,SolidityUnit.getImportDirective(source_unit))

    for contract_node in contract_list:
        event_list.extend(SolidityUnit.getEventDefinitionFromContractDefinition(contract_node))

    event_content_list = SolidityUnit.getAllVariableFromEventDefinition(event_list)

    if len(event_content_list) == 0:
        return 0

    for contract_node in contract_list:
        function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
        for function_node in function_list:
            emit_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
            if len(emit_list) == 0:
                continue

            for emit_node in emit_list:
                emit_name = emit_node['eventCall']['expression']['name']
                parameter = []
                for item in emit_node['eventCall']['arguments']:
                    if item['type'] == 'Identifier':
                        parameter.append(item['name'])
                    elif item['type'] == 'MemberAccess':
                        parameter.append(item['memberName'])
                event = SolidityUnit.getEventDefinitionFromList(emit_name, event_content_list)
                if event is None:
                    continue
                if SolidityUnit.IsOrderError(parameter, event):
                    result.add(function_node['name'])
    return list(result)


def test_emitChangeParameter_Gas(absolute_path_node):
    num = 0
    source_unit = SolidityUnit.solidity_parse(absolute_path_node)

    if source_unit is None:
        return 0

    contract_list = SolidityUnit.getContractDefinition(source_unit)

    if not IsContainedEmitStatement(contract_list):
        return 0

    for contract_node in contract_list:
        # Get all global variables
        state_variable_list = SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node)
        state_typeName_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(state_variable_list)
        function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
        for function_node in function_list:
            emit_statement_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
            if len(emit_statement_list) == 0:
                continue
            function_name = function_node['name']
            # Get all temp variable
            temp_variable_list = FunctionDefinition.getVariableDeclarationStatementFromFunctionDefinition(function_node)
            temp_typename_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(temp_variable_list)
            temp_typename_list.extend(FunctionDefinition.getParameterVariableFromFunctionDefinition(function_node))
            # Get all variable in emit
            emit_variableName_list = FunctionDefinition.getAllVariableFromEmitStatementList(emit_statement_list)
            for emit_node in emit_variableName_list:
                for variable in emit_node:
                    if variable not in temp_typename_list and variable in state_typeName_list:
                        # print(
                        #     "Advice: you can use temporary variables instead of global variables to reduce about 800 gas when emit something")
                        # print("\tLocation:  function " + function_name)\
                        num += 1
    return num


def _test_emitChangeParameter_Gas(absolute_path_node):
    result = set()
    source_unit = SolidityUnit.solidity_parse(absolute_path_node)

    if source_unit is None:
        return 0

    contract_list = SolidityUnit.getContractDefinition(source_unit)

    if not IsContainedEmitStatement(contract_list):
        return 0

    for contract_node in contract_list:
        # Get all global variables
        state_variable_list = SolidityUnit.getStateVariableDeclarationFromContractDefinition(contract_node)
        state_typeName_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(state_variable_list)
        function_list = SolidityUnit.getFunctionDefinitionFromContractDefinition(contract_node)
        for function_node in function_list:
            emit_statement_list = FunctionDefinition.getEmitStatementFromFunctionDefinition(function_node)
            if len(emit_statement_list) == 0:
                continue
            function_name = function_node['name']
            # Get all temp variable
            temp_variable_list = FunctionDefinition.getVariableDeclarationStatementFromFunctionDefinition(function_node)
            temp_typename_list = FunctionDefinition.getAllNameTypeFromStateVariableDeclaration(temp_variable_list)
            temp_typename_list.extend(FunctionDefinition.getParameterVariableFromFunctionDefinition(function_node))
            # Get all variable in emit
            emit_variableName_list = FunctionDefinition.getAllVariableFromEmitStatementList(emit_statement_list)
            for emit_node in emit_variableName_list:
                for variable in emit_node:
                    if variable not in temp_typename_list and variable in state_typeName_list:
                        result.add(function_name)
    return list(result)


def operator_1():
    repositories_list = getRepositoriesNameList()

    # test_emitSwapOrder("/home/yantong/Code/check/test/EmitSwapOrder/1.sol")

    for i in range(0,len(repositories_list)):
        repository_name = repositories_list[i]
        repo_path = "/home/yantong/Code/CodeLine/repos/" + repository_name
        if os.path.isdir(repo_path):
            absolute_path_list = getAllAbsolutePathOfSolidityFiles(repo_path)
            for j in range(0,len(absolute_path_list)):
                absolute_path_node = absolute_path_list[j]
                print(str(i) + "\t" + str(j) + "\t" + absolute_path_node)
                result = test_emitSwapOrder(absolute_path_node)
                if result > 0:
                    with open("__result_emitSwapOrder.txt","a") as file:
                        file.write(repository_name + "," + absolute_path_node + "\n")
                result = test_emitChangeParameter_Gas(absolute_path_node)
                if result > 0:
                    with open("__result_emitChangeParameter_Gas.txt","a") as file:
                        file.write(repository_name + "," + absolute_path_node + "\n")


def dealwithAbsolutePath(repoName , absolutePath):
    pathList = absolutePath.split("/")
    path = "https://github.com/" + repoName.replace(" ","/") + "/blob/master/" + "/".join(pathList[7:])

    return path


def operator_2():
    emitSwapOrder_list = []
    emitChangeParameter_Gas = []
    # with open("result_emitSwapOrder.txt","r") as file:
    #     emitSwapOrder_list = file.read().split("\n")[:-1]
    with open("__result_emitChangeParameter_Gas.txt","r") as file:
        emitChangeParameter_Gas = file.read().split("\n")[:-1]

    for item in emitSwapOrder_list:
        absolutePath = item.split(",")[1]
        result = _test_emitSwapOrder(absolutePath)
        for node in result:
            with open("location_emitSwapOrder.txt","a") as file:
                file.write(dealwithAbsolutePath(item.split(",")[0],absolutePath) + "," + node + "\n")

    for item in emitChangeParameter_Gas:
        absolutePath = item.split(",")[1]
        result = _test_emitChangeParameter_Gas(absolutePath)
        for node in result:
            with open("__location_emitChangeParameter_Gas.txt","a") as file:
                file.write(dealwithAbsolutePath(item.split(",")[0],absolutePath) + "," + node + "\n")

if __name__ == '__main__':
    # operator_1()
    operator_2()




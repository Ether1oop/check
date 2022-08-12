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

    for i in range(0,200):
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
    relative_path_list = queue.Queue()
    event_list = []
    for import_node in import_list:
        relative_path_list.put(import_node['path'])

    while relative_path_list.qsize() > 0:
        path_item = SolidityUnit.repairNewPath(absolute_path, relative_path_list.get())
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

            relative_path_list.put(import_node['path'])

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
                if SolidityUnit.calculateSimilarity(parameter, event):
                    print("Advice: The order of variables recorded in emit should be consistent with the event definition")
                    print("\tLocation: function " + function_node['name'])
                    num += 1
    return num


if __name__ == '__main__':
    repositories_list = getRepositoriesNameList()

    # test_emitSwapOrder("/home/yantong/Code/check/test/EmitSwapOrder/1.sol")

    for i in range(1,len(repositories_list)):
        repository_name = repositories_list[i]
        repo_path = "/home/yantong/Code/CodeLine/repos/" + repository_name
        if os.path.isdir(repo_path):
            absolute_path_list = getAllAbsolutePathOfSolidityFiles(repo_path)
            for j in range(1,len(absolute_path_list)):
                absolute_path_node = absolute_path_list[j]
                print(str(i) + "\t" + str(j) + "\t" + absolute_path_node)
                result = test_emitSwapOrder(absolute_path_node)
                if result > 0:
                    with open("result.txt","a") as file:
                        file.write(repository_name + "," + absolute_path_node)



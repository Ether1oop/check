import solidity_parser
import FunctionDefinition
import Rules
import SolidityUnit


def solidity_parse(path):
    try:
        source_unit = solidity_parser.parse_file(path)
        return source_unit
    except:
        print("parse error!")


source_unit = solidity_parse("test/EmitChangeParameter/gas_1.sol")

# functionList = handleFunctionDefinition.retrieveTransferFromContract(solidityUnit.getContractDefinition(source_unit))
# FunctionDefinition.getAllEmitStatementFromFunctionDefinition(source_unit['children'][5]['subNodes'][21])
# a = FunctionDefinition.getAllVariableDeclarationStatementFromFunctionDefinition(source_unit['children'][5]['subNodes'][24])
Rules.emitChangeParameter_Gas(SolidityUnit.getContractDefinition(source_unit)[0])
print("S")

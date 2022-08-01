import solidity_parser
import handleFunctionDefinition
import rules
import solidityUnit


def solidity_parse(path):
    try:
        source_unit = solidity_parser.parse_file(path)
        return source_unit
    except:
        print("parse error!")


source_unit = solidity_parse("test/EmitAdd/1.sol")

functionList = handleFunctionDefinition.retrieveAllFunctionNameFromContract(solidityUnit.getContractDefinition(source_unit))

print("S")

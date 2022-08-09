import os

import solidity_parser
import FunctionDefinition
import Rules
import SolidityUnit
import os

workingPath = os.getcwd()
workingPath = workingPath.replace("\\", "/")
absolute_path = workingPath + "/test/EmitChangeParameter/meta_1.sol"
absolute_path = "D:\Code\check\\test\\teller-protocol-v1-cc56e2954ab13e5217a9333ccf8edf96ecd96236\contracts\lending\\ttoken\strategies\compound/TTokenCompoundStrategy_1.sol"
absolute_path = "D:\Code\\check\\test\\NFT-Worlds-Staking-Rental-Contract-b6310daa5285969abeacfe0f654e3a3a37a35fbd\\src/NFTWEscrow.sol"
absolute_path = absolute_path.replace("\\", "/")
source_unit = SolidityUnit.solidity_parse(absolute_path)

# functionList = handleFunctionDefinition.retrieveTransferFromContract(solidityUnit.getContractDefinition(source_unit))
# FunctionDefinition.getAllEmitStatementFromFunctionDefinition(source_unit['children'][5]['subNodes'][21])
# a = FunctionDefinition.getAllVariableDeclarationStatementFromFunctionDefinition(source_unit['children'][5]['subNodes'][24])
# Rules.emitChangeParameter_Gas(SolidityUnit.getContractDefinition(source_unit)[0])
# Rules.emitChangeParameter_Version(SolidityUnit.getContractDefinition(source_unit)[0])
Rules.emitChangeParameter_MetaTransaction(absolute_path, source_unit)
print("S")

import Rules
import SolidityUnit
import os
import tkinter.filedialog

if __name__ == '__main__':
    absolute_path = tkinter.filedialog.askopenfilename(title="choose file", filetypes=[('solidity files', '.sol')])
    source_unit = SolidityUnit.solidity_parse(absolute_path)
    contract_list = SolidityUnit.getContractDefinition(source_unit)
    Rules.emitChangeParameter_MetaTransaction(absolute_path, source_unit)

    for contract_node in contract_list:
        Rules.emitAdd_AfterTransfer(contract_node)
        Rules.emitAdd_AfterApprove(contract_node)
        Rules.emitAdd_AfterConstruct(contract_node)
        Rules.emitChangeParameter_Gas(contract_node)
        Rules.emitChangeParameter_Version(contract_node)
        Rules.emitSwapOrder(contract_node)

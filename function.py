import solidity_parser


def solidity_parse(path):
    try:
        source_unit = solidity_parser.parse_file(path)
        # source_unit
        children_list = source_unit['children']
        print("S")
    except:
        print("parse error!")


solidity_parse("test/EmitAdd/2.sol")
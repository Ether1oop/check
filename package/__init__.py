import os.path
import sys
import function

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("missing subcommand or path to solidity file")

    # path = sys.argv[1]
    path = "/home/yantong/Code/check/test/EmitChangeParameter/gas_1.sol"
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for item in files:
                absolute_path = os.path.join(root, item)
                if os.path.splitext(absolute_path)[1] == '.sol':
                    function.scan(absolute_path)
    elif os.path.isfile(path):
        function.scan(path)
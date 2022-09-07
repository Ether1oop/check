# Problematic Event Logging Parameter Checker for Gas Saving
To show the feasibility of automatic event logging assistance from our findings, we design a simple problematic event logging parameter checker which helps identify gas saving opportunities. 

The checker is motivated by the non-neglectable number of parameter changes that replace Storage type variable with Memory type variable.

It supported by [python-solidity-parser](https://github.com/ConsenSys/python-solidity-parser)

## install

Download the package from `/dist`.

##### whl
```
#> pip install gas_reducer-0.0.1-py3-none-any.whl
```
or
```
#> pip3 install gas_reducer-0.0.1-py3-none-any.whl
```

##### tar.gz
```
#> tar -xzvf gas_reducer-0.0.1.tar.gz
#> cd gas_reducer-0.0.1
#> python3 setup.py install
```

## How To
```
#> python3 -m gas_reducer <path_to_contract.sol>
```
or
```
#> python3 -m gas_reducer <path_to_your_project>
```
the output will be:
```
Advice: Use Memory Type Variable Instead of Storage Type Variable in Event to Save Gas
Location:
	 filename: [which file needed to fix]
	 function name: [The function where the problematic event is located]
	 event name: [which event you can improve]
	 variable name: [the name of problematic event logging parameter]
...
```



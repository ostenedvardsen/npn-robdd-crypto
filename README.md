# npn-robdd-crypto
This codebase utilizes CUDD and SageMath to find the lowest possible ROBDD size across variable orderings of n-variable NPN classes, paired with the basic cryptographic properties, nonlinearity, algebraic degree and balancedness. 

## Input
The NPN classes must be supplied in a CSV file with the columns:
- `num`: that identifies the row
- `hex_func`: hexadecimal representation of the truth table of the NPN representative

## Requirements
- SageMath
- Python 3.x
- CUDD via the `dd` library

## How to run
Place `npn_robdd.py`, `npn_crypto_properties.py`, and `combine_csv.py` in the same folder as `npn_N_args.csv`. The file of NPN classes must be called `npn_N_args.csv`, where the N is replaced with the dimension of the classes. Open a terminal and navigate to that folder. 

Run: 
1. `python npn_robdd.py`. When prompted with "Please input the n of your function.", input the value of N.
2. `sage npn_crypto_properties.py`. When prompted with "Please input the n of your function.", input the value of N. 
3. `python combine_csv.py`. When prompted with "Please input the n of your function.", input the value of N. 

The final results are now found in `npn_merged_N.csv`, where the N is replaced with the dimension of the classes.

The published data is intended for general observations. If observations on specific functions are needed, then the code must be run on a supplied NPN class dataset. 

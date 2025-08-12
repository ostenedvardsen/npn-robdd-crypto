from collections import Counter, deque
import gc
gc.enable
import math
import csv
from itertools import permutations
from dd.cudd import BDD
import pandas as pd


def truthtable(functionOutputDecimal, N):
    output_size = pow(2,N)
    
    functionOutputBinary = bin(functionOutputDecimal)[2:].zfill(output_size)
    functionOutputBinary = functionOutputBinary[::-1]

    functionTruthTable = []

    for i in range(output_size):
        if(functionOutputBinary[i] == '1'):
            variableValues = bin(i)[2:].zfill(N)
            variableValues = variableValues[::-1]
            inputRow = {}

            for j in range(N):
                variableName = 'x' + str(j)
 
                if(variableValues[j] == '1'):
                    
                    inputRow[variableName] = True
                else: 
                    inputRow[variableName] = False

            functionTruthTable.append(inputRow)

    return functionTruthTable

def is_complement(p):
    return p.negated

def not_complement(p):
    return ~p if p.negated else p

def complement(p):
    return ~p

def list_to_dict(c):
    return {var: level for level, var in enumerate(c)}

def size_without_complements(root):
    stack = [root]
    seen  = set()

    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)

        n = not_complement(p)
        if n.var is None:
            continue

        if is_complement(p):
            stack.append(complement(n.low))
            stack.append(complement(n.high))
        else:
            stack.append(n.low)
            stack.append(n.high)

    return len(seen)


def main():
    print("Please input the n of your function.")
    N = int(input())

    filenameN = "npn_" + str(N) + "_args.csv"

    df = pd.read_csv(
        filenameN,
        skiprows = range(1,1),
        converters={
            'hex_func': str,
        }
    )
    print(df)

    perm = []
    for i in range (N):
        perm.append('x' + str(i))
    perm_list = list(permutations(perm))

    data = [['num',
             'hex_func',
            'smallest_robdd_size',
            'robdd_size_distribution'
            ]]

    for row in df.itertuples():
        num = row.num
        print("Current function: " + str(num))

        f_output_hex = str(row.hex_func)
        f_output_dec = int(f_output_hex, 16)
        f_tt = truthtable(f_output_dec, N)

        size = math.inf
        size_distribution_count = Counter()

        bdd_manager = BDD()
        bdd_manager.configure(reordering=False)
        bdd_manager.declare(*perm_list[0])
        
        f = bdd_manager.false
        for row in f_tt: 
            f |= bdd_manager.cube(row)

        for i in range (math.factorial(N)):            
            if(i != 0):
                BDD.reorder(bdd_manager, list_to_dict(perm_list[i])) 

            if(size_without_complements(f) < size):
                size = size_without_complements(f)
            
            
            size_distribution_count[size_without_complements(f)] += 1

        size_distribution_list = size_distribution_count.items()
        size_distribution_list = sorted(size_distribution_list)


        data.append([
            num, 
            f_output_hex, 
            size, 
            size_distribution_list
        ])

    filenameX = 'npn_robdd_results_n' + N + '.csv'

    with open(filenameX, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


print(main())
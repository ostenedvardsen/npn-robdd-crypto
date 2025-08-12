from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
import pandas as pd
import csv
from multiprocessing import get_context

import gc
gc.enable()

def compute_properties(args):
    (n,
     num,
     functionOutputHex
     ) = args

    f = BooleanFunction(functionOutputHex)

    algebraic_degree = f.algebraic_degree()
    is_balanced = f.is_balanced()
    nonlinearity = f.nonlinearity()
    correlation_immunity = f.correlation_immunity()
    resiliency_order = f.resiliency_order()
    algebraic_immunity = f.algebraic_immunity()

    bent = 0
    semi_bent = 0

    if(f.is_bent()):
        bent = 1

    else: 
        if(n % 2 == 1):
            amplitude = 2 ** ( (n + 1) / 2)
        else:
            amplitude = 2 ** ( (n + 2) / 2)    

        if(f.is_plateaued()):
            wht = f.walsh_hadamard_transform()
            nonzero = False
            not_bent = False

            for i in wht:
                if(i == 0):
                    continue

                if(abs(i) != amplitude):
                    not_bent = True
                    break
                
                nonzero = True
            
            if(not_bent == False and nonzero == True):
                semi_bent = 1


    del f
    gc.collect()

    return [
        num,
        functionOutputHex,
        algebraic_degree,
        is_balanced,
        nonlinearity,
        correlation_immunity,
        resiliency_order,
        algebraic_immunity,
        bent,
        semi_bent
        ]


if __name__ == "__main__":
    print("Please input the n of your function.")
    N = int(input())

    filenameN = "npn_robdd_results_n" + str(N) + ".csv"

    df = pd.read_csv(
        filenameN,
        skiprows = range(1,1),
        dtype={'hex_func': str}
    )
    print(df)

    tasks = []
    for row in df.itertuples():
        tasks.append((
            N,
            row.num,
            row.hex_func,
            ))
    print("Number of tasks: ", len(tasks))

    results = []
    for i in range(0, len(tasks), 200):
        chunk = tasks[i:i + 200]

        ctx = get_context("spawn")
        with ctx.Pool(
            processes=8,
            maxtasksperchild=200
        ) as pool:
            results.extend(pool.map(compute_properties, chunk))
            print("Processed chunk: ", i, " to ", i + len(chunk))

    data = [['num', 'hex_func', 'algebraic_degree', 'is_balanced', 'nonlinearity', 'correlation_immunity', 'resiliency_order', 'algebraic_immunity', 'bent', 'semi_bent']]

    for result in results:
        data.append(result)

    filenameX = 'npn_robdd_crypto_results_n' + str(N) + '.csv'
    with open(filenameX, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


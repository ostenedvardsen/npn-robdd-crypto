
import pandas as pd

def main(): 
    print("Please input the n of your function.")
    N = int(input())

    filename1 = "npn_robdd_results_n" + str(N) + ".csv"
    filename2 = 'npn_robdd_crypto_results_n' + str(N) + ".csv"   

    df1 = pd.read_csv(filename1, dtype={'hex_func': str})
    df2 = pd.read_csv(filename2, dtype={'hex_func': str})

    merged = pd.merge(df1, df2, on=['num', 'hex_func'], how='inner')
    
    print(merged.head())
    filename3 = 'npn_merged_' + str(N) + '.csv'
    merged.to_csv(filename3, index=False)

main()

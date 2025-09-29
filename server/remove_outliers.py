import pandas as pd

def remove_outliers(df, column, lower_quantile=0.05, upper_quantile=0.95):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df_filtered = df[(df[column] >= lower) & (df[column] <= upper)]
    
    print(f"Original: {len(df)} rows, Now: {len(df_filtered)} rows")
    print(f"Dropped {len(df) - len(df_filtered)} outliers from '{column}'")

    return df_filtered
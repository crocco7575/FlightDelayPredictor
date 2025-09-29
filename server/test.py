import pandas as pd

df = pd.read_csv("january22->april25.csv")

max = df['Arrival Delay'].max()
min = df['Arrival Delay'].min()
print(f'max:{max} min: {min}')
print(df.columns.tolist())
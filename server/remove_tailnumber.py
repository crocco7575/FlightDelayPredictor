import pandas as pd

# Load the dataset
df = pd.read_csv("january22->april25.csv")

# Drop the TailNumber column
df = df.drop(columns=["Tail Number"], errors='ignore')  # 'ignore' prevents error if it's not there

# Save to a new file (or overwrite the old one)
df.to_csv("january22->april25.csv", index=False)

print("TailNumber column removed and file saved.")
import pandas as pd

# List of months to process
dfs = ['january22', 'february22', 'march22', 'april22', 'may22', 'june22', 
       'july22', 'august22', 'september22', 'october22', 'november22', 'december22',
       'january23', 'february23', 'march23', 'april23', 'may23', 'june23', 
       'july23', 'august23', 'september23', 'october23', 'november23', 'december23',
       'january24', 'february24', 'march24', 'april24', 'may24', 'june24', 
       'july24', 'august24', 'september24', 'october24', 'november24', 'december24', 
       'january25', 'february25', 'march25', 'april25']

for month in dfs:
    # Load CSV
    df = pd.read_csv(f'./data/{month}.csv')

    # Drop unnecessary columns
    drop_cols = [
        'Mkt Carrier Code', 'Wheels Off', 'Wheels On',
        'Origin Weather Datetime', 'Destination Weather Datetime',
        'Origin_condition', 'Destination_condition'
    ]
    df = df.drop(columns=drop_cols)

    # Encode categorical columns
    for col in ['Origin', 'Destination', 'Carrier Code']:
        df[col] = df[col].astype('category').cat.codes

    # Convert date to datetime and then extract month
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df['Month'] = df['Date'].dt.month  # Add month as a new feature
    df['Date'] = df['Date'].astype(int) // 10**9  # Convert to Unix timestamp

    # Fill missing values
    df = df.dropna()

    # Save to cleaned file
    df.to_csv(f'./data/{month}_cleaned.csv', index=False)

print("Preprocessing complete. Cleaned data saved to data folder.")

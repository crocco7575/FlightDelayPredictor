import pandas as pd
df = pd.read_csv("january22->april25")
# Convert Date (unix seconds) to datetime
df['Date'] = pd.to_datetime(df['Date'], unit='s')

# Split into components
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
df['DayOfWeek'] = df['Date'].dt.dayofweek   # 0=Mon, 6=Sun
df['IsWeekend'] = df['DayOfWeek'].isin([5,6]).astype(int)
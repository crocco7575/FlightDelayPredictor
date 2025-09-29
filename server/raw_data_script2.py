import pandas as pd
from remove_outliers import remove_outliers
import holidays


# Load all CSV files
df1 = pd.read_csv('./data/december24_cleaned.csv')
df2 = pd.read_csv('./data/january25_cleaned.csv')
df4 = pd.read_csv('./data/february25_cleaned.csv')
df3 = pd.read_csv('./data/march25_cleaned.csv')
df5 = pd.read_csv('./data/april25_cleaned.csv')
df6 = pd.read_csv('./data/may24_cleaned.csv')
df7 = pd.read_csv('./data/june24_cleaned.csv')
df8 = pd.read_csv('./data/july24_cleaned.csv')
df9 = pd.read_csv('./data/august24_cleaned.csv')
df10 = pd.read_csv('./data/september24_cleaned.csv')
df11 = pd.read_csv('./data/october24_cleaned.csv')
df12 = pd.read_csv('./data/november24_cleaned.csv')


df13 = pd.read_csv('./data/january23_cleaned.csv')
df14 = pd.read_csv('./data/february23_cleaned.csv')
df15 = pd.read_csv('./data/march23_cleaned.csv')
df16 = pd.read_csv('./data/april23_cleaned.csv')
df17 = pd.read_csv('./data/may23_cleaned.csv')
df18 = pd.read_csv('./data/june23_cleaned.csv')
df19 = pd.read_csv('./data/july23_cleaned.csv')
df20 = pd.read_csv('./data/august23_cleaned.csv')
df21 = pd.read_csv('./data/september23_cleaned.csv')
df22 = pd.read_csv('./data/october23_cleaned.csv')
df23 = pd.read_csv('./data/november23_cleaned.csv')
df24 = pd.read_csv('./data/december23_cleaned.csv')
df25 = pd.read_csv('./data/january24_cleaned.csv')
df26 = pd.read_csv('./data/february24_cleaned.csv')
df27 = pd.read_csv('./data/march24_cleaned.csv')
df28 = pd.read_csv('./data/april24_cleaned.csv')

df29 = pd.read_csv('./data/january22_cleaned.csv')
df30 = pd.read_csv('./data/february22_cleaned.csv')
df31 = pd.read_csv('./data/march22_cleaned.csv')
df32 = pd.read_csv('./data/april22_cleaned.csv')
df33 = pd.read_csv('./data/may22_cleaned.csv')
df34 = pd.read_csv('./data/june22_cleaned.csv')
df35 = pd.read_csv('./data/july22_cleaned.csv')
df36 = pd.read_csv('./data/august22_cleaned.csv')
df37 = pd.read_csv('./data/september22_cleaned.csv')
df38 = pd.read_csv('./data/october22_cleaned.csv')
df39 = pd.read_csv('./data/november22_cleaned.csv')
df40 = pd.read_csv('./data/december22_cleaned.csv')

#######################################

# Concatenate dataset and drop columns that wont work

#######################################
all_dfs = [df5, df6, df7, df8, df9, df10, df11, df12, df1, df2, 
           df3, df4, df13, df14, df15, df16, df17, df18, df19, 
           df20, df21, df22, df23, df24, df25, df26, df27, df28,
           df29, df30, df31, df32, df33, df34, df35, df36, df37, df38,
           df39, df40]
# Concatenate them
# for num in range(len(all_dfs)):
#     all_dfs[num] = remove_outliers(all_dfs[num], "Arrival Delay")

combined_df = pd.DataFrame()
for df in all_dfs:
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Optionally, drop duplicates
combined_df = combined_df.drop_duplicates()
combined_df = remove_outliers(combined_df, "Arrival Delay")
# Save to a new file


# Load the raw dataset


# List of columns to drop (not useful for arrival delay prediction)
columns_to_drop = [
    'Flight Delay',            # Redundant with Arrival Delay
    'Departure Delay',         # Too correlated with target
    'Actual Arrival',
    'Scheduled Departure',
    'Actual Flight Time',     # Highly correlated with actual departure
    'Actual Departure',
    'Flight Number',           # Might be too high-cardinality
    'Taxi Out',
    'Taxi In',
    'Air Time',
    'Carrier Delay',
    'Weather Delay',
    'NAS Delay',
    'Security Delay',
    'Late Aircraft Delay',
 ]

# Drop the columns
combined_df_cleaned = combined_df.drop(columns=columns_to_drop)


combined_df_cleaned= combined_df_cleaned.dropna()

##############################################

# FEATURE ENGINEERING SECTION BELOW 🧪

#############################################

############## ROUTE AVERAGE DELAY
# Calculate average delay for each route
route_avg_delay = combined_df_cleaned.groupby(['Origin', 'Destination'])['Arrival Delay'].mean().reset_index()
route_avg_delay.rename(columns={'Arrival Delay': 'Route_Avg_Delay'}, inplace=True)

# Merge it back into the original DataFrame
combined_df_cleaned = pd.merge(combined_df_cleaned, route_avg_delay, on=['Origin', 'Destination'], how='left')


############ CARRIER-ROUTE AVERAGE DELAY
# Calculate carrier average delay for each route
route_carrier_delay = combined_df_cleaned.groupby(['Carrier Code', 'Origin', 'Destination'])['Arrival Delay'].mean().reset_index()
route_carrier_delay.rename(columns={'Arrival Delay': 'Carrier_Route_Avg_Delay'}, inplace=True)
combined_df_cleaned = pd.merge(combined_df_cleaned, route_carrier_delay, on=['Carrier Code', 'Origin', 'Destination'], how='left')


############ HOLIDAYS
us_holidays = holidays.US()

# Convert timestamp to date if not already
combined_df_cleaned['Flight_Date'] = pd.to_datetime(combined_df_cleaned['Date'], unit='s')  # or use format='%Y%m%d' if needed
combined_df_cleaned['IsHoliday'] = combined_df_cleaned['Flight_Date'].isin(us_holidays).astype(int)
combined_df_cleaned.drop(columns=['Flight_Date'], inplace=True)

########### ROUTE BUSYNESS
route_counts = combined_df_cleaned.groupby(['Origin', 'Destination']).size().reset_index(name='Route_Busyness')
combined_df_cleaned = combined_df_cleaned.merge(route_counts, on=['Origin', 'Destination'], how='left')

########### PREV TAIL-NUMBER DELAY
# Sort the dataset by TailNumber and Date (timestamped)
combined_df_cleaned = combined_df_cleaned.sort_values(by=['Tail Number', 'Date'])

# Create the feature: previous arrival delay for this aircraft
combined_df_cleaned['PrevTailDelay'] = combined_df_cleaned.groupby('Tail Number')['Arrival Delay'].shift(1)

# Optional: fill NaNs (i.e., first flight for that tail number)
combined_df_cleaned['PrevTailDelay'] = combined_df_cleaned['PrevTailDelay'].fillna(0)


##############################

# SAVE DATASET ✅

#############################
# Save cleaned dataset
combined_df_cleaned.to_csv("january22->april25.csv", index=False)

print("✅ Cleaned dataset saved")

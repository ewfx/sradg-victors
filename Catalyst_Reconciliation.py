import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('catalyst_monthly.csv')
df2 = pd.read_csv('catalyst_history.csv')

# Drop the 'ReconDate' column from both dataframes for the reconciliation process
df1_without_recondate = df1.drop(columns=['ReconDate'])
df2_without_recondate = df2.drop(columns=['ReconDate'])

# Perform an outer join to get all rows from both DataFrames and include an indicator column
all_rows = pd.merge(df1_without_recondate, df2_without_recondate, how='outer', indicator=True)

# Create a new column 'Anamoly' to track whether rows match or not
all_rows['Anamoly'] = all_rows['_merge'].apply(lambda x: 'Yes' if x == 'both' else 'No')

# Merge 'MatchStatus' with df1 based on the columns that are common (excluding 'ReconDate')
# We use an inner join and merge based on all the other columns except 'ReconDate'
df1_with_status = pd.merge(df1, all_rows[['Anamoly'] + df1_without_recondate.columns.tolist()],
                           how='left', left_on=df1_without_recondate.columns.tolist(), 
                           right_on=df2_without_recondate.columns.tolist())

# Optionally, save the results to a new CSV file
df1_with_status.to_csv('Catalyst Reconcilation.csv', index=False)

print("Reconciliation completed with match status.")

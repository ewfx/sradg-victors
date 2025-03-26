import pandas as pd

# Load the two CSV files into pandas DataFrames
file1 = 'IHub_Current_Data.csv'
file2 = 'IHub_History_Data.csv'

try:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    print("Files loaded successfully")
except Exception as e:
    print(f"Error loading files: {e}")

# Check the columns of both dataframes
print("Columns in file1:", df1.columns)
print("Columns in file2:", df2.columns)

# Ensure that the key columns exist in both DataFrames
required_columns = ['Account', 'SecondaryAccount', 'PrimaryAccount']
missing_columns_1 = [col for col in required_columns if col not in df1.columns]
missing_columns_2 = [col for col in required_columns if col not in df2.columns]

if missing_columns_1 or missing_columns_2:
    print(f"Missing columns in file1: {missing_columns_1}")
    print(f"Missing columns in file2: {missing_columns_2}")
else:
    print("Both files contain the required columns.")

# Ensure 'AsOfDate' is in the columns
if 'AsOfDate' not in df2.columns:
    print("Error: 'AsOfDate' column is missing in file2.")
else:
    df2['AsOfDate'] = pd.to_datetime(df2['AsOfDate'])  # Convert to datetime

    # Sort df2 by AsOfDate (descending order) and drop duplicates
    df2_sorted = df2.sort_values('AsOfDate', ascending=False).drop_duplicates(subset=required_columns, keep='first')

    # Merge the DataFrames on the key columns: 'Account', 'SecondaryAccount', 'PrimaryAccount'
    try:
        merged_df = pd.merge(df1, df2_sorted, on=required_columns, how='inner', suffixes=('_file1', '_file2'))
        print("Merge successful")
    except Exception as e:
        print(f"Error during merge: {e}")

    # Check the columns in the merged DataFrame
    print("Columns in merged DataFrame:", merged_df.columns)

    # Proceed with balance difference and comment generation...
    if 'BalanceDifference_file1' in merged_df.columns and 'BalanceDifference_file2' in merged_df.columns:
        merged_df['balancedifference'] = merged_df['BalanceDifference_file1'] - merged_df['BalanceDifference_file2']
    else:
        print("Error: 'balancedifference' columns not found in the merged DataFrame.")
        print(merged_df.head())

    # Function to categorize based on balance difference
    def generate_comment(balance_diff):
        # Handling small differences, both positive and negative
        if -0.10 < balance_diff < 0.10:
            return 'Consider a Match as difference is Negligible'

        # For minor differences, positive values
        elif 0.10 <= abs(balance_diff) < 1000:
            return 'Very Minor Difference'

        # For moderate differences, positive values
        elif 1000 <= abs(balance_diff) < 10000:
            return 'Consistently Match'

        # For larger differences, positive values
        elif 10000 <= abs(balance_diff) < 100000:
            return "Consistent increase or decrease in outstanding balance"

        # For very large differences, positive values
        elif abs(balance_diff) >= 100000:
            return 'Huge spike in outstanding balances'

        # Handling minor negative differences
        elif -0.10 >= balance_diff > -1000:
            return "Very Minor Difference Inconsistently"

        # For negative moderate differences
        elif -1000 >= balance_diff > -10000:
            return "Inconsistently there is a Difference in outstanding balance"

        # For large negative differences
        elif balance_diff <= -10000:
            return "Inconsistently there is a huge Difference in outstanding balance"

        # Default match case
        else:
            return 'Match'

    try:
        merged_df['comments'] = merged_df['balancedifference'].apply(generate_comment)
        print("Comments generated successfully")
    except Exception as e:
        print(f"Error generating comments: {e}")

    # Function to determine anomaly
    def check_anomaly(group):
        # Check if the BalanceDifference is consistently increasing or decreasing
        diff_changes = group['balancedifference'].diff().dropna()
        if len(diff_changes) > 0 and diff_changes.min() > 0:
            return 'Yes'  # Consistently increasing
        elif len(diff_changes) > 0 and diff_changes.max() < 0:
            return 'Yes'  # Consistently decreasing
        else:
            return 'No'  # Not consistent

    # Apply the anomaly check function group-wise
    # We need to reset the index after applying the function to ensure proper assignment of the 'Anomaly' column
    merged_df['Anomaly'] = merged_df.groupby(['Account', 'SecondaryAccount', 'PrimaryAccount']).apply(
        lambda group: check_anomaly(group)
    ).reset_index(level=[0, 1, 2], drop=True)

    # Create a list of the specific columns to keep from merged_df (including the 'comments' and 'Anomaly' columns)
    columns_to_keep = [
        'AsOfDate_file1', 'Company_file1', 'Account', 'AU_file1',
        'Currency_file1', 'PrimaryAccount', 'SecondaryAccount',
        'GLBalance_file1', 'iHUbBalance_file1', 'BalanceDifference_file1',
        'MatchStatus_file1', 'comments', 'Anomaly'
    ]  # List of columns you need

    # Select the required columns from merged_df
    output_df = merged_df[columns_to_keep]

    # Save the output to a new CSV file
    try:
        output_df.to_csv('IHub_Reconciliation.csv', index=False)
        print("Reconciliation file with comments and anomalies saved successfully.")
    except Exception as e:
        print(f"Error saving the file: {e}")

    # Optionally, print the first few rows of the resulting DataFrame
    print(output_df.head())

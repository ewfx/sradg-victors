import pandas as pd

# Load the two CSV files into pandas DataFrames
file1 = 'random_data_current_month_test1.csv'
file2 = 'random_data_history_test1.csv'

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

# Debug: Check if 'AsOfDate_file2' exists in file2
print(f"Columns in file2: {df2.columns}")

# Ensure 'AsOfDate_file2' is in the columns
if 'AsOfDate' not in df2.columns:
    print("Error: 'AsOfDate' column is missing in file2.")
else:
    # Proceed with further processing
    df2['AsOfDate'] = pd.to_datetime(df2['AsOfDate'])  # Convert to datetime

    # Sort df2 by AsOfDate_file2 (descending order) and drop duplicates
    df2_sorted = df2.sort_values('AsOfDate', ascending=False).drop_duplicates(subset=required_columns, keep='first')

    # Check after sorting and dropping duplicates
    print("Columns in sorted file2:", df2_sorted.columns)

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
        if 0 < abs(balance_diff) < 0.10:
            return 'Consider a Match as difference is Negligible'
        elif 0.11 <= abs(balance_diff) < 1000:
            return 'Very Minor Difference'
        elif 1000 <= abs(balance_diff) < 10000:
            return 'Consistently Match'
        elif 10000 <= abs(balance_diff) < 100000:
            return "Consistent increase or decrease in outstanding balance"
        elif abs(balance_diff) >= 100000:
            return 'Consistent increase in outstanding balances'
        elif -0.10 < balance_diff <= 0:
            return "Very Minor Difference Inconsistently"
        elif -1000 <= balance_diff < -10000:
            return "Inconsistently there is a Difference in outstanding balance"
        elif -10000 >= balance_diff:
            return "Inconsistently there is a huge Difference in outstanding balance"
        else:
            return 'Match'

    try:
        merged_df['comments'] = merged_df['balancedifference'].apply(generate_comment)
        print("Comments generated successfully")
    except Exception as e:
        print(f"Error generating comments: {e}")

    # Create a list of the specific columns to keep from merged_df (including the 'comments' column)
    columns_to_keep = [
        'AsOfDate_file1', 'Company_file1', 'Account', 'AU_file1',
        'Currency_file1', 'PrimaryAccount', 'SecondaryAccount',
        'GLBalance_file1', 'iHUbBalance_file1', 'BalanceDifference_file1',
        'MatchStatus_file1', 'comments'
    ]  # List of columns you need

    # Select the required columns from merged_df
    output_df = merged_df[columns_to_keep]

    # Save the output to a new CSV file
    try:
        output_df.to_csv('reconciled_with_comments_test1.csv', index=False)
        print("Reconciliation file with comments saved successfully.")
    except Exception as e:
        print(f"Error saving the file: {e}")

    # Optionally, print the first few rows of the resulting DataFrame
    print(output_df.head())

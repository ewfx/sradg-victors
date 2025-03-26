#Generate History File
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate random dates
def generate_random_dates(start_date, end_date, n):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    diff = end - start
    return [start + timedelta(days=np.random.randint(0, diff.days)) for _ in range(n)]

# Create random data
num_rows = 100000
# Generate a list of numbers with leading zeros (e.g., 00001, 00002, etc.)
numbers_with_leading_zeros = [f"{i:05}" for i in range(1, 7)]  # Pool of numbers with leading zeros (1 to 6)
# Use random.choices() to sample numbers with replacement
repeated_numbers = random.choices(numbers_with_leading_zeros, k=num_rows)

data = {
    'AsOfDate': generate_random_dates('2020-01-01', '2025-02-28', num_rows), # Random dates in 2023
    'Company': repeated_numbers,
    'Account': np.random.randint(1111111, 9999999, num_rows),
    'AU': np.random.randint(1000, 7000, num_rows),   
    'Currency': np.random.choice(['USD', 'EUR', 'INR', 'AFN', 'ALL','ISO-4217'], num_rows),
    'PrimaryAccount':  np.random.choice(['Deferred Costs','Principal'], num_rows),
    'SecondaryAccount': np.random.choice(['Deferred Costs','Principal'], num_rows),
    'GLBalance': np.random.randint(30000, 120000, num_rows),
    'iHUbBalance': np.random.randint(30000, 120000, num_rows)
}

# Create a DataFrame
df = pd.DataFrame(data)

#Calclulate difference
df['BalanceDifference'] = df['GLBalance'] - df['iHUbBalance']

#Match Status
df['MatchStatus']=df['BalanceDifference'].apply(lambda x: 'Match' if x == 0 else 'Break')

# Save to CSV
df.to_csv('IHub_History_Data.csv', index=False)

print("Random data with dates saved as 'IHub_History_Data.csv'")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
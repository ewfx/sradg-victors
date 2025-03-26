#Generate Current month file
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Function to generate random alphanumeric data (for Cusip code, typically 9 characters)
def generate_random_alphanumeric(length=9):  # Cusip codes are 9 characters long
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Generate random dates
def generate_random_dates(start_date, end_date, n):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    diff = end - start
    return [start + timedelta(days=np.random.randint(0, diff.days)) for _ in range(n)]

# Create random data
num_rows = 10000
# Generate a list of numbers with leading zeros (e.g., 00001, 00002, etc.)
numbers_with_leading_zeros = [f"{i:05}" for i in range(1, 7)]  # Pool of numbers with leading zeros (1 to 6)
# Use random.choices() to sample numbers with replacement
repeated_numbers = random.choices(numbers_with_leading_zeros, k=num_rows)

data = {
     'Match_Status': np.random.choice(['Impact_Only', 'Catalyst_Only', 'Quantity_Break', 'Price_Break'], num_rows),
    'RiskDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
     'Comment': np.random.choice(['Factor rounding is causing minor delta in qty. OF is same and systems are in line', 'Proce break driven by rounding because qty is less than 1000. Total money still matches between all systems', 'Blotter code updated directly in impact causing a false break,due to an additional line item for cx', 'Intrest update on account of periodic VAR updates ONLY in backend,FIMO updated intrest back to original in impact'], num_rows),
    'QuantityDifference': repeated_numbers,
    'TradeID': np.random.randint(1111111, 9999999, num_rows),
    'DeskName': np.random.choice(['RMBS-Agency CMOs', 'Treasury', 'HighYield - Industry Desks', 'Agency'], num_rows),   
    'ReconDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023 
    'BUY_SELL': np.random.choice(['B', 'S'], num_rows),
     'Trade_Date': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
     'Settle_Date': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
    'Inventory': np.random.choice(['CM10', 'A480', 'TQ40', 'H210', 'UV70'], num_rows),
    'AU': np.random.randint(1000, 7000, num_rows),   
    'Price': np.random.randint(30000, 120000, num_rows),   
    'Cusip': [generate_random_alphanumeric() for _ in range(num_rows)],
    'Quantity': repeated_numbers,
    'Original_FACE': np.random.randint(1111111, 9999999, num_rows),
    'Price_Tolerance': np.random.uniform(0.001, 0.999, num_rows),
    'Quantity_Tolerance': repeated_numbers,
    'PriceDifference': np.random.uniform(-500.00, 1000.00, num_rows),
    'OriginalFaceDifference': np.random.uniform(-500.00, 1000.00, num_rows),
     'Trading_Unit_Name': np.random.choice(['RMBS', 'Liquid Products - Treasuries', 'High Grade Trading', 'Liquid Products - Agencies'], num_rows),   
    'Catalyst_Action': np.random.choice(['NEW', 'SUBMITALLOC', 'TRADEUPDATE'], num_rows),
    'Catalyst_BUYSELL': np.random.choice(['B', 'S'], num_rows),
    'Catalyst_Cusip': [generate_random_alphanumeric() for _ in range(num_rows)],
     'Catalyst_EntryDateTime': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
     'catalyst_ETLID': [f'{np.random.randint(1000, 9999)}_IPP' for _ in range(num_rows)],  # Generate random numbers and append '_IPP'
    'Catalyst_Inventory': np.random.choice(['CM10', 'A480', 'TQ40', 'H210', 'UV70'], num_rows), 
     'Catalyst_OriginalFace': np.random.randint(30000, 120000, num_rows),   
      'Catalyst_Price': np.random.randint(30000, 120000, num_rows), 
    'Catalyst_Price_Tolerance': np.random.uniform(0.001, 0.999, num_rows),
    'Catalyst_Quantity': np.random.randint(1111111, 9999999, num_rows),
     'Catalyst_Quantity_Tolerance': repeated_numbers,
    'Catalyst_ReconDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023 
     'Catalyst_SettleDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
     'Catalyst_TradeDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
    'Catalyst_TradeID': np.random.randint(1111111, 9999999, num_rows),
    'Impact_Blotter_code': [f'{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}' for _ in range(num_rows)],  # Generate two-character Impact_Blotter_code
     'Impact_Business_Dt': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
    'Impact_BUYSELL': np.random.choice(['B', 'S'], num_rows),
    'Impact_CRNT_POOL_FCTR_RT': np.random.uniform(0.001, 999, num_rows),
    'Impact_Cusip': [generate_random_alphanumeric() for _ in range(num_rows)],
    'Impact_Inventory': np.random.choice(['CM10', 'A480', 'TQ40', 'H210', 'UV70'], num_rows),
     'Impact_Original_FACE': np.random.randint(1111111, 9999999, num_rows),
    'Impact_Price': np.random.uniform(1, 999, num_rows),
    'Impact_Price_Tolerance': np.random.uniform(0.001, 0.999, num_rows),
     'Impact_Quantity': np.random.randint(1111111, 9999999, num_rows),
     'Impact_Quantity_Tolerance': repeated_numbers,
    'Impact_ReconDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023 
     'Impact_SettleDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
     'Impact_TradeDate': generate_random_dates('2023-01-01', '2023-01-31', num_rows), # Random dates in 2023
    'Impact_TradeID': repeated_numbers,   
    }

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('catalyst_monthly.csv', index=False)

print("Data saved as catalyst_monthly.csv'")
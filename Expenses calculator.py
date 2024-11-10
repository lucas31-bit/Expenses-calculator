# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:05:37 2024

@author: lucas
"""

import pandas as pd

# Load the Excel file
file_path = 'Wbwdata.xlsx'
df = pd.read_excel(file_path, header=None, names=['Name', 'Value'])  

# Display the contents of the DataFrame
print(df)

# Split the people into those who owe (negative values) and those who are owed (positive values)
owes = df[df['Value'] < 0].copy()
owed = df[df['Value'] > 0].copy()

owes['Value'] = owes['Value'].abs()

# Prepare list to track transactions
transactions = []

# Match debtors with creditors
i, j = 0, 0
while i < len(owes) and j < len(owed):
    if owes.iloc[i]['Value'] < owed.iloc[j]['Value']:
        # Debtor i pays off part of creditor j's amount
        transactions.append(f"{owes.iloc[i]['Name']} pays {owed.iloc[j]['Name']} {owes.iloc[i]['Value']}")
        owes.iloc[j, owes.columns.get_loc('Value')] -= owes.iloc[i]['Value']
        i += 1
    elif owes.iloc[i]['Value'] > owed.iloc[j]['Value']:
        # Debtor i pays off creditor j completely
        transactions.append(f"{owes.iloc[i]['Name']} pays {owed.iloc[j]['Name']} {owed.iloc[j]['Value']}")
        owes.iloc[i, owes.columns.get_loc('Value')] -= owed.iloc[j]['Value']
        j += 1
    else:
        # Debtor i pays creditor j exactly
        transactions.append(f"{owes.iloc[i]['Name']} pays {owed.iloc[j]['Name']} {owes.iloc[i]['Value']}")
        i += 1
        j += 1

# Output the transactions
for transaction in transactions:
    print(transaction)

# Test function 
def biggest_change(transactions):
    if not transactions:
        return None
    if len(transactions) == 1:
        return 0
    differences = np.diff(transactions)
    abs_differences = np.abs(differences)
    return abs_differences.max()

transactions = []
result = biggest_change(transactions)
assert result == None

transactions = [1]
result = biggest_change(transactions)
assert result == 0

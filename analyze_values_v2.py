import pandas as pd
import re

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR
file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

def clean_currency(x):
    if isinstance(x, str):
        return float(re.sub(r'[$,]', '', x))
    return float(x)

df['Charge'] = df['Charge'].apply(clean_currency)

avg_charges = df.groupby('Charge Type')['Charge'].mean().sort_values(ascending=False)
print("--- Top 20 Charge Types by Average Amount ---")
print(avg_charges.head(20))

print("\n--- Charge Value Distribution ---")
print(df['Charge'].describe())

counts = df['Tracking Number'].value_counts()
single_row_tracking = counts[counts == 1].index
single_row_df = df[df['Tracking Number'].isin(single_row_tracking)]
print("\n--- Distribution of Charges for Single-Row Shipments ---")
print(single_row_df['Charge'].describe())

print("\n--- Top 10 Charge Types in Single-Row Shipments ---")
print(single_row_df['Charge Type'].value_counts().head(10))

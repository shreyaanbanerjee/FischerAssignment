import pandas as pd

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR
file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

avg_charges = df.groupby('Charge Type')['Charge'].mean().sort_values(ascending=False)
print("--- Top 20 Charge Types by Average Amount ---")
print(avg_charges.head(20))

print("\n--- Bottom 20 Charge Types by Average Amount ---")
print(avg_charges.tail(20))

print("\n--- Charge Value Distribution ---")
print(df['Charge'].describe())

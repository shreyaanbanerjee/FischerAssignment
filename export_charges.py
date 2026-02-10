import pandas as pd

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR

file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

unique_charges = df['Charge Type'].unique()
with open(os.path.join(DATA_DIR, 'charge_types.txt'), 'w') as f:
    for c in sorted(unique_charges):
        f.write(c + '\n')

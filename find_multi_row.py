import pandas as pd

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR
file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

counts = df['Tracking Number'].value_counts()
multi_row_shipments = counts[counts > 1]
print(f"Shipments with multiple rows: {len(multi_row_shipments)}")
print(multi_row_shipments.head())

if len(multi_row_shipments) > 0:
    sample_mn = multi_row_shipments.index[0]
    print(f"\n--- Charges for {sample_mn} ---")
    print(df[df['Tracking Number'] == sample_mn][['Charge Type', 'Charge', 'Service Level']])

single_row_shipments = counts[counts == 1]
print(f"\nShipments with single row: {len(single_row_shipments)}")
if len(single_row_shipments) > 0:
    sample_sn = single_row_shipments.index[0]
    print(f"\n--- Charges for {sample_sn} ---")
    print(df[df['Tracking Number'] == sample_sn][['Charge Type', 'Charge', 'Service Level']])

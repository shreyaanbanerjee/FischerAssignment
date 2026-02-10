import pandas as pd

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR
file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

num_shipments = df['Tracking Number'].nunique()
print(f"Total Shipments: {num_shipments}")

charge_counts = df['Charge Type'].value_counts()
print("\nTop 20 Charge Types by frequency:")
print(charge_counts.head(20))

freight_shipments = df[df['Charge Type'] == 'Freight']['Tracking Number'].nunique()
print(f"\nShipments with 'Freight' charge: {freight_shipments}")

all_tracking = set(df['Tracking Number'])
freight_tracking = set(df[df['Charge Type'] == 'Freight']['Tracking Number'])
missing_freight = all_tracking - freight_tracking
print(f"Shipments without 'Freight': {len(missing_freight)}")

if len(missing_freight) > 0:
    print("Sample shipments without Freight:")
    print(df[df['Tracking Number'].isin(list(missing_freight)[:5])])

print("\nService Level Counts:")
print(df['Service Level'].value_counts())

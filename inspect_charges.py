import pandas as pd

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR
file_path = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
df = pd.read_csv(file_path)

sample_tracking = ['1F1234567890126007', '1F9876543210987654', '5F98765MNBVC', '1F1234567890123458'] # Added a known one

print("--- Inspecting Charges for Sample Shipments ---")
for tn in sample_tracking:
    print(f"\nTracking Number: {tn}")
    print(df[df['Tracking Number'] == tn][['Carrier Name', 'Charge Type', 'Charge', 'Service Level', 'Weight (lbs)']])

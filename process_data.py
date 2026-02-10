import pandas as pd
import re
import numpy as np

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR

INPUT_FILE = os.path.join(DATA_DIR, 'FJ Assignment - FJ Assignment - Sheet1.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'processed_shipments.csv')

def clean_currency(x):
    """Removes currency symbols and converts to float."""
    if isinstance(x, str):
        return float(re.sub(r'[$,]', '', x))
    return float(x)

def categorize_charge(charge_type):
    """Categorizes charge types into Base or Surcharge."""
    base_indicators = ['Base Rate', 'Freight']
    
    if charge_type in base_indicators:
        return 'Base'
    return 'Surcharge'

def main():
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    print("Cleaning 'Charge' column...")
    df['Charge Amount'] = df['Charge'].apply(clean_currency)
    
    print("Categorizing charges...")
    df['Charge Category'] = df['Charge Type'].apply(categorize_charge)
    
    print("Aggregating data by Tracking Number...")
    
    agg_rules = {
        'Carrier Name': 'first',
        'Service Level': 'first',
        'Zones': 'first',
        'Weight (lbs)': 'first',
        'Dimensions (in)': 'first',
        'Date of Delivery': 'first',
        'Charge Amount': 'sum',
    }
    
    grouped = df.groupby('Tracking Number').agg(agg_rules).reset_index()
    
    base_costs = df[df['Charge Category'] == 'Base'].groupby('Tracking Number')['Charge Amount'].sum()
    grouped['Base Cost'] = grouped['Tracking Number'].map(base_costs).fillna(0.0)
    
    surcharge_costs = df[df['Charge Category'] == 'Surcharge'].groupby('Tracking Number')['Charge Amount'].sum()
    grouped['Surcharge Cost'] = grouped['Tracking Number'].map(surcharge_costs).fillna(0.0)
    
    print("Calculating normalized metrics...")
    
    def clean_weight(w):
        if isinstance(w, str):
             match = re.search(r'(\d+(\.\d+)?)', w)
             if match:
                 return float(match.group(1))
        return float(w)

    grouped['Weight (lbs)'] = grouped['Weight (lbs)'].apply(clean_weight)
    
    grouped['Cost per Lb'] = grouped['Charge Amount'] / grouped['Weight (lbs)']
    
    grouped['Surcharge %'] = (grouped['Surcharge Cost'] / grouped['Charge Amount']) * 100
    
    print(f"Saving processed data to {OUTPUT_FILE}...")
    grouped.to_csv(OUTPUT_FILE, index=False)
    
    print("Processing complete.")
    print(grouped.head())
    print("\nSummary Statistics:")
    print(grouped[['Charge Amount', 'Base Cost', 'Surcharge Cost', 'Cost per Lb']].describe())

if __name__ == "__main__":
    main()

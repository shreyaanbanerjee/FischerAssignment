import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = SCRIPT_DIR

INPUT_FILE = os.path.join(DATA_DIR, 'processed_shipments.csv')
OUTPUT_DIR = DATA_DIR + os.sep

def main():
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    total_spend = df['Charge Amount'].sum()
    avg_cost = df['Charge Amount'].mean()
    print(f"Total Spend: ${total_spend:.2f}")
    print(f"Average Cost per Shipment: ${avg_cost:.2f}")

    print("\n--- Carrier Analysis ---")
    carrier_stats = df.groupby('Carrier Name').agg({
        'Tracking Number': 'count',
        'Charge Amount': 'mean',
        'Cost per Lb': 'mean',
        'Surcharge %': 'mean'
    }).rename(columns={'Tracking Number': 'Shipment Count', 'Charge Amount': 'Avg Cost'}).sort_values('Avg Cost', ascending=False)
    
    print(carrier_stats)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=carrier_stats.index, y=carrier_stats['Avg Cost'])
    plt.title('Average Cost per Shipment by Carrier')
    plt.xticks(rotation=45)
    plt.ylabel('Average Cost ($)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'carrier_cost_comparison.png')
    plt.close()

    print("\n--- Worst 10% Analysis ---")
    threshold_price = df['Charge Amount'].quantile(0.90)
    print(f"90th Percentile Cost Threshold: ${threshold_price:.2f}")
    
    worst_shipments = df[df['Charge Amount'] >= threshold_price]
    worst_spend = worst_shipments['Charge Amount'].sum()
    worst_pct_of_total = (worst_spend / total_spend) * 100
    
    print(f"Number of shipments in worst 10%: {len(worst_shipments)}")
    print(f"Total Spend of worst 10%: ${worst_spend:.2f}")
    print(f"Percentage of Total Spend: {worst_pct_of_total:.1f}%")
    
    print("\nworst 10% by Carrier:")
    print(worst_shipments['Carrier Name'].value_counts(normalize=True) * 100)
    
    print("\nworst 10% by Zone:")
    print(worst_shipments['Zones'].value_counts(normalize=True) * 100)
    
    print("\nworst 10% by Service Level:")
    print(worst_shipments['Service Level'].value_counts(normalize=True) * 100)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['Charge Amount'], bins=20, kde=True)
    plt.axvline(threshold_price, color='r', linestyle='--', label='90th Percentile')
    plt.title('Distribution of Shipment Costs')
    plt.xlabel('Total Charge Amount ($)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'cost_distribution.png')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Weight (lbs)', y='Charge Amount', hue='Carrier Name')
    plt.title('Shipment Cost vs Weight')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'cost_vs_weight.png')
    plt.close()

if __name__ == "__main__":
    main()

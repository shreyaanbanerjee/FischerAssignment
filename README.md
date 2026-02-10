# Fischer Jordan Data Analytics Assignment: Shipment Cost Normalization

## Overview

This project implements a normalized shipment cost model for a shoe company shipping 4lb parcels across India. The goal is to enable fair cost comparisons between carriers (Delhivery, DTDC, Bluedart, etc.) by isolating base shipping costs from surcharges and identifying high-cost outliers.

## Solution Approach

### 1. Data Cleaning & Standardization
The raw data presented several inconsistencies which were addressed:
-   **Currency Cleanup**: Removed symbols (`$`, `,`) and converted strings to floating-point numbers.
-   **Weight Standardization**: Extracted numeric values from mixed formats (e.g., `4 lbs` -> `4.0`) to ensure accurate "Cost per Lb" calculations.
-   **Zone Normalization**: Standardized the `Zones` column (e.g., converting `Zone 3` -> `3`) to allow for proper aggregation by zone.
-   **Rounding**: All monetary values were rounded to 2 decimal places for reporting clarity.

### 2. Cost Normalization Model
To compare carriers fairly, charges were categorized into two main buckets:

| Category | Definition | Rationale |
| :--- | :--- | :--- |
| **Base Cost** | Charges explicitly labeled as `Base Rate` or `Freight`. | Represents the fundamental cost of moving the package from A to B. |
| **Surcharge** | All other charges (e.g., Fuel Surcharge, Handling Fees, Remote Area Fees). | These are often variable or avoidable costs that distort the true shipping efficiency. |

### 3. Aggregation Strategy
The data was aggregated by **Tracking Number** to create a single row per shipment.
-   **Dimensions/Weights**: Taken as the `max` value per shipment to handle potential data entry errors where one line might be zero.
-   **Costs**: Summed across all lines for a given tracking number.

---

## Key Findings & Analysis

### Carrier Performance
The normalization process revealed significant differences in cost structures.

| Carrier | Max Cost Contribution | Notes |
| :--- | :--- | :--- |
| **Safe Express** | High | Consistently high cost per shipment. |
| **FedEx** | High | Significant contribution to the worst performing shipments. |

### "Worst 10%" Analysis (Bonus)

We identified the **top 10% most expensive shipments** (based on normalized total cost) to understand where the money is being lost.

-   **Threshold**: Any shipment costing **$105.00** or more is in the worst 10%.
-   **Financial Impact**: These 16 shipments (15% of volume) account for **36.1% of the Total Spend** ($1,875.00 out of $5,197.50).

#### Concentration of High Costs:
1.  **By Carrier**: 
    -   **FedEx** and **Delhivery** each account for **18.75%** of these bad shipments.
    -   Together with **Blue Dart** (12.5%), these three major carriers drive half of the high-cost volume.
2.  **By Zone**:
    -   **Zone 4** is the most expensive destination, accounting for **37.5%** of the worst shipments.
    -   **Zone 2** follows with 25%.
3.  **By Service Level**:
    -   **Standard** (31.25%) and **Economy** (25%) services appear frequently in the high-cost list, suggesting that "slower" doesn't always mean "cheaper" when surcharges are factored in.

---

## Assumptions & Edge Cases

1.  **Multiple Rows**: It is assumed that multiple rows for a single `Tracking Number` represent different charge components for the *same* package.
2.  **Missing Weights**: If weight is missing or 0, we default to the `max` found for that tracking number, or leave it as is (which affects Cost/Lb metrics).
3.  **Base Cost Definitions**: We strictly defined `Base` only as "Base Rate" or "Freight". If a carrier bundles base cost into a generic "Shipping Charge" without distinction, it might end up classified as a Surcharge, potentially skewing the `Surcharge %` metric for that specific carrier.

## How to Run the Analysis

### Prerequisites
-   Python 3.x
-   pandas
-   matplotlib
-   seaborn

### Execution
1.  **Process and Normalize Data**:
    ```bash
    python3 process_data.py
    ```
    *Generates `processed_shipments.csv`*

2.  **Run Analysis & Generate Charts**:
    ```bash
    python3 analyze_results.py
    ```
    *Outputs summary stats to console and saves charts (`carrier_cost_comparison.png`, `cost_vs_weight.png`) to the project folder.*

---
*Generated for Fischer Jordan Data Analytics Assignment*
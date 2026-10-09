"""
1_dataset_showcase.py
----------------------
Showcases the cleaned Fruit & Vegetable Spoilage Sensor dataset:
loads it, prints a full profile to the terminal, and saves 7 EDA plots to outputs/.

Refactored to systematically use the modular src package.
"""

from src.config import OUTPUT_DIR, NUMERIC_FEATURES
from src.data_loader import load_data, get_dataset_summary
from src.visualizer import generate_all_eda_plots
import pandas as pd

def main():
    print("=" * 70)
    print("DATASET OVERVIEW & EXPLORATORY PROFILE")
    print("=" * 70)

    df = load_data()
    summary = get_dataset_summary(df)

    print(f"Shape: {summary['total_rows']} rows x {summary['total_cols']} columns\n")
    print("Columns and dtypes:")
    print(df.dtypes, "\n")

    print("First 5 rows:")
    print(df.head(), "\n")

    print("Missing values per column:")
    for col, count in summary["missing_values"].items():
        print(f"  {col}: {count}")
    print()

    print("Duplicate rows:", summary["duplicate_rows"], "\n")

    print("=" * 70)
    print("DESCRIPTIVE STATISTICS (numeric fields)")
    print("=" * 70)
    print(df[NUMERIC_FEATURES].describe().T, "\n")

    print("Class balance:")
    print(df["Class"].value_counts(), "\n")

    print("Fruit balance:")
    print(df["Fruit"].value_counts(), "\n")

    print("Fruit x Class cross-tab:")
    print(pd.crosstab(df["Fruit"], df["Class"]), "\n")

    print("Mean sensor readings by Class:")
    print(df.groupby("Class")[NUMERIC_FEATURES].mean().round(2), "\n")

    print("Correlation matrix (numeric fields):")
    print(df[NUMERIC_FEATURES].corr().round(3), "\n")

    print("=" * 70)
    print("GENERATING EDA PLOTS")
    print("=" * 70)
    saved_plots = generate_all_eda_plots(df, OUTPUT_DIR)
    for p in saved_plots:
        print(f"  [+] Saved {OUTPUT_DIR}/{p}")

    print("=" * 70)
    print(f"Successfully saved {len(saved_plots)} EDA plots to '{OUTPUT_DIR}/'")
    print("=" * 70)


if __name__ == "__main__":
    main()

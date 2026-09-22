"""
data_loader.py
--------------
Handles CSV ingestion, cleaning, and feature engineering for the
Automobile Parts India dataset.
"""

import re
import pandas as pd

DATASET_PATH = "automobile_parts_india.csv"

COLUMN_RENAMES = {
    "Part ID": "part_id",
    "Supplier": "supplier",
    "Target OEM": "target_oem",
    "Plant Location": "plant_location",
    "Lead Time (Days)": "lead_time_days",
    "Component Category": "component_category",
    "Stock Status": "stock_status",
    "Batch Quantity": "batch_quantity",
    "Unit Cost (INR)": "unit_cost_inr",
    "Total Batch Value (INR)": "total_batch_value_inr",
    "GST Rate (%)": "gst_rate_pct",
    "GST Amount (INR)": "gst_amount_inr",
    "Final Value with GST (INR)": "final_value_with_gst_inr",
}


def _clean_currency(series: pd.Series) -> pd.Series:
    """Strip ₹, commas, whitespace and coerce to float."""
    return (
        series.astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .pipe(pd.to_numeric, errors="coerce")
    )


def load_and_clean(path: str = DATASET_PATH) -> pd.DataFrame:
    """
    Load the CSV, clean currency columns, fill missing values,
    and engineer the Sales (= Batch Quantity × Unit Cost) column.

    Returns
    -------
    pd.DataFrame
        Fully cleaned and enriched DataFrame.
    """
    df = pd.read_csv(path)

    # ── Rename columns ──────────────────────────────────────────────────────
    df.rename(columns=COLUMN_RENAMES, inplace=True)

    # ── Clean currency / numeric columns ────────────────────────────────────
    for col in ["unit_cost_inr", "total_batch_value_inr",
                "gst_amount_inr", "final_value_with_gst_inr"]:
        df[col] = _clean_currency(df[col])

    df["batch_quantity"] = pd.to_numeric(df["batch_quantity"], errors="coerce")
    df["lead_time_days"] = pd.to_numeric(df["lead_time_days"], errors="coerce")
    df["gst_rate_pct"]   = pd.to_numeric(df["gst_rate_pct"],   errors="coerce")

    # ── Missing-value report (stored before filling) ─────────────────────────
    missing_report = df.isnull().sum().rename("missing_count").to_frame()
    missing_report["missing_pct"] = (
        missing_report["missing_count"] / len(df) * 100
    ).round(2)
    missing_report = missing_report[missing_report["missing_count"] > 0]

    # ── Fill missing values ──────────────────────────────────────────────────
    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode()[0] if not df[c].mode().empty else "Unknown")

    # ── Feature engineering: Sales = Batch Quantity × Unit Cost ─────────────
    df["sales_inr"] = df["batch_quantity"] * df["unit_cost_inr"]

    # ── Profit margin approximation (pre-GST value vs final) ─────────────────
    df["effective_gst_pct"] = (
        df["gst_amount_inr"] / df["total_batch_value_inr"] * 100
    ).round(2)

    df["_missing_report"] = None          # placeholder; actual report stored below

    # Attach the missing report as a module-level attribute for display
    load_and_clean.missing_report = missing_report

    return df


def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for key numeric columns."""
    cols = [
        "batch_quantity", "unit_cost_inr",
        "total_batch_value_inr", "gst_amount_inr",
        "final_value_with_gst_inr", "sales_inr", "lead_time_days",
    ]
    return df[cols].describe().T.rename(columns=str).round(2)

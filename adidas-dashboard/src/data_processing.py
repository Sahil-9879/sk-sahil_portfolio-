"""
Data processing module for the Adidas Sales Analytics Dashboard.

Handles CSV loading, column mapping, cleaning, type conversion,
and derived field creation. Uses @st.cache_data for performance.
"""

import pandas as pd
import numpy as np
import streamlit as st
import os

# ---------------------------------------------------------------------------
# Column name mapping – maps common variations to internal standard names
# ---------------------------------------------------------------------------
COLUMN_ALIASES = {
    # Internal name -> list of possible source names (case-insensitive match)
    "retailer":        ["retailer", "retailer name"],
    "retailer_id":     ["retailer id", "retailer_id", "retailerid"],
    "date":            ["invoice date", "invoicedate", "date", "sales date", "order date"],
    "region":          ["region"],
    "state":           ["state"],
    "city":            ["city"],
    "product":         ["product", "product category", "product name", "category"],
    "price_per_unit":  ["price per unit", "priceperunit", "unit price", "selling price", "avg price"],
    "units_sold":      ["units sold", "unitssold", "units", "quantity"],
    "total_sales":     ["total sales", "totalsales", "revenue", "total revenue", "sales"],
    "operating_profit":["operating profit", "operatingprofit", "profit", "op profit"],
    "operating_margin":["operating margin", "operatingmargin", "margin", "op margin"],
    "sales_method":    ["sales method", "salesmethod", "sales channel", "channel", "method"],
}


def _resolve_columns(df: pd.DataFrame) -> dict:
    """Build a mapping from internal column names to actual DataFrame column names."""
    lower_cols = {c.strip().lower(): c for c in df.columns}
    mapping = {}
    for internal_name, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_cols:
                mapping[internal_name] = lower_cols[alias]
                break
    return mapping


def _rename_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Rename DataFrame columns to internal standard names."""
    reverse = {v: k for k, v in mapping.items()}
    return df.rename(columns=reverse)


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Convert a series to numeric, stripping currency symbols and commas."""
    if series.dtype == object:
        series = series.astype(str).str.replace(r'[\$,€£¥]', '', regex=True)
    return pd.to_numeric(series, errors='coerce')


@st.cache_data(show_spinner=False)
def load_and_process_data(filepath: str) -> tuple[pd.DataFrame, dict]:
    """
    Load the Adidas sales CSV, clean it, and return the processed DataFrame
    along with a dict of available internal column names.

    Returns
    -------
    df : pd.DataFrame  – cleaned data with standard column names
    available : dict    – {internal_name: True} for columns present
    """
    if not os.path.exists(filepath):
        st.error(f"Dataset not found at `{filepath}`")
        st.stop()

    df = pd.read_csv(filepath)

    # Resolve and rename columns
    mapping = _resolve_columns(df)
    df = _rename_columns(df, mapping)

    # Track which standard columns are available
    available = {col: True for col in COLUMN_ALIASES if col in df.columns}

    # --- Type conversions ---
    if "date" in available:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=False)
        df.dropna(subset=["date"], inplace=True)

    numeric_cols = ["price_per_unit", "units_sold", "total_sales",
                    "operating_profit", "operating_margin"]
    for col in numeric_cols:
        if col in available:
            df[col] = _clean_numeric(df[col])

    # --- Derived columns ---
    if "date" in available:
        df["year"]    = df["date"].dt.year
        df["month"]   = df["date"].dt.month
        df["quarter"] = df["date"].dt.quarter
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
        df["month_name"] = df["date"].dt.strftime("%b %Y")

    if "total_sales" in available and "units_sold" in available:
        df["avg_revenue_per_unit"] = np.where(
            df["units_sold"] > 0,
            df["total_sales"] / df["units_sold"],
            0
        )

    if "operating_profit" in available and "total_sales" in available:
        df["profit_margin"] = np.where(
            df["total_sales"] > 0,
            (df["operating_profit"] / df["total_sales"]) * 100,
            0
        )

    # Remove rows with all-NaN numeric columns
    df.dropna(how="all", subset=[c for c in numeric_cols if c in available], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df, available


def apply_filters(df: pd.DataFrame, filters: dict, available: dict) -> pd.DataFrame:
    """
    Apply user-selected filters to the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
    filters : dict – keys are internal column names, values are the filter value(s)
    available : dict – which columns exist

    Returns
    -------
    pd.DataFrame – filtered copy
    """
    filtered = df.copy()

    # Date range filter
    if "date_range" in filters and "date" in available:
        start, end = filters["date_range"]
        filtered = filtered[
            (filtered["date"] >= pd.Timestamp(start)) &
            (filtered["date"] <= pd.Timestamp(end))
        ]

    # Categorical filters
    categorical_filters = ["region", "state", "city", "product", "retailer", "sales_method"]
    for col in categorical_filters:
        if col in filters and col in available:
            values = filters[col]
            if values:  # non-empty list
                filtered = filtered[filtered[col].isin(values)]

    return filtered


def get_filter_options(df: pd.DataFrame, available: dict) -> dict:
    """Return sorted unique values for each available categorical column."""
    options = {}
    for col in ["region", "state", "city", "product", "retailer", "sales_method"]:
        if col in available:
            options[col] = sorted(df[col].dropna().unique().tolist())
    return options


def format_number(value: float, prefix: str = "$", suffix: str = "") -> str:
    """Format large numbers with K/M/B suffixes."""
    if pd.isna(value) or value is None:
        return f"{prefix}0{suffix}"
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    if abs_val >= 1_000_000_000:
        return f"{sign}{prefix}{abs_val / 1_000_000_000:.2f}B{suffix}"
    elif abs_val >= 1_000_000:
        return f"{sign}{prefix}{abs_val / 1_000_000:.2f}M{suffix}"
    elif abs_val >= 1_000:
        return f"{sign}{prefix}{abs_val / 1_000:.1f}K{suffix}"
    else:
        return f"{sign}{prefix}{abs_val:,.2f}{suffix}"


def format_integer(value: float) -> str:
    """Format an integer with comma separators and K/M suffixes."""
    if pd.isna(value) or value is None:
        return "0"
    abs_val = abs(int(value))
    sign = "-" if value < 0 else ""
    if abs_val >= 1_000_000:
        return f"{sign}{abs_val / 1_000_000:.2f}M"
    elif abs_val >= 1_000:
        return f"{sign}{abs_val:,}"
    else:
        return f"{sign}{abs_val}"

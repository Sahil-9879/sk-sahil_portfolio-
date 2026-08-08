"""
Business insights module for the Adidas Sales Analytics Dashboard.

Dynamically generates natural-language insights from filtered data.
"""

import pandas as pd
from src.data_processing import format_number, format_integer


def generate_insights(df: pd.DataFrame, available: dict) -> list[str]:
    """
    Generate a list of key business insight strings from the current DataFrame.

    Parameters
    ----------
    df : pd.DataFrame – filtered dataset
    available : dict – which columns are present

    Returns
    -------
    list[str] – human-readable insight bullets
    """
    if df.empty:
        return ["No data available to generate insights."]

    insights = []

    # --- Revenue insights ---
    if "total_sales" in available and "region" in available:
        region_rev = df.groupby("region")["total_sales"].sum()
        if not region_rev.empty:
            top_region = region_rev.idxmax()
            top_rev = region_rev.max()
            insights.append(
                f"🏆 **{top_region}** generated the highest revenue at "
                f"**{format_number(top_rev)}**, leading all regions."
            )
            bot_region = region_rev.idxmin()
            bot_rev = region_rev.min()
            if top_region != bot_region:
                insights.append(
                    f"📉 **{bot_region}** had the lowest revenue at "
                    f"**{format_number(bot_rev)}** — a potential growth opportunity."
                )

    # --- Product insights ---
    if "total_sales" in available and "product" in available:
        product_rev = df.groupby("product")["total_sales"].sum()
        if not product_rev.empty:
            top_product = product_rev.idxmax()
            insights.append(
                f"👟 **{top_product}** is the top-performing product category by revenue "
                f"({format_number(product_rev.max())})."
            )

    # --- Retailer insights ---
    if "total_sales" in available and "retailer" in available:
        retailer_rev = df.groupby("retailer")["total_sales"].sum()
        if not retailer_rev.empty:
            top_retailer = retailer_rev.idxmax()
            insights.append(
                f"🏪 **{top_retailer}** is the highest-performing retailer, contributing "
                f"**{format_number(retailer_rev.max())}** in revenue."
            )

    # --- Profit insights ---
    if "operating_profit" in available and "product" in available:
        product_profit = df.groupby("product")["operating_profit"].sum()
        if not product_profit.empty:
            top_profit_product = product_profit.idxmax()
            insights.append(
                f"💰 **{top_profit_product}** generated the highest operating profit "
                f"({format_number(product_profit.max())})."
            )

    # --- Units insights ---
    if "units_sold" in available and "product" in available:
        product_units = df.groupby("product")["units_sold"].sum()
        if not product_units.empty:
            top_units_product = product_units.idxmax()
            insights.append(
                f"📦 **{top_units_product}** had the highest sales volume "
                f"with **{format_integer(product_units.max())}** units sold."
            )

    # --- Seasonal insights ---
    if "total_sales" in available and "date" in available:
        try:
            monthly = df.groupby(df["date"].dt.to_period("M"))["total_sales"].sum()
            if not monthly.empty:
                best_month = monthly.idxmax()
                insights.append(
                    f"📅 **{best_month.strftime('%B %Y')}** was the strongest sales month "
                    f"with **{format_number(monthly.max())}** in revenue."
                )
        except Exception:
            pass

    # --- Quarterly insights ---
    if "total_sales" in available and "quarter" in df.columns and "year" in df.columns:
        try:
            quarterly = df.groupby(["year", "quarter"])["total_sales"].sum()
            if not quarterly.empty:
                best_q = quarterly.idxmax()
                insights.append(
                    f"📊 **Q{best_q[1]} {int(best_q[0])}** showed the strongest quarterly performance "
                    f"({format_number(quarterly.max())})."
                )
        except Exception:
            pass

    # --- Sales method insights ---
    if "total_sales" in available and "sales_method" in available:
        method_rev = df.groupby("sales_method")["total_sales"].sum()
        if not method_rev.empty:
            top_method = method_rev.idxmax()
            pct = (method_rev.max() / method_rev.sum()) * 100
            insights.append(
                f"🛒 **{top_method}** is the dominant sales channel, accounting for "
                f"**{pct:.1f}%** of total revenue."
            )

    # --- Profit margin insight ---
    if "profit_margin" in df.columns:
        avg_margin = df["profit_margin"].mean()
        insights.append(
            f"📈 The average profit margin across all transactions is **{avg_margin:.1f}%**."
        )

    return insights if insights else ["Insufficient data to generate insights."]

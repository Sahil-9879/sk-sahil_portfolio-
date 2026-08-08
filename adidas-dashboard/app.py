"""
Adidas Interactive Sales Analytics Dashboard
Main Streamlit application with 3 tabs: Overview, Sales Analysis, Product & Region
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

from src.data_processing import (
    load_and_process_data, apply_filters, get_filter_options,
    format_number, format_integer,
)
from src.charts import (
    create_line_chart, create_bar_chart, create_donut_chart,
    create_scatter_chart, create_grouped_bar_chart, COLORS,
)
from src.insights import generate_insights

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Adidas Sales Analytics",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background: #0E1117; }
[data-testid="stSidebar"] { background: #13161C; border-right: 1px solid #2A2D35; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #C0C0C0; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; max-width: 1400px; }

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #1A1D23 0%, #21242B 100%);
    border: 1px solid #2A2D35;
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,212,170,0.08); }
.kpi-label { font-size: 0.7rem; font-weight: 600; color: #8B8D94; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-size: 1.55rem; font-weight: 700; color: #FFFFFF; }
.kpi-accent { color: #00D4AA; }

/* Section headers */
.section-header { font-size: 1.15rem; font-weight: 600; color: #E0E0E0; margin: 1.5rem 0 0.6rem 0; padding-bottom: 6px; border-bottom: 2px solid #00D4AA; display: inline-block; }

/* Insight box */
.insight-box {
    background: #1A1D23;
    border-left: 3px solid #00D4AA;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    color: #C8C8C8;
    font-size: 0.92rem;
    line-height: 1.5;
}
.insight-box b { color: #FFFFFF; font-weight: 600; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; border-bottom: 1px solid #2A2D35; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8B8D94; border-radius: 8px 8px 0 0; padding: 10px 24px; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #1A1D23; color: #00D4AA !important; border-bottom: 2px solid #00D4AA; }

/* Sidebar branding */
.sidebar-brand { text-align: center; padding: 10px 0 20px 0; border-bottom: 1px solid #2A2D35; margin-bottom: 20px; }
.sidebar-brand h2 { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; margin: 0; letter-spacing: 2px; }
.sidebar-brand p { color: #00D4AA; font-size: 0.7rem; letter-spacing: 3px; font-weight: 500; margin: 4px 0 0 0; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stStatusWidget"] { visibility: hidden; }

/* Dataframe styling */
[data-testid="stDataFrame"] { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "adidas_sales.csv")
CURRENCY = "$"

df_full, available = load_and_process_data(DATA_PATH)

# ---------------------------------------------------------------------------
# Sidebar — Filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>👟 ADIDAS</h2>
        <p>SALES ANALYTICS</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎛️ Filters")

    filters = {}
    options = get_filter_options(df_full, available)

    # Date range
    if "date" in available:
        min_date = df_full["date"].min().date()
        max_date = df_full["date"].max().date()
        date_range = st.date_input(
            "📅 Date Range", value=(min_date, max_date),
            min_value=min_date, max_value=max_date, key="date_filter"
        )
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            filters["date_range"] = date_range

    # Categorical filters
    filter_labels = {
        "region": "🌍 Region", "state": "🏛️ State", "city": "🏙️ City",
        "product": "👟 Product", "retailer": "🏪 Retailer", "sales_method": "🛒 Sales Method",
    }
    for col, label in filter_labels.items():
        if col in options:
            selected = st.multiselect(label, options[col], key=f"filter_{col}")
            if selected:
                filters[col] = selected

    # Reset button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("filter_") or key == "date_filter":
                del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.caption(f"📊 Dataset: {len(df_full):,} records")
    if "date" in available:
        st.caption(f"📅 {min_date.strftime('%b %Y')} — {max_date.strftime('%b %Y')}")

# Apply filters
df = apply_filters(df_full, filters, available)


# ---------------------------------------------------------------------------
# Helper: KPI rendering
# ---------------------------------------------------------------------------
def render_kpis(data: pd.DataFrame):
    """Render the 5 KPI metric cards."""
    kpis = []
    if "total_sales" in available:
        kpis.append(("TOTAL REVENUE", format_number(data["total_sales"].sum(), CURRENCY), "kpi-accent"))
    if "units_sold" in available:
        kpis.append(("UNITS SOLD", format_integer(data["units_sold"].sum()), ""))
    if "operating_profit" in available:
        kpis.append(("OPERATING PROFIT", format_number(data["operating_profit"].sum(), CURRENCY), "kpi-accent"))
    if "price_per_unit" in available:
        avg_price = data["price_per_unit"].mean() if len(data) > 0 else 0
        kpis.append(("AVG. PRICE", f"{CURRENCY}{avg_price:,.2f}", ""))
    kpis.append(("TRANSACTIONS", f"{len(data):,}", ""))

    cols = st.columns(len(kpis))
    for i, (label, value, css_class) in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {css_class}">{value}</div>
            </div>
            """, unsafe_allow_html=True)


def no_data_message():
    st.warning("⚠️ No data available for the selected filters. Please adjust your filter criteria.")


def safe_plotly_chart(fig, key=None):
    """Render a plotly chart with error handling."""
    try:
        st.plotly_chart(fig, use_container_width=True, key=key)
    except Exception as e:
        st.error(f"Chart rendering error: {e}")


def build_agg_dict(base_col, base_agg, available_cols):
    """Build a safe aggregation dictionary only using available columns."""
    agg = {base_col: (base_col, base_agg)}

    if "operating_profit" in available_cols:
        agg["Profit"] = ("operating_profit", "sum")
    else:
        agg["Profit"] = (base_col, "sum")

    if "units_sold" in available_cols:
        agg["Units"] = ("units_sold", "sum")
    else:
        agg["Units"] = (base_col, "count")

    if "price_per_unit" in available_cols:
        agg["Avg_Price"] = ("price_per_unit", "mean")

    return agg


# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Sales Analysis", "👟 Product & Region"])

# ===== TAB 1 — OVERVIEW =====
with tab1:
    st.markdown("## Adidas Sales Analytics")
    st.markdown("*Interactive business intelligence dashboard for Adidas sales performance*")
    st.markdown("")

    render_kpis(df)

    if df.empty:
        no_data_message()
    else:
        st.markdown("")

        # Chart 1 & 2: Revenue Over Time + Revenue by Region
        c1, c2 = st.columns([3, 2])
        with c1:
            if "total_sales" in available and "month_year" in df.columns:
                monthly = df.groupby("month_year", as_index=False)["total_sales"].sum()
                monthly = monthly.sort_values("month_year")
                fig = create_line_chart(monthly, "month_year", "total_sales",
                                        title="Revenue Over Time", y_prefix=CURRENCY)
                safe_plotly_chart(fig, key="ov_revenue_time")
        with c2:
            if "total_sales" in available and "region" in available:
                region_data = df.groupby("region", as_index=False)["total_sales"].sum()
                region_data = region_data.sort_values("total_sales", ascending=False)
                fig = create_bar_chart(region_data, "region", "total_sales",
                                       title="Revenue by Region", y_prefix=CURRENCY)
                safe_plotly_chart(fig, key="ov_revenue_region")

        # Chart 3 & 4: Retailer + Product
        c3, c4 = st.columns(2)
        with c3:
            if "total_sales" in available and "retailer" in available:
                ret_data = df.groupby("retailer", as_index=False)["total_sales"].sum()
                ret_data = ret_data.sort_values("total_sales", ascending=True)
                fig = create_bar_chart(ret_data, "retailer", "total_sales",
                                       title="Sales by Retailer", horizontal=True, y_prefix=CURRENCY)
                safe_plotly_chart(fig, key="ov_retailer")
        with c4:
            if "total_sales" in available and "product" in available:
                prod_data = df.groupby("product", as_index=False)["total_sales"].sum()
                prod_data = prod_data.sort_values("total_sales", ascending=False)
                fig = create_donut_chart(prod_data, "product", "total_sales",
                                         title="Product Category Performance")
                safe_plotly_chart(fig, key="ov_product_donut")

        # Chart 5: Profit Trend
        if "operating_profit" in available and "month_year" in df.columns:
            profit_monthly = df.groupby("month_year", as_index=False)["operating_profit"].sum()
            profit_monthly = profit_monthly.sort_values("month_year")
            fig = create_line_chart(profit_monthly, "month_year", "operating_profit",
                                    title="Operating Profit Trend", color="#FF6B6B", y_prefix=CURRENCY)
            safe_plotly_chart(fig, key="ov_profit_trend")

        # Key Business Insights
        st.markdown('<div class="section-header">🔍 Key Business Insights</div>', unsafe_allow_html=True)
        insights = generate_insights(df, available)
        for insight in insights:
            # Convert markdown bold **text** to HTML <b>text</b> for inside HTML divs
            clean_insight = insight.replace("**", "<b>", 1).replace("**", "</b>", 1)
            while "**" in clean_insight:
                clean_insight = clean_insight.replace("**", "<b>", 1).replace("**", "</b>", 1)
            st.markdown(f'<div class="insight-box">{clean_insight}</div>', unsafe_allow_html=True)

        # Data table
        with st.expander("📋 View Detailed Data"):
            display_cols = [c for c in ["date","retailer","region","state","city","product",
                                         "units_sold","total_sales","operating_profit","sales_method"]
                           if c in df.columns]
            st.dataframe(df[display_cols].head(500), use_container_width=True, height=400)

# ===== TAB 2 — SALES ANALYSIS =====
with tab2:
    st.markdown("## 📈 Sales Analysis")
    st.markdown("*Explore detailed sales performance with dynamic metric selection*")
    st.markdown("")

    if df.empty:
        no_data_message()
    else:
        # Metric selector
        metric_map = {}
        if "total_sales" in available:
            metric_map["Revenue"] = "total_sales"
        if "units_sold" in available:
            metric_map["Units Sold"] = "units_sold"
        if "operating_profit" in available:
            metric_map["Operating Profit"] = "operating_profit"
        if "price_per_unit" in available:
            metric_map["Average Price"] = "price_per_unit"

        if not metric_map:
            st.warning("No metrics available in the dataset.")
        else:
            selected_metric_label = st.selectbox(
                "📊 Select Metric", list(metric_map.keys()), key="sa_metric"
            )
            selected_metric = metric_map[selected_metric_label]
            is_currency = selected_metric in ("total_sales", "operating_profit")
            prefix = CURRENCY if is_currency else ""

            render_kpis(df)
            st.markdown("")

            # Chart 1: Sales Trend
            if "month_year" in df.columns:
                if selected_metric == "price_per_unit":
                    trend = df.groupby("month_year", as_index=False)[selected_metric].mean()
                else:
                    trend = df.groupby("month_year", as_index=False)[selected_metric].sum()
                trend = trend.sort_values("month_year")
                fig = create_line_chart(trend, "month_year", selected_metric,
                                        title=f"{selected_metric_label} Trend Over Time", y_prefix=prefix)
                safe_plotly_chart(fig, key="sa_trend")

            c1, c2 = st.columns(2)

            # Chart 2: Region Comparison
            with c1:
                if "region" in available:
                    if selected_metric == "price_per_unit":
                        region_metric = df.groupby("region", as_index=False)[selected_metric].mean()
                    else:
                        region_metric = df.groupby("region", as_index=False)[selected_metric].sum()
                    region_metric = region_metric.sort_values(selected_metric, ascending=False)
                    fig = create_bar_chart(region_metric, "region", selected_metric,
                                           title=f"{selected_metric_label} by Region", y_prefix=prefix)
                    safe_plotly_chart(fig, key="sa_region")

            # Chart 3: Retailer Performance
            with c2:
                if "retailer" in available:
                    if selected_metric == "price_per_unit":
                        ret_metric = df.groupby("retailer", as_index=False)[selected_metric].mean()
                    else:
                        ret_metric = df.groupby("retailer", as_index=False)[selected_metric].sum()
                    ret_metric = ret_metric.sort_values(selected_metric, ascending=True)
                    fig = create_bar_chart(ret_metric, "retailer", selected_metric,
                                           title=f"Retailer {selected_metric_label}",
                                           horizontal=True, y_prefix=prefix)
                    safe_plotly_chart(fig, key="sa_retailer")

            c3, c4 = st.columns(2)

            # Chart 4: Sales Method
            with c3:
                if "sales_method" in available:
                    if selected_metric == "price_per_unit":
                        method_data = df.groupby("sales_method", as_index=False)[selected_metric].mean()
                    else:
                        method_data = df.groupby("sales_method", as_index=False)[selected_metric].sum()
                    method_data = method_data.sort_values(selected_metric, ascending=False)
                    fig = create_bar_chart(method_data, "sales_method", selected_metric,
                                           title=f"{selected_metric_label} by Sales Method", y_prefix=prefix)
                    safe_plotly_chart(fig, key="sa_method")

            # Chart 5: Monthly Performance
            with c4:
                if "month" in df.columns:
                    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
                    if selected_metric == "price_per_unit":
                        monthly_perf = df.groupby("month", as_index=False)[selected_metric].mean()
                    else:
                        monthly_perf = df.groupby("month", as_index=False)[selected_metric].sum()
                    monthly_perf["month_label"] = monthly_perf["month"].map(month_names)
                    monthly_perf = monthly_perf.sort_values("month")
                    fig = create_bar_chart(monthly_perf, "month_label", selected_metric,
                                           title=f"Monthly {selected_metric_label}", y_prefix=prefix)
                    safe_plotly_chart(fig, key="sa_monthly")

            # Chart 6: Metric Comparison (normalized per-region)
            if ("region" in available and "total_sales" in available
                    and "units_sold" in available and "operating_profit" in available):
                st.markdown(
                    '<div class="section-header">📊 Multi-Metric Comparison by Region (Normalized %)</div>',
                    unsafe_allow_html=True,
                )
                compare = df.groupby("region", as_index=False).agg(
                    Revenue=("total_sales", "sum"),
                    Units=("units_sold", "sum"),
                    Profit=("operating_profit", "sum"),
                )
                # Normalize each metric to percentage of max for fair comparison
                for col in ["Revenue", "Units", "Profit"]:
                    max_val = compare[col].max()
                    if max_val > 0:
                        compare[f"{col}_pct"] = compare[col] / max_val * 100
                    else:
                        compare[f"{col}_pct"] = 0
                fig = create_grouped_bar_chart(compare, "region",
                                               ["Revenue_pct", "Units_pct", "Profit_pct"],
                                               labels=["Revenue %", "Units %", "Profit %"],
                                               title="Normalized Metric Comparison (% of Max)")
                safe_plotly_chart(fig, key="sa_comparison")

            with st.expander("📋 View Detailed Data"):
                display_cols = [c for c in ["date","retailer","region","product","units_sold",
                                             "total_sales","operating_profit","sales_method"]
                               if c in df.columns]
                st.dataframe(df[display_cols].head(500), use_container_width=True, height=400)

# ===== TAB 3 — PRODUCT & REGION ANALYSIS =====
with tab3:
    st.markdown("## 👟 Product & Region Analysis")
    st.markdown("*Deep-dive into product performance and regional breakdowns*")
    st.markdown("")

    if df.empty:
        no_data_message()
    else:
        # ---- PRODUCT ANALYSIS ----
        st.markdown('<div class="section-header">🏷️ Product Analysis</div>', unsafe_allow_html=True)

        if "product" in available and "total_sales" in available:
            # Build aggregation safely
            agg_spec = {"Revenue": ("total_sales", "sum")}
            if "operating_profit" in available:
                agg_spec["Profit"] = ("operating_profit", "sum")
            if "units_sold" in available:
                agg_spec["Units"] = ("units_sold", "sum")
            if "price_per_unit" in available:
                agg_spec["Avg_Price"] = ("price_per_unit", "mean")

            prod_agg = df.groupby("product", as_index=False).agg(**agg_spec)

            c1, c2 = st.columns(2)
            with c1:
                top_rev = prod_agg.sort_values("Revenue", ascending=True).tail(10)
                fig = create_bar_chart(top_rev, "product", "Revenue",
                                       title="Top Products by Revenue", horizontal=True, y_prefix=CURRENCY)
                safe_plotly_chart(fig, key="pr_top_rev")
            with c2:
                if "Profit" in prod_agg.columns:
                    top_profit = prod_agg.sort_values("Profit", ascending=True).tail(10)
                    fig = create_bar_chart(top_profit, "product", "Profit",
                                           title="Product Profitability", horizontal=True, y_prefix=CURRENCY,
                                           color_sequence=["#FF6B6B","#FF8E8E","#FFB4B4","#4ECDC4","#45B7D1","#96CEB4"])
                    safe_plotly_chart(fig, key="pr_top_profit")

            c3, c4 = st.columns(2)
            with c3:
                if "Units" in prod_agg.columns:
                    top_units = prod_agg.sort_values("Units", ascending=False)
                    fig = create_bar_chart(top_units, "product", "Units",
                                           title="Units Sold by Product", y_prefix="")
                    safe_plotly_chart(fig, key="pr_units")
            with c4:
                if "Avg_Price" in prod_agg.columns and "Units" in prod_agg.columns:
                    fig = create_scatter_chart(
                        prod_agg, "Avg_Price", "Units",
                        title="Price vs Units Sold",
                        x_label="Average Price ($)", y_label="Total Units Sold",
                    )
                    # Add product labels
                    for _, row in prod_agg.iterrows():
                        short_name = row["product"]
                        if "'s " in short_name:
                            short_name = short_name.split("'s ")[-1]
                        fig.add_annotation(
                            x=row["Avg_Price"], y=row["Units"],
                            text=short_name[:15],
                            showarrow=False, yshift=14,
                            font=dict(size=9, color="#8B8D94"),
                        )
                    safe_plotly_chart(fig, key="pr_scatter")

        # ---- REGION ANALYSIS ----
        st.markdown("")
        st.markdown('<div class="section-header">🌍 Region Analysis</div>', unsafe_allow_html=True)

        if "region" in available and "total_sales" in available:
            region_agg_spec = {"Revenue": ("total_sales", "sum")}
            if "operating_profit" in available:
                region_agg_spec["Profit"] = ("operating_profit", "sum")
            if "units_sold" in available:
                region_agg_spec["Units"] = ("units_sold", "sum")

            region_agg = df.groupby("region", as_index=False).agg(**region_agg_spec)

            c1, c2, c3 = st.columns(3)
            with c1:
                ra = region_agg.sort_values("Revenue", ascending=False)
                fig = create_bar_chart(ra, "region", "Revenue", title="Revenue by Region",
                                       y_prefix=CURRENCY, height=380)
                safe_plotly_chart(fig, key="pr_reg_rev")
            with c2:
                if "Profit" in region_agg.columns:
                    ra = region_agg.sort_values("Profit", ascending=False)
                    fig = create_bar_chart(ra, "region", "Profit", title="Profit by Region",
                                           y_prefix=CURRENCY, height=380,
                                           color_sequence=["#FF6B6B","#FF8E8E","#FFB4B4","#FFEAA7","#DDA0DD"])
                    safe_plotly_chart(fig, key="pr_reg_profit")
            with c3:
                if "Units" in region_agg.columns:
                    ra = region_agg.sort_values("Units", ascending=False)
                    fig = create_bar_chart(ra, "region", "Units", title="Units by Region",
                                           y_prefix="", height=380,
                                           color_sequence=["#45B7D1","#4ECDC4","#96CEB4","#A8E6CF","#FFEAA7"])
                    safe_plotly_chart(fig, key="pr_reg_units")

            # Drill-down: Region → State → City
            if "state" in available:
                st.markdown('<div class="section-header">🔍 Regional Drill-Down</div>', unsafe_allow_html=True)
                st.markdown("*Select a region to explore state and city performance*")

                regions_list = sorted(df["region"].dropna().unique().tolist())
                if regions_list:
                    selected_region = st.selectbox("Select Region", regions_list, key="drilldown_region")

                    region_df = df[df["region"] == selected_region]

                    if not region_df.empty:
                        state_agg = region_df.groupby("state", as_index=False).agg(
                            Revenue=("total_sales", "sum"),
                        ).sort_values("Revenue", ascending=True)

                        c1, c2 = st.columns(2)
                        with c1:
                            fig = create_bar_chart(state_agg, "state", "Revenue",
                                                   title=f"States in {selected_region} — Revenue",
                                                   horizontal=True, y_prefix=CURRENCY)
                            safe_plotly_chart(fig, key="pr_drill_state")

                        with c2:
                            if "city" in available:
                                states_in_region = sorted(region_df["state"].dropna().unique().tolist())
                                if states_in_region:
                                    selected_state = st.selectbox("Select State", states_in_region,
                                                                  key="drilldown_state")
                                    state_df = region_df[region_df["state"] == selected_state]
                                    if not state_df.empty:
                                        city_agg = state_df.groupby("city", as_index=False).agg(
                                            Revenue=("total_sales", "sum"),
                                        ).sort_values("Revenue", ascending=True)
                                        fig = create_bar_chart(city_agg, "city", "Revenue",
                                                               title=f"Cities in {selected_state} — Revenue",
                                                               horizontal=True, y_prefix=CURRENCY)
                                        safe_plotly_chart(fig, key="pr_drill_city")

        # Data table
        with st.expander("📋 View Detailed Data"):
            display_cols = [c for c in ["date","product","region","state","city","retailer",
                                         "units_sold","total_sales","operating_profit","price_per_unit"]
                           if c in df.columns]
            st.dataframe(df[display_cols].head(500), use_container_width=True, height=400)

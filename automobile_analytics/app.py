"""
app.py  –  Automobile Parts India  |  Sales Analytics Dashboard
----------------------------------------------------------------
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_and_clean, get_summary_stats

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Automobile Parts India — Sales Analytics",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* ── Global font & background ── */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        .main > div { padding-top: 1rem; }

        /* ── Hero card ── */
        .hero-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 32px 36px 28px 36px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            gap: 28px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        .hero-icon {
            flex-shrink: 0;
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #0ea5e9 0%, #0066cc 100%);
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hero-text h1 {
            margin: 0 0 6px 0;
            font-size: 1.75rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.3px;
        }
        .hero-text p {
            margin: 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .hero-badge {
            margin-left: auto;
            flex-shrink: 0;
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #0369a1;
            white-space: nowrap;
        }

        /* ── Metric cards ── */
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px 20px 14px 20px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            transition: box-shadow 0.2s;
        }
        [data-testid="stMetric"]:hover {
            box-shadow: 0 4px 16px rgba(0,102,204,0.12);
        }
        [data-testid="stMetricLabel"] > div {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #64748b !important;
        }
        [data-testid="stMetricValue"] > div {
            font-size: 1.45rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }

        /* ── Section headers ── */
        .section-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            border-left: 4px solid #0066cc;
            padding: 4px 0 4px 12px;
            margin-top: 1.8rem;
            margin-bottom: 0.75rem;
            letter-spacing: -0.1px;
        }

        /* ── Insight / warning boxes ── */
        .insight-box {
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-left: 4px solid #0ea5e9;
            border-radius: 10px;
            padding: 14px 18px;
            margin-top: 10px;
            font-size: 0.91rem;
            color: #0c4a6e;
            line-height: 1.6;
        }
        .warning-box {
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 14px 18px;
            margin-top: 10px;
            font-size: 0.91rem;
            color: #78350f;
            line-height: 1.6;
        }

        /* ── Sidebar polish ── */
        [data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        [data-testid="stSidebar"] .sidebar-logo-wrap {
            background: linear-gradient(135deg, #0ea5e9, #0066cc);
            border-radius: 14px;
            padding: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 6px;
        }
        [data-testid="stSidebar"] .sidebar-logo-title {
            color: #ffffff;
            font-weight: 800;
            font-size: 1.05rem;
        }
        [data-testid="stSidebar"] .sidebar-logo-sub {
            color: #bae6fd;
            font-size: 0.75rem;
        }
        .filter-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #64748b;
            margin-bottom: 2px;
        }

        /* ── Tab bar ── */
        [data-testid="stTabs"] [role="tab"] {
            font-weight: 600;
            font-size: 0.88rem;
            padding: 8px 16px;
            border-radius: 8px 8px 0 0;
            color: #475569;
        }
        [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
            color: #0066cc;
            border-bottom: 3px solid #0066cc;
        }

        /* ── Dataframe header ── */
        [data-testid="stDataFrame"] thead th {
            background: #f1f5f9 !important;
            font-weight: 700 !important;
            color: #334155 !important;
            font-size: 0.82rem !important;
        }

        /* ── Divider ── */
        hr { border-color: #e2e8f0 !important; margin: 1.2rem 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Data loading (cached)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data(show_spinner="Loading dataset…")
def get_data():
    df = load_and_clean()
    missing = load_and_clean.missing_report
    return df, missing


df, missing_report = get_data()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Sidebar — global filters
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    # ── Branded sidebar header ────────────────────────────────────────────
    st.markdown(
        """
        <div class="sidebar-logo-wrap">
            <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                <rect width="36" height="36" rx="10" fill="white" fill-opacity="0.15"/>
                <rect x="4" y="22" width="6" height="10" rx="2" fill="white"/>
                <rect x="12" y="16" width="6" height="16" rx="2" fill="white" fill-opacity="0.85"/>
                <rect x="20" y="10" width="6" height="22" rx="2" fill="white" fill-opacity="0.7"/>
                <rect x="28" y="5" width="6" height="27" rx="2" fill="white" fill-opacity="0.55"/>
                <polyline points="7,21 15,15 23,9 31,4" stroke="white" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <circle cx="31" cy="4" r="2.5" fill="white"/>
            </svg>
            <div>
                <div class="sidebar-logo-title">Auto Parts India</div>
                <div class="sidebar-logo-sub">Sales Analytics · 1,000 Records</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    all_suppliers     = sorted(df["supplier"].unique())
    all_categories    = sorted(df["component_category"].unique())
    all_oems          = sorted(df["target_oem"].unique())
    all_locations     = sorted(df["plant_location"].unique())
    all_stock_status  = sorted(df["stock_status"].unique())

    st.markdown('<p class="filter-label">Supplier</p>', unsafe_allow_html=True)
    sel_suppliers  = st.multiselect("", all_suppliers,  default=all_suppliers,
                                    key="sup", label_visibility="collapsed")

    st.markdown('<p class="filter-label">Component Category</p>', unsafe_allow_html=True)
    sel_categories = st.multiselect("", all_categories, default=all_categories,
                                    key="cat", label_visibility="collapsed")

    st.markdown('<p class="filter-label">Target OEM</p>', unsafe_allow_html=True)
    sel_oems       = st.multiselect("", all_oems,       default=all_oems,
                                    key="oem", label_visibility="collapsed")

    st.markdown('<p class="filter-label">Plant Location</p>', unsafe_allow_html=True)
    sel_locations  = st.multiselect("", all_locations,  default=all_locations,
                                    key="loc", label_visibility="collapsed")

    st.markdown('<p class="filter-label">Stock Status</p>', unsafe_allow_html=True)
    sel_stock      = st.multiselect("", all_stock_status, default=all_stock_status,
                                    key="stk", label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<p class="filter-label">Batch Quantity Range</p>', unsafe_allow_html=True)
    min_qty, max_qty = int(df["batch_quantity"].min()), int(df["batch_quantity"].max())
    qty_range = st.slider("", min_qty, max_qty, (min_qty, max_qty),
                          key="qty", label_visibility="collapsed")

# ── Apply filters ─────────────────────────────────────────────────────────
fdf = df[
    df["supplier"].isin(sel_suppliers) &
    df["component_category"].isin(sel_categories) &
    df["target_oem"].isin(sel_oems) &
    df["plant_location"].isin(sel_locations) &
    df["stock_status"].isin(sel_stock) &
    df["batch_quantity"].between(qty_range[0], qty_range[1])
].copy()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Hero card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <rect x="3" y="26" width="7" height="11" rx="2" fill="white"/>
                <rect x="13" y="19" width="7" height="18" rx="2" fill="white" fill-opacity="0.85"/>
                <rect x="23" y="12" width="7" height="25" rx="2" fill="white" fill-opacity="0.7"/>
                <rect x="33" y="5"  width="7" height="32" rx="2" fill="white" fill-opacity="0.55"/>
                <polyline points="6.5,25 16.5,18 26.5,11 36.5,4.5"
                    stroke="white" stroke-width="2.2"
                    stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <circle cx="36.5" cy="4.5" r="3" fill="white"/>
            </svg>
        </div>
        <div class="hero-text">
            <h1>Automobile Parts India</h1>
            <p>Sales Analytics Dashboard &nbsp;·&nbsp; End-to-end data analytics covering
            data quality, sales computation, category insights,
            supplier benchmarking, and inventory intelligence.</p>
        </div>
        <div class="hero-badge">📦 1,000 Records · 7 Suppliers · 9 OEMs</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Navigation tabs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tabs = st.tabs([
    "📋 Overview",
    "🔍 Data Quality",
    "💰 Sales Analysis",
    "📦 Category & OEM Insights",
    "🏭 Supplier Benchmarking",
    "📊 Inventory Intelligence",
    "💡 Business Decisions",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Dataset at a Glance</div>',
                unsafe_allow_html=True)

    total_records    = len(fdf)
    total_sales      = fdf["sales_inr"].sum()
    avg_unit_cost    = fdf["unit_cost_inr"].mean()
    total_gst        = fdf["gst_amount_inr"].sum()
    total_final_val  = fdf["final_value_with_gst_inr"].sum()
    avg_lead_time    = fdf["lead_time_days"].mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Parts",         f"{total_records:,}")
    c2.metric("Total Sales (₹)",     f"₹{total_sales/1e7:.2f} Cr")
    c3.metric("Avg Unit Cost (₹)",   f"₹{avg_unit_cost:,.0f}")
    c4.metric("Total GST (₹)",       f"₹{total_gst/1e7:.2f} Cr")
    c5.metric("Final Value (₹)",     f"₹{total_final_val/1e7:.2f} Cr")
    c6.metric("Avg Lead Time",       f"{avg_lead_time:.1f} days")

    st.markdown("---")
    st.markdown('<div class="section-header">Raw Data Preview</div>',
                unsafe_allow_html=True)
    display_cols = [
        "part_id", "supplier", "target_oem", "plant_location",
        "component_category", "stock_status", "batch_quantity",
        "unit_cost_inr", "sales_inr", "gst_rate_pct",
        "final_value_with_gst_inr", "lead_time_days",
    ]
    st.dataframe(
        fdf[display_cols]
        .rename(columns={
            "part_id": "Part ID", "supplier": "Supplier",
            "target_oem": "Target OEM", "plant_location": "Plant Location",
            "component_category": "Category", "stock_status": "Stock Status",
            "batch_quantity": "Qty", "unit_cost_inr": "Unit Cost (₹)",
            "sales_inr": "Sales (₹)", "gst_rate_pct": "GST %",
            "final_value_with_gst_inr": "Final Value (₹)",
            "lead_time_days": "Lead Time (Days)",
        })
        .style.format({
            "Unit Cost (₹)": "₹{:,.0f}",
            "Sales (₹)": "₹{:,.0f}",
            "Final Value (₹)": "₹{:,.0f}",
            "GST %": "{:.0f}%",
        }),
        use_container_width=True,
        height=420,
    )

    st.markdown('<div class="section-header">Descriptive Statistics</div>',
                unsafe_allow_html=True)
    summary = get_summary_stats(fdf)
    st.dataframe(summary.style.format("{:,.2f}"), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA QUALITY
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Missing Value Report</div>',
                unsafe_allow_html=True)

    if missing_report.empty:
        st.markdown(
            '<div class="insight-box">✅ No missing values detected in the dataset. '
            "All 1,000 records are complete.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.dataframe(missing_report, use_container_width=True)

    st.markdown('<div class="section-header">Data Types & Column Info</div>',
                unsafe_allow_html=True)
    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Count": df.notnull().sum().values,
        "Unique Values": [df[c].nunique() for c in df.columns],
    })
    dtype_df = dtype_df[dtype_df["Column"] != "_missing_report"]
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Duplicate Records</div>',
                unsafe_allow_html=True)
    dup_count = df.duplicated(subset=["part_id"]).sum()
    if dup_count == 0:
        st.markdown(
            '<div class="insight-box">✅ No duplicate Part IDs found.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="warning-box">⚠️ {dup_count} duplicate Part IDs detected. '
            "Review them before proceeding.</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header">Unit Cost Distribution</div>',
                unsafe_allow_html=True)
    fig_hist = px.histogram(
        fdf, x="unit_cost_inr", nbins=40,
        color="component_category",
        labels={"unit_cost_inr": "Unit Cost (₹)", "count": "Count"},
        title="Unit Cost Distribution by Component Category",
        template="plotly_white",
    )
    fig_hist.update_layout(bargap=0.05, legend_title_text="Category")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown('<div class="section-header">GST Rate Breakdown</div>',
                unsafe_allow_html=True)
    gst_counts = fdf["gst_rate_pct"].value_counts().reset_index()
    gst_counts.columns = ["GST Rate (%)", "Count"]
    fig_gst = px.bar(
        gst_counts, x="GST Rate (%)", y="Count",
        color="GST Rate (%)", text="Count",
        title="Number of Parts by GST Rate",
        template="plotly_white",
        color_continuous_scale="Blues",
    )
    fig_gst.update_traces(textposition="outside")
    st.plotly_chart(fig_gst, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SALES ANALYSIS   (Sales = Batch Quantity × Unit Cost)
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(
        '<div class="section-header">'
        "Sales = Batch Quantity × Unit Cost (INR)"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="insight-box">'
        "Sales revenue is computed as <strong>Batch Quantity × Unit Cost (INR)</strong>. "
        "This represents the gross revenue before GST for each part batch."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Top-level KPIs ────────────────────────────────────────────────────
    st.markdown("#### Key Sales Metrics")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sales",         f"₹{fdf['sales_inr'].sum()/1e9:.3f} B")
    k2.metric("Average Sales/Part",  f"₹{fdf['sales_inr'].mean():,.0f}")
    k3.metric("Median Sales/Part",   f"₹{fdf['sales_inr'].median():,.0f}")
    k4.metric("Highest Single Batch",f"₹{fdf['sales_inr'].max():,.0f}")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    # ── Sales by Category ─────────────────────────────────────────────────
    with col_l:
        st.markdown('<div class="section-header">Sales by Component Category</div>',
                    unsafe_allow_html=True)
        cat_sales = (
            fdf.groupby("component_category")["sales_inr"]
            .agg(total="sum", avg="mean", count="count")
            .reset_index()
            .sort_values("total", ascending=False)
        )
        cat_sales["total_cr"] = (cat_sales["total"] / 1e7).round(2)
        fig_cat = px.bar(
            cat_sales, x="component_category", y="total_cr",
            color="component_category",
            text=cat_sales["total_cr"].apply(lambda v: f"₹{v:.1f} Cr"),
            labels={"component_category": "Category", "total_cr": "Sales (₹ Cr)"},
            title="Total Sales by Category",
            template="plotly_white",
        )
        fig_cat.update_traces(textposition="outside")
        fig_cat.update_layout(showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.dataframe(
            cat_sales[["component_category", "total_cr", "avg", "count"]]
            .rename(columns={
                "component_category": "Category",
                "total_cr": "Total Sales (₹ Cr)",
                "avg": "Avg Sales (₹)",
                "count": "Parts Count",
            })
            .style.format({"Total Sales (₹ Cr)": "{:.2f}", "Avg Sales (₹)": "₹{:,.0f}"}),
            use_container_width=True, hide_index=True,
        )

    # ── Sales by Supplier ─────────────────────────────────────────────────
    with col_r:
        st.markdown('<div class="section-header">Sales by Supplier</div>',
                    unsafe_allow_html=True)
        sup_sales = (
            fdf.groupby("supplier")["sales_inr"]
            .agg(total="sum", avg="mean", count="count")
            .reset_index()
            .sort_values("total", ascending=False)
        )
        sup_sales["total_cr"] = (sup_sales["total"] / 1e7).round(2)
        fig_sup = px.bar(
            sup_sales, x="supplier", y="total_cr",
            color="supplier",
            text=sup_sales["total_cr"].apply(lambda v: f"₹{v:.1f} Cr"),
            labels={"supplier": "Supplier", "total_cr": "Sales (₹ Cr)"},
            title="Total Sales by Supplier",
            template="plotly_white",
        )
        fig_sup.update_traces(textposition="outside")
        fig_sup.update_layout(showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_sup, use_container_width=True)
        st.dataframe(
            sup_sales[["supplier", "total_cr", "avg", "count"]]
            .rename(columns={
                "supplier": "Supplier",
                "total_cr": "Total Sales (₹ Cr)",
                "avg": "Avg Sales (₹)",
                "count": "Parts Count",
            })
            .style.format({"Total Sales (₹ Cr)": "{:.2f}", "Avg Sales (₹)": "₹{:,.0f}"}),
            use_container_width=True, hide_index=True,
        )

    # ── Sales distribution scatter ────────────────────────────────────────
    st.markdown('<div class="section-header">Batch Quantity vs Sales</div>',
                unsafe_allow_html=True)
    fig_scatter = px.scatter(
        fdf, x="batch_quantity", y="sales_inr",
        color="component_category",
        size="unit_cost_inr",
        hover_data=["part_id", "supplier", "target_oem"],
        labels={
            "batch_quantity": "Batch Quantity",
            "sales_inr": "Sales (₹)",
            "component_category": "Category",
        },
        title="Batch Quantity vs Sales — coloured by Category, sized by Unit Cost",
        template="plotly_white",
        opacity=0.7,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ── Top 10 parts by sales ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Top 15 Parts by Sales Revenue</div>',
                unsafe_allow_html=True)
    top15 = (
        fdf[["part_id", "supplier", "component_category",
             "batch_quantity", "unit_cost_inr", "sales_inr"]]
        .sort_values("sales_inr", ascending=False)
        .head(15)
        .rename(columns={
            "part_id": "Part ID", "supplier": "Supplier",
            "component_category": "Category",
            "batch_quantity": "Qty", "unit_cost_inr": "Unit Cost (₹)",
            "sales_inr": "Sales (₹)",
        })
    )
    st.dataframe(
        top15.style.format({"Unit Cost (₹)": "₹{:,.0f}", "Sales (₹)": "₹{:,.0f}"}),
        use_container_width=True, hide_index=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — CATEGORY & OEM INSIGHTS
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    col_l, col_r = st.columns(2)

    # ── Category pie ──────────────────────────────────────────────────────
    with col_l:
        st.markdown('<div class="section-header">Category Share of Total Sales</div>',
                    unsafe_allow_html=True)
        cat_pie = fdf.groupby("component_category")["sales_inr"].sum().reset_index()
        fig_pie = px.pie(
            cat_pie, names="component_category", values="sales_inr",
            title="Sales Share by Category",
            hole=0.4,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── OEM pie ───────────────────────────────────────────────────────────
    with col_r:
        st.markdown('<div class="section-header">OEM Share of Total Sales</div>',
                    unsafe_allow_html=True)
        oem_pie = fdf.groupby("target_oem")["sales_inr"].sum().reset_index()
        fig_oem_pie = px.pie(
            oem_pie, names="target_oem", values="sales_inr",
            title="Sales Share by Target OEM",
            hole=0.4,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_oem_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_oem_pie, use_container_width=True)

    # ── OEM × Category heatmap ────────────────────────────────────────────
    st.markdown('<div class="section-header">OEM × Category Sales Heatmap (₹ Cr)</div>',
                unsafe_allow_html=True)
    pivot = (
        fdf.groupby(["target_oem", "component_category"])["sales_inr"]
        .sum()
        .unstack(fill_value=0)
        / 1e7
    ).round(2)
    fig_heat = px.imshow(
        pivot,
        labels=dict(x="Component Category", y="Target OEM", color="Sales (₹ Cr)"),
        title="Sales Heatmap: OEM vs Component Category",
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        template="plotly_white",
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Avg unit cost per OEM ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Average Unit Cost per Target OEM</div>',
                unsafe_allow_html=True)
    oem_cost = (
        fdf.groupby("target_oem")["unit_cost_inr"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_oem_cost = px.bar(
        oem_cost, x="target_oem", y="unit_cost_inr",
        color="unit_cost_inr",
        text=oem_cost["unit_cost_inr"].apply(lambda v: f"₹{v:,.0f}"),
        labels={"target_oem": "Target OEM", "unit_cost_inr": "Avg Unit Cost (₹)"},
        title="Average Unit Cost per OEM",
        template="plotly_white",
        color_continuous_scale="Viridis",
    )
    fig_oem_cost.update_traces(textposition="outside")
    fig_oem_cost.update_layout(xaxis_tickangle=-30, coloraxis_showscale=False)
    st.plotly_chart(fig_oem_cost, use_container_width=True)

    # ── Parts count per location ──────────────────────────────────────────
    st.markdown('<div class="section-header">Parts Count by Plant Location</div>',
                unsafe_allow_html=True)
    loc_cnt = fdf["plant_location"].value_counts().reset_index()
    loc_cnt.columns = ["Plant Location", "Count"]
    fig_loc = px.bar(
        loc_cnt, x="Plant Location", y="Count",
        color="Count", text="Count",
        title="Number of Parts per Plant Location",
        template="plotly_white",
        color_continuous_scale="Teal",
    )
    fig_loc.update_traces(textposition="outside")
    fig_loc.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_loc, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — SUPPLIER BENCHMARKING
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Supplier Performance Overview</div>',
                unsafe_allow_html=True)

    sup_bench = (
        fdf.groupby("supplier")
        .agg(
            total_sales=("sales_inr", "sum"),
            avg_sales=("sales_inr", "mean"),
            total_parts=("part_id", "count"),
            avg_unit_cost=("unit_cost_inr", "mean"),
            avg_lead_time=("lead_time_days", "mean"),
            total_gst=("gst_amount_inr", "sum"),
            avg_batch_qty=("batch_quantity", "mean"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )
    sup_bench["total_sales_cr"] = (sup_bench["total_sales"] / 1e7).round(2)

    st.dataframe(
        sup_bench[[
            "supplier", "total_sales_cr", "avg_unit_cost",
            "avg_lead_time", "total_parts", "avg_batch_qty",
        ]]
        .rename(columns={
            "supplier": "Supplier",
            "total_sales_cr": "Total Sales (₹ Cr)",
            "avg_unit_cost": "Avg Unit Cost (₹)",
            "avg_lead_time": "Avg Lead Time (Days)",
            "total_parts": "Parts Count",
            "avg_batch_qty": "Avg Batch Qty",
        })
        .style.format({
            "Total Sales (₹ Cr)": "{:.2f}",
            "Avg Unit Cost (₹)": "₹{:,.0f}",
            "Avg Lead Time (Days)": "{:.1f}",
            "Avg Batch Qty": "{:.0f}",
        }),
        use_container_width=True, hide_index=True,
    )

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-header">Avg Lead Time by Supplier</div>',
                    unsafe_allow_html=True)
        fig_lt = px.bar(
            sup_bench.sort_values("avg_lead_time"),
            x="avg_lead_time", y="supplier",
            orientation="h",
            color="avg_lead_time",
            text=sup_bench.sort_values("avg_lead_time")["avg_lead_time"].apply(
                lambda v: f"{v:.1f} d"
            ),
            labels={"avg_lead_time": "Avg Lead Time (Days)", "supplier": "Supplier"},
            title="Average Lead Time by Supplier",
            template="plotly_white",
            color_continuous_scale="RdYlGn_r",
        )
        fig_lt.update_traces(textposition="outside")
        fig_lt.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_lt, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">Avg Unit Cost by Supplier</div>',
                    unsafe_allow_html=True)
        fig_uc = px.bar(
            sup_bench.sort_values("avg_unit_cost"),
            x="avg_unit_cost", y="supplier",
            orientation="h",
            color="avg_unit_cost",
            text=sup_bench.sort_values("avg_unit_cost")["avg_unit_cost"].apply(
                lambda v: f"₹{v:,.0f}"
            ),
            labels={"avg_unit_cost": "Avg Unit Cost (₹)", "supplier": "Supplier"},
            title="Average Unit Cost by Supplier",
            template="plotly_white",
            color_continuous_scale="Blues",
        )
        fig_uc.update_traces(textposition="outside")
        fig_uc.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_uc, use_container_width=True)

    # ── Radar chart — supplier scorecard ─────────────────────────────────
    st.markdown('<div class="section-header">Supplier Multi-Metric Scorecard (Radar)</div>',
                unsafe_allow_html=True)

    # Normalise metrics 0→1 (higher = better for sales; lower = better for cost & lead time)
    radar_df = sup_bench.copy()
    for col, invert in [
        ("total_sales_cr", False),
        ("avg_unit_cost", True),
        ("avg_lead_time", True),
        ("avg_batch_qty", False),
        ("total_parts", False),
    ]:
        mn, mx = radar_df[col].min(), radar_df[col].max()
        norm = (radar_df[col] - mn) / (mx - mn + 1e-9)
        radar_df[f"norm_{col}"] = 1 - norm if invert else norm

    categories = ["Sales Volume", "Cost Efficiency", "Speed",
                  "Batch Size", "Part Count"]
    norm_cols   = ["norm_total_sales_cr", "norm_avg_unit_cost",
                   "norm_avg_lead_time", "norm_avg_batch_qty", "norm_total_parts"]

    fig_radar = go.Figure()
    colors_radar = px.colors.qualitative.Set1
    for i, row in radar_df.iterrows():
        values = [row[c] for c in norm_cols]
        values += [values[0]]  # close the polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["supplier"],
            opacity=0.6,
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Normalised Supplier Scorecard",
        template="plotly_white",
        height=480,
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — INVENTORY INTELLIGENCE
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Stock Status Overview</div>',
                unsafe_allow_html=True)

    stock_cnt  = fdf["stock_status"].value_counts().reset_index()
    stock_cnt.columns = ["Stock Status", "Count"]
    stock_sales = (
        fdf.groupby("stock_status")["sales_inr"]
        .sum()
        .reset_index()
        .rename(columns={"stock_status": "Stock Status", "sales_inr": "Total Sales (₹)"})
    )

    col_l, col_r = st.columns(2)
    with col_l:
        fig_stock_cnt = px.pie(
            stock_cnt, names="Stock Status", values="Count",
            title="Parts Distribution by Stock Status",
            hole=0.45, template="plotly_white",
            color_discrete_map={
                "Overstocked": "#ef4444",
                "Optimal Stock": "#22c55e",
                "Reorder Needed": "#f59e0b",
            },
        )
        fig_stock_cnt.update_traces(textinfo="percent+label+value")
        st.plotly_chart(fig_stock_cnt, use_container_width=True)

    with col_r:
        fig_stock_sales = px.bar(
            stock_sales, x="Stock Status", y="Total Sales (₹)",
            color="Stock Status",
            text=stock_sales["Total Sales (₹)"].apply(lambda v: f"₹{v/1e7:.1f} Cr"),
            title="Total Sales by Stock Status",
            template="plotly_white",
            color_discrete_map={
                "Overstocked": "#ef4444",
                "Optimal Stock": "#22c55e",
                "Reorder Needed": "#f59e0b",
            },
        )
        fig_stock_sales.update_traces(textposition="outside")
        fig_stock_sales.update_layout(showlegend=False)
        st.plotly_chart(fig_stock_sales, use_container_width=True)

    # ── Lead time box by category ─────────────────────────────────────────
    st.markdown('<div class="section-header">Lead Time Distribution by Category</div>',
                unsafe_allow_html=True)
    fig_box = px.box(
        fdf, x="component_category", y="lead_time_days",
        color="component_category",
        points="outliers",
        labels={"component_category": "Category", "lead_time_days": "Lead Time (Days)"},
        title="Lead Time Box Plot by Component Category",
        template="plotly_white",
    )
    fig_box.update_layout(showlegend=False, xaxis_tickangle=-20)
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Overstocked parts detail ──────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Overstocked Parts (High Risk)</div>',
                unsafe_allow_html=True)
    overstocked = (
        fdf[fdf["stock_status"] == "Overstocked"]
        [["part_id", "supplier", "component_category",
          "batch_quantity", "unit_cost_inr", "sales_inr", "lead_time_days"]]
        .sort_values("sales_inr", ascending=False)
    )
    st.markdown(
        f'<div class="warning-box">⚠️ <strong>{len(overstocked):,} parts</strong> '
        f"are currently overstocked — representing "
        f"<strong>₹{overstocked['sales_inr'].sum()/1e9:.2f} B</strong> in tied-up capital."
        "</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        overstocked
        .rename(columns={
            "part_id": "Part ID", "supplier": "Supplier",
            "component_category": "Category", "batch_quantity": "Qty",
            "unit_cost_inr": "Unit Cost (₹)", "sales_inr": "Sales (₹)",
            "lead_time_days": "Lead Time (d)",
        })
        .style.format({"Unit Cost (₹)": "₹{:,.0f}", "Sales (₹)": "₹{:,.0f}"}),
        use_container_width=True, height=380,
    )

    # ── Reorder-needed parts ──────────────────────────────────────────────
    st.markdown('<div class="section-header">🔴 Parts Requiring Immediate Reorder</div>',
                unsafe_allow_html=True)
    reorder = (
        fdf[fdf["stock_status"] == "Reorder Needed"]
        [["part_id", "supplier", "component_category",
          "batch_quantity", "unit_cost_inr", "lead_time_days"]]
        .sort_values("lead_time_days", ascending=False)
    )
    st.markdown(
        f'<div class="insight-box">📋 <strong>{len(reorder):,} parts</strong> need reorder. '
        f"Prioritise the {min(5,len(reorder))} with longest lead times shown below.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        reorder.head(20)
        .rename(columns={
            "part_id": "Part ID", "supplier": "Supplier",
            "component_category": "Category", "batch_quantity": "Qty",
            "unit_cost_inr": "Unit Cost (₹)", "lead_time_days": "Lead Time (d)",
        })
        .style.format({"Unit Cost (₹)": "₹{:,.0f}"}),
        use_container_width=True, hide_index=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — BUSINESS DECISIONS
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">📌 Data-Driven Business Insights & Recommendations</div>',
                unsafe_allow_html=True)

    # ── Build insights from filtered data ────────────────────────────────
    top_cat      = fdf.groupby("component_category")["sales_inr"].sum().idxmax()
    top_supplier = fdf.groupby("supplier")["sales_inr"].sum().idxmax()
    top_oem      = fdf.groupby("target_oem")["sales_inr"].sum().idxmax()
    top_loc      = fdf.groupby("plant_location")["sales_inr"].sum().idxmax()

    low_lead_sup  = fdf.groupby("supplier")["lead_time_days"].mean().idxmin()
    high_lead_sup = fdf.groupby("supplier")["lead_time_days"].mean().idxmax()

    over_count    = (fdf["stock_status"] == "Overstocked").sum()
    reorder_count = (fdf["stock_status"] == "Reorder Needed").sum()
    optimal_count = (fdf["stock_status"] == "Optimal Stock").sum()

    pct_over     = over_count    / len(fdf) * 100
    pct_reorder  = reorder_count / len(fdf) * 100
    pct_optimal  = optimal_count / len(fdf) * 100

    avg_lead_by_cat  = fdf.groupby("component_category")["lead_time_days"].mean()
    slowest_cat      = avg_lead_by_cat.idxmax()
    fastest_cat      = avg_lead_by_cat.idxmin()

    insights = [
        {
            "icon": "💰", "type": "Revenue", "colour": "insight-box",
            "title": f"Top Revenue Category: {top_cat}",
            "body": (
                f"<strong>{top_cat}</strong> generates the highest cumulative sales. "
                "Priority procurement and quality audits for this category will "
                "safeguard the bulk of revenue."
            ),
        },
        {
            "icon": "🏆", "type": "Supplier", "colour": "insight-box",
            "title": f"Top Performing Supplier: {top_supplier}",
            "body": (
                f"<strong>{top_supplier}</strong> drives the most sales volume. "
                "Expanding long-term contracts and strategic partnerships with this "
                "supplier will stabilise supply and unlock bulk discounts."
            ),
        },
        {
            "icon": "🚗", "type": "OEM", "colour": "insight-box",
            "title": f"Largest OEM Customer: {top_oem}",
            "body": (
                f"<strong>{top_oem}</strong> accounts for the greatest share of orders. "
                "Maintaining dedicated inventory buffers for this OEM will reduce "
                "the risk of production line stoppages."
            ),
        },
        {
            "icon": "⚡", "type": "Supply Chain", "colour": "insight-box",
            "title": f"Fastest Supplier: {low_lead_sup}",
            "body": (
                f"<strong>{low_lead_sup}</strong> has the shortest average lead time. "
                "For time-critical components, preference should be given to this "
                "supplier to minimise production delays."
            ),
        },
        {
            "icon": "🐢", "type": "Supply Chain Risk", "colour": "warning-box",
            "title": f"Slowest Supplier: {high_lead_sup}",
            "body": (
                f"<strong>{high_lead_sup}</strong> has the longest average lead time. "
                "Review capacity and consider dual-sourcing to mitigate single-supplier "
                "dependency risk."
            ),
        },
        {
            "icon": "📦", "type": "Inventory", "colour": "warning-box",
            "title": f"Overstocking: {pct_over:.1f}% of Parts",
            "body": (
                f"{over_count:,} parts ({pct_over:.1f}%) are overstocked, "
                "tying up capital and warehouse space. Implement JIT (Just-In-Time) "
                "ordering for slow-moving categories to reduce carrying costs."
            ),
        },
        {
            "icon": "🔴", "type": "Inventory Risk", "colour": "warning-box",
            "title": f"Reorder Alert: {pct_reorder:.1f}% of Parts Need Restocking",
            "body": (
                f"{reorder_count:,} parts ({pct_reorder:.1f}%) require immediate "
                "reorder. Cross-reference with lead times — longest-lead parts should "
                "be ordered first to prevent stockouts."
            ),
        },
        {
            "icon": "✅", "type": "Positive Signal", "colour": "insight-box",
            "title": f"Optimal Stock: {pct_optimal:.1f}% of Parts Well-Managed",
            "body": (
                f"{optimal_count:,} parts ({pct_optimal:.1f}%) are at optimal stock levels. "
                "Replicate the ordering patterns for these parts across the rest of "
                "the portfolio to drive better overall inventory health."
            ),
        },
        {
            "icon": "🌍", "type": "Location", "colour": "insight-box",
            "title": f"Highest-Sales Plant: {top_loc}",
            "body": (
                f"<strong>{top_loc}</strong> is the leading production hub by sales value. "
                "Infrastructure investments and capacity expansion here will yield "
                "the highest return."
            ),
        },
        {
            "icon": "⏱️", "type": "Category Lead Time", "colour": "warning-box",
            "title": f"Slowest Category to Procure: {slowest_cat}",
            "body": (
                f"<strong>{slowest_cat}</strong> has the longest average procurement lead time "
                f"({avg_lead_by_cat[slowest_cat]:.1f} days). Maintain a strategic safety stock "
                "for this category to prevent line stoppages."
            ),
        },
    ]

    for ins in insights:
        st.markdown(
            f'<div class="{ins["colour"]}">'
            f'<strong>{ins["icon"]} [{ins["type"]}] {ins["title"]}</strong><br>'
            f'{ins["body"]}'
            "</div><br>",
            unsafe_allow_html=True,
        )

    # ── Summary table ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Quick-Reference Decision Summary</div>',
                unsafe_allow_html=True)
    summary_tbl = pd.DataFrame([
        ["Top Revenue Category",       top_cat,        "Prioritise procurement & QA"],
        ["Top Supplier",               top_supplier,   "Expand long-term contracts"],
        ["Largest OEM Customer",       top_oem,        "Maintain dedicated buffer stock"],
        ["Fastest Supplier",           low_lead_sup,   "Prefer for time-critical parts"],
        ["Slowest Supplier",           high_lead_sup,  "Dual-source to reduce risk"],
        ["Overstocked Parts",          f"{over_count:,} ({pct_over:.1f}%)",
                                                       "Implement JIT ordering"],
        ["Reorder-Needed Parts",       f"{reorder_count:,} ({pct_reorder:.1f}%)",
                                                       "Initiate POs immediately"],
        ["Optimal-Stock Parts",        f"{optimal_count:,} ({pct_optimal:.1f}%)",
                                                       "Replicate ordering pattern"],
        ["Best Production Hub",        top_loc,        "Prioritise investment"],
        ["Slowest Procurement Category", slowest_cat,  "Maintain safety stock"],
    ], columns=["Metric", "Finding", "Recommended Action"])

    st.dataframe(summary_tbl, use_container_width=True, hide_index=True)


# ────────────────────────────────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#888;font-size:0.82rem;'>"
    "🔧 Automobile Parts India Sales Analytics · Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True,
)

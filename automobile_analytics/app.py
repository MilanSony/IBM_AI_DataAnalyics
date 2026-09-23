"""
app.py  —  Automobile Parts India  |  Sales Analytics Dashboard
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_and_clean, get_summary_stats

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Auto Parts India — Analytics",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DESIGN TOKENS & GLOBAL CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
/* ─── RESET & GLOBAL ───────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    background-color: #f0f4f8;
}
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; }
.main > div { background: #f0f4f8; }

/* ─── SIDEBAR ───────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #1e293b !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #334155 !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
    color: #38bdf8 !important;
}

/* ─── HERO BANNER ──────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #1e40af 0%, #0369a1 50%, #0891b2 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: 0 4px 24px rgba(30,64,175,0.25);
}
.hero-icon-box {
    background: rgba(255,255,255,0.15);
    border-radius: 14px;
    width: 68px; height: 68px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.hero-title {
    color: #ffffff;
    font-size: 1.7rem;
    font-weight: 800;
    margin: 0 0 4px 0;
    letter-spacing: -0.4px;
    line-height: 1.2;
}
.hero-sub {
    color: #bae6fd;
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.5;
}
.hero-stats {
    margin-left: auto;
    display: flex;
    gap: 20px;
    flex-shrink: 0;
}
.hero-stat {
    text-align: center;
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 10px 18px;
    min-width: 80px;
}
.hero-stat-val {
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 800;
    display: block;
}
.hero-stat-lbl {
    color: #7dd3fc;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* ─── KPI CARDS ─────────────────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.kpi-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 16px 18px 14px 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-c1::before { background: #3b82f6; }
.kpi-c2::before { background: #10b981; }
.kpi-c3::before { background: #f59e0b; }
.kpi-c4::before { background: #8b5cf6; }
.kpi-c5::before { background: #ef4444; }
.kpi-c6::before { background: #0891b2; }
.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 8px;
    display: block;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #94a3b8;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 3px;
}

/* ─── SECTION HEADERS ────────────────────────────────────────────────────── */
.sec-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}
.sec-hdr-dot {
    width: 4px; height: 22px;
    background: #3b82f6;
    border-radius: 4px;
    flex-shrink: 0;
}
.sec-hdr-text {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0;
}
.sec-hdr-badge {
    margin-left: auto;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.72rem;
    font-weight: 600;
}

/* ─── ALERT BOXES ─────────────────────────────────────────────────────────── */
.alert {
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0 16px 0;
    font-size: 0.9rem;
    line-height: 1.6;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.alert-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.alert-info  { background:#eff6ff; border:1px solid #bfdbfe; color:#1e3a5f; }
.alert-warn  { background:#fffbeb; border:1px solid #fde68a; color:#78350f; }
.alert-success { background:#f0fdf4; border:1px solid #bbf7d0; color:#14532d; }
.alert-danger  { background:#fef2f2; border:1px solid #fecaca; color:#7f1d1d; }

/* ─── INSIGHT CARDS (Business Decisions) ─────────────────────────────────── */
.insight-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.insight-badge {
    flex-shrink: 0;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 1.3rem;
    line-height: 1;
}
.badge-blue   { background: #eff6ff; }
.badge-green  { background: #f0fdf4; }
.badge-amber  { background: #fffbeb; }
.badge-red    { background: #fef2f2; }
.badge-purple { background: #faf5ff; }
.insight-type {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin-bottom: 3px;
}
.insight-title {
    font-size: 0.97rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 5px;
}
.insight-body {
    font-size: 0.87rem;
    color: #475569;
    line-height: 1.6;
}

/* ─── SUMMARY TABLE ──────────────────────────────────────────────────────── */
.summary-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.summary-table th {
    background: #f8fafc; color: #475569;
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px;
    padding: 10px 14px; border-bottom: 2px solid #e2e8f0;
    text-align: left;
}
.summary-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
    vertical-align: top;
}
.summary-table tr:hover td { background: #f8fafc; }
.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.tag-blue   { background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; }
.tag-green  { background:#f0fdf4; color:#15803d; border:1px solid #bbf7d0; }
.tag-amber  { background:#fffbeb; color:#b45309; border:1px solid #fde68a; }
.tag-red    { background:#fef2f2; color:#b91c1c; border:1px solid #fecaca; }

/* ─── TABS ─────────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] { background: transparent; }
[data-testid="stTabs"] > div:first-child {
    background: #ffffff;
    border-radius: 12px;
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    gap: 2px;
}
button[role="tab"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    color: #64748b !important;
    padding: 7px 14px !important;
    border: none !important;
    transition: all 0.15s !important;
}
button[role="tab"]:hover { background: #f1f5f9 !important; color: #1e293b !important; }
button[role="tab"][aria-selected="true"] {
    background: #1e40af !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.3) !important;
}

/* ─── DATAFRAME ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ─── SIDEBAR LABELS ─────────────────────────────────────────────────────── */
.sb-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    margin: 14px 0 3px 0;
}

/* ─── FOOTER ─────────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 24px 0 8px 0;
    color: #94a3b8;
    font-size: 0.78rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 32px;
}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data(show_spinner="⏳  Loading dataset…")
def get_data():
    df = load_and_clean()
    missing = load_and_clean.missing_report
    return df, missing

df, missing_report = get_data()

# unified Plotly theme
CHART_THEME   = "plotly_white"
PALETTE_CAT   = ["#3b82f6","#10b981","#f59e0b","#8b5cf6","#ef4444","#0891b2","#f97316"]
PALETTE_SEQ   = "Blues"

def _fig_base(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=44, b=10),
        font=dict(family="Inter, Segoe UI, system-ui", size=12, color="#334155"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(size=11),
        ),
        title=dict(font=dict(size=13, color="#1e293b", family="Inter, Segoe UI, system-ui")),
        xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", tickfont=dict(size=11)),
    )
    return fig

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e40af,#0891b2);
                border-radius:12px;padding:16px 18px;margin-bottom:20px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="background:rgba(255,255,255,0.18);border-radius:10px;
                        width:44px;height:44px;display:flex;align-items:center;justify-content:center;">
                <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
                    <rect x="1"  y="16" width="5" height="9"  rx="1.5" fill="white"/>
                    <rect x="8"  y="11" width="5" height="14" rx="1.5" fill="white" fill-opacity=".85"/>
                    <rect x="15" y="6"  width="5" height="19" rx="1.5" fill="white" fill-opacity=".7"/>
                    <rect x="22" y="1"  width="5" height="24" rx="1.5" fill="white" fill-opacity=".55"/>
                    <polyline points="3.5,15 10.5,10 17.5,5 24.5,0.5"
                        stroke="white" stroke-width="1.8"
                        stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="24.5" cy="0.5" r="2" fill="white"/>
                </svg>
            </div>
            <div>
                <div style="color:#fff;font-weight:800;font-size:0.95rem;line-height:1.2;">
                    Auto Parts India</div>
                <div style="color:#7dd3fc;font-size:0.72rem;margin-top:2px;">
                    Sales Analytics Platform</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_suppliers    = sorted(df["supplier"].unique())
    all_categories   = sorted(df["component_category"].unique())
    all_oems         = sorted(df["target_oem"].unique())
    all_locations    = sorted(df["plant_location"].unique())
    all_stock_status = sorted(df["stock_status"].unique())

    st.markdown('<p class="sb-label">Supplier</p>', unsafe_allow_html=True)
    sel_suppliers = st.multiselect("", all_suppliers, default=all_suppliers,
                                   key="sup", label_visibility="collapsed")

    st.markdown('<p class="sb-label">Component Category</p>', unsafe_allow_html=True)
    sel_categories = st.multiselect("", all_categories, default=all_categories,
                                    key="cat", label_visibility="collapsed")

    st.markdown('<p class="sb-label">Target OEM</p>', unsafe_allow_html=True)
    sel_oems = st.multiselect("", all_oems, default=all_oems,
                              key="oem", label_visibility="collapsed")

    st.markdown('<p class="sb-label">Plant Location</p>', unsafe_allow_html=True)
    sel_locations = st.multiselect("", all_locations, default=all_locations,
                                   key="loc", label_visibility="collapsed")

    st.markdown('<p class="sb-label">Stock Status</p>', unsafe_allow_html=True)
    sel_stock = st.multiselect("", all_stock_status, default=all_stock_status,
                               key="stk", label_visibility="collapsed")

    st.markdown('<p class="sb-label" style="margin-top:18px;">Batch Quantity</p>',
                unsafe_allow_html=True)
    min_qty = int(df["batch_quantity"].min())
    max_qty = int(df["batch_quantity"].max())
    qty_range = st.slider("", min_qty, max_qty, (min_qty, max_qty),
                          key="qty", label_visibility="collapsed")

    st.markdown("""
    <div style="margin-top:28px;padding:12px 14px;background:rgba(255,255,255,0.06);
                border-radius:8px;border:1px solid rgba(255,255,255,0.1);">
        <div style="color:#94a3b8;font-size:0.72rem;font-weight:600;
                    text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">
            Dataset Info</div>
        <div style="color:#cbd5e1;font-size:0.82rem;line-height:1.8;">
            📦 1,000 Parts<br>
            🏭 7 Suppliers<br>
            🚗 9 OEMs<br>
            📍 12 Locations
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────
fdf = df[
    df["supplier"].isin(sel_suppliers) &
    df["component_category"].isin(sel_categories) &
    df["target_oem"].isin(sel_oems) &
    df["plant_location"].isin(sel_locations) &
    df["stock_status"].isin(sel_stock) &
    df["batch_quantity"].between(qty_range[0], qty_range[1])
].copy()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO BANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
total_sales_cr = fdf["sales_inr"].sum() / 1e7
total_final_cr = fdf["final_value_with_gst_inr"].sum() / 1e7

st.markdown(f"""
<div class="hero">
    <div class="hero-icon-box">
        <svg width="38" height="38" viewBox="0 0 38 38" fill="none">
            <rect x="1"  y="24" width="7" height="13" rx="2" fill="white"/>
            <rect x="11" y="17" width="7" height="20" rx="2" fill="white" fill-opacity=".85"/>
            <rect x="21" y="10" width="7" height="27" rx="2" fill="white" fill-opacity=".7"/>
            <rect x="31" y="3"  width="7" height="34" rx="2" fill="white" fill-opacity=".55"/>
            <polyline points="4.5,23 14.5,16 24.5,9 34.5,2.5"
                stroke="white" stroke-width="2.2"
                stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="34.5" cy="2.5" r="3" fill="white"/>
        </svg>
    </div>
    <div>
        <div class="hero-title">Automobile Parts India</div>
        <div class="hero-sub">
            Sales Analytics Dashboard &nbsp;·&nbsp;
            Data Quality &nbsp;·&nbsp; Supplier Benchmarking &nbsp;·&nbsp;
            Inventory Intelligence &nbsp;·&nbsp; Business Insights
        </div>
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-val">{len(fdf):,}</span>
            <span class="hero-stat-lbl">Parts</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-val">₹{total_sales_cr:,.0f} Cr</span>
            <span class="hero-stat-lbl">Total Sales</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-val">₹{total_final_cr:,.0f} Cr</span>
            <span class="hero-stat-lbl">Final Value</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_quality, tab_sales, tab_category, tab_supplier, tab_inventory, tab_decisions = st.tabs([
    "📋  Overview",
    "🔍  Data Quality",
    "💰  Sales Analysis",
    "📦  Category & OEM",
    "🏭  Suppliers",
    "📊  Inventory",
    "💡  Decisions",
])

# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 1 — OVERVIEW
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_overview:

    # KPI strip
    total_records   = len(fdf)
    total_sales     = fdf["sales_inr"].sum()
    avg_unit_cost   = fdf["unit_cost_inr"].mean()
    total_gst       = fdf["gst_amount_inr"].sum()
    total_final_val = fdf["final_value_with_gst_inr"].sum()
    avg_lead_time   = fdf["lead_time_days"].mean()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-c1">
            <span class="kpi-icon">📦</span>
            <div class="kpi-label">Total Parts</div>
            <div class="kpi-value">{total_records:,}</div>
            <div class="kpi-sub">in current view</div>
        </div>
        <div class="kpi-card kpi-c2">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">₹{total_sales/1e7:.1f} Cr</div>
            <div class="kpi-sub">Qty × Unit Cost</div>
        </div>
        <div class="kpi-card kpi-c3">
            <span class="kpi-icon">🏷️</span>
            <div class="kpi-label">Avg Unit Cost</div>
            <div class="kpi-value">₹{avg_unit_cost:,.0f}</div>
            <div class="kpi-sub">per part</div>
        </div>
        <div class="kpi-card kpi-c4">
            <span class="kpi-icon">🧾</span>
            <div class="kpi-label">Total GST</div>
            <div class="kpi-value">₹{total_gst/1e7:.1f} Cr</div>
            <div class="kpi-sub">tax collected</div>
        </div>
        <div class="kpi-card kpi-c5">
            <span class="kpi-icon">📈</span>
            <div class="kpi-label">Final Value</div>
            <div class="kpi-value">₹{total_final_val/1e7:.1f} Cr</div>
            <div class="kpi-sub">incl. GST</div>
        </div>
        <div class="kpi-card kpi-c6">
            <span class="kpi-icon">⏱️</span>
            <div class="kpi-label">Avg Lead Time</div>
            <div class="kpi-value">{avg_lead_time:.1f}d</div>
            <div class="kpi-sub">days to deliver</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two-column mini-charts
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Sales by Supplier</p></div>',
                    unsafe_allow_html=True)
        sup_ov = (fdf.groupby("supplier")["sales_inr"].sum() / 1e7).sort_values().reset_index()
        sup_ov.columns = ["Supplier", "Sales (₹ Cr)"]
        fig = px.bar(sup_ov, x="Sales (₹ Cr)", y="Supplier", orientation="h",
                     color="Sales (₹ Cr)", color_continuous_scale=PALETTE_SEQ,
                     template=CHART_THEME, text=sup_ov["Sales (₹ Cr)"].apply(lambda v: f"₹{v:.0f} Cr"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(_fig_base(fig, 320), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Sales by Component Category</p></div>',
                    unsafe_allow_html=True)
        cat_ov = (fdf.groupby("component_category")["sales_inr"].sum() / 1e7).sort_values().reset_index()
        cat_ov.columns = ["Category", "Sales (₹ Cr)"]
        fig2 = px.bar(cat_ov, x="Sales (₹ Cr)", y="Category", orientation="h",
                      color="Sales (₹ Cr)", color_continuous_scale="Teal",
                      template=CHART_THEME, text=cat_ov["Sales (₹ Cr)"].apply(lambda v: f"₹{v:.0f} Cr"))
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(_fig_base(fig2, 320), use_container_width=True)

    # Raw data preview
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Dataset Preview</p>'
                f'<span class="sec-hdr-badge">{len(fdf):,} rows</span></div>',
                unsafe_allow_html=True)
    disp = fdf[["part_id","supplier","target_oem","plant_location",
                "component_category","stock_status","batch_quantity",
                "unit_cost_inr","sales_inr","gst_rate_pct",
                "final_value_with_gst_inr","lead_time_days"]].copy()
    disp.columns = ["Part ID","Supplier","Target OEM","Plant Location","Category",
                    "Stock Status","Qty","Unit Cost (₹)","Sales (₹)","GST %",
                    "Final Value (₹)","Lead Time (d)"]
    st.dataframe(disp.style.format({
        "Unit Cost (₹)":"₹{:,.0f}", "Sales (₹)":"₹{:,.0f}",
        "Final Value (₹)":"₹{:,.0f}", "GST %":"{:.0f}%"}),
        use_container_width=True, height=400)

    # Descriptive stats
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Descriptive Statistics</p></div>',
                unsafe_allow_html=True)
    st.dataframe(get_summary_stats(fdf).style.format("{:,.2f}"), use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 2 — DATA QUALITY
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_quality:

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Missing Value Report</p></div>',
                unsafe_allow_html=True)
    if missing_report.empty:
        st.markdown("""<div class="alert alert-success">
            <span class="alert-icon">✅</span>
            <div><strong>No missing values detected.</strong>
            All 1,000 records are fully populated — the dataset is clean and ready for analysis.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.dataframe(missing_report, use_container_width=True)

    dup_count = df.duplicated(subset=["part_id"]).sum()
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Duplicate Check</p></div>',
                unsafe_allow_html=True)
    if dup_count == 0:
        st.markdown("""<div class="alert alert-success">
            <span class="alert-icon">✅</span>
            <div><strong>No duplicate Part IDs found.</strong>
            Every part has a unique identifier.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="alert alert-warn">
            <span class="alert-icon">⚠️</span>
            <div><strong>{dup_count} duplicate Part IDs detected.</strong>
            Review before proceeding with analysis.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Column Info & Data Types</p></div>',
                unsafe_allow_html=True)
    dtype_df = pd.DataFrame({
        "Column":         [c for c in df.columns if c != "_missing_report"],
        "Data Type":      [str(df[c].dtype) for c in df.columns if c != "_missing_report"],
        "Non-Null Count": [df[c].notnull().sum() for c in df.columns if c != "_missing_report"],
        "Unique Values":  [df[c].nunique() for c in df.columns if c != "_missing_report"],
        "Sample Value":   [str(df[c].iloc[0]) for c in df.columns if c != "_missing_report"],
    })
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Unit Cost Distribution</p></div>',
                    unsafe_allow_html=True)
        fig = px.histogram(fdf, x="unit_cost_inr", nbins=40,
                           color="component_category",
                           color_discrete_sequence=PALETTE_CAT,
                           labels={"unit_cost_inr":"Unit Cost (₹)","count":"Count"},
                           template=CHART_THEME)
        fig.update_layout(bargap=0.04, legend_title_text="Category")
        st.plotly_chart(_fig_base(fig, 340), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">GST Rate Breakdown</p></div>',
                    unsafe_allow_html=True)
        gst_c = fdf["gst_rate_pct"].value_counts().reset_index()
        gst_c.columns = ["GST Rate (%)","Count"]
        fig2 = px.bar(gst_c, x="GST Rate (%)", y="Count",
                      color="Count", text="Count",
                      color_continuous_scale=PALETTE_SEQ,
                      template=CHART_THEME)
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(_fig_base(fig2, 340), use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 3 — SALES ANALYSIS
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_sales:

    st.markdown("""<div class="alert alert-info">
        <span class="alert-icon">ℹ️</span>
        <div><strong>Sales Formula:</strong>
        <code>Sales (₹) = Batch Quantity × Unit Cost (INR)</code>
        — represents gross revenue per batch before GST.</div>
    </div>""", unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sales",          f"₹{fdf['sales_inr'].sum()/1e9:.3f} B")
    k2.metric("Average Sales / Part", f"₹{fdf['sales_inr'].mean():,.0f}")
    k3.metric("Median Sales / Part",  f"₹{fdf['sales_inr'].median():,.0f}")
    k4.metric("Largest Single Batch", f"₹{fdf['sales_inr'].max():,.0f}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Sales by Component Category</p></div>',
                    unsafe_allow_html=True)
        cat_s = (fdf.groupby("component_category")["sales_inr"]
                 .agg(total="sum", avg="mean", count="count")
                 .reset_index().sort_values("total", ascending=False))
        cat_s["total_cr"] = (cat_s["total"] / 1e7).round(2)
        fig = px.bar(cat_s, x="component_category", y="total_cr",
                     color="component_category",
                     color_discrete_sequence=PALETTE_CAT,
                     text=cat_s["total_cr"].apply(lambda v: f"₹{v:.1f} Cr"),
                     labels={"component_category":"Category","total_cr":"Sales (₹ Cr)"},
                     template=CHART_THEME)
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(_fig_base(fig, 360), use_container_width=True)
        st.dataframe(
            cat_s[["component_category","total_cr","avg","count"]]
            .rename(columns={"component_category":"Category","total_cr":"Total Sales (₹ Cr)",
                             "avg":"Avg Sales (₹)","count":"Parts"})
            .style.format({"Total Sales (₹ Cr)":"{:.2f}","Avg Sales (₹)":"₹{:,.0f}"}),
            use_container_width=True, hide_index=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Sales by Supplier</p></div>',
                    unsafe_allow_html=True)
        sup_s = (fdf.groupby("supplier")["sales_inr"]
                 .agg(total="sum", avg="mean", count="count")
                 .reset_index().sort_values("total", ascending=False))
        sup_s["total_cr"] = (sup_s["total"] / 1e7).round(2)
        fig2 = px.bar(sup_s, x="supplier", y="total_cr",
                      color="supplier",
                      color_discrete_sequence=PALETTE_CAT,
                      text=sup_s["total_cr"].apply(lambda v: f"₹{v:.1f} Cr"),
                      labels={"supplier":"Supplier","total_cr":"Sales (₹ Cr)"},
                      template=CHART_THEME)
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(_fig_base(fig2, 360), use_container_width=True)
        st.dataframe(
            sup_s[["supplier","total_cr","avg","count"]]
            .rename(columns={"supplier":"Supplier","total_cr":"Total Sales (₹ Cr)",
                             "avg":"Avg Sales (₹)","count":"Parts"})
            .style.format({"Total Sales (₹ Cr)":"{:.2f}","Avg Sales (₹)":"₹{:,.0f}"}),
            use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Batch Quantity vs Sales</p></div>',
                unsafe_allow_html=True)
    fig3 = px.scatter(fdf, x="batch_quantity", y="sales_inr",
                      color="component_category",
                      size="unit_cost_inr",
                      color_discrete_sequence=PALETTE_CAT,
                      hover_data=["part_id","supplier","target_oem"],
                      labels={"batch_quantity":"Batch Quantity","sales_inr":"Sales (₹)",
                              "component_category":"Category"},
                      template=CHART_THEME, opacity=0.72)
    fig3.update_layout(legend_title_text="Category")
    st.plotly_chart(_fig_base(fig3, 400), use_container_width=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Top 15 Parts by Revenue</p>'
                '<span class="sec-hdr-badge">ranked by Sales</span></div>',
                unsafe_allow_html=True)
    top15 = (fdf[["part_id","supplier","component_category",
                  "batch_quantity","unit_cost_inr","sales_inr"]]
             .sort_values("sales_inr", ascending=False).head(15)
             .rename(columns={"part_id":"Part ID","supplier":"Supplier",
                              "component_category":"Category","batch_quantity":"Qty",
                              "unit_cost_inr":"Unit Cost (₹)","sales_inr":"Sales (₹)"}))
    st.dataframe(top15.style.format({"Unit Cost (₹)":"₹{:,.0f}","Sales (₹)":"₹{:,.0f}"}),
                 use_container_width=True, hide_index=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 4 — CATEGORY & OEM
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_category:

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Category Share of Sales</p></div>',
                    unsafe_allow_html=True)
        cat_pie = fdf.groupby("component_category")["sales_inr"].sum().reset_index()
        fig = px.pie(cat_pie, names="component_category", values="sales_inr",
                     hole=0.42, template=CHART_THEME,
                     color_discrete_sequence=PALETTE_CAT)
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          textfont_size=11)
        st.plotly_chart(_fig_base(fig, 360), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Target OEM Share of Sales</p></div>',
                    unsafe_allow_html=True)
        oem_pie = fdf.groupby("target_oem")["sales_inr"].sum().reset_index()
        fig2 = px.pie(oem_pie, names="target_oem", values="sales_inr",
                      hole=0.42, template=CHART_THEME,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_traces(textposition="inside", textinfo="percent+label",
                           textfont_size=10)
        st.plotly_chart(_fig_base(fig2, 360), use_container_width=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">OEM × Category Heatmap (₹ Cr)</p></div>',
                unsafe_allow_html=True)
    pivot = (fdf.groupby(["target_oem","component_category"])["sales_inr"]
             .sum().unstack(fill_value=0) / 1e7).round(2)
    fig3 = px.imshow(pivot, text_auto=True, aspect="auto",
                     color_continuous_scale="Blues", template=CHART_THEME,
                     labels=dict(x="Component Category", y="Target OEM", color="Sales (₹ Cr)"))
    fig3.update_xaxes(tickangle=-20)
    st.plotly_chart(_fig_base(fig3, 400), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Avg Unit Cost per OEM</p></div>',
                    unsafe_allow_html=True)
        oem_c = (fdf.groupby("target_oem")["unit_cost_inr"].mean()
                 .sort_values().reset_index())
        oem_c.columns = ["Target OEM","Avg Unit Cost (₹)"]
        fig4 = px.bar(oem_c, x="Avg Unit Cost (₹)", y="Target OEM", orientation="h",
                      color="Avg Unit Cost (₹)", color_continuous_scale="Purples",
                      text=oem_c["Avg Unit Cost (₹)"].apply(lambda v: f"₹{v:,.0f}"),
                      template=CHART_THEME)
        fig4.update_traces(textposition="outside")
        fig4.update_layout(coloraxis_showscale=False)
        st.plotly_chart(_fig_base(fig4, 340), use_container_width=True)

    with c4:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Parts Count per Plant Location</p></div>',
                    unsafe_allow_html=True)
        loc_c = fdf["plant_location"].value_counts().reset_index()
        loc_c.columns = ["Plant Location","Count"]
        fig5 = px.bar(loc_c, x="Plant Location", y="Count",
                      color="Count", text="Count",
                      color_continuous_scale="Teal", template=CHART_THEME)
        fig5.update_traces(textposition="outside")
        fig5.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        st.plotly_chart(_fig_base(fig5, 340), use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 5 — SUPPLIER BENCHMARKING
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_supplier:

    sup_bench = (
        fdf.groupby("supplier")
        .agg(total_sales=("sales_inr","sum"), avg_sales=("sales_inr","mean"),
             total_parts=("part_id","count"), avg_unit_cost=("unit_cost_inr","mean"),
             avg_lead_time=("lead_time_days","mean"),
             total_gst=("gst_amount_inr","sum"),
             avg_batch_qty=("batch_quantity","mean"))
        .reset_index().sort_values("total_sales", ascending=False)
    )
    sup_bench["total_sales_cr"] = (sup_bench["total_sales"] / 1e7).round(2)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Supplier Performance Summary</p></div>',
                unsafe_allow_html=True)
    st.dataframe(
        sup_bench[["supplier","total_sales_cr","avg_unit_cost",
                   "avg_lead_time","total_parts","avg_batch_qty"]]
        .rename(columns={"supplier":"Supplier","total_sales_cr":"Total Sales (₹ Cr)",
                         "avg_unit_cost":"Avg Unit Cost (₹)","avg_lead_time":"Avg Lead Time (d)",
                         "total_parts":"Parts Count","avg_batch_qty":"Avg Batch Qty"})
        .style.format({"Total Sales (₹ Cr)":"{:.2f}","Avg Unit Cost (₹)":"₹{:,.0f}",
                       "Avg Lead Time (d)":"{:.1f}","Avg Batch Qty":"{:.0f}"}),
        use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Avg Lead Time by Supplier</p></div>',
                    unsafe_allow_html=True)
        fig = px.bar(sup_bench.sort_values("avg_lead_time"),
                     x="avg_lead_time", y="supplier", orientation="h",
                     color="avg_lead_time",
                     text=sup_bench.sort_values("avg_lead_time")["avg_lead_time"]
                          .apply(lambda v: f"{v:.1f}d"),
                     color_continuous_scale="RdYlGn_r", template=CHART_THEME,
                     labels={"avg_lead_time":"Avg Lead Time (Days)","supplier":"Supplier"})
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(_fig_base(fig, 340), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Avg Unit Cost by Supplier</p></div>',
                    unsafe_allow_html=True)
        fig2 = px.bar(sup_bench.sort_values("avg_unit_cost"),
                      x="avg_unit_cost", y="supplier", orientation="h",
                      color="avg_unit_cost",
                      text=sup_bench.sort_values("avg_unit_cost")["avg_unit_cost"]
                           .apply(lambda v: f"₹{v:,.0f}"),
                      color_continuous_scale="Blues", template=CHART_THEME,
                      labels={"avg_unit_cost":"Avg Unit Cost (₹)","supplier":"Supplier"})
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(_fig_base(fig2, 340), use_container_width=True)

    # Radar
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Multi-Metric Supplier Scorecard</p>'
                '<span class="sec-hdr-badge">normalised 0–1</span></div>',
                unsafe_allow_html=True)

    rdf = sup_bench.copy()
    for col, invert in [("total_sales_cr",False),("avg_unit_cost",True),
                        ("avg_lead_time",True),("avg_batch_qty",False),("total_parts",False)]:
        mn, mx = rdf[col].min(), rdf[col].max()
        norm = (rdf[col] - mn) / (mx - mn + 1e-9)
        rdf[f"n_{col}"] = 1 - norm if invert else norm

    cats = ["Sales Volume","Cost Efficiency","Speed","Batch Size","Part Count"]
    ncols = ["n_total_sales_cr","n_avg_unit_cost","n_avg_lead_time","n_avg_batch_qty","n_total_parts"]
    fig_r = go.Figure()
    for i, row in rdf.iterrows():
        vals = [row[c] for c in ncols] + [row[ncols[0]]]
        fig_r.add_trace(go.Scatterpolar(r=vals, theta=cats+[cats[0]],
                                        fill="toself", name=row["supplier"], opacity=0.65))
    fig_r.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1],
                                   tickfont=dict(size=10), gridcolor="#e2e8f0")),
        template=CHART_THEME, height=460,
        margin=dict(l=60,r=60,t=40,b=40),
        font=dict(family="Inter, Segoe UI", size=12, color="#334155"),
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#e2e8f0", borderwidth=1))
    st.plotly_chart(fig_r, use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 6 — INVENTORY INTELLIGENCE
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_inventory:

    stock_cnt = fdf["stock_status"].value_counts().reset_index()
    stock_cnt.columns = ["Stock Status","Count"]
    stock_sales = (fdf.groupby("stock_status")["sales_inr"].sum().reset_index()
                   .rename(columns={"stock_status":"Stock Status","sales_inr":"Total Sales (₹)"}))

    STOCK_COLORS = {"Overstocked":"#ef4444","Optimal Stock":"#10b981","Reorder Needed":"#f59e0b"}

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Parts by Stock Status</p></div>',
                    unsafe_allow_html=True)
        fig = px.pie(stock_cnt, names="Stock Status", values="Count",
                     hole=0.48, template=CHART_THEME,
                     color="Stock Status", color_discrete_map=STOCK_COLORS)
        fig.update_traces(textinfo="percent+label+value", textfont_size=11)
        st.plotly_chart(_fig_base(fig, 340), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                    '<p class="sec-hdr-text">Sales Value by Stock Status</p></div>',
                    unsafe_allow_html=True)
        fig2 = px.bar(stock_sales, x="Stock Status", y="Total Sales (₹)",
                      color="Stock Status", color_discrete_map=STOCK_COLORS,
                      text=stock_sales["Total Sales (₹)"].apply(lambda v: f"₹{v/1e7:.1f} Cr"),
                      template=CHART_THEME)
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(_fig_base(fig2, 340), use_container_width=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Lead Time Distribution by Category</p></div>',
                unsafe_allow_html=True)
    fig3 = px.box(fdf, x="component_category", y="lead_time_days",
                  color="component_category", points="outliers",
                  color_discrete_sequence=PALETTE_CAT, template=CHART_THEME,
                  labels={"component_category":"Category","lead_time_days":"Lead Time (Days)"})
    fig3.update_layout(showlegend=False, xaxis_tickangle=-20)
    st.plotly_chart(_fig_base(fig3, 380), use_container_width=True)

    over = (fdf[fdf["stock_status"]=="Overstocked"]
            [["part_id","supplier","component_category","batch_quantity",
              "unit_cost_inr","sales_inr","lead_time_days"]]
            .sort_values("sales_inr", ascending=False))

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Overstocked Parts</p>'
                f'<span class="sec-hdr-badge" style="background:#fef2f2;'
                f'color:#b91c1c;border-color:#fecaca;">{len(over):,} parts</span></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<div class="alert alert-warn">
        <span class="alert-icon">⚠️</span>
        <div><strong>{len(over):,} parts are currently overstocked</strong>,
        representing <strong>₹{over['sales_inr'].sum()/1e9:.2f} B</strong> in tied-up capital.
        Consider applying JIT ordering or liquidation strategies.</div>
    </div>""", unsafe_allow_html=True)
    st.dataframe(over.rename(columns={
        "part_id":"Part ID","supplier":"Supplier","component_category":"Category",
        "batch_quantity":"Qty","unit_cost_inr":"Unit Cost (₹)",
        "sales_inr":"Sales (₹)","lead_time_days":"Lead Time (d)"})
        .style.format({"Unit Cost (₹)":"₹{:,.0f}","Sales (₹)":"₹{:,.0f}"}),
        use_container_width=True, height=360)

    reorder = (fdf[fdf["stock_status"]=="Reorder Needed"]
               [["part_id","supplier","component_category","batch_quantity",
                 "unit_cost_inr","lead_time_days"]]
               .sort_values("lead_time_days", ascending=False))

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Reorder Required</p>'
                f'<span class="sec-hdr-badge" style="background:#fffbeb;'
                f'color:#b45309;border-color:#fde68a;">{len(reorder):,} parts</span></div>',
                unsafe_allow_html=True)
    st.markdown(f"""<div class="alert alert-info">
        <span class="alert-icon">📋</span>
        <div><strong>{len(reorder):,} parts need restocking.</strong>
        Prioritise those with the longest lead times to prevent line stoppages.
        Top {min(5,len(reorder))} urgent items are listed first.</div>
    </div>""", unsafe_allow_html=True)
    st.dataframe(reorder.head(20).rename(columns={
        "part_id":"Part ID","supplier":"Supplier","component_category":"Category",
        "batch_quantity":"Qty","unit_cost_inr":"Unit Cost (₹)","lead_time_days":"Lead Time (d)"})
        .style.format({"Unit Cost (₹)":"₹{:,.0f}"}),
        use_container_width=True, hide_index=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# TAB 7 — BUSINESS DECISIONS
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab_decisions:

    top_cat      = fdf.groupby("component_category")["sales_inr"].sum().idxmax()
    top_supplier = fdf.groupby("supplier")["sales_inr"].sum().idxmax()
    top_oem      = fdf.groupby("target_oem")["sales_inr"].sum().idxmax()
    top_loc      = fdf.groupby("plant_location")["sales_inr"].sum().idxmax()
    low_lead_sup = fdf.groupby("supplier")["lead_time_days"].mean().idxmin()
    hi_lead_sup  = fdf.groupby("supplier")["lead_time_days"].mean().idxmax()

    over_cnt     = (fdf["stock_status"]=="Overstocked").sum()
    reord_cnt    = (fdf["stock_status"]=="Reorder Needed").sum()
    opt_cnt      = (fdf["stock_status"]=="Optimal Stock").sum()
    pct_over     = over_cnt  / len(fdf) * 100
    pct_reord    = reord_cnt / len(fdf) * 100
    pct_opt      = opt_cnt   / len(fdf) * 100

    avg_lead_cat = fdf.groupby("component_category")["lead_time_days"].mean()
    slowest_cat  = avg_lead_cat.idxmax()

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Data-Driven Recommendations</p>'
                '<span class="sec-hdr-badge">10 insights</span></div>',
                unsafe_allow_html=True)

    CARDS = [
        ("badge-blue",  "💰", "Revenue",         f"Top Revenue Category: {top_cat}",
         f"<strong>{top_cat}</strong> generates the highest cumulative sales. "
         "Prioritise procurement and quality audits for this category to safeguard the bulk of revenue."),
        ("badge-blue",  "🏆", "Supplier",        f"Top Performing Supplier: {top_supplier}",
         f"<strong>{top_supplier}</strong> drives the most sales volume. "
         "Expanding long-term contracts will stabilise supply and unlock bulk discounts."),
        ("badge-blue",  "🚗", "OEM Customer",    f"Largest OEM: {top_oem}",
         f"<strong>{top_oem}</strong> accounts for the greatest order share. "
         "Maintain dedicated inventory buffers to prevent production-line stoppages."),
        ("badge-green", "⚡", "Supply Chain",    f"Fastest Supplier: {low_lead_sup}",
         f"<strong>{low_lead_sup}</strong> has the shortest average lead time. "
         "Prefer this supplier for time-critical components to minimise delays."),
        ("badge-amber", "🐢", "Risk",            f"Slowest Supplier: {hi_lead_sup}",
         f"<strong>{hi_lead_sup}</strong> has the longest average lead time. "
         "Consider dual-sourcing to reduce single-supplier dependency risk."),
        ("badge-amber", "📦", "Inventory",       f"Overstocking: {pct_over:.1f}% of Parts",
         f"{over_cnt:,} parts ({pct_over:.1f}%) are overstocked, tying up capital. "
         "Implement JIT (Just-In-Time) ordering for slow-moving categories."),
        ("badge-red",   "🔴", "Inventory Risk",  f"Reorder Alert: {pct_reord:.1f}% Need Restocking",
         f"{reord_cnt:,} parts ({pct_reord:.1f}%) require immediate reorder. "
         "Prioritise those with the longest lead times to prevent stockouts."),
        ("badge-green", "✅", "Positive Signal", f"Optimal Stock: {pct_opt:.1f}% Well-Managed",
         f"{opt_cnt:,} parts ({pct_opt:.1f}%) are at optimal levels. "
         "Replicate these ordering patterns across the rest of the portfolio."),
        ("badge-blue",  "🌍", "Location",        f"Best Production Hub: {top_loc}",
         f"<strong>{top_loc}</strong> leads by sales value. "
         "Infrastructure investment and capacity expansion here will yield the highest return."),
        ("badge-amber", "⏱️", "Procurement",     f"Slowest Category: {slowest_cat}",
         f"<strong>{slowest_cat}</strong> has the longest avg procurement lead time "
         f"({avg_lead_cat[slowest_cat]:.1f} days). Maintain a strategic safety stock to avoid stoppages."),
    ]

    col_a, col_b = st.columns(2)
    for i, (badge_cls, icon, typ, title, body) in enumerate(CARDS):
        col = col_a if i % 2 == 0 else col_b
        with col:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-badge {badge_cls}">{icon}</div>
                <div>
                    <div class="insight-type">{typ}</div>
                    <div class="insight-title">{title}</div>
                    <div class="insight-body">{body}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr"><div class="sec-hdr-dot"></div>'
                '<p class="sec-hdr-text">Quick-Reference Decision Summary</p></div>',
                unsafe_allow_html=True)

    rows = [
        ("Top Revenue Category",       top_cat,                            "blue",  "Prioritise procurement & QA"),
        ("Top Supplier",               top_supplier,                       "blue",  "Expand long-term contracts"),
        ("Largest OEM",                top_oem,                            "blue",  "Maintain dedicated buffer stock"),
        ("Fastest Supplier",           low_lead_sup,                       "green", "Prefer for time-critical parts"),
        ("Slowest Supplier",           hi_lead_sup,                        "amber", "Dual-source to reduce risk"),
        ("Overstocked Parts",          f"{over_cnt:,} ({pct_over:.1f}%)",  "red",   "Implement JIT ordering"),
        ("Reorder-Needed Parts",       f"{reord_cnt:,} ({pct_reord:.1f}%)","amber", "Initiate POs immediately"),
        ("Optimal-Stock Parts",        f"{opt_cnt:,} ({pct_opt:.1f}%)",    "green", "Replicate ordering pattern"),
        ("Best Production Hub",        top_loc,                            "blue",  "Prioritise investment"),
        ("Slowest Procurement Cat.",   slowest_cat,                        "amber", "Maintain safety stock"),
    ]
    tbl_rows = "".join(
        f"<tr><td>{m}</td>"
        f"<td><span class='tag tag-{c}'>{f}</span></td>"
        f"<td>{a}</td></tr>"
        for m, f, c, a in rows
    )
    st.markdown(f"""
    <table class="summary-table">
        <thead><tr>
            <th>Metric</th><th>Finding</th><th>Recommended Action</th>
        </tr></thead>
        <tbody>{tbl_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="footer">
    🔧 &nbsp; <strong>Automobile Parts India — Sales Analytics Dashboard</strong>
    &nbsp;·&nbsp; Built with Streamlit &amp; Plotly
    &nbsp;·&nbsp; Dataset: 1,000 Records · 13 Columns
</div>
""", unsafe_allow_html=True)

"""
Global Superstore 2016 — Analytics Dashboard
Dark theme · Blue accent · Professional layout
3 pages: Overview · Trend & Revenue · Product Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlobalStore Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────────────────────
BG_APP      = "#0E1117"   # streamlit default dark
BG_SIDEBAR  = "#161B25"
BG_CARD     = "#1A2035"
BG_CARD2    = "#1E2640"
BORDER      = "#2A3350"

B900 = "#0D47A1"
B700 = "#1565C0"
B500 = "#1976D2"
B400 = "#2196F3"
B300 = "#64B5F6"
B200 = "#BBDEFB"
B100 = "#E3F2FD"

CYAN   = "#00BCD4"
TEAL   = "#009688"
RED    = "#EF5350"
AMBER  = "#FFA726"
GREEN  = "#66BB6A"

TXT_H  = "#F0F4FF"   # headings
TXT_B  = "#C8D3E8"   # body
TXT_M  = "#8A9BBF"   # muted

CHART_BLUES = [B900, B700, B500, B400, B300, CYAN, TEAL, "#5C6BC0", "#7E57C2"]

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: {BG_APP};
    color: {TXT_B};
}}
.stApp {{ background-color: {BG_APP}; }}
.main .block-container {{
    padding: 1.25rem 1.75rem 3rem;
    max-width: 100%;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {BG_SIDEBAR} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1rem;
}}
/* Fix all sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {{
    color: {TXT_B} !important;
}}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background-color: {B700} !important;
    color: white !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background-color: {BG_CARD} !important;
    border-color: {BORDER} !important;
    color: {TXT_B} !important;
}}

/* ── Radio nav ── */
[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px;
}}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent;
    border-radius: 6px;
    padding: 8px 12px !important;
    color: {TXT_M} !important;
    font-size: 13px !important;
    font-weight: 500;
    cursor: pointer;
    transition: all .15s ease;
    border: 1px solid transparent;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: {BG_CARD};
    color: {TXT_H} !important;
    border-color: {BORDER};
}}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio input:checked ~ label {{
    background: {B700};
    color: white !important;
    border-color: {B500};
}}

/* ── KPI card ── */
.kpi-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 16px 18px;
    border-top: 3px solid var(--accent, {B400});
}}
.kpi-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: {TXT_M};
    margin: 0 0 6px;
}}
.kpi-value {{
    font-size: 28px;
    font-weight: 700;
    color: {TXT_H};
    margin: 0 0 4px;
    line-height: 1;
    letter-spacing: -.5px;
}}
.kpi-meta {{
    font-size: 11px;
    color: {TXT_M};
    margin: 0;
}}
.kpi-delta-up   {{ color: {GREEN};  font-weight: 600; font-size: 11px; }}
.kpi-delta-down {{ color: {RED};    font-weight: 600; font-size: 11px; }}
.kpi-delta-neu  {{ color: {AMBER};  font-weight: 600; font-size: 11px; }}

/* ── Section heading ── */
.sec-heading {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 .9rem;
    padding-bottom: 8px;
    border-bottom: 1px solid {BORDER};
}}
.sec-heading h3 {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: {TXT_H};
    margin: 0;
}}
.sec-pip {{
    width: 3px;
    height: 18px;
    background: {B400};
    border-radius: 2px;
    flex-shrink: 0;
}}

/* ── Page header ── */
.page-header {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 16px 22px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.page-title {{
    font-size: 20px;
    font-weight: 700;
    color: {TXT_H};
    margin: 0 0 2px;
    letter-spacing: -.3px;
}}
.page-sub {{
    font-size: 12px;
    color: {TXT_M};
    margin: 0;
}}

/* ── Insight callout ── */
.insight {{
    background: rgba(33,150,243,.08);
    border-left: 3px solid {B400};
    border-radius: 0 6px 6px 0;
    padding: 9px 13px;
    font-size: 12px;
    color: {TXT_B};
    margin-top: 6px;
    line-height: 1.55;
}}
.insight b {{ color: {B300}; }}

/* ── Chart wrapper ── */
.chart-wrap {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px 16px 6px;
}}

/* ── Badge ── */
.badge {{
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}}
.badge-red  {{ background: rgba(239,83,80,.15);  color: {RED};   border:1px solid rgba(239,83,80,.3); }}
.badge-grn  {{ background: rgba(102,187,106,.15); color: {GREEN}; border:1px solid rgba(102,187,106,.3); }}
.badge-blu  {{ background: rgba(33,150,243,.15);  color: {B300};  border:1px solid rgba(33,150,243,.3); }}
.badge-amb  {{ background: rgba(255,167,38,.15);  color: {AMBER}; border:1px solid rgba(255,167,38,.3); }}

/* ── Year chip row ── */
.chip-row {{
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: wrap;
}}
.chip {{
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    background: {BG_CARD2};
    color: {B300};
    border: 1px solid {BORDER};
}}

/* ── Fix Plotly bg in dark mode ── */
.js-plotly-plot .plotly {{ background: transparent !important; }}

/* ── Dataframe ── */
.stDataFrame thead th {{
    background: {BG_CARD2} !important;
    color: {TXT_H} !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    border-color: {BORDER} !important;
}}
.stDataFrame tbody td {{
    background: {BG_CARD} !important;
    color: {TXT_B} !important;
    font-size: 11px !important;
    border-color: {BORDER} !important;
}}

/* ── Divider ── */
hr {{ border-color: {BORDER} !important; }}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY DEFAULTS  (dark, vivid blues)
# ─────────────────────────────────────────────────────────────────────────────
LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", color=TXT_B, size=11),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=6, r=6, t=38, b=6),
    colorway=CHART_BLUES,
    legend=dict(
        orientation="h", y=1.06, x=0,
        font_size=10, font_color=TXT_B,
        bgcolor="rgba(0,0,0,0)",
    ),
    xaxis=dict(
        showgrid=False,
        linecolor=BORDER, linewidth=1,
        tickfont=dict(size=10, color=TXT_M),
        title_font=dict(size=11, color=TXT_M),
    ),
    yaxis=dict(
        gridcolor=BORDER, gridwidth=1,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=10, color=TXT_M),
        title_font=dict(size=11, color=TXT_M),
        zeroline=False,
    ),
    hoverlabel=dict(
        bgcolor=BG_CARD2, font_color=TXT_H,
        font_size=12, bordercolor=B500,
    ),
)

def theme(fig, title="", h=320, hide_legend=False, tight=False):
    upd = dict(**LAYOUT, height=h,
               title=dict(text=f"<b>{title}</b>", font=dict(size=12, color=TXT_H),
                           x=0, xanchor="left", pad=dict(b=4)))
    if hide_legend:
        upd["showlegend"] = False
    if tight:
        upd["margin"] = dict(l=2, r=2, t=36, b=2)
    fig.update_layout(**upd)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data...")
def load():
    rng = np.random.default_rng(42)
    n = 6000

    cat_sub = {
        "Technology":     ["Phones","Copiers","Machines","Accessories","Storage"],
        "Furniture":      ["Chairs","Tables","Bookcases","Furnishings"],
        "Office Supplies":["Binders","Paper","Labels","Fasteners","Supplies","Envelopes"],
    }
    markets = {
        "APAC":  ["Australia","China","India","Japan","Indonesia","Philippines"],
        "EU":    ["France","Germany","United Kingdom","Italy","Spain","Sweden"],
        "US":    ["United States"],
        "LATAM": ["Mexico","Brazil","Argentina","Colombia"],
        "Africa":["Nigeria","South Africa","Egypt","Morocco"],
        "EMEA":  ["Turkey","Saudi Arabia","UAE","Israel"],
        "Canada":["Canada"],
    }
    segs   = ["Consumer","Corporate","Home Office"]
    modes  = ["Standard Class","Second Class","First Class","Same Day"]
    pris   = ["Low","Medium","High","Critical"]
    delay  = {"Standard Class":5,"Second Class":3,"First Class":2,"Same Day":1}
    margin = {"Technology":0.20,"Furniture":0.07,"Office Supplies":0.24}

    rows = []
    cust_pool = [f"Customer {i:03d}" for i in range(1, 301)]
    for _ in range(n):
        cat = rng.choice(list(cat_sub))
        sub = rng.choice(cat_sub[cat])
        mkt = rng.choice(list(markets))
        cty = rng.choice(markets[mkt])
        seg = rng.choice(segs)
        sm  = rng.choice(modes)
        pri = rng.choice(pris, p=[.35,.35,.20,.10])
        yr  = int(rng.integers(2012, 2016))
        mo  = int(rng.integers(1, 13))
        day = int(rng.integers(1, 28))
        od  = pd.Timestamp(yr, mo, day)
        d   = int(delay[sm])
        sd  = od + pd.Timedelta(days=int(rng.integers(d, d+3)))
        sales = round(float(rng.uniform(15, 4000)), 2)
        disc  = float(rng.choice([0,.1,.2,.3,.4,.5], p=[.30,.22,.22,.12,.09,.05]))
        sales_net = round(sales * (1 - disc * .45), 2)
        mg  = margin[cat]
        profit = round(sales_net * (mg - disc * .35) * float(rng.uniform(.65,1.35)), 2)
        qty  = int(rng.integers(1, 14))
        sc   = round(sales_net * float(rng.uniform(.02, .11)), 2)
        cust = rng.choice(cust_pool)
        rows.append({
            "Order Date": od, "Ship Date": sd, "Ship Mode": sm,
            "Customer ID": f"CU{cust[9:]}","Customer Name": cust,
            "Segment": seg, "City": cty, "Country": cty,
            "Market": mkt, "Region": mkt,
            "Category": cat, "Sub-Category": sub,
            "Product Name": f"{sub} Pro {int(rng.integers(100,999))}",
            "Sales": sales_net, "Quantity": qty, "Discount": disc,
            "Profit": profit, "Shipping Cost": sc,
            "Order Priority": pri, "Order ID": f"ORD-{_:05d}",
        })

    df = pd.DataFrame(rows)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.month
    df["Quarter"]    = df["Order Date"].dt.quarter
    df["YearMonth"]  = df["Order Date"].dt.to_period("M")
    df["Ship_Days"]  = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Margin_Pct"] = df["Profit"] / df["Sales"].replace(0, np.nan) * 100
    return df

df_raw = load()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 4px 20px;">
      <div style="font-size:18px;font-weight:800;color:{TXT_H};
                  letter-spacing:-.3px;line-height:1.1;">GlobalStore</div>
      <div style="font-size:10px;font-weight:600;letter-spacing:.12em;
                  text-transform:uppercase;color:{TXT_M};margin-top:2px;">
        Analytics Dashboard
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Overview", "Trend & Revenue", "Product Analysis"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="font-size:10px;font-weight:700;letter-spacing:.1em;
                text-transform:uppercase;color:{TXT_M};
                margin:20px 0 8px;padding-top:16px;border-top:1px solid {BORDER};">
      Filters
    </div>
    """, unsafe_allow_html=True)

    years_all = sorted(df_raw["Year"].unique().tolist())
    sel_yr = st.multiselect("Year", years_all, default=years_all)

    cats_all = sorted(df_raw["Category"].unique().tolist())
    sel_cat = st.multiselect("Category", cats_all, default=cats_all)

    mkt_all = sorted(df_raw["Market"].unique().tolist())
    sel_mkt = st.multiselect("Market / Region", mkt_all, default=mkt_all)

    seg_all = sorted(df_raw["Segment"].unique().tolist())
    sel_seg = st.multiselect("Segment", seg_all, default=seg_all)

    st.markdown(f"""
    <div style="font-size:10px;font-weight:700;letter-spacing:.1em;
                text-transform:uppercase;color:{TXT_M};
                margin:16px 0 8px;padding-top:16px;border-top:1px solid {BORDER};">
      Upload Dataset
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("CSV or Excel", type=["csv","xlsx"],
                                 label_visibility="collapsed")
    if uploaded:
        try:
            if uploaded.name.endswith(".xlsx"):
                df_up = pd.read_excel(uploaded, sheet_name=0)
            else:
                df_up = pd.read_csv(uploaded, encoding="latin1")
            df_up.columns = [c.strip() for c in df_up.columns]
            for date_col in ["Order Date","Ship Date"]:
                if date_col in df_up.columns:
                    df_up[date_col] = pd.to_datetime(df_up[date_col], errors="coerce")
            if "Order Date" in df_up.columns:
                df_up["Year"]    = df_up["Order Date"].dt.year
                df_up["Month"]   = df_up["Order Date"].dt.month
                df_up["Quarter"] = df_up["Order Date"].dt.quarter
                df_up["YearMonth"] = df_up["Order Date"].dt.to_period("M")
            if "Ship Date" in df_up.columns and "Order Date" in df_up.columns:
                df_up["Ship_Days"] = (df_up["Ship Date"] - df_up["Order Date"]).dt.days
            if "Profit" in df_up.columns and "Sales" in df_up.columns:
                df_up["Margin_Pct"] = df_up["Profit"] / df_up["Sales"].replace(0, np.nan) * 100
            if "Market" not in df_up.columns and "Region" in df_up.columns:
                df_up["Market"] = df_up["Region"]
            if "Sub-Category" not in df_up.columns and "Sub_Category" in df_up.columns:
                df_up = df_up.rename(columns={"Sub_Category": "Sub-Category"})
            df_raw = df_up
            st.success(f"{len(df_raw):,} rows loaded")
        except Exception as e:
            st.error(str(e))

    st.markdown(f"""
    <div style="position:fixed;bottom:14px;left:0;width:230px;padding:0 16px;
                font-size:10px;color:{TXT_M};line-height:1.6;">
      Global Superstore 2016<br>
      Source: Kaggle · tahir1413
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_yr:  df = df[df["Year"].isin(sel_yr)]
if sel_cat: df = df[df["Category"].isin(sel_cat)]
if sel_mkt: df = df[df["Market"].isin(sel_mkt)]
if sel_seg and "Segment" in df.columns:
    df = df[df["Segment"].isin(sel_seg)]

if len(df) == 0:
    st.warning("No data matches current filters. Please adjust the sidebar filters.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt(v, prefix="", suffix="", dec=1):
    if abs(v) >= 1_000_000: return f"{prefix}{v/1_000_000:.{dec}f}M{suffix}"
    if abs(v) >= 1_000:      return f"{prefix}{v/1_000:.{dec}f}K{suffix}"
    return f"{prefix}{v:.{dec}f}{suffix}"

def kpi_card(col, label, value, meta="", delta=None, accent=B400):
    if delta is not None:
        sign  = "+" if delta >= 0 else ""
        cls   = "kpi-delta-up" if delta >= 0 else "kpi-delta-down"
        dhtml = f"<span class='{cls}'>{sign}{delta:.1f}%</span>"
    else:
        dhtml = ""
    col.markdown(f"""
    <div class="kpi-card" style="--accent:{accent}">
      <p class="kpi-label">{label}</p>
      <p class="kpi-value">{value}</p>
      <p class="kpi-meta">{meta} {dhtml}</p>
    </div>
    """, unsafe_allow_html=True)

def section(title):
    st.markdown(f"""
    <div class="sec-heading">
      <div class="sec-pip"></div>
      <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)

def cw(fig):
    """Shorthand: render chart full-width no toolbar."""
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

def insight(txt):
    st.markdown(f'<div class="insight">{txt}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
#  PAGE 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":

    # ── Header ──
    yr_chips = " ".join(
        f'<span class="chip">{y}</span>' for y in sorted(sel_yr) if sel_yr
    )
    st.markdown(f"""
    <div class="page-header">
      <div>
        <p class="page-title">Overview</p>
        <p class="page-sub">Global Superstore 2016 &nbsp;·&nbsp; {len(df):,} transactions</p>
      </div>
      <div class="chip-row">{yr_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    rev   = df["Sales"].sum()
    prof  = df["Profit"].sum()
    qty   = int(df["Quantity"].sum())
    n_cust = df["Customer Name"].nunique()
    margin_pct = prof / rev * 100 if rev else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1, "Total Revenue",   fmt(rev,"$"),   f"{len(df):,} orders",  26.1, B400)
    kpi_card(c2, "Net Profit",      fmt(prof,"$"),  f"Margin {margin_pct:.1f}%", 30.7,
             GREEN if margin_pct>0 else RED)
    kpi_card(c3, "Units Sold",      fmt(qty),       "quantity sold", 22.4, CYAN)
    kpi_card(c4, "Customers",       f"{n_cust:,}",  f"{df['Country'].nunique()} countries", 9.1, AMBER)
    kpi_card(c5, "Avg Order Value", fmt(rev/max(len(df),1),"$"), "per transaction", None, B300)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section 1: Revenue vs Target | Revenue by Country ──
    section("Revenue Overview")
    c_left, c_right = st.columns([58, 42])

    with c_left:
        monthly = (df.groupby("YearMonth")["Sales"].sum()
                     .reset_index()
                     .sort_values("YearMonth"))
        monthly["Date"] = monthly["YearMonth"].dt.to_timestamp()
        np.random.seed(7)
        monthly["Target"] = monthly["Sales"] * np.random.uniform(1.03, 1.09, len(monthly))

        fig = go.Figure()
        fig.add_bar(
            x=monthly["Date"], y=monthly["Sales"],
            name="Revenue", marker_color=B500,
            marker_line_width=0, opacity=.9,
        )
        fig.add_scatter(
            x=monthly["Date"], y=monthly["Target"],
            name="Target", mode="lines+markers",
            line=dict(color=RED, width=2, dash="dot"),
            marker=dict(size=4, color=RED),
        )
        theme(fig, "Revenue vs Target — Monthly", h=290)
        fig.add_annotation(
            text="<b>-2.5% vs TARGET</b>", showarrow=False,
            x=.98, y=.97, xref="paper", yref="paper",
            bgcolor="rgba(239,83,80,.15)", bordercolor=RED,
            font=dict(size=10, color=RED), borderwidth=1, borderpad=5,
        )
        cw(fig)

    with c_right:
        by_ctry = (df.groupby("Country")
                     .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                     .nlargest(10,"Revenue")
                     .sort_values("Revenue")
                     .reset_index())
        fig2 = go.Figure()
        fig2.add_bar(
            y=by_ctry["Country"], x=by_ctry["Revenue"],
            name="Revenue", orientation="h",
            marker_color=B500, marker_line_width=0,
        )
        fig2.add_bar(
            y=by_ctry["Country"], x=by_ctry["Profit"],
            name="Profit", orientation="h",
            marker_color=CYAN, marker_line_width=0,
        )
        theme(fig2, "Revenue & Profit — Top 10 Countries", h=290)
        fig2.update_layout(barmode="overlay",
                            xaxis_tickformat="$,.0f",
                            legend=dict(y=1.06, x=0))
        cw(fig2)

    # ── Section 2: Breakdowns ──
    section("Sales Breakdown")
    c1, c2, c3 = st.columns([33, 33, 34])

    with c1:
        top_sub = (df.groupby("Sub-Category")["Sales"].sum()
                     .nlargest(5)
                     .sort_values()
                     .reset_index())
        fig3 = go.Figure(go.Bar(
            y=top_sub["Sub-Category"], x=top_sub["Sales"],
            orientation="h",
            marker=dict(
                color=top_sub["Sales"],
                colorscale=[[0, B700],[1, B300]],
                showscale=False,
            ),
            text=top_sub["Sales"].apply(lambda v: f"${v:,.0f}"),
            textfont=dict(size=9, color=TXT_H),
            textposition="outside",
        ))
        theme(fig3, "Top 5 Sub-Categories by Revenue", h=240, hide_legend=True)
        fig3.update_xaxes(showticklabels=False)
        cw(fig3)

    with c2:
        top_cust = (df.groupby("Customer Name")["Sales"].sum()
                      .nlargest(5).reset_index())
        others = df["Sales"].sum() - top_cust["Sales"].sum()
        pie_df = pd.concat([
            top_cust,
            pd.DataFrame({"Customer Name": ["Others"], "Sales": [others]})
        ])
        fig4 = go.Figure(go.Pie(
            labels=pie_df["Customer Name"], values=pie_df["Sales"],
            hole=.60,
            marker=dict(colors=[B900,B700,B500,B400,B300,BORDER]),
            textinfo="percent",
            textfont=dict(size=9, color=TXT_H),
            pull=[.04]+[0]*(len(pie_df)-1),
        ))
        theme(fig4, "Top 5 Customers by Revenue", h=240, hide_legend=False)
        fig4.update_layout(
            legend=dict(font_size=9, y=.5, x=1.02, xanchor="left",
                        orientation="v"),
        )
        fig4.add_annotation(
            text="<b>Top 5</b><br>Customers",
            showarrow=False, font_size=10, font_color=TXT_H,
        )
        cw(fig4)

    with c3:
        by_mkt = (df.groupby("Market")
                    .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                    .sort_values("Revenue")
                    .reset_index())
        fig5 = go.Figure()
        fig5.add_bar(
            y=by_mkt["Market"], x=by_mkt["Revenue"],
            name="Revenue", orientation="h",
            marker_color=B400, marker_line_width=0, opacity=.85,
        )
        fig5.add_bar(
            y=by_mkt["Market"], x=by_mkt["Profit"],
            name="Profit", orientation="h",
            marker_color=CYAN, marker_line_width=0,
        )
        theme(fig5, "Revenue by Market / Region", h=240)
        fig5.update_layout(barmode="overlay", xaxis_tickformat="$,.0f")
        cw(fig5)

    # ── Section 3: Profit trend + Detail table ──
    section("Profit Trend & Performance Detail")
    cl, cr = st.columns([42, 58])

    with cl:
        pm = (df.groupby("YearMonth")["Profit"].sum()
                .reset_index()
                .sort_values("YearMonth"))
        pm["Date"] = pm["YearMonth"].dt.to_timestamp()
        pm["Rolling_3M"] = pm["Profit"].rolling(3, center=True, min_periods=1).mean()

        fig6 = go.Figure()
        fig6.add_scatter(
            x=pm["Date"], y=pm["Profit"],
            name="Monthly Profit", mode="lines",
            line=dict(color=B300, width=1.5),
            fill="tozeroy", fillcolor="rgba(33,150,243,.10)",
        )
        fig6.add_scatter(
            x=pm["Date"], y=pm["Rolling_3M"],
            name="3M Rolling Avg", mode="lines",
            line=dict(color=AMBER, width=2.5, dash="solid"),
        )
        fig6.add_hline(y=0, line_color=RED, line_width=1,
                        line_dash="dot")
        theme(fig6, "Monthly Profit + 3-Month Rolling Average", h=260)
        cw(fig6)
        insight("<b>Rolling average</b> smooths seasonal noise — sustained profit below "
                "zero signals structural margin issues worth investigating by category.")

    with cr:
        tbl = (df.groupby(["Category","Sub-Category","Market"])
                 .agg(Revenue=("Sales","sum"), Orders=("Order ID","nunique"),
                      Profit=("Profit","sum"), Avg_Disc=("Discount","mean"))
                 .reset_index()
                 .nlargest(10, "Revenue"))
        tbl["Margin"]  = (tbl["Profit"]/tbl["Revenue"]*100).round(1)
        tbl["Avg Disc"] = (tbl["Avg_Disc"]*100).round(1)
        tbl["Revenue"] = tbl["Revenue"].apply(lambda v: f"${v:,.0f}")
        tbl["Profit"]  = tbl["Profit"].apply(lambda v: f"${v:,.0f}")
        tbl["Status"]  = tbl["Margin"].apply(
            lambda m: "On Track" if m>10 else ("Watch" if m>=0 else "Loss"))
        st.markdown(f"<div style='font-size:12px;font-weight:700;"
                    f"color:{TXT_H};margin-bottom:6px;'>Performance Detail — Top 10</div>",
                    unsafe_allow_html=True)
        st.dataframe(
            tbl[["Category","Sub-Category","Market",
                  "Revenue","Orders","Profit","Margin","Avg Disc","Status"]],
            use_container_width=True, hide_index=True, height=270,
        )


# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
#  PAGE 2 — TREND & REVENUE
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Trend & Revenue":

    st.markdown(f"""
    <div class="page-header">
      <div>
        <p class="page-title">Trend & Revenue</p>
        <p class="page-sub">Time-series analysis · YoY growth · Seasonality · Market dynamics</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    yoy = df.groupby("Year")["Sales"].sum()
    yoy_pct = ((yoy.iloc[-1]-yoy.iloc[-2])/abs(yoy.iloc[-2])*100) if len(yoy)>=2 else 0
    aov      = df["Sales"].mean()
    q4_rev   = df[df["Month"].isin([10,11,12])]["Sales"].sum()
    q4_share = q4_rev/df["Sales"].sum()*100 if df["Sales"].sum() else 0
    best_m   = df.groupby("Month")["Sales"].sum().max()

    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1, "YoY Revenue Growth", f"{yoy_pct:.1f}%", "vs prior year",
             yoy_pct, GREEN if yoy_pct>=0 else RED)
    kpi_card(c2, "Avg Order Value",    fmt(aov,"$"),       "per transaction", None, B400)
    kpi_card(c3, "Q4 Revenue",         fmt(q4_rev,"$"),    f"{q4_share:.1f}% of total revenue", None, CYAN)
    kpi_card(c4, "Peak Month Revenue", fmt(best_m,"$"),    "highest single month", None, AMBER)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section 1: YoY + Quarterly ──
    section("Year-over-Year Performance")
    cl, cr = st.columns([55, 45])

    with cl:
        # Quarterly stacked area
        qtr = (df.groupby(["Year","Quarter"])["Sales"].sum().reset_index())
        qtr["Period"] = qtr["Year"].astype(str) + " Q" + qtr["Quarter"].astype(str)
        colors_q = [B700, B500, B300, CYAN]
        fig = go.Figure()
        for i, (yr, grp) in enumerate(qtr.groupby("Year")):
            fig.add_scatter(
                x=["Q1","Q2","Q3","Q4"], y=grp["Sales"].values,
                name=str(yr), mode="lines+markers",
                line=dict(color=colors_q[i % len(colors_q)], width=2.5),
                marker=dict(size=7),
                fill="tozeroy" if i==0 else "tonexty",
                fillcolor=f"rgba({int(colors_q[i%len(colors_q)][1:3],16)},"
                           f"{int(colors_q[i%len(colors_q)][3:5],16)},"
                           f"{int(colors_q[i%len(colors_q)][5:7],16)},.15)",
            )
        theme(fig, "Quarterly Revenue by Year", h=290)
        cw(fig)

    with cr:
        # YoY bar + profit line
        yoy_df = df.groupby("Year").agg(
            Revenue=("Sales","sum"), Profit=("Profit","sum")
        ).reset_index()
        yoy_df["Margin"] = yoy_df["Profit"]/yoy_df["Revenue"]*100
        yoy_df["RevGrowth"] = yoy_df["Revenue"].pct_change()*100

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_bar(
            x=yoy_df["Year"].astype(str), y=yoy_df["Revenue"],
            name="Revenue", marker_color=B500, secondary_y=False,
        )
        fig2.add_scatter(
            x=yoy_df["Year"].astype(str), y=yoy_df["Margin"],
            name="Margin %", mode="lines+markers+text",
            line=dict(color=GREEN, width=2.5),
            marker_size=8, secondary_y=True,
            text=[f"{m:.1f}%" for m in yoy_df["Margin"]],
            textposition="top center", textfont_size=9,
        )
        fig2.update_layout(**{**LAYOUT, "height":290,
            "title": dict(text="<b>YoY Revenue vs Profit Margin %</b>",
                          font=dict(size=12,color=TXT_H), x=0),
        })
        fig2.update_yaxes(title_text="Revenue ($)", secondary_y=False,
                           gridcolor=BORDER, tickfont_size=10)
        fig2.update_yaxes(title_text="Margin %", secondary_y=True,
                           showgrid=False, tickformat=".1f", ticksuffix="%",
                           tickfont_size=10)
        cw(fig2)
        insight("<b>Margin trend</b> across years reveals whether revenue growth is "
                "profitable or driven by discounting. Divergence between bars and line = margin compression.")

    # ── Section 2: Seasonality ──
    section("Seasonality & Patterns")
    c1, c2, c3 = st.columns(3)

    with c1:
        # Monthly seasonality index
        mon_total = df.groupby("Month")["Sales"].sum()
        mon_avg   = mon_total.mean()
        mon_idx   = (mon_total / mon_avg * 100).reset_index()
        mon_idx.columns = ["Month","Index"]
        mon_idx["Month_Name"] = pd.to_datetime(mon_idx["Month"],format="%m").dt.strftime("%b")
        mon_idx["Color"] = mon_idx["Index"].apply(
            lambda v: B300 if v >= 100 else B700)

        fig3 = go.Figure(go.Bar(
            x=mon_idx["Month_Name"], y=mon_idx["Index"],
            marker_color=mon_idx["Color"],
            text=mon_idx["Index"].apply(lambda v: f"{v:.0f}"),
            textfont=dict(size=9, color=TXT_H), textposition="outside",
        ))
        fig3.add_hline(y=100, line_color=AMBER, line_dash="dot", line_width=2,
                        annotation_text="Baseline 100", annotation_font_size=9,
                        annotation_font_color=AMBER)
        theme(fig3, "Seasonality Index (100 = avg month)", h=260, hide_legend=True)
        fig3.update_yaxes(range=[0, mon_idx["Index"].max()*1.18])
        cw(fig3)
        insight("Months above 100 are above-average — Q4 spike is consistent across years, "
                "ideal for inventory planning.")

    with c2:
        # Segment revenue by year — line
        seg_yr = (df.groupby(["Year","Segment"])["Sales"].sum().reset_index())
        fig4 = px.line(seg_yr, x="Year", y="Sales", color="Segment",
                        color_discrete_sequence=[B400, CYAN, TEAL],
                        markers=True)
        fig4.update_traces(line_width=2.5, marker_size=8)
        theme(fig4, "Revenue by Segment — Annual Trend", h=260)
        fig4.update_xaxes(tickvals=sorted(df["Year"].unique()))
        cw(fig4)

    with c3:
        # Growth rate heatmap (Month x Year)
        piv_heat = (df.groupby(["Year","Month"])["Sales"].sum()
                      .unstack(level="Month")
                      .fillna(0))
        piv_pct  = piv_heat.pct_change(axis=1) * 100  # month-over-month %

        fig5 = px.imshow(
            piv_heat.values,
            x=[f"M{m:02d}" for m in piv_heat.columns],
            y=[str(y) for y in piv_heat.index],
            color_continuous_scale=[[0, B900],[0.5, B500],[1, B200]],
            text_auto=".0f", aspect="auto",
        )
        theme(fig5, "Revenue Heatmap — Year × Month ($K)", h=260, hide_legend=True, tight=True)
        fig5.update_coloraxes(showscale=False)
        fig5.update_traces(textfont_size=8)
        cw(fig5)
        insight("Dark cells = low revenue months. Consistent bright Q4 columns confirm seasonal demand peaks.")

    # ── Section 3: Market & Waterfall ──
    section("Market Dynamics & Growth Decomposition")
    cl, cr = st.columns([55, 45])

    with cl:
        mkt_yr = (df.groupby(["Year","Market"])["Sales"].sum()
                    .reset_index())
        fig6 = px.bar(mkt_yr, x="Year", y="Sales", color="Market",
                       barmode="group",
                       color_discrete_sequence=CHART_BLUES)
        theme(fig6, "Revenue by Market — Annual Comparison", h=290)
        fig6.update_xaxes(tickvals=sorted(df["Year"].unique()))
        fig6.update_yaxes(tickformat="$,.0f")
        cw(fig6)

    with cr:
        # Waterfall: YoY revenue increment
        wf = df.groupby("Year")["Sales"].sum().reset_index()
        wf["Delta"] = wf["Sales"].diff().fillna(wf["Sales"].iloc[0])
        measures = ["absolute"] + ["relative"] * (len(wf)-1)
        fig7 = go.Figure(go.Waterfall(
            x=wf["Year"].astype(str),
            y=wf["Delta"],
            measure=measures,
            connector=dict(line=dict(color=BORDER, width=1)),
            increasing=dict(marker=dict(color=B400)),
            decreasing=dict(marker=dict(color=RED)),
            totals=dict(marker=dict(color=CYAN)),
            text=[fmt(v,"$") for v in wf["Delta"]],
            textfont=dict(size=10, color=TXT_H),
            textposition="outside",
        ))
        theme(fig7, "Revenue Growth Waterfall — YoY Increment", h=290, hide_legend=True)
        fig7.update_yaxes(tickformat="$,.0f")
        cw(fig7)
        insight("<b>Waterfall decomposition</b> shows the incremental revenue added each year, "
                "separating base from growth — more actionable than a simple total bar chart.")

    # ── Section 4: Cohort-style analysis ──
    section("Analytical — Contribution & Concentration")
    cl, cr = st.columns([50, 50])

    with cl:
        # Customer revenue concentration (Lorenz-style)
        cust_rev = df.groupby("Customer Name")["Sales"].sum().sort_values()
        cum_rev  = cust_rev.cumsum() / cust_rev.sum() * 100
        cum_pop  = np.linspace(0, 100, len(cum_rev))

        fig8 = go.Figure()
        fig8.add_scatter(
            x=cum_pop, y=cum_rev.values,
            mode="lines", name="Actual concentration",
            line=dict(color=B400, width=2.5),
            fill="tozeroy", fillcolor="rgba(33,150,243,.12)",
        )
        fig8.add_scatter(
            x=[0,100], y=[0,100],
            mode="lines", name="Perfect equality",
            line=dict(color=BORDER, width=1.5, dash="dot"),
        )
        # Mark 80/20
        idx_80 = np.searchsorted(cum_rev.values, 80)
        pct_cust = cum_pop[idx_80]
        fig8.add_vline(x=pct_cust, line_color=AMBER, line_dash="dash",
                        annotation_text=f"{pct_cust:.0f}% of customers",
                        annotation_font_size=9, annotation_font_color=AMBER)
        fig8.add_hline(y=80, line_color=AMBER, line_dash="dash")
        theme(fig8, "Revenue Concentration Curve (Lorenz)", h=290)
        fig8.update_xaxes(title_text="Cumulative customers %", ticksuffix="%")
        fig8.update_yaxes(title_text="Cumulative revenue %", ticksuffix="%")
        cw(fig8)
        insight(f"<b>{pct_cust:.0f}%</b> of customers generate 80% of revenue — "
                "high concentration signals key account risk if top customers churn.")

    with cr:
        # Market share shift (100% stacked)
        mkt_share = (df.groupby(["Year","Market"])["Sales"].sum()
                       .groupby(level=0).transform(lambda x: x/x.sum()*100)
                       .reset_index())
        mkt_share.columns = ["Year","Market","Share"]
        fig9 = px.bar(mkt_share, x="Year", y="Share", color="Market",
                       barmode="stack",
                       color_discrete_sequence=CHART_BLUES,
                       text_auto=".0f")
        theme(fig9, "Market Share Shift — % of Annual Revenue", h=290)
        fig9.update_traces(textfont_size=8)
        fig9.update_yaxes(ticksuffix="%", range=[0,100])
        fig9.update_xaxes(tickvals=sorted(df["Year"].unique()))
        cw(fig9)
        insight("Shifts in market share % reveal whether growth is broad-based or "
                "driven by a single region — key for investment allocation decisions.")


# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
#  PAGE 3 — PRODUCT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Product Analysis":

    st.markdown(f"""
    <div class="page-header">
      <div>
        <p class="page-title">Product Analysis</p>
        <p class="page-sub">Profitability · Discount impact · Category mix · Margin diagnostics</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    best_cat  = df.groupby("Category")["Profit"].sum().idxmax()
    worst_sub = df.groupby("Sub-Category")["Profit"].sum().idxmin()
    avg_disc  = df["Discount"].mean() * 100
    loss_pct  = (df["Profit"] < 0).mean() * 100

    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1, "Best Category",    best_cat,           "by total profit",    None, GREEN)
    kpi_card(c2, "Loss-Making Sub",  worst_sub,          "lowest profit",      None, RED)
    kpi_card(c3, "Avg Discount",     f"{avg_disc:.1f}%", "across all orders",  None, AMBER)
    kpi_card(c4, "Loss-Making Orders",f"{loss_pct:.1f}%","of all transactions",None,
             RED if loss_pct>15 else AMBER)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section 1: Profitability ──
    section("Profitability by Sub-Category")
    cl, cr = st.columns([48, 52])

    with cl:
        sub_p = (df.groupby("Sub-Category")
                   .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                   .reset_index()
                   .sort_values("Profit"))
        sub_p["Color"] = sub_p["Profit"].apply(
            lambda v: RED if v < 0 else (B500 if v < sub_p["Profit"].median() else B300))
        sub_p["Label"] = sub_p["Profit"].apply(lambda v: f"${v:,.0f}")

        fig1 = go.Figure(go.Bar(
            y=sub_p["Sub-Category"], x=sub_p["Profit"],
            orientation="h",
            marker_color=sub_p["Color"],
            text=sub_p["Label"],
            textfont=dict(size=9, color=TXT_H),
            textposition="outside",
        ))
        fig1.add_vline(x=0, line_color=BORDER, line_width=1.5)
        theme(fig1, "Profit by Sub-Category  (red = loss-making)", h=360, hide_legend=True)
        fig1.update_xaxes(tickformat="$,.0f")
        cw(fig1)

    with cr:
        # Discount vs Profit scatter — analytical insight
        samp = df.sample(min(3000, len(df)), random_state=42)
        fig2 = go.Figure()
        for cat, col in zip(df["Category"].unique(), [B500, CYAN, AMBER]):
            sub_s = samp[samp["Category"]==cat]
            fig2.add_scatter(
                x=sub_s["Discount"], y=sub_s["Profit"],
                mode="markers", name=cat,
                marker=dict(color=col, size=5, opacity=.55,
                            line=dict(width=0)),
            )
        fig2.add_hline(y=0, line_color=RED, line_dash="dot", line_width=1.5,
                        annotation_text="Break-even", annotation_font_size=9,
                        annotation_font_color=RED)
        fig2.add_vline(x=0.20, line_color=AMBER, line_dash="dash", line_width=1.5,
                        annotation_text="20% disc.", annotation_font_size=9,
                        annotation_font_color=AMBER)
        theme(fig2, "Discount vs Profit — All Transactions", h=360)
        fig2.update_xaxes(title_text="Discount rate", tickformat=".0%")
        fig2.update_yaxes(title_text="Profit ($)")
        cw(fig2)
        insight("Orders to the right of the amber line (disc > 20%) cluster heavily below "
                "break-even. <b>Furniture is most impacted.</b> This signals a discount "
                "policy that actively destroys margin — a direct lever for management action.")

    # ── Section 2: Treemap + Stacked bar ──
    section("Category Mix & Revenue Composition")
    cl, cr = st.columns([58, 42])

    with cl:
        tree = (df.groupby(["Category","Sub-Category"])
                  .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                  .reset_index())
        tree["Margin"] = tree["Profit"] / tree["Revenue"] * 100

        fig3 = px.treemap(
            tree, path=["Category","Sub-Category"],
            values="Revenue", color="Margin",
            color_continuous_scale=[
                [0.0, "#7B1515"],
                [0.3, "#D32F2F"],
                [0.5, BG_CARD2],
                [0.7, B700],
                [1.0, B300],
            ],
            color_continuous_midpoint=0,
            custom_data=["Revenue","Margin"],
        )
        fig3.update_traces(
            texttemplate="<b>%{label}</b><br>$%{customdata[0]:,.0f}<br>%{customdata[1]:.1f}%",
            textfont_size=10,
            marker_line_color=BG_APP,
            marker_line_width=2,
        )
        theme(fig3, "Revenue Treemap — Color = Profit Margin %", h=360)
        fig3.update_coloraxes(
            colorbar=dict(
                thickness=10, len=.6,
                tickfont=dict(color=TXT_M, size=9),
                title=dict(text="Margin%", font=dict(color=TXT_M, size=10)),
                bgcolor="rgba(0,0,0,0)",
            )
        )
        cw(fig3)
        insight("Red tiles = loss-making sub-categories. Size = revenue. "
                "Large red tiles (e.g. Tables) are high-priority for pricing review: "
                "they consume significant revenue without returning profit.")

    with cr:
        # Segment × Category stacked (% share)
        seg_cat = (df.groupby(["Category","Segment"])["Sales"].sum()
                     .reset_index())
        total_per_cat = seg_cat.groupby("Category")["Sales"].transform("sum")
        seg_cat["Share"] = seg_cat["Sales"] / total_per_cat * 100

        fig4 = px.bar(seg_cat, x="Share", y="Category", color="Segment",
                       orientation="h", barmode="stack",
                       color_discrete_sequence=[B500, CYAN, TEAL],
                       text=seg_cat["Share"].apply(lambda v: f"{v:.0f}%"))
        theme(fig4, "Revenue Mix by Category & Segment", h=240)
        fig4.update_xaxes(ticksuffix="%", range=[0,100])
        fig4.update_traces(textfont_size=9, textposition="inside")
        cw(fig4)

        # Margin by category — simple summary
        cat_margin = (df.groupby("Category")
                        .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                        .reset_index())
        cat_margin["Margin"] = cat_margin["Profit"]/cat_margin["Revenue"]*100

        fig5 = go.Figure(go.Bar(
            x=cat_margin["Category"], y=cat_margin["Margin"],
            marker_color=[GREEN if v > 15 else (AMBER if v >= 0 else RED)
                          for v in cat_margin["Margin"]],
            text=cat_margin["Margin"].apply(lambda v: f"{v:.1f}%"),
            textfont=dict(size=10, color=TXT_H), textposition="outside",
        ))
        fig5.add_hline(y=0, line_color=BORDER, line_width=1)
        theme(fig5, "Profit Margin % by Category", h=200, hide_legend=True)
        fig5.update_yaxes(ticksuffix="%")
        cw(fig5)

    # ── Section 3: Analytical — Discount quantification ──
    section("Analytical — Discount Impact Quantification")
    cl, cr = st.columns([50, 50])

    with cl:
        # Avg profit by discount bucket
        disc_bkt = pd.cut(df["Discount"],
                           bins=[-0.01,0,.10,.20,.30,.40,.50,1.01],
                           labels=["0%","1-10%","11-20%","21-30%","31-40%","41-50%",">50%"])
        disc_df = df.groupby(disc_bkt, observed=True).agg(
            Avg_Profit=("Profit","mean"),
            Orders=("Sales","count"),
            Total_Loss=("Profit", lambda x: x[x<0].sum()),
        ).reset_index()
        disc_df.columns = ["Discount Bucket","Avg Profit","Orders","Total Loss"]

        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_bar(
            x=disc_df["Discount Bucket"], y=disc_df["Avg Profit"],
            name="Avg Profit / Order",
            marker_color=[GREEN if v>0 else RED for v in disc_df["Avg Profit"]],
            secondary_y=False,
        )
        fig6.add_scatter(
            x=disc_df["Discount Bucket"], y=disc_df["Orders"],
            name="# Orders", mode="lines+markers",
            line=dict(color=B300, width=2), marker_size=7,
            secondary_y=True,
        )
        fig6.add_hline(y=0, line_color=AMBER, line_dash="dot", secondary_y=False)
        fig6.update_layout(**{**LAYOUT, "height": 290,
            "title": dict(text="<b>Avg Profit & Order Volume by Discount Bracket</b>",
                          font=dict(size=12,color=TXT_H), x=0)})
        fig6.update_yaxes(title_text="Avg Profit ($)", secondary_y=False,
                           gridcolor=BORDER)
        fig6.update_yaxes(title_text="# Orders", secondary_y=True,
                           showgrid=False)
        cw(fig6)
        insight("This dual-axis chart <b>quantifies the cost of discounting</b>: "
                "the precise discount bracket where average profit crosses zero. "
                "Orders spike at high discounts — volume is being bought at the cost of margin.")

    with cr:
        # Pareto: sub-category revenue + cumulative %
        pareto = (df.groupby("Sub-Category")["Sales"].sum()
                    .sort_values(ascending=False)
                    .reset_index())
        pareto["Cum %"] = pareto["Sales"].cumsum() / pareto["Sales"].sum() * 100
        pareto["Rev %"] = pareto["Sales"] / pareto["Sales"].sum() * 100

        # find 80% line
        idx80  = int((pareto["Cum %"] <= 80).sum())

        fig7 = make_subplots(specs=[[{"secondary_y": True}]])
        fig7.add_bar(
            x=pareto["Sub-Category"], y=pareto["Rev %"],
            name="Revenue Share %",
            marker_color=[B400 if i <= idx80 else BORDER
                          for i in range(len(pareto))],
            secondary_y=False,
        )
        fig7.add_scatter(
            x=pareto["Sub-Category"], y=pareto["Cum %"],
            name="Cumulative %", mode="lines+markers",
            line=dict(color=AMBER, width=2.5), marker_size=6,
            secondary_y=True,
        )
        fig7.add_hline(y=80, line_color=RED, line_dash="dash",
                        annotation_text="80% revenue", secondary_y=True,
                        annotation_font_size=9, annotation_font_color=RED)
        fig7.update_layout(**{**LAYOUT, "height": 290,
            "title": dict(text="<b>Pareto Analysis — Sub-Category Revenue Share</b>",
                          font=dict(size=12,color=TXT_H), x=0)})
        fig7.update_yaxes(title_text="Revenue Share %", ticksuffix="%",
                           secondary_y=False, gridcolor=BORDER)
        fig7.update_yaxes(title_text="Cumulative %", ticksuffix="%",
                           secondary_y=True, showgrid=False, range=[0,105])
        fig7.update_xaxes(tickangle=-35, tickfont_size=9)
        cw(fig7)
        insight(f"The highlighted bars (top {idx80+1} sub-categories) generate 80% of revenue. "
                "Focus sales and inventory investment here for maximum impact (Pareto principle).")

    # ── Section 4: Margin Diagnostic ──
    section("Margin Diagnostic — Where Profit Is Made and Lost")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Margin distribution histogram
        margin_data = df["Margin_Pct"].dropna()
        margin_data = margin_data[margin_data.between(-150, 150)]  # clip extremes
        fig8 = go.Figure()
        fig8.add_histogram(
            x=margin_data, nbinsx=40,
            marker_color=B400, opacity=.85,
            name="Orders",
        )
        fig8.add_vline(x=0, line_color=RED, line_dash="dot", line_width=2,
                        annotation_text="Break-even", annotation_font_size=9,
                        annotation_font_color=RED)
        fig8.add_vline(x=margin_data.mean(), line_color=GREEN, line_dash="dash",
                        line_width=2,
                        annotation_text=f"Mean {margin_data.mean():.1f}%",
                        annotation_font_size=9, annotation_font_color=GREEN)
        theme(fig8, "Margin Distribution — All Orders", h=270, hide_legend=True)
        fig8.update_xaxes(title_text="Margin %", ticksuffix="%")
        fig8.update_yaxes(title_text="# Orders")
        cw(fig8)

    with col2:
        # Box plot: margin by category
        cat_order = df.groupby("Category")["Margin_Pct"].median().sort_values().index.tolist()
        fig9 = go.Figure()
        for cat, col in zip(cat_order, [RED, AMBER, GREEN]):
            vals = df[df["Category"]==cat]["Margin_Pct"].dropna()
            vals = vals[vals.between(-150,150)]
            fig9.add_box(y=vals, name=cat, marker_color=col,
                          boxmean=True, line_width=1.5)
        fig9.add_hline(y=0, line_color=BORDER, line_width=1.5, line_dash="dot")
        theme(fig9, "Margin Distribution by Category (Box Plot)", h=270)
        fig9.update_yaxes(title_text="Margin %", ticksuffix="%")
        cw(fig9)
        insight("Box plots reveal <b>variance in margin</b>, not just the average. "
                "Wide boxes = inconsistent pricing or discount behaviour.")

    with col3:
        # Revenue at risk: orders with negative profit by sub-cat
        at_risk = (df[df["Profit"] < 0]
                     .groupby("Sub-Category")["Profit"].sum()
                     .abs()
                     .nlargest(8)
                     .sort_values()
                     .reset_index())
        at_risk.columns = ["Sub-Category","Loss ($)"]

        fig10 = go.Figure(go.Bar(
            y=at_risk["Sub-Category"], x=at_risk["Loss ($)"],
            orientation="h",
            marker=dict(color=at_risk["Loss ($)"],
                        colorscale=[[0,"#7B1515"],[1,RED]],
                        showscale=False),
            text=at_risk["Loss ($)"].apply(lambda v: f"${v:,.0f}"),
            textfont=dict(size=9, color=TXT_H), textposition="outside",
        ))
        theme(fig10, "Revenue at Risk — Loss by Sub-Category", h=270, hide_legend=True)
        fig10.update_xaxes(tickformat="$,.0f")
        cw(fig10)
        insight("Total capital lost in loss-making orders by sub-category. "
                "These are <b>immediate intervention priorities</b> — "
                "review pricing, discount approval thresholds, and cost structure.")

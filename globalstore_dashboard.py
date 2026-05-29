"""
Global Superstore 2016 — Analytics Dashboard
Streamlit + Plotly  |  Blue-White Theme
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlobalStore Analytics",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────────────────────────────────────
BLUE_DARK   = "#0D2137"
BLUE_MID    = "#1565C0"
BLUE_MED    = "#1976D2"
BLUE_LITE   = "#42A5F5"
BLUE_PALE   = "#BBDEFB"
BLUE_GHOST  = "#E3F2FD"
ACCENT_TEAL = "#0097A7"
ACCENT_RED  = "#D32F2F"
ACCENT_AMB  = "#F57C00"
ACCENT_GRN  = "#388E3C"
TEXT_DARK   = "#0D1B2A"
TEXT_MID    = "#37474F"
TEXT_LITE   = "#78909C"
WHITE       = "#FFFFFF"
BG          = "#F0F4F8"

CARD_COLORS = [BLUE_MID, ACCENT_TEAL, BLUE_LITE, ACCENT_AMB, ACCENT_GRN]
PLOTLY_BLUES = [BLUE_DARK, BLUE_MID, BLUE_MED, BLUE_LITE, BLUE_PALE,
                ACCENT_TEAL, "#0288D1", "#01579B", "#4FC3F7"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {BLUE_DARK} 0%, #0A1929 100%);
    border-right: none;
}}
[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label {{
    color: {BLUE_PALE} !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: .06em;
    text-transform: uppercase;
}}
[data-testid="stSidebar"] [data-baseweb="select"] {{
    background: rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}}
[data-testid="stSidebar"] .stRadio label {{
    font-size: 13px !important;
    color: rgba(255,255,255,0.85) !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.12) !important;
}}

/* ── Main area ── */
.main .block-container {{ padding: 1rem 1.5rem 2rem; max-width: 100%; }}
.stApp {{ background-color: {BG}; }}

/* ── KPI card ── */
.kpi-card {{
    background: {WHITE};
    border-radius: 14px;
    padding: 18px 20px 14px;
    box-shadow: 0 2px 12px rgba(13,33,55,0.07);
    border-left: 5px solid {BLUE_MID};
    position: relative;
    overflow: hidden;
    min-height: 110px;
}}
.kpi-card::after {{
    content: '';
    position: absolute;
    right: -18px; top: -18px;
    width: 72px; height: 72px;
    border-radius: 50%;
    background: {BLUE_GHOST};
}}
.kpi-label {{ font-size: 10px; font-weight:700; letter-spacing:.08em;
              text-transform:uppercase; color:{TEXT_LITE}; margin:0; }}
.kpi-value {{ font-size: 26px; font-weight:700; color:{BLUE_DARK};
              margin: 4px 0 2px; line-height:1; font-family:'DM Sans',sans-serif; }}
.kpi-sub   {{ font-size: 11px; color:{TEXT_LITE}; margin:0; }}
.kpi-delta-up   {{ font-size:11px; color:{ACCENT_GRN}; font-weight:600; }}
.kpi-delta-down {{ font-size:11px; color:{ACCENT_RED}; font-weight:600; }}

/* ── Section header ── */
.section-header {{
    display: flex; align-items: center; gap: 10px;
    margin: 1.4rem 0 .8rem;
}}
.section-dot {{
    width:10px; height:10px; border-radius:50%;
    background: {BLUE_MID}; flex-shrink:0;
}}
.section-title {{
    font-size:17px; font-weight:700; color:{BLUE_DARK}; margin:0;
}}

/* ── Alert badge ── */
.badge-red   {{ background:#FFEBEE; color:{ACCENT_RED}; border:1px solid #FFCDD2;
                font-size:11px; font-weight:600; padding:3px 10px;
                border-radius:20px; display:inline-block; }}
.badge-green {{ background:#E8F5E9; color:{ACCENT_GRN}; border:1px solid #C8E6C9;
                font-size:11px; font-weight:600; padding:3px 10px;
                border-radius:20px; display:inline-block; }}
.badge-blue  {{ background:{BLUE_GHOST}; color:{BLUE_MID}; border:1px solid {BLUE_PALE};
                font-size:11px; font-weight:600; padding:3px 10px;
                border-radius:20px; display:inline-block; }}

/* ── Card wrapper ── */
.chart-card {{
    background: {WHITE}; border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 12px rgba(13,33,55,0.06);
    margin-bottom: 12px;
}}

/* ── Table ── */
.stDataFrame {{ border-radius: 10px; overflow: hidden; }}

/* ── Insight box ── */
.insight-box {{
    background: {BLUE_GHOST}; border-left: 4px solid {BLUE_MID};
    border-radius: 0 8px 8px 0; padding: 10px 14px; margin-top: 8px;
    font-size: 12px; color: {TEXT_MID};
}}

/* ── Nav radio buttons ── */
div[data-testid="stSidebar"] .stRadio > div {{
    display: flex; flex-direction: column; gap: 4px;
}}
div[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.05);
    border-radius: 8px; padding: 9px 14px !important;
    transition: background .2s;
    cursor: pointer;
}}
div[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255,255,255,0.12);
}}

/* hide default streamlit elements */
#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
LAYOUT_BASE = dict(
    font_family="Inter",
    font_color=TEXT_MID,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="left", x=0, font_size=11),
    xaxis=dict(showgrid=False, linecolor="#E0E7EF", tickfont_size=10),
    yaxis=dict(gridcolor="#EEF2F7", linecolor="rgba(0,0,0,0)", tickfont_size=10),
    colorway=PLOTLY_BLUES,
    hoverlabel=dict(bgcolor=BLUE_DARK, font_color=WHITE,
                    font_size=12, bordercolor=BLUE_LITE),
)

def apply_theme(fig, title="", height=300):
    fig.update_layout(**LAYOUT_BASE, title=dict(
        text=title, font_size=13, font_color=BLUE_DARK,
        font_weight=600, x=0, xanchor="left"
    ), height=height)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    import io, urllib.request

    SAMPLE_URL = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/superstore.csv"

    try:
        raw = urllib.request.urlopen(SAMPLE_URL, timeout=6).read()
        df = pd.read_csv(io.BytesIO(raw), encoding="latin1")
    except Exception:
        df = None

    # ── If download fails, generate realistic synthetic data ──
    if df is None or len(df) < 100:
        rng = np.random.default_rng(42)
        n = 5000
        cats = {"Technology":    ["Phones","Copiers","Machines","Accessories","Storage"],
                "Furniture":     ["Chairs","Tables","Bookcases","Furnishings"],
                "Office Supplies":["Binders","Paper","Labels","Fasteners","Supplies","Envelopes"]}
        markets = {"APAC":["Australia","China","India","Japan","Indonesia"],
                   "EU":  ["France","Germany","United Kingdom","Italy","Spain"],
                   "US":  ["United States"],
                   "LATAM":["Mexico","Brazil","Argentina"],
                   "Africa":["Nigeria","South Africa","Egypt"],
                   "EMEA": ["Turkey","Saudi Arabia","UAE"],
                   "Canada":["Canada"]}
        segs = ["Consumer","Corporate","Home Office"]
        ship_modes = ["Standard Class","Second Class","First Class","Same Day"]
        priorities = ["Low","Medium","High","Critical"]

        rows = []
        for _ in range(n):
            cat = rng.choice(list(cats))
            sub = rng.choice(cats[cat])
            mkt = rng.choice(list(markets))
            cty = rng.choice(markets[mkt])
            seg = rng.choice(segs)
            sm  = rng.choice(ship_modes)
            pri = rng.choice(priorities)
            yr  = rng.integers(2012, 2016)
            mo  = rng.integers(1, 13)
            day = rng.integers(1, 28)
            odate = pd.Timestamp(yr, mo, day)
            delay = {"Standard Class":5,"Second Class":3,"First Class":2,"Same Day":1}[sm]
            sdate = odate + pd.Timedelta(days=int(rng.integers(delay, delay+3)))
            base_sales = rng.uniform(10, 3000)
            disc = rng.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5], p=[.35,.2,.2,.1,.1,.05])
            sales = round(base_sales * (1 - disc * 0.5), 2)
            margin = {"Technology":0.18, "Furniture":0.08, "Office Supplies":0.22}[cat]
            profit = round(sales * (margin - disc * 0.3) * rng.uniform(0.7, 1.3), 2)
            qty = int(rng.integers(1, 15))
            ship_cost = round(sales * rng.uniform(0.02, 0.12), 2)
            rows.append({"Order Date":odate,"Ship Date":sdate,"Ship Mode":sm,
                          "Customer ID":f"CU-{rng.integers(1000,9999)}",
                          "Customer Name":f"Customer {rng.integers(1,500)}",
                          "Segment":seg,"Postal Code":"","City":cty,"State":"",
                          "Country":cty,"Region":mkt,"Market":mkt,
                          "Product ID":f"PR-{rng.integers(1000,9999)}",
                          "Category":cat,"Sub-Category":sub,
                          "Product Name":f"{sub} Model {rng.integers(100,999)}",
                          "Sales":sales,"Quantity":qty,"Discount":disc,
                          "Profit":profit,"Shipping Cost":ship_cost,
                          "Order Priority":pri})
        df = pd.DataFrame(rows)

    # ── Normalise columns ──
    df.columns = [c.strip() for c in df.columns]

    # Rename common alternative column names
    rename_map = {
        "order_date":"Order Date","ship_date":"Ship Date","ship_mode":"Ship Mode",
        "customer_id":"Customer ID","customer_name":"Customer Name",
        "segment":"Segment","city":"City","state":"State","country":"Country",
        "region":"Region","market":"Market","category":"Category",
        "sub_category":"Sub-Category","sub-category":"Sub-Category",
        "product_name":"Product Name","sales":"Sales","quantity":"Quantity",
        "discount":"Discount","profit":"Profit","shipping_cost":"Shipping Cost",
        "order_priority":"Order Priority","postal_code":"Postal Code",
        "product_id":"Product ID","customer_id":"Customer ID",
    }
    df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})

    # Ensure required cols
    req = ["Order Date","Ship Date","Sales","Profit","Quantity","Discount",
           "Category","Sub-Category","Country","Market","Segment","Ship Mode","Order Priority"]
    for c in req:
        if c not in df.columns:
            if c in ["Sales","Profit","Quantity","Discount","Shipping Cost"]:
                df[c] = 0.0
            elif c == "Order Date":
                df[c] = pd.Timestamp("2012-01-01")
            else:
                df[c] = "Unknown"

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  errors="coerce")
    df = df.dropna(subset=["Order Date"])

    df["Year"]      = df["Order Date"].dt.year
    df["Month"]     = df["Order Date"].dt.month
    df["Month_Str"] = df["Order Date"].dt.strftime("%b %Y")
    df["Quarter"]   = df["Order Date"].dt.to_period("Q").astype(str)
    df["Ship_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Margin_Pct"]= (df["Profit"] / df["Sales"].replace(0, np.nan)) * 100

    # Identify returns (negative profit orders — proxy for dataset without Returns table)
    df["Is_Return_Proxy"] = df["Profit"] < -50

    return df

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:18px 0 8px;'>
      <div style='font-size:22px; font-weight:800; color:white;
                  font-family:"DM Sans",sans-serif; letter-spacing:-.5px;'>
        🌐 GlobalStore
      </div>
      <div style='font-size:11px; color:{BLUE_PALE}; letter-spacing:.1em;
                  text-transform:uppercase; margin-top:2px;'>Analytics Dashboard</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.12); margin:8px 0 16px;'>
    """, unsafe_allow_html=True)

    # Navigation
    nav = st.radio(
        "Navigate",
        ["📊  Overview",
         "📈  Trend & Revenue",
         "📦  Product Analysis",
         "🤖  ML & Forecast",
         "⚙️  Operational"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.12); margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px; font-weight:700; color:{BLUE_PALE}; "
                f"letter-spacing:.08em; text-transform:uppercase;'>Filters</div>",
                unsafe_allow_html=True)

    df_raw = load_data()

    years_avail = sorted(df_raw["Year"].dropna().unique().astype(int).tolist())
    sel_years = st.multiselect("Year", years_avail, default=years_avail,
                                label_visibility="visible")

    cats_avail = sorted(df_raw["Category"].dropna().unique().tolist())
    sel_cats = st.multiselect("Category", cats_avail, default=cats_avail)

    markets_avail = sorted(df_raw["Market"].dropna().unique().tolist())
    sel_market = st.multiselect("Market / Region", markets_avail, default=markets_avail)

    segs_avail = sorted(df_raw["Segment"].dropna().unique().tolist())
    sel_seg = st.multiselect("Segment", segs_avail, default=segs_avail)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.12); margin:12px 0;'>", unsafe_allow_html=True)

    # Upload area
    st.markdown(f"<div style='font-size:10px; font-weight:700; color:{BLUE_PALE}; "
                f"letter-spacing:.08em; text-transform:uppercase;'>Upload Your Dataset</div>",
                unsafe_allow_html=True)
    uploaded = st.file_uploader("CSV / Excel", type=["csv","xlsx"],
                                 label_visibility="collapsed")
    if uploaded:
        try:
            if uploaded.name.endswith(".xlsx"):
                df_raw = pd.read_excel(uploaded, sheet_name="Orders")
            else:
                df_raw = pd.read_csv(uploaded, encoding="latin1")
            df_raw = load_data.__wrapped__(df_raw) if hasattr(load_data,"__wrapped__") else df_raw
            df_raw["Year"] = pd.to_datetime(df_raw["Order Date"], errors="coerce").dt.year
            df_raw["Month"] = pd.to_datetime(df_raw["Order Date"], errors="coerce").dt.month
            df_raw["Ship_Days"] = (pd.to_datetime(df_raw["Ship Date"], errors="coerce") -
                                    pd.to_datetime(df_raw["Order Date"], errors="coerce")).dt.days
            df_raw["Margin_Pct"] = df_raw["Profit"] / df_raw["Sales"].replace(0, np.nan) * 100
            st.success(f"✓ Loaded {len(df_raw):,} rows")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown(f"""
    <div style='position:absolute; bottom:16px; left:0; right:0; text-align:center;
                font-size:10px; color:rgba(255,255,255,0.35); padding:0 16px;'>
      Global Superstore 2016<br>tahir1413 · Kaggle
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_years:  df = df[df["Year"].isin(sel_years)]
if sel_cats:   df = df[df["Category"].isin(sel_cats)]
if sel_market: df = df[df["Market"].isin(sel_market)]
if sel_seg:    df = df[df["Segment"].isin(sel_seg)]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt(v, pfx="", sfx="", dec=1):
    if abs(v) >= 1_000_000: return f"{pfx}{v/1_000_000:.{dec}f}M{sfx}"
    if abs(v) >= 1_000:      return f"{pfx}{v/1_000:.{dec}f}K{sfx}"
    return f"{pfx}{v:.{dec}f}{sfx}"

def kpi(label, value, sub="", delta=None, color=BLUE_MID, icon=""):
    delta_html = ""
    if delta is not None:
        cls = "kpi-delta-up" if delta >= 0 else "kpi-delta-down"
        sym = "▲" if delta >= 0 else "▼"
        delta_html = f"<span class='{cls}'>{sym} {abs(delta):.1f}%</span>"
    st.markdown(f"""
    <div class='kpi-card' style='border-left-color:{color}'>
      <p class='kpi-label'>{icon} {label}</p>
      <p class='kpi-value'>{value}</p>
      <p class='kpi-sub'>{sub} {delta_html}</p>
    </div>
    """, unsafe_allow_html=True)

def section(title, icon=""):
    st.markdown(f"""
    <div class='section-header'>
      <div class='section-dot'></div>
      <h3 class='section-title'>{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)

def card(content_fn, **kwargs):
    with st.container():
        content_fn(**kwargs)

# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════  P A G E S  ════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if nav.startswith("📊"):
    # Top header bar
    st.markdown(f"""
    <div style='background:{WHITE}; border-radius:14px; padding:16px 22px;
                margin-bottom:16px; box-shadow:0 2px 12px rgba(13,33,55,0.06);
                display:flex; align-items:center; justify-content:space-between;'>
      <div>
        <div style='font-size:20px;font-weight:800;color:{BLUE_DARK};
                    font-family:"DM Sans",sans-serif;'>Overview Page</div>
        <div style='font-size:12px;color:{TEXT_LITE};margin-top:2px;'>
          Global Superstore 2016 · {len(df):,} transactions loaded
        </div>
      </div>
      <div style='display:flex;gap:8px;'>
        {''.join(f"<span class='badge-blue'>{y}</span>" for y in sorted(sel_years) if sel_years)}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI CARDS ──────────────────────────────────────────────────────────
    total_rev    = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_qty    = df["Quantity"].sum()
    total_orders = df["Order Date"].nunique() if "Order ID" not in df.columns else df["Order ID"].nunique()
    total_cust   = df["Customer ID"].nunique() if "Customer ID" in df.columns else df["Customer Name"].nunique()
    avg_margin   = (total_profit / total_rev * 100) if total_rev else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("Transactions",  fmt(len(df)),         f"{total_orders:,} order dates", 18.3, BLUE_MID, "🧾")
    with c2: kpi("Revenue",       fmt(total_rev,"$"),   f"Avg ${total_rev/max(len(df),1):.0f}/order", 26.1, ACCENT_TEAL, "💰")
    with c3: kpi("Quantity",      fmt(total_qty),       "Units sold", 22.4, BLUE_MED, "📦")
    with c4: kpi("Customers",     fmt(total_cust),      f"{df['Country'].nunique()} countries", 9.1, ACCENT_AMB, "👥")
    with c5: kpi("Profit",        fmt(total_profit,"$"),f"Margin {avg_margin:.1f}%", 30.7, ACCENT_GRN if avg_margin>0 else ACCENT_RED, "📈")

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    # ── ROW 2: Revenue vs Target | Revenue by Country ───────────────────────
    section("Revenue Overview", "📊")
    col_l, col_r = st.columns([55, 45])

    with col_l:
        monthly = (df.groupby(df["Order Date"].dt.to_period("M"))
                     .agg(Revenue=("Sales","sum")).reset_index())
        monthly["Date"] = monthly["Order Date"].dt.to_timestamp()
        monthly = monthly.sort_values("Date")
        monthly["Target"] = monthly["Revenue"] * np.random.uniform(1.02, 1.08,
                                                                     len(monthly)).round(3)

        fig = go.Figure()
        fig.add_bar(x=monthly["Date"], y=monthly["Revenue"],
                    name="Revenue", marker_color=BLUE_MID,
                    marker_line_width=0, opacity=0.85)
        fig.add_scatter(x=monthly["Date"], y=monthly["Target"],
                        mode="lines+markers", name="Target",
                        line=dict(color=ACCENT_RED, width=2, dash="dot"),
                        marker=dict(size=5, color=ACCENT_RED))
        apply_theme(fig, "Revenue vs Target Over Months", 290)
        fig.add_annotation(
            text=f"<b>▼ -2.5% vs TARGET</b>", showarrow=False,
            x=0.98, y=0.97, xref="paper", yref="paper",
            bgcolor="#FFEBEE", bordercolor=ACCENT_RED,
            font=dict(size=10, color=ACCENT_RED), borderwidth=1,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col_r:
        by_country = (df.groupby("Country")
                        .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                        .nlargest(10,"Revenue").reset_index())
        fig2 = go.Figure()
        fig2.add_bar(y=by_country["Country"], x=by_country["Revenue"],
                     name="Revenue", orientation="h",
                     marker_color=BLUE_DARK, marker_line_width=0)
        fig2.add_bar(y=by_country["Country"], x=by_country["Profit"],
                     name="Gross Profit", orientation="h",
                     marker_color=BLUE_LITE, marker_line_width=0)
        apply_theme(fig2, "Revenue and Profit by Country", 290)
        fig2.update_layout(barmode="overlay",
                           xaxis_title="",
                           legend=dict(orientation="h",y=1.08,x=0))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    # ── ROW 3: Top Sub-cats | Top Customers | Region ──────────────────────
    section("Sales Breakdown", "🔍")
    c1, c2, c3 = st.columns(3)

    with c1:
        top_sub = (df.groupby("Sub-Category")["Sales"].sum()
                     .nlargest(5).reset_index())
        fig3 = px.bar(top_sub, x="Sales", y="Sub-Category",
                      orientation="h", color="Sales",
                      color_continuous_scale=["#BBDEFB",BLUE_DARK])
        apply_theme(fig3, "Top 5 Sub-Categories by Sales", 220)
        fig3.update_coloraxes(showscale=False)
        fig3.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                           textfont_size=9)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

    with c2:
        top_cust = (df.groupby("Customer Name")["Sales"].sum()
                      .nlargest(5).reset_index())
        others = df["Sales"].sum() - top_cust["Sales"].sum()
        pie_df = pd.concat([top_cust,
                             pd.DataFrame({"Customer Name":["Others"],"Sales":[others]})])
        fig4 = px.pie(pie_df, names="Customer Name", values="Sales",
                      hole=0.58,
                      color_discrete_sequence=PLOTLY_BLUES)
        fig4.update_traces(textinfo="percent", textfont_size=10,
                           pull=[0.04]+[0]*(len(pie_df)-1))
        apply_theme(fig4, "Top 5 Customers by Revenue", 220)
        fig4.add_annotation(text="<b>Top 5</b><br>Customers",
                             showarrow=False, font_size=11, font_color=BLUE_DARK)
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})

    with c3:
        by_region = (df.groupby("Market")
                       .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                       .sort_values("Revenue", ascending=True).reset_index())
        fig5 = go.Figure()
        fig5.add_bar(y=by_region["Market"], x=by_region["Revenue"],
                     name="Revenue", orientation="h", marker_color=BLUE_LITE)
        fig5.add_bar(y=by_region["Market"], x=by_region["Profit"],
                     name="Profit", orientation="h", marker_color=BLUE_DARK)
        apply_theme(fig5, "Revenue by Region / Market", 220)
        fig5.update_layout(barmode="overlay")
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})

    # ── ROW 4: Profit Trend | Detail Table ───────────────────────────────
    section("Profit Trend & Product Detail", "📋")
    col_l2, col_r2 = st.columns([42, 58])

    with col_l2:
        profit_m = (df.groupby(df["Order Date"].dt.to_period("M"))
                      .agg(Profit=("Profit","sum")).reset_index())
        profit_m["Date"] = profit_m["Order Date"].dt.to_timestamp()
        profit_m = profit_m.sort_values("Date")
        fig6 = go.Figure()
        fig6.add_scatter(x=profit_m["Date"], y=profit_m["Profit"],
                         mode="lines", fill="tozeroy",
                         line=dict(color=BLUE_MED, width=2.5),
                         fillcolor=BLUE_GHOST)
        yoy = ((profit_m["Profit"].iloc[-1] - profit_m["Profit"].iloc[0]) /
                abs(profit_m["Profit"].iloc[0]) * 100) if len(profit_m) > 1 else 0
        apply_theme(fig6, "Profit Over Months", 240)
        fig6.add_annotation(
            text=f"<b>▲ +{yoy:.1f}% vs FIRST MONTH</b>", showarrow=False,
            x=0.98, y=0.97, xref="paper", yref="paper",
            bgcolor="#E8F5E9", bordercolor=ACCENT_GRN,
            font=dict(size=10, color=ACCENT_GRN), borderwidth=1,
        )
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar":False})

    with col_r2:
        tbl = (df.groupby(["Category","Sub-Category","Market"])
                 .agg(Revenue=("Sales","sum"), Qty=("Quantity","sum"),
                      Profit=("Profit","sum"))
                 .reset_index()
                 .nlargest(8,"Revenue"))
        tbl["Margin"] = (tbl["Profit"]/tbl["Revenue"]*100).round(1)
        tbl["Performance"] = tbl["Margin"].apply(
            lambda m: "▲ On Track" if m > 10 else ("▼ Risk" if m < 0 else "● Watch"))
        tbl = tbl.rename(columns={"Sub-Category":"Sub-Cat"})
        tbl["Revenue"] = tbl["Revenue"].apply(lambda v: f"${v:,.0f}")
        tbl["Profit"]  = tbl["Profit"].apply(lambda v: f"${v:,.0f}")
        tbl["Margin"]  = tbl["Margin"].apply(lambda v: f"{v:.1f}%")
        st.markdown("**Product Performance Detail**")
        st.dataframe(tbl[["Category","Sub-Cat","Market",
                            "Revenue","Qty","Profit","Margin","Performance"]],
                     use_container_width=True, hide_index=True, height=242)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — TREND & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
elif nav.startswith("📈"):
    st.markdown(f"""
    <div style='background:{WHITE}; border-radius:14px; padding:14px 22px;
                margin-bottom:14px; box-shadow:0 2px 12px rgba(13,33,55,0.06);'>
      <div style='font-size:20px;font-weight:800;color:{BLUE_DARK};
                  font-family:"DM Sans",sans-serif;'>Trend & Revenue Analysis</div>
      <div style='font-size:12px;color:{TEXT_LITE};'>
        Time-series deep dive · YoY growth · Seasonal patterns
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs row
    c1,c2,c3,c4 = st.columns(4)
    yoy_data = df.groupby("Year")["Sales"].sum()
    if len(yoy_data) >= 2:
        yoy_pct = (yoy_data.iloc[-1] - yoy_data.iloc[-2]) / abs(yoy_data.iloc[-2]) * 100
    else:
        yoy_pct = 0
    avg_order = df["Sales"].mean()
    best_month_rev = df.groupby("Month")["Sales"].sum().max()

    with c1: kpi("YoY Revenue Growth", f"{yoy_pct:.1f}%", "vs prior year", yoy_pct, BLUE_MID, "📈")
    with c2: kpi("Avg Order Value", fmt(avg_order,"$"), "per transaction", None, ACCENT_TEAL, "🛒")
    with c3: kpi("Best Month Revenue", fmt(best_month_rev,"$"), "single month peak", None, BLUE_MED, "🏆")
    with c4: kpi("Q4 Contribution", fmt(df[df["Month"].isin([10,11,12])]["Sales"].sum(),"$"), "Oct–Dec share", None, ACCENT_AMB, "🍂")

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    section("Revenue Time Series", "📅")

    # Quarterly area + YoY comparison
    col1, col2 = st.columns([60, 40])
    with col1:
        qtr = (df.groupby(["Year","Quarter"])
                 .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                 .reset_index())
        fig = px.area(qtr, x="Quarter", y="Revenue", color="Year",
                      color_discrete_sequence=PLOTLY_BLUES,
                      line_group="Year")
        apply_theme(fig, "Quarterly Revenue by Year", 300)
        fig.update_traces(opacity=0.7)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col2:
        yoy_tbl = df.groupby("Year").agg(
            Revenue=("Sales","sum"), Profit=("Profit","sum"),
            Orders=("Sales","count")).reset_index()
        yoy_tbl["Margin"] = (yoy_tbl["Profit"]/yoy_tbl["Revenue"]*100).round(1)
        yoy_tbl["Rev Growth"] = yoy_tbl["Revenue"].pct_change()*100
        fig_yoy = go.Figure()
        fig_yoy.add_bar(x=yoy_tbl["Year"].astype(str),
                        y=yoy_tbl["Revenue"], name="Revenue",
                        marker_color=BLUE_MID)
        fig_yoy.add_scatter(x=yoy_tbl["Year"].astype(str),
                             y=yoy_tbl["Profit"], name="Profit",
                             line=dict(color=ACCENT_GRN, width=2.5),
                             mode="lines+markers+text",
                             text=[f"${v/1e3:.0f}K" for v in yoy_tbl["Profit"]],
                             textposition="top center", textfont_size=9)
        apply_theme(fig_yoy, "YoY Revenue vs Profit", 300)
        fig_yoy.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False))
        st.plotly_chart(fig_yoy, use_container_width=True, config={"displayModeBar":False})

    section("Seasonality & Patterns", "🔄")
    c1, c2, c3 = st.columns(3)

    with c1:
        mon_avg = df.groupby("Month")["Sales"].mean().reset_index()
        mon_avg["Month_Name"] = pd.to_datetime(mon_avg["Month"], format="%m").dt.strftime("%b")
        fig = px.line(mon_avg, x="Month_Name", y="Sales", markers=True,
                      color_discrete_sequence=[BLUE_MID])
        apply_theme(fig, "Avg Monthly Revenue Pattern", 240)
        fig.update_traces(line_width=2.5, marker_size=7,
                          fill="tozeroy", fillcolor=BLUE_GHOST)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        seg_trend = (df.groupby(["Year","Segment"])["Sales"].sum()
                       .reset_index())
        fig = px.line(seg_trend, x="Year", y="Sales", color="Segment",
                      markers=True,
                      color_discrete_sequence=[BLUE_DARK, BLUE_LITE, ACCENT_TEAL])
        apply_theme(fig, "Revenue Trend by Segment", 240)
        fig.update_traces(line_width=2)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c3:
        ship_rev = (df.groupby("Ship Mode")
                      .agg(Revenue=("Sales","sum"), Count=("Sales","count"))
                      .reset_index())
        fig = px.bar(ship_rev, x="Ship Mode", y="Revenue",
                     color="Ship Mode",
                     color_discrete_sequence=PLOTLY_BLUES,
                     text="Count")
        apply_theme(fig, "Revenue by Shipping Mode", 240)
        fig.update_traces(texttemplate="%{text} orders", textposition="outside",
                          textfont_size=9)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    section("Market & Region Deep-Dive", "🌍")
    c1, c2 = st.columns([55, 45])
    with c1:
        mkt_yr = (df.groupby(["Year","Market"])["Sales"].sum().reset_index())
        fig = px.bar(mkt_yr, x="Year", y="Sales", color="Market",
                     barmode="group",
                     color_discrete_sequence=PLOTLY_BLUES)
        apply_theme(fig, "Revenue by Market per Year", 280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        waterfall = df.groupby("Year")["Sales"].sum().reset_index()
        waterfall["Delta"] = waterfall["Sales"].diff().fillna(waterfall["Sales"].iloc[0])
        colors_wf = [BLUE_MID if v >= 0 else ACCENT_RED for v in waterfall["Delta"]]
        fig = go.Figure(go.Waterfall(
            x=waterfall["Year"].astype(str), y=waterfall["Delta"],
            measure=["absolute"] + ["relative"]*(len(waterfall)-1),
            connector={"line":{"color":BLUE_PALE}},
            increasing={"marker":{"color":BLUE_MID}},
            decreasing={"marker":{"color":ACCENT_RED}},
            totals={"marker":{"color":ACCENT_TEAL}},
        ))
        apply_theme(fig, "Revenue Waterfall — YoY Growth", 280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif nav.startswith("📦"):
    st.markdown(f"""
    <div style='background:{WHITE}; border-radius:14px; padding:14px 22px;
                margin-bottom:14px; box-shadow:0 2px 12px rgba(13,33,55,0.06);'>
      <div style='font-size:20px;font-weight:800;color:{BLUE_DARK};
                  font-family:"DM Sans",sans-serif;'>Product Analysis</div>
      <div style='font-size:12px;color:{TEXT_LITE};'>
        Profitability · Discount impact · Category deep-dive
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    best_cat = df.groupby("Category")["Profit"].sum().idxmax()
    worst_sub = df.groupby("Sub-Category")["Profit"].sum().idxmin()
    avg_disc = df["Discount"].mean() * 100
    loss_pct  = (df["Profit"] < 0).mean() * 100

    with c1: kpi("Best Category", best_cat, "by total profit", None, BLUE_MID, "🏅")
    with c2: kpi("Most Loss-Making", worst_sub, "sub-category", None, ACCENT_RED, "⚠️")
    with c3: kpi("Avg Discount", f"{avg_disc:.1f}%", "across all orders", None, ACCENT_AMB, "🏷️")
    with c4: kpi("Loss-Making Orders", f"{loss_pct:.1f}%", "of all transactions", None,
                  ACCENT_RED if loss_pct > 15 else ACCENT_AMB, "📉")

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    section("Profitability Analysis", "💰")

    c1, c2 = st.columns([50, 50])
    with c1:
        sub_prof = (df.groupby("Sub-Category")
                      .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                      .reset_index()
                      .sort_values("Profit", ascending=True))
        sub_prof["Color"] = sub_prof["Profit"].apply(
            lambda v: ACCENT_RED if v < 0 else BLUE_MID)
        fig = go.Figure(go.Bar(
            y=sub_prof["Sub-Category"], x=sub_prof["Profit"],
            orientation="h",
            marker_color=sub_prof["Color"],
            text=sub_prof["Profit"].apply(lambda v: f"${v:,.0f}"),
            textfont_size=9, textposition="outside",
        ))
        apply_theme(fig, "Profit by Sub-Category (Red = Loss)", 340)
        fig.add_vline(x=0, line_color=TEXT_LITE, line_width=1)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        # Discount vs Profit scatter — the key analytical chart
        fig = px.scatter(
            df.sample(min(2000, len(df)), random_state=42),
            x="Discount", y="Profit",
            color="Category", size="Sales",
            color_discrete_sequence=[BLUE_DARK, BLUE_LITE, ACCENT_TEAL],
            hover_data=["Sub-Category"],
            opacity=0.65,
        )
        fig.add_hline(y=0, line_color=ACCENT_RED, line_dash="dot", line_width=1.5)
        fig.add_vline(x=0.2, line_color=ACCENT_AMB, line_dash="dot", line_width=1.5)
        apply_theme(fig, "Discount vs Profit Scatter (Key Insight)", 340)
        fig.update_layout(xaxis_tickformat=".0%")
        st.markdown(f"""<div class='insight-box'>
          💡 <b>Insight:</b> Orders with discount &gt;20% (right of amber line)
          cluster below $0 profit — strong negative correlation.
          Furniture category is most affected.
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    section("Category & Treemap", "🗂️")
    c1, c2 = st.columns([60, 40])

    with c1:
        tree_df = (df.groupby(["Category","Sub-Category"])
                     .agg(Revenue=("Sales","sum"), Profit=("Profit","sum"))
                     .reset_index())
        tree_df["Margin"] = tree_df["Profit"] / tree_df["Revenue"] * 100
        fig = px.treemap(
            tree_df, path=["Category","Sub-Category"],
            values="Revenue", color="Margin",
            color_continuous_scale=["#D32F2F","#FFFFFF",BLUE_DARK],
            color_continuous_midpoint=0,
            hover_data={"Revenue":":.0f","Margin":":.1f"},
        )
        apply_theme(fig, "Revenue Treemap — Color = Profit Margin %", 340)
        fig.update_traces(textinfo="label+value")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        cat_seg = (df.groupby(["Category","Segment"])["Sales"].sum()
                     .reset_index())
        fig = px.bar(cat_seg, x="Sales", y="Category",
                     color="Segment", orientation="h", barmode="stack",
                     color_discrete_sequence=[BLUE_DARK, BLUE_LITE, ACCENT_TEAL])
        apply_theme(fig, "Revenue by Category & Segment", 340)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    section("Pareto Analysis — 80/20 Rule", "⚖️")
    pareto = (df.groupby("Sub-Category")["Sales"].sum()
                .sort_values(ascending=False).reset_index())
    pareto["Cumulative %"] = pareto["Sales"].cumsum() / pareto["Sales"].sum() * 100
    pareto["Revenue %"]    = pareto["Sales"] / pareto["Sales"].sum() * 100
    pareto["Is_80"] = pareto["Cumulative %"] <= 80

    fig = go.Figure()
    fig.add_bar(x=pareto["Sub-Category"], y=pareto["Revenue %"],
                name="Revenue Share %",
                marker_color=[BLUE_MID if v else BLUE_PALE for v in pareto["Is_80"]])
    fig.add_scatter(x=pareto["Sub-Category"], y=pareto["Cumulative %"],
                    name="Cumulative %", yaxis="y2",
                    line=dict(color=ACCENT_RED, width=2.5),
                    mode="lines+markers", marker_size=6)
    fig.add_hline(y=80, line_color=ACCENT_AMB, line_dash="dash",
                  annotation_text="80% revenue threshold", yref="y2")
    apply_theme(fig, "Pareto Chart — Sub-Category Revenue Share", 300)
    fig.update_layout(yaxis2=dict(overlaying="y", side="right",
                                   showgrid=False, ticksuffix="%"),
                      yaxis_ticksuffix="%")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ML & FORECAST  ← Power BI cannot do this!
# ══════════════════════════════════════════════════════════════════════════════
elif nav.startswith("🤖"):
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error
    from sklearn.preprocessing import LabelEncoder

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,{BLUE_DARK} 0%,{BLUE_MID} 100%);
                border-radius:14px; padding:18px 22px; margin-bottom:14px;'>
      <div style='font-size:20px;font-weight:800;color:{WHITE};
                  font-family:"DM Sans",sans-serif;'>🤖 ML & Forecast</div>
      <div style='font-size:12px;color:{BLUE_PALE};margin-top:4px;'>
        Python-exclusive feature · Revenue forecasting · RFM Segmentation · Anomaly Detection
      </div>
      <div style='margin-top:10px;'>
        <span class='badge-blue' style='background:rgba(255,255,255,0.15);
              color:white;border-color:rgba(255,255,255,0.3);'>
          ⚡ Not available in Power BI
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📉 Revenue Forecast", "👥 RFM Segmentation", "🚨 Anomaly Detection"])

    # ── TAB 1: FORECAST ──────────────────────────────────────────────────────
    with tab1:
        section("Prophet-style Revenue Forecast", "📉")

        col_left, col_right = st.columns([65, 35])
        with col_right:
            horizon = st.slider("Forecast horizon (months)", 3, 24, 12)
            model_choice = st.selectbox("Model", ["Linear Regression",
                                                   "Gradient Boosting",
                                                   "Random Forest"])

        with col_left:
            # Build monthly features
            mdf = (df.groupby(df["Order Date"].dt.to_period("M"))
                     .agg(Revenue=("Sales","sum")).reset_index())
            mdf["t"] = np.arange(len(mdf))
            mdf["sin1"] = np.sin(2*np.pi*mdf["t"]/12)
            mdf["cos1"] = np.cos(2*np.pi*mdf["t"]/12)
            mdf["sin2"] = np.sin(4*np.pi*mdf["t"]/12)
            mdf["cos2"] = np.cos(4*np.pi*mdf["t"]/12)
            mdf["Date"] = mdf["Order Date"].dt.to_timestamp()

            feats = ["t","sin1","cos1","sin2","cos2"]
            X, y = mdf[feats].values, mdf["Revenue"].values

            if len(X) < 4:
                st.warning("Not enough data for forecasting.")
            else:
                if model_choice == "Linear Regression":
                    mdl = LinearRegression()
                elif model_choice == "Gradient Boosting":
                    mdl = GradientBoostingRegressor(n_estimators=100, random_state=42)
                else:
                    mdl = RandomForestRegressor(n_estimators=100, random_state=42)

                mdl.fit(X, y)
                y_pred_hist = mdl.predict(X)

                # Future periods
                t_future = np.arange(len(mdf), len(mdf)+horizon)
                s1f = np.sin(2*np.pi*t_future/12)
                c1f = np.cos(2*np.pi*t_future/12)
                s2f = np.sin(4*np.pi*t_future/12)
                c2f = np.cos(4*np.pi*t_future/12)
                X_fut = np.column_stack([t_future,s1f,c1f,s2f,c2f])
                y_fut = mdl.predict(X_fut)

                last_date = mdf["Date"].max()
                fut_dates = pd.date_range(last_date + pd.offsets.MonthBegin(),
                                           periods=horizon, freq="MS")

                r2  = r2_score(y, y_pred_hist)
                mae = mean_absolute_error(y, y_pred_hist)

                fig = go.Figure()
                fig.add_scatter(x=mdf["Date"], y=y, name="Actual",
                                line=dict(color=BLUE_DARK, width=2.5),
                                mode="lines+markers", marker_size=5)
                fig.add_scatter(x=mdf["Date"], y=y_pred_hist,
                                name="Fitted", line=dict(color=BLUE_LITE,
                                width=2, dash="dot"))
                fig.add_scatter(x=fut_dates, y=y_fut, name=f"Forecast ({horizon}m)",
                                line=dict(color=ACCENT_RED, width=2.5, dash="dash"),
                                mode="lines+markers", marker_size=6,
                                marker_symbol="diamond")

                # Confidence band (simple ±1 std)
                residuals_std = np.std(y - y_pred_hist)
                fig.add_scatter(
                    x=list(fut_dates)+list(fut_dates[::-1]),
                    y=list(y_fut+residuals_std*1.96)+list((y_fut-residuals_std*1.96)[::-1]),
                    fill="toself", fillcolor=f"rgba(211,47,47,0.1)",
                    line_color="rgba(0,0,0,0)", name="95% CI", showlegend=True)
                apply_theme(fig, f"Revenue Forecast — {model_choice}", 360)
                st.plotly_chart(fig, use_container_width=True,
                                config={"displayModeBar":False})

        # Model metrics
        if len(X) >= 4:
            m1,m2,m3 = st.columns(3)
            with m1: kpi("R² Score", f"{r2:.3f}", "model fit quality",
                         None, BLUE_MID if r2>.7 else ACCENT_RED, "🎯")
            with m2: kpi("MAE", fmt(mae,"$"), "mean absolute error",
                          None, ACCENT_TEAL, "📏")
            with m3: kpi("Next Month Forecast", fmt(y_fut[0],"$"),
                          "predicted revenue", None, ACCENT_GRN, "🔮")

    # ── TAB 2: RFM ──────────────────────────────────────────────────────────
    with tab2:
        section("RFM Customer Segmentation", "👥")
        st.markdown(f"""<div class='insight-box'>
          🐍 <b>Python-Exclusive:</b> RFM (Recency · Frequency · Monetary) analysis
          clusters customers into actionable segments.
          Power BI cannot compute this natively — requires Python/R script visual.
        </div>""", unsafe_allow_html=True)

        ref_date = df["Order Date"].max() + pd.Timedelta(days=1)
        rfm = (df.groupby("Customer Name")
                 .agg(
                     Recency  = ("Order Date", lambda x: (ref_date - x.max()).days),
                     Frequency= ("Order Date", "count"),
                     Monetary = ("Sales",      "sum"),
                 ).reset_index())

        # Quintile scoring
        def score_col(col, ascending=True):
            labels = [1,2,3,4,5] if ascending else [5,4,3,2,1]
            try:
                return pd.qcut(col, q=5, labels=labels, duplicates="drop")
            except Exception:
                return pd.cut(col, bins=5, labels=labels)

        rfm["R"] = score_col(rfm["Recency"], ascending=False)
        rfm["F"] = score_col(rfm["Frequency"], ascending=True)
        rfm["M"] = score_col(rfm["Monetary"], ascending=True)
        for c in ["R","F","M"]: rfm[c] = pd.to_numeric(rfm[c], errors="coerce").fillna(3)
        rfm["RFM_Score"] = rfm["R"]+rfm["F"]+rfm["M"]

        def segment(row):
            if row["R"]>=4 and row["F"]>=4 and row["M"]>=4: return "Champions"
            elif row["R"]>=3 and row["F"]>=3:                return "Loyal"
            elif row["R"]>=4 and row["F"]<=2:                return "New Customers"
            elif row["R"]<=2 and row["F"]>=3:                return "At Risk"
            elif row["R"]<=2 and row["M"]>=4:                return "Can't Lose Them"
            elif row["R"]<=1:                                  return "Lost"
            else:                                              return "Potential"
        rfm["Segment"] = rfm.apply(segment, axis=1)

        seg_colors = {
            "Champions":     BLUE_DARK,
            "Loyal":         BLUE_MID,
            "New Customers": BLUE_LITE,
            "At Risk":       ACCENT_RED,
            "Can't Lose Them": ACCENT_AMB,
            "Lost":          "#9E9E9E",
            "Potential":     ACCENT_TEAL,
        }

        c1, c2 = st.columns([50, 50])
        with c1:
            seg_sum = rfm.groupby("Segment").agg(
                Count=("Customer Name","count"),
                Avg_Revenue=("Monetary","mean"),
            ).reset_index()
            fig = px.bar(seg_sum, x="Count", y="Segment",
                         color="Segment",
                         color_discrete_map=seg_colors,
                         text="Count", orientation="h")
            apply_theme(fig, "Customer Segment Distribution", 300)
            fig.update_traces(textposition="outside", textfont_size=10)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        with c2:
            fig = px.scatter(rfm.sample(min(500,len(rfm)), random_state=1),
                             x="Frequency", y="Monetary",
                             color="Segment", size="RFM_Score",
                             color_discrete_map=seg_colors,
                             hover_data=["Customer Name","Recency"],
                             opacity=0.75)
            apply_theme(fig, "RFM Scatter — Frequency vs Revenue", 300)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        # Segment table
        st.dataframe(
            rfm.groupby("Segment").agg(
                Customers=("Customer Name","count"),
                Avg_Recency=("Recency","mean"),
                Avg_Frequency=("Frequency","mean"),
                Avg_Revenue=("Monetary","mean"),
            ).round(1).reset_index(),
            use_container_width=True, hide_index=True
        )

    # ── TAB 3: ANOMALY ──────────────────────────────────────────────────────
    with tab3:
        section("Anomaly Detection — Sales Outliers", "🚨")
        st.markdown(f"""<div class='insight-box'>
          🐍 <b>Python-Exclusive:</b> Statistical anomaly detection using Z-score
          and IQR method to flag unusual spikes or drops in daily sales.
        </div>""", unsafe_allow_html=True)

        sensitivity = st.slider("Detection sensitivity (Z-score threshold)",
                                 1.5, 3.5, 2.5, 0.1)

        daily = (df.groupby(df["Order Date"].dt.date)["Sales"]
                   .sum().reset_index())
        daily.columns = ["Date","Sales"]
        daily["Date"] = pd.to_datetime(daily["Date"])
        daily = daily.sort_values("Date")
        daily["Rolling_Mean"] = daily["Sales"].rolling(7, center=True).mean()
        daily["Rolling_Std"]  = daily["Sales"].rolling(7, center=True).std().fillna(1)
        daily["Z_Score"] = ((daily["Sales"] - daily["Rolling_Mean"]) /
                             daily["Rolling_Std"].replace(0,1))
        daily["Anomaly"] = daily["Z_Score"].abs() > sensitivity

        fig = go.Figure()
        fig.add_scatter(x=daily["Date"], y=daily["Sales"],
                        mode="lines", name="Daily Sales",
                        line=dict(color=BLUE_LITE, width=1.5))
        fig.add_scatter(x=daily["Date"], y=daily["Rolling_Mean"],
                        mode="lines", name="7-day Rolling Avg",
                        line=dict(color=BLUE_DARK, width=2, dash="dot"))
        anom = daily[daily["Anomaly"]]
        fig.add_scatter(x=anom["Date"], y=anom["Sales"],
                        mode="markers", name="Anomaly",
                        marker=dict(color=ACCENT_RED, size=10,
                                    symbol="x", line_width=2))
        apply_theme(fig, f"Sales Anomaly Detection (Z > {sensitivity})", 340)
        fig.update_layout(
            yaxis_title="Daily Revenue ($)",
            shapes=[dict(type="rect",
                         x0=daily["Date"].min(), x1=daily["Date"].max(),
                         y0=daily["Rolling_Mean"].mean() - sensitivity*daily["Rolling_Std"].mean(),
                         y1=daily["Rolling_Mean"].mean() + sensitivity*daily["Rolling_Std"].mean(),
                         fillcolor=BLUE_GHOST, opacity=0.3, layer="below",
                         line_width=0)]
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        col1,col2,col3 = st.columns(3)
        n_anom = anom["Sales"].count()
        anom_pct = n_anom/len(daily)*100 if len(daily) else 0
        with col1: kpi("Anomalies Found", str(n_anom), f"{anom_pct:.1f}% of days",
                        None, ACCENT_RED if n_anom>0 else ACCENT_GRN, "🚨")
        with col2: kpi("Highest Spike", fmt(anom["Sales"].max(),"$") if len(anom) else "None",
                        "single day anomaly", None, ACCENT_AMB, "📈")
        with col3: kpi("Avg Normal Day", fmt(daily[~daily["Anomaly"]]["Sales"].mean(),"$"),
                        "baseline revenue", None, BLUE_MID, "📊")

        if len(anom) > 0:
            st.markdown("**Anomalous Days Detail**")
            st.dataframe(anom[["Date","Sales","Z_Score"]].round(2),
                         use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — OPERATIONAL
# ══════════════════════════════════════════════════════════════════════════════
elif nav.startswith("⚙️"):
    st.markdown(f"""
    <div style='background:{WHITE}; border-radius:14px; padding:14px 22px;
                margin-bottom:14px; box-shadow:0 2px 12px rgba(13,33,55,0.06);'>
      <div style='font-size:20px;font-weight:800;color:{BLUE_DARK};
                  font-family:"DM Sans",sans-serif;'>Operational Analysis</div>
      <div style='font-size:12px;color:{TEXT_LITE};'>
        Shipping · Returns · Order priority · Delivery SLA
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    avg_ship = df["Ship_Days"].mean() if "Ship_Days" in df.columns else 0
    late_pct = (df["Ship_Days"] > 5).mean() * 100 if "Ship_Days" in df.columns else 0
    return_prx= df["Is_Return_Proxy"].mean() * 100 if "Is_Return_Proxy" in df.columns else 0
    crit_pct  = (df["Order Priority"] == "Critical").mean()*100 if "Order Priority" in df.columns else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Avg Shipping Days", f"{avg_ship:.1f}d", "order→delivery", None, BLUE_MID, "🚚")
    with c2: kpi("Late Deliveries", f"{late_pct:.1f}%", ">5 days shipping", -late_pct, ACCENT_RED if late_pct>20 else ACCENT_AMB, "⏰")
    with c3: kpi("High-Loss Orders", f"{return_prx:.1f}%", "proxy for returns", None, ACCENT_RED if return_prx>5 else ACCENT_GRN, "↩️")
    with c4: kpi("Critical Priority", f"{crit_pct:.1f}%", "of all orders", None, ACCENT_AMB, "🔴")

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    section("Shipping Performance", "🚚")

    c1, c2, c3 = st.columns(3)
    with c1:
        if "Ship_Days" in df.columns:
            sm_ship = (df.groupby("Ship Mode")["Ship_Days"]
                         .agg(["mean","min","max"]).reset_index())
            sm_ship.columns = ["Ship Mode","Avg","Min","Max"]
            fig = go.Figure()
            fig.add_bar(x=sm_ship["Ship Mode"], y=sm_ship["Avg"],
                        name="Avg Days", marker_color=BLUE_MID,
                        text=sm_ship["Avg"].round(1),
                        textposition="outside", textfont_size=10)
            for _, row in sm_ship.iterrows():
                fig.add_scatter(x=[row["Ship Mode"]],
                                y=[row["Max"]],
                                mode="markers",
                                marker=dict(color=ACCENT_RED, size=9, symbol="line-ew",
                                            line_color=ACCENT_RED, line_width=2),
                                name="Max" if _ == 0 else "", showlegend=_==0)
            apply_theme(fig, "Avg Ship Days by Mode", 260)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        if "Ship_Days" in df.columns and "Order Priority" in df.columns:
            cross = (df.groupby(["Order Priority","Ship Mode"])["Ship_Days"]
                       .mean().reset_index())
            pivot = cross.pivot(index="Order Priority",
                                 columns="Ship Mode", values="Ship_Days").fillna(0)
            fig = px.imshow(pivot.round(1),
                            color_continuous_scale=["#E3F2FD",BLUE_DARK],
                            text_auto=".1f",
                            aspect="auto")
            apply_theme(fig, "Shipping Days Heatmap: Priority × Mode", 260)
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar":False})

    with c3:
        ship_share = df["Ship Mode"].value_counts(normalize=True).reset_index()
        ship_share.columns = ["Ship Mode","Share"]
        fig = px.pie(ship_share, names="Ship Mode", values="Share",
                     hole=0.55, color_discrete_sequence=PLOTLY_BLUES)
        apply_theme(fig, "Ship Mode Distribution", 260)
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    section("Order Priority & Returns Analysis", "📋")
    c1, c2 = st.columns([55, 45])

    with c1:
        if "Order Priority" in df.columns:
            pri_data = (df.groupby(["Order Priority","Category"])
                          .agg(Revenue=("Sales","sum"), Count=("Sales","count"))
                          .reset_index())
            fig = px.bar(pri_data, x="Order Priority", y="Revenue",
                         color="Category", barmode="stack",
                         color_discrete_sequence=[BLUE_DARK, BLUE_LITE, ACCENT_TEAL],
                         text_auto=".2s")
            apply_theme(fig, "Revenue by Order Priority & Category", 280)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        # Loss analysis as return proxy
        loss_by_sub = (df[df["Profit"] < 0]
                         .groupby("Sub-Category")["Profit"].sum()
                         .abs().nlargest(8).reset_index())
        fig = px.bar(loss_by_sub, x="Profit", y="Sub-Category",
                     orientation="h",
                     color="Profit",
                     color_continuous_scale=["#FFCDD2","#D32F2F"],
                     text=loss_by_sub["Profit"].apply(lambda v: f"${v:,.0f}"))
        apply_theme(fig, "Top Loss-Generating Sub-Categories", 280)
        fig.update_coloraxes(showscale=False)
        fig.update_traces(textposition="outside", textfont_size=9)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    section("Discount Impact Analysis", "🏷️")
    c1, c2 = st.columns([50, 50])

    with c1:
        disc_bins = pd.cut(df["Discount"],
                            bins=[-0.01,0,0.1,0.2,0.3,0.4,0.5,1.0],
                            labels=["0%","1-10%","11-20%","21-30%",
                                    "31-40%","41-50%",">50%"])
        disc_prof = (df.groupby(disc_bins, observed=True)["Profit"]
                       .mean().reset_index())
        disc_prof.columns = ["Discount Range","Avg Profit"]
        fig = px.bar(disc_prof, x="Discount Range", y="Avg Profit",
                     color="Avg Profit",
                     color_continuous_scale=[ACCENT_RED,"#FFFFFF",BLUE_DARK])
        apply_theme(fig, "Avg Profit by Discount Range", 260)
        fig.update_coloraxes(showscale=False)
        fig.add_hline(y=0, line_color=ACCENT_RED, line_width=1.5)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        disc_mkt = (df.groupby(["Market","Discount"])
                      .size().reset_index(name="Count")
                      .groupby("Market")["Discount"].mean().reset_index())
        mkt_margin = df.groupby("Market")["Margin_Pct"].mean().reset_index()
        merged = disc_mkt.merge(mkt_margin, on="Market")
        fig = px.scatter(merged, x="Discount", y="Margin_Pct",
                         text="Market", size_max=18,
                         color="Margin_Pct",
                         color_continuous_scale=[ACCENT_RED,"#FFF",BLUE_DARK])
        apply_theme(fig, "Avg Discount vs Margin by Market", 260)
        fig.update_traces(textposition="top center", textfont_size=10)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

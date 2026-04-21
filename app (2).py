"""
ASCENT — Advanced Scenarios and Carbon Emissions Navigation Tool India
WRI India | Full-sector GHG emissions questionnaire with IPCC 2019 formulas
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import io

st.set_page_config(
    page_title="ASCENT — WRI India",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── COLOUR TOKENS ────────────────────────────────────────────────────────────
NAVY       = "#1B2A4A"
TEAL       = "#4AADA8"
TEAL_DARK  = "#35837F"
CREAM      = "#F0EAD6"
DARK_TEXT  = "#1A1A2E"
MID_TEXT   = "#374151"
LIGHT_BG   = "#F8FAFC"
CARD_BG    = "#FFFFFF"
BORDER     = "#E2E8F0"
RED        = "#E63946"
ORANGE     = "#F4A261"
GREEN_DK   = "#2D6A4F"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;900&family=Inter:wght@300;400;500;600&display=swap');
html,body{{background:{LIGHT_BG}!important}}
.main{{background:{LIGHT_BG}!important}}
.main .block-container{{background:{LIGHT_BG}!important;padding:0 2rem 2rem 2rem!important;max-width:1400px}}
*,p,span,label,div,h1,h2,h3,h4,li{{font-family:'Inter',sans-serif;color:{DARK_TEXT}}}

/* HERO */
.hero-wrap{{position:relative;border-radius:0 0 20px 20px;overflow:hidden;min-height:160px;
  margin:-1rem -2rem 2rem -2rem;box-shadow:0 4px 24px rgba(27,42,74,.18)}}
.hero-bg{{position:absolute;inset:0;background:linear-gradient(135deg,{NAVY} 0%,#243558 100%);}}
.hero-content{{position:relative;z-index:2;padding:1.8rem 3rem;display:flex;align-items:center;gap:2.5rem}}
.hero-title{{font-family:'Montserrat',sans-serif;font-size:2.2rem;font-weight:900;color:#FFF;margin:0;letter-spacing:.5px}}
.hero-sub{{font-size:.88rem;color:rgba(255,255,255,.75);margin:4px 0 12px;font-weight:300;font-style:italic}}
.hero-badges{{display:flex;gap:7px;flex-wrap:wrap}}
.badge{{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.30);color:#fff!important;
  padding:3px 11px;border-radius:20px;font-size:.72rem;font-weight:600;backdrop-filter:blur(4px)}}

/* SIDEBAR */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"]>div,
section[data-testid="stSidebar"]>div>div,
section[data-testid="stSidebar"]>div>div>div{{background:#FFFFFF!important;border-right:1px solid #E5E7EB!important}}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{{color:#111111!important}}
section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="input"] input,
section[data-testid="stSidebar"] [data-baseweb="base-input"] input{{
  background:#FFFFFF!important;border:1px solid #9CA3AF!important;
  color:#000000!important;-webkit-text-fill-color:#000000!important;border-radius:6px!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{
  background:#FFFFFF!important;border:1px solid #9CA3AF!important;color:#111111!important}}
section[data-testid="stSidebar"] .stMarkdown h3{{
  color:{TEAL}!important;font-family:'Montserrat',sans-serif!important;
  font-size:.9rem!important;font-weight:700!important;text-transform:uppercase;
  letter-spacing:.08em;margin:.8rem 0 .4rem 0}}
section[data-testid="stSidebar"] .streamlit-expanderHeader{{
  background:#F3F4F6!important;border:1px solid #D1D5DB!important;border-radius:8px!important}}
section[data-testid="stSidebar"] .streamlit-expanderHeader p{{color:#111111!important;font-weight:600}}

/* FORMULA PILL */
.formula-pill{{background:#EEF2FF;border:1px solid #C7D2FE;border-radius:8px;
  padding:8px 12px;font-size:.78rem;color:#312E81!important;margin:4px 0 8px;font-family:monospace}}
.unit-pill{{display:inline-block;background:{TEAL};color:#fff!important;border-radius:12px;
  padding:1px 8px;font-size:.7rem;font-weight:600;margin-left:4px}}

/* TABS */
.stTabs [data-baseweb="tab-list"]{{background:#FFFFFF;border:1px solid {BORDER};border-radius:10px;padding:4px;gap:3px}}
.stTabs [data-baseweb="tab"]{{color:{MID_TEXT}!important;font-family:'Inter',sans-serif;font-weight:600;
  font-size:.85rem;border-radius:7px;padding:8px 16px;border:none!important}}
.stTabs [aria-selected="true"]{{background:{NAVY}!important;color:#FFFFFF!important}}

/* KPI METRICS */
div[data-testid="stMetric"]{{background:{CARD_BG}!important;border:1px solid {BORDER}!important;
  border-radius:12px!important;padding:1rem 1.2rem!important;box-shadow:0 2px 8px rgba(27,42,74,.07)!important}}
div[data-testid="stMetric"] label{{color:{MID_TEXT}!important;font-size:.72rem!important;
  text-transform:uppercase;letter-spacing:.08em;font-weight:600!important}}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{{color:{NAVY}!important;
  font-family:'Montserrat',sans-serif!important;font-weight:700!important;font-size:1.5rem!important}}

.sec-hdr{{font-family:'Montserrat',sans-serif;font-size:1.05rem;font-weight:700;color:{NAVY};
  letter-spacing:.02em;border-left:4px solid {TEAL};padding-left:10px;margin:1.6rem 0 .8rem}}

[data-testid="stPlotlyChart"]{{background:{CARD_BG}!important;border:1px solid {BORDER}!important;
  border-radius:12px!important;padding:.5rem!important;box-shadow:0 2px 10px rgba(27,42,74,.07)!important}}

[data-testid="stDataFrame"]{{border:1px solid {BORDER}!important;border-radius:10px!important;
  overflow:hidden!important;background:{CARD_BG}!important}}
[data-testid="stDataFrame"] th{{background:{NAVY}!important;color:#FFFFFF!important;
  font-weight:600!important;font-size:.8rem!important;text-transform:uppercase}}
[data-testid="stDataFrame"] td{{color:{DARK_TEXT}!important;font-size:.85rem!important}}

.stDownloadButton button,.stButton button{{background:{TEAL}!important;color:#FFFFFF!important;
  font-family:'Montserrat',sans-serif!important;font-weight:700!important;border-radius:8px!important;
  border:none!important;padding:.4rem 1.4rem!important}}
.stDownloadButton button:hover,.stButton button:hover{{background:{TEAL_DARK}!important}}

.stAlert{{border-radius:10px!important;border-left:4px solid {TEAL}!important}}
hr{{border-color:{BORDER}!important}}
.empty-card{{background:{CARD_BG};border:2px dashed {TEAL};border-radius:14px;padding:2.5rem;text-align:center;margin-bottom:1.5rem}}
.empty-card h3{{color:{NAVY};font-family:'Montserrat',sans-serif;font-weight:700}}
.empty-card p{{color:{MID_TEXT};font-size:.9rem}}
.pill{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:.78rem;font-weight:700;margin:2px}}
.hot-dry{{background:#FFF3CD;color:#4A2E00!important;border:1px solid #F5A623}}
.warm-humid{{background:#D1ECF1;color:#0A3C45!important;border:1px solid #4AADA8}}
.composite{{background:#D4EDDA;color:#0B3320!important;border:1px solid #28A745}}
.cold{{background:#CCE5FF;color:#002050!important;border:1px solid #007BFF}}
.temperate{{background:#E2D9F3;color:#2A0F35!important;border:1px solid #9C27B0}}
.footer{{text-align:center;padding:1rem;color:{MID_TEXT}!important;font-size:.75rem;
  border-top:1px solid {BORDER};margin-top:2rem}}
</style>
""", unsafe_allow_html=True)

# ─── STATIC LOOKUP DATA ────────────────────────────────────────────────────────
INDIA_CITIES = [
 {"state":"Andhra Pradesh","district":"Anantapur","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Guntur","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Visakhapatnam","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Tawang","climate":"Cold"},
 {"state":"Assam","district":"Kamrup","climate":"Warm & humid"},
 {"state":"Assam","district":"Dibrugarh","climate":"Warm & humid"},
 {"state":"Bihar","district":"Patna","climate":"Composite"},
 {"state":"Bihar","district":"Gaya","climate":"Composite"},
 {"state":"Chandigarh","district":"Chandigarh","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Raipur","climate":"Composite"},
 {"state":"Delhi","district":"New Delhi","climate":"Composite"},
 {"state":"Goa","district":"North Goa","climate":"Warm & humid"},
 {"state":"Goa","district":"South Goa","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Ahmedabad","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Surat","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Vadodara","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Rajkot","climate":"Composite"},
 {"state":"Gujarat","district":"Gandhinagar","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Kachchh","climate":"Composite"},
 {"state":"Gujarat","district":"Jamnagar","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Mahesana","climate":"Hot and Dry"},
 {"state":"Haryana","district":"Gurgaon","climate":"Composite"},
 {"state":"Haryana","district":"Faridabad","climate":"Composite"},
 {"state":"Haryana","district":"Hisar","climate":"Composite"},
 {"state":"Himachal Pradesh","district":"Shimla","climate":"Cold"},
 {"state":"Himachal Pradesh","district":"Kangra","climate":"Cold"},
 {"state":"Jammu & Kashmir","district":"Jammu","climate":"Composite"},
 {"state":"Jammu & Kashmir","district":"Srinagar","climate":"Cold"},
 {"state":"Jharkhand","district":"Ranchi","climate":"Composite"},
 {"state":"Jharkhand","district":"Dhanbad","climate":"Composite"},
 {"state":"Karnataka","district":"Bangalore Urban","climate":"Composite"},
 {"state":"Karnataka","district":"Mysore","climate":"Composite"},
 {"state":"Karnataka","district":"Bellary","climate":"Hot and Dry"},
 {"state":"Karnataka","district":"Dakshina Kannada","climate":"Warm & humid"},
 {"state":"Kerala","district":"Thiruvananthapuram","climate":"Warm & humid"},
 {"state":"Kerala","district":"Ernakulam","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kozhikode","climate":"Warm & humid"},
 {"state":"Kerala","district":"Wayanad","climate":"Warm & humid"},
 {"state":"Ladakh","district":"Leh","climate":"Cold"},
 {"state":"Ladakh","district":"Kargil","climate":"Cold"},
 {"state":"Madhya Pradesh","district":"Bhopal","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Indore","climate":"Composite"},
 {"state":"Maharashtra","district":"Mumbai City","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Pune","climate":"Composite"},
 {"state":"Maharashtra","district":"Nashik","climate":"Composite"},
 {"state":"Maharashtra","district":"Nagpur","climate":"Composite"},
 {"state":"Maharashtra","district":"Aurangabad","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Solapur","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Thane","climate":"Warm & humid"},
 {"state":"Manipur","district":"Imphal West","climate":"Warm & humid"},
 {"state":"Meghalaya","district":"East Khasi Hills","climate":"Warm & humid"},
 {"state":"Odisha","district":"Khordha","climate":"Warm & humid"},
 {"state":"Odisha","district":"Cuttack","climate":"Warm & humid"},
 {"state":"Puducherry","district":"Puducherry","climate":"Warm & humid"},
 {"state":"Punjab","district":"Ludhiana","climate":"Composite"},
 {"state":"Punjab","district":"Amritsar","climate":"Composite"},
 {"state":"Rajasthan","district":"Jaipur","climate":"Composite"},
 {"state":"Rajasthan","district":"Jodhpur","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Jaisalmer","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Bikaner","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Udaipur","climate":"Hot and Dry"},
 {"state":"Sikkim","district":"East Sikkim","climate":"Cold"},
 {"state":"Sikkim","district":"South Sikkim","climate":"Temperate"},
 {"state":"Tamil Nadu","district":"Chennai","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Coimbatore","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Madurai","climate":"Warm & humid"},
 {"state":"Telangana","district":"Hyderabad","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Rangareddy","climate":"Hot and Dry"},
 {"state":"Tripura","district":"West Tripura","climate":"Warm & humid"},
 {"state":"Uttar Pradesh","district":"Lucknow","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Kanpur Nagar","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Agra","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Varanasi","climate":"Composite"},
 {"state":"Uttarakhand","district":"Dehradun","climate":"Composite"},
 {"state":"Uttarakhand","district":"Nainital","climate":"Cold"},
 {"state":"West Bengal","district":"Kolkata","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Darjeeling","climate":"Cold"},
 {"state":"West Bengal","district":"North 24 Parganas","climate":"Warm & humid"},
 {"state":"Andaman & Nicobar Islands","district":"South Andaman","climate":"Warm & humid"},
]

# ─── EMISSION FACTORS (IPCC 2019 / CEA 2023) ──────────────────────────────────
# Fuel: (CO2 t/TJ, CH4 t/TJ, N2O t/TJ, NCV_TJ_per_tonne, density_t_per_kL)
FUEL_EF = {
    "Electricity":        (0.82,   0.0,     0.0,     None,    None),   # t CO2e/MWh direct
    "Coal":               (94.6,   0.0003,  0.0015,  0.02326, 1.3),
    "Firewood":           (112.0,  0.03,    0.004,   0.01560, 0.65),
    "Kerosene":           (71.9,   0.003,   0.0006,  0.04360, 0.80),
    "LPG":                (63.1,   0.0003,  0.0001,  0.04740, 0.55),
    "PNG":                (56.1,   0.001,   0.0001,  0.04800, None),
    "Petrol":             (69.3,   0.003,   0.0006,  0.04470, 0.742),
    "Diesel":             (74.1,   0.003,   0.0006,  0.04260, 0.840),
    "CNG":                (56.1,   0.001,   0.0001,  0.04740, None),
    "Auto LPG":           (63.1,   0.0003,  0.0001,  0.04740, 0.55),
    "Aviation gasoline":  (70.0,   0.003,   0.0006,  0.04400, 0.72),
    "Jet kerosene":       (71.9,   0.003,   0.0006,  0.04360, 0.80),
    "Natural gas (TJ)":   (56.1,   0.001,   0.0001,  1.0,     None),
    "MSW incineration":   (0.69,   0.000013,0.000032,None,    None),   # t CO2/MWh
}
GWP = {"CO2": 1.0, "CH4": 28.0, "N2O": 265.0}

def fuel_to_co2e(fuel_name: str, quantity: float, unit: str) -> float:
    """Convert fuel quantity to t CO2e using IPCC 2019 Tier 1 factors."""
    if quantity <= 0 or fuel_name not in FUEL_EF:
        return 0.0
    ef = FUEL_EF[fuel_name]
    co2_factor, ch4_factor, n2o_factor, ncv, density = ef

    if fuel_name == "Electricity":
        # quantity in MWh
        return quantity * co2_factor
    if fuel_name == "MSW incineration":
        # quantity in MWh
        return quantity * (co2_factor + ch4_factor * GWP["CH4"] + n2o_factor * GWP["N2O"])

    # Convert to TJ
    if unit == "MWh":
        tj = quantity * 0.0036
    elif unit == "kL":
        if density is None:
            return 0.0
        tj = quantity * density * ncv  # kL → t → TJ
    elif unit == "tonne":
        tj = quantity * ncv
    elif unit == "TJ":
        tj = quantity
    else:
        tj = 0.0

    co2e = tj * (co2_factor + ch4_factor * GWP["CH4"] + n2o_factor * GWP["N2O"])
    return co2e


# ─── SECTOR COLOUR MAP ────────────────────────────────────────────────────────
SECTOR_COLORS = {
    "Buildings – Residential":    "#C0392B",
    "Buildings – Commercial":     "#E74C3C",
    "Buildings – Public & Inst.": "#F1948A",
    "Buildings – Industrial":     "#FADBD8",
    "Electricity Generation":     "#922B21",
    "Transport – Road":           "#E67E22",
    "Transport – Rail":           "#F39C12",
    "Transport – Water/Aviation": "#F9E4B7",
    "Waste – Solid Waste":        "#16A085",
    "Waste – Biological":         "#1ABC9C",
    "Waste – Wastewater":         "#4AADA8",
    "AFOLU":                      "#27AE60",
    "IPPU":                       "#8E44AD",
}
UNIT_COST = {
    "Buildings – Residential":    10.0,
    "Buildings – Commercial":     11.0,
    "Buildings – Public & Inst.":  9.0,
    "Buildings – Industrial":     14.0,
    "Electricity Generation":     8.0,
    "Transport – Road":           18.0,
    "Transport – Rail":           15.0,
    "Transport – Water/Aviation": 12.0,
    "Waste – Solid Waste":         8.0,
    "Waste – Biological":          6.0,
    "Waste – Wastewater":          9.5,
    "AFOLU":                        3.5,
    "IPPU":                        22.0,
}
SECTORS = list(SECTOR_COLORS.keys())
CLIMATE_STYLES = {
    "Hot and Dry":  "hot-dry",
    "Warm & humid": "warm-humid",
    "Composite":    "composite",
    "Cold":         "cold",
    "Temperate":    "temperate",
}

CT = dict(
    template="plotly_white",
    font=dict(family="Inter, sans-serif", size=12, color="#1A1A2E"),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FAFBFC",
    title_font=dict(family="Montserrat, sans-serif", size=14, color="#1B2A4A"),
)
def cax(fig):
    fig.update_xaxes(gridcolor="#E2E8F0", linecolor="#CBD5E1",
                     tickfont_color="#374151", title_font_color="#1B2A4A")
    fig.update_yaxes(gridcolor="#E2E8F0", linecolor="#CBD5E1",
                     tickfont_color="#374151", title_font_color="#1B2A4A")
    fig.update_layout(legend=dict(font=dict(color="#374151", size=11)))
    return fig

# ─── COMPUTATION HELPERS ──────────────────────────────────────────────────────
def project_bau(base, r, n):
    return {s: max(v, 0) * (1 + r) ** n for s, v in base.items()}

def apply_mitigation(bau, strat):
    return {s: bau[s] * (1 - strat.get(s, 0)) for s in bau}

def timeseries(base, r, by, yrs, ep, ha):
    rows = []
    for yr in yrs:
        n = yr - by
        b = project_bau(base, r, n)
        e = apply_mitigation(b, ep)
        h = apply_mitigation(b, ha)
        rows.append({
            "Year": yr,
            "Reference": sum(b.values()),
            "Existing & Planned": sum(e.values()),
            "High Ambition": sum(h.values()),
            **{f"BAU_{s}": v for s, v in b.items()},
            **{f"HA_{s}":  v for s, v in h.items()},
        })
    return pd.DataFrame(rows)

def budget_table(base, ha, r, n):
    bau = project_bau(base, r, n)
    rows = []
    for s, frac in ha.items():
        red = bau[s] * frac
        rows.append({
            "Sector": s,
            "BAU (t CO₂e)": round(bau[s]),
            "Reduction %": f"{frac*100:.0f}%",
            "GHG Reduced (t CO₂e)": round(red),
            "Investment (₹ Crore)": round(red / 1e6 * UNIT_COST.get(s, 10.0), 1)
        })
    df = pd.DataFrame(rows)
    total = pd.DataFrame([{
        "Sector": "TOTAL",
        "BAU (t CO₂e)": round(df["BAU (t CO₂e)"].sum()),
        "Reduction %": "",
        "GHG Reduced (t CO₂e)": round(df["GHG Reduced (t CO₂e)"].sum()),
        "Investment (₹ Crore)": round(df["Investment (₹ Crore)"].sum(), 1)
    }])
    return pd.concat([df, total], ignore_index=True)


# ─── CHARTS ───────────────────────────────────────────────────────────────────
def chart_traj(df, city, tpct, by):
    fig = go.Figure()
    cfgs = {
        "Reference":          ("#DC2626", "solid",    3.0),
        "Existing & Planned": ("#D97706", "dash",     2.2),
        "High Ambition":      ("#059669", "longdash", 2.5),
    }
    for name, (col, dash, w) in cfgs.items():
        fig.add_trace(go.Scatter(
            x=df["Year"], y=(df[name] / 1e6).round(4), name=name,
            mode="lines+markers",
            line=dict(color=col, dash=dash, width=w),
            marker=dict(size=7, color=col, line=dict(width=1.5, color="#fff"))
        ))
    if tpct > 0:
        brow = df[df["Year"] == by]["Reference"].values
        if len(brow):
            tval = brow[0] * (1 - tpct / 100) / 1e6
            fig.add_hline(y=tval, line_dash="dot", line_color="#7C3AED", line_width=2,
                          annotation_text=f" Net-zero target ({tpct:.0f}% reduction)",
                          annotation_font_color="#7C3AED", annotation_font_size=11)
    fig.update_layout(
        title=f"<b>GHG Emission Scenarios — {city}</b>",
        xaxis_title="Year", yaxis_title="GHG Emissions (Mt CO₂e)",
        hovermode="x unified", height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CT
    )
    return cax(fig)

def chart_wedge(df, prefix, label):
    fig = go.Figure()
    for s in SECTORS:
        col = f"{prefix}{s}"
        if col not in df.columns: continue
        rgb = bytes.fromhex(SECTOR_COLORS[s].lstrip("#"))
        fig.add_trace(go.Scatter(
            x=df["Year"], y=(df[col].clip(lower=0) / 1e6).round(4),
            name=s, mode="lines", stackgroup="one",
            fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.8)",
            line=dict(color=SECTOR_COLORS[s], width=0.8)
        ))
    fig.update_layout(
        title=dict(text=f"<b>{label}</b>", x=0, xanchor="left"),
        xaxis_title="Year", yaxis_title="Mt CO₂e",
        hovermode="x unified", height=480,
        margin=dict(t=40, b=160, l=60, r=20),
        legend=dict(orientation="h", yanchor="top", y=-0.22,
                    xanchor="center", x=0.5, font_size=10,
                    traceorder="reversed", itemwidth=100),
        **CT
    )
    return cax(fig)

def chart_pie(base):
    pos = {s: v for s, v in base.items() if v > 0}
    if not pos:
        fig = go.Figure()
        fig.update_layout(title="Enter emissions to see profile", **CT)
        return fig
    fig = go.Figure(go.Pie(
        labels=list(pos.keys()),
        values=[round(v / 1e3, 2) for v in pos.values()],
        marker=dict(colors=[SECTOR_COLORS[s] for s in pos],
                    line=dict(color="#FFFFFF", width=2)),
        hole=0.44, textinfo="label+percent",
        textfont=dict(size=11, color="#1A1A2E"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} kt CO₂e<extra></extra>"
    ))
    fig.update_layout(title="<b>Base Year Emission Profile</b>",
                      height=400, **CT)
    return fig

def chart_budget(bdf):
    df = bdf[bdf["Sector"] != "TOTAL"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df["Sector"], y=df["Investment (₹ Crore)"],
        name="Investment (₹ Cr)",
        marker_color=[SECTOR_COLORS.get(s, "#888") for s in df["Sector"]],
        marker_line=dict(width=0), opacity=0.9,
        hovertemplate="<b>%{x}</b><br>₹%{y:,.1f} Crore<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["Sector"], y=df["GHG Reduced (t CO₂e)"] / 1e6,
        name="GHG Reduced (Mt)", mode="lines+markers",
        line=dict(color="#1B2A4A", width=2.5),
        marker=dict(size=9, color="#1B2A4A", line=dict(width=2, color="#fff")),
        hovertemplate="<b>%{x}</b><br>%{y:.4f} Mt CO₂e<extra></extra>"
    ), secondary_y=True)
    fig.update_layout(title="<b>Investment vs GHG Reduction (High Ambition)</b>",
                      height=380, **CT)
    fig.update_yaxes(title_text="Investment (₹ Crore)", secondary_y=False,
                     gridcolor="#E2E8F0", tickfont_color="#374151", title_font_color="#1B2A4A")
    fig.update_yaxes(title_text="GHG Reduced (Mt CO₂e)", secondary_y=True,
                     tickfont_color="#374151", title_font_color="#1B2A4A")
    fig.update_xaxes(tickfont_color="#374151", title_font_color="#1B2A4A")
    fig.update_layout(legend=dict(font=dict(color="#374151")))
    return fig

def chart_sensitivity(base, ha, r, by, ty):
    rates = np.arange(0.005, 0.101, 0.005)
    n = ty - by
    bv, hv = [], []
    for gr in rates:
        b = project_bau(base, gr, n)
        h = apply_mitigation(b, ha)
        bv.append(sum(b.values()) / 1e6)
        hv.append(sum(h.values()) / 1e6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rates, y=[round(v,4) for v in bv],
        name="Reference (BAU)", mode="lines+markers",
        line=dict(color="#DC2626", width=2.5),
        marker=dict(size=6, color="#DC2626")))
    fig.add_trace(go.Scatter(x=rates, y=[round(v,4) for v in hv],
        name="High Ambition", mode="lines+markers",
        line=dict(color="#059669", dash="dash", width=2.5),
        marker=dict(size=6, color="#059669"),
        fill="tonexty", fillcolor="rgba(5,150,105,0.10)"))
    fig.update_layout(
        title=f"<b>Sensitivity: Growth Rate vs {ty} Emissions</b>",
        xaxis=dict(title="Annual Growth Rate", tickformat=".1%"),
        yaxis_title="Mt CO₂e", hovermode="x unified", height=380, **CT)
    return cax(fig)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — FULL SECTOR QUESTIONNAIRE
# ═══════════════════════════════════════════════════════════════════════════════

def formula_note(text: str):
    st.markdown(f'<div class="formula-pill">{text}</div>', unsafe_allow_html=True)

def unit_label(unit: str) -> str:
    return f' <span class="unit-pill">{unit}</span>'

with st.sidebar:
    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;text-align:center">
      <div style="font-family:'Montserrat',sans-serif;font-size:1.6rem;font-weight:900;
                  color:#1B2A4A;letter-spacing:1px">ASCENT</div>
      <p style="color:#374151;font-size:.73rem;margin:2px 0 6px">
        WRI India GHG Questionnaire
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ── SECTION A: Basic Information ─────────────────────────────────────────
    st.markdown("### A. Basic Information")

    all_states = sorted(set(c["state"] for c in INDIA_CITIES))
    sel_state  = st.selectbox("State / UT", all_states, key="sel_state")
    dist_list  = sorted([c for c in INDIA_CITIES if c["state"] == sel_state],
                        key=lambda x: x["district"])
    dnames     = [c["district"] for c in dist_list]
    sel_district = st.selectbox("District", dnames, key="sel_district")
    sel_info   = next(c for c in dist_list if c["district"] == sel_district)
    auto_climate = sel_info["climate"]
    cstyle     = CLIMATE_STYLES.get(auto_climate, "composite")
    st.markdown(f'<span class="pill {cstyle}">{auto_climate}</span>',
                unsafe_allow_html=True)

    tier_opts = ["City / ULB", "District", "State", "Gram Panchayat"]
    tier      = st.selectbox("Governance Tier", tier_opts, key="tier")
    population = st.number_input("Population", value=500_000, step=10_000, format="%d", key="pop")
    area_sqkm  = st.number_input("Area (sq. km)", value=150, step=10, key="area")
    avg_rain   = st.number_input("Avg. Rainfall (mm/yr)", value=700, step=50, key="rain")
    city_gdp   = st.number_input("GDP (₹ Crore)", value=5_000, step=500, key="gdp")
    st.divider()

    # ── SECTION B: Years & Growth ────────────────────────────────────────────
    st.markdown("### B. Timeline & Growth")
    base_year   = int(st.number_input("Base Year",      value=2025, step=1, key="by"))
    interim1    = int(st.number_input("Interim Year 1", value=2030, step=1, key="i1"))
    interim2    = int(st.number_input("Interim Year 2", value=2040, step=1, key="i2"))
    target_year = int(st.number_input("Target Year",    value=2050, step=1, key="ty"))
    years_list  = sorted(set([base_year, interim1, interim2, target_year] +
                             list(range(base_year, target_year + 1))))
    growth_rate = st.slider("Annual growth rate (%)", 0.5, 10.0, 2.0, 0.1,
                             format="%.1f%%", key="gr") / 100
    st.divider()

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 1: BUILDINGS & ENERGY
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 1. Buildings & Energy")
    formula_note("E = Fuel_TJ × EF_CO₂ + CH₄_TJ × 28 + N₂O_TJ × 265 (t CO₂e)")
    st.caption("EF source: IPCC 2019 Volume 2; Electricity EF: CEA 2023 (0.82 t/MWh)")

    _fuels_std = [
        ("Electricity", "MWh",   "i"),
        ("Firewood",    "tonne", "i"),
        ("Kerosene",    "kL",    "i"),
        ("PNG",         "tonne", "i"),
        ("LPG",         "tonne", "i"),
    ]
    _fuels_ind = _fuels_std + [("Coal", "tonne", "i")]

    def _fuel_inputs(prefix, fuels):
        vals = {}
        for fuel, unit, _ in fuels:
            vals[fuel] = st.number_input(
                f"{fuel} ({unit})",
                value=0.0, step=1.0, format="%.1f",
                key=f"{prefix}_{fuel.replace(' ','_')}"
            )
        return vals

    b_em = {}
    with st.expander("1.1 Residential buildings"):
        r = _fuel_inputs("res", _fuels_std)
        b_em["Buildings – Residential"] = sum(fuel_to_co2e(k, v, u)
            for (k, u, _), v in zip(_fuels_std, r.values()))

    with st.expander("1.2 Commercial buildings"):
        r = _fuel_inputs("com", _fuels_std)
        b_em["Buildings – Commercial"] = sum(fuel_to_co2e(k, v, u)
            for (k, u, _), v in zip(_fuels_std, r.values()))

    with st.expander("1.3 Institutional buildings & utilities"):
        r = _fuel_inputs("ins", _fuels_std)
        b_em["Buildings – Public & Inst."] = sum(fuel_to_co2e(k, v, u)
            for (k, u, _), v in zip(_fuels_std, r.values()))

    with st.expander("1.4 Manufacturing industries & construction"):
        r = _fuel_inputs("ind", _fuels_ind)
        b_em["Buildings – Industrial"] = sum(fuel_to_co2e(k, v, u)
            for (k, u, _), v in zip(_fuels_ind, r.values()))

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 2: ELECTRICITY GENERATION
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 2. Electricity Generation")
    formula_note("CO₂e = Fuel_TJ × EF (Scope 1 for generators)")
    with st.expander("2.1 Renewable mix (MW capacity + MWh gen.)"):
        sol_mw = st.number_input("Solar PV capacity (MW)", 0.0, step=1.0, key="sol_mw")
        sol_mwh= st.number_input("Solar PV generation (MWh)", 0.0, step=100.0, key="sol_mwh")
        wind_mw= st.number_input("Wind capacity (MW)", 0.0, step=1.0, key="wind_mw")
        hyd_mwh= st.number_input("Hydel generation (MWh)", 0.0, step=100.0, key="hyd_mwh")
        bio_mwh= st.number_input("Biomass generation (MWh)", 0.0, step=100.0, key="bio_mwh")
    with st.expander("2.2–2.5 Fossil & waste-to-energy"):
        ng_tj  = st.number_input("Natural gas (TJ)", 0.0, step=1.0, key="ng_tj")
        coal_tj= st.number_input("Coal for power (TJ)", 0.0, step=1.0, key="coal_tj")
        msw_mwh= st.number_input("MSW incineration (MWh)", 0.0, step=100.0, key="msw_pw")
    b_em["Electricity Generation"] = (
        fuel_to_co2e("Natural gas (TJ)", ng_tj, "TJ") +
        fuel_to_co2e("Coal", coal_tj, "TJ") +
        fuel_to_co2e("MSW incineration", msw_mwh, "MWh")
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 3: TRANSPORT
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 3. Transport")
    st.caption("Option 3A (fuel sales) preferred when data available")

    with st.expander("3A Road — fuel sales approach"):
        formula_note("E = Σ Fuel_a × EF_a  (IPCC Eq. 3.2.1)")
        t_pet  = st.number_input("Petrol (kL)", 0.0, step=100.0, key="t_pet")
        t_die  = st.number_input("Diesel (kL)", 0.0, step=100.0, key="t_die")
        t_cng  = st.number_input("CNG (tonne)", 0.0, step=100.0, key="t_cng")
        t_alpg = st.number_input("Auto LPG (tonne)", 0.0, step=10.0, key="t_alpg")
        t_elec = st.number_input("EV charging (MWh)", 0.0, step=100.0, key="t_elec")
    b_em["Transport – Road"] = (
        fuel_to_co2e("Petrol", t_pet, "kL") +
        fuel_to_co2e("Diesel", t_die, "kL") +
        fuel_to_co2e("CNG",    t_cng, "tonne") +
        fuel_to_co2e("Auto LPG", t_alpg, "tonne") +
        fuel_to_co2e("Electricity", t_elec, "MWh")
    )

    with st.expander("3A Metro / local train"):
        formula_note("E = Σ Fuel_j × EF_j  (IPCC Eq. 3.4.1)")
        r_die  = st.number_input("Diesel (kL)", 0.0, step=100.0, key="r_die")
        r_elec = st.number_input("Electricity (MWh)", 0.0, step=100.0, key="r_elec")
    b_em["Transport – Rail"] = (
        fuel_to_co2e("Diesel", r_die, "kL") +
        fuel_to_co2e("Electricity", r_elec, "MWh")
    )

    with st.expander("3A Waterborne & aviation"):
        formula_note("E = Σ Fuel × EF  (IPCC Eq. 3.5.1 / 3.6.1)")
        w_pet  = st.number_input("Waterborne petrol (kL)", 0.0, step=10.0, key="w_pet")
        w_die  = st.number_input("Waterborne diesel (kL)", 0.0, step=10.0, key="w_die")
        av_gas = st.number_input("Aviation gasoline (kL)", 0.0, step=10.0, key="av_gas")
        av_jet = st.number_input("Jet kerosene (kL)", 0.0, step=10.0, key="av_jet")
    b_em["Transport – Water/Aviation"] = (
        fuel_to_co2e("Petrol", w_pet, "kL") +
        fuel_to_co2e("Diesel", w_die, "kL") +
        fuel_to_co2e("Aviation gasoline", av_gas, "kL") +
        fuel_to_co2e("Jet kerosene", av_jet, "kL")
    )

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 4: SOLID WASTE
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 4. Solid Waste")
    formula_note("CH₄ = [ΣCH₄_gen − Recovery] × (1 − OX_T)  [IPCC Eq.3.1]")

    with st.expander("4.1–4.4 Generation & management"):
        sw_total = st.number_input("Total MSW generation (tonnes/day)", 0.0, step=10.0, key="sw_tot")
        st.caption("Composition (tonnes/day)")
        sw_org  = st.number_input("Organic (food + garden)", 0.0, step=1.0, key="sw_org")
        sw_pap  = st.number_input("Paper / cardboard", 0.0, step=1.0, key="sw_pap")
        sw_pla  = st.number_input("Plastics", 0.0, step=1.0, key="sw_pla")
        sw_oth  = st.number_input("Other (metal, glass, textiles…)", 0.0, step=1.0, key="sw_oth")
        st.caption("Management method share (%)")
        sw_lf_m = st.number_input("Landfill managed (MCF=1.0)", 0.0, 100.0, 50.0, 1.0, key="sw_lfm")
        sw_lf_u = st.number_input("Landfill unmanaged (MCF=0.6)", 0.0, 100.0, 20.0, 1.0, key="sw_lfu")
        sw_inc  = st.number_input("Incineration", 0.0, 100.0, 5.0, 1.0, key="sw_inc")
        sw_com  = st.number_input("Composting / Anaerobic digestion", 0.0, 100.0, 10.0, 1.0, key="sw_com")
        sw_rec  = st.number_input("Recycled / other", 0.0, 100.0, 15.0, 1.0, key="sw_rec")

    # Simplified CH4 from SWDS using first-order decay defaults
    DOC_f   = 0.5    # degradable organic carbon fraction of waste
    MCF_m   = 1.0
    MCF_u   = 0.6
    OX      = 0.1    # oxidation factor
    F_CH4   = 0.5    # fraction of CH4 in landfill gas
    sw_annual = sw_total * 365
    lf_m_mass = sw_annual * sw_lf_m / 100
    lf_u_mass = sw_annual * sw_lf_u / 100
    doc_m = lf_m_mass * DOC_f * MCF_m
    doc_u = lf_u_mass * DOC_f * MCF_u
    ch4_lf = (doc_m + doc_u) * F_CH4 * (16/12) * (1 - OX)
    # N2O from incineration (batch, default EF = 60 g N2O/t wet)
    inc_mass = sw_annual * sw_inc / 100
    n2o_inc  = inc_mass * 60e-6 * GWP["N2O"]
    # Biological treatment CH4 (EF = 4 g CH4/kg for compost)
    bio_mass = sw_annual * sw_com / 100
    ch4_bio  = bio_mass * 4e-6 * GWP["CH4"]
    b_em["Waste – Solid Waste"]  = ch4_lf * GWP["CH4"] + n2o_inc
    b_em["Waste – Biological"]   = ch4_bio

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 5: WASTEWATER
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 5. Wastewater")
    formula_note("CH₄ = [Σ(U_i × T_ij × EF_j)](TOW − S) − R  [IPCC Eq.6.1]")
    formula_note("N₂O = N_eff × EF_eff × 44/28  [IPCC Eq.6.7]")

    with st.expander("5.1–5.9 Supply, generation & treatment"):
        ww_lpcd  = st.number_input("Water supply (LPCD)", 100.0, step=5.0, key="ww_lpcd")
        ww_coll  = st.number_input("Collection efficiency (%)", 0.0, 100.0, 60.0, 1.0, key="ww_coll")
        ww_bod   = st.number_input("Per capita BOD (g/person/day)", 34.0, step=1.0, key="ww_bod")
        ww_prot  = st.number_input("Per capita protein (kg/person/yr)", 21.54, step=0.5, key="ww_prot")
        st.caption("Treatment share (%)")
        ww_aerob = st.number_input("Aerobic (ASP / activated sludge)", 0.0, 100.0, 30.0, 1.0, key="ww_aer")
        ww_uasb  = st.number_input("Anaerobic (UASB / lagoon)", 0.0, 100.0, 20.0, 1.0, key="ww_uasb")
        ww_sep   = st.number_input("Septic tanks", 0.0, 100.0, 20.0, 1.0, key="ww_sep")
        ww_open  = st.number_input("Open drain / untreated", 0.0, 100.0, 30.0, 1.0, key="ww_open")

    BOD_total = population * ww_bod / 1000 * 365  # kg BOD/yr
    EF_j = {"aerobic": 0.1, "uasb": 0.3, "septic": 0.5, "open": 0.8}  # kgCH4/kgBOD
    ch4_ww = BOD_total * (
        (ww_aerob/100)*EF_j["aerobic"] +
        (ww_uasb/100)*EF_j["uasb"] +
        (ww_sep/100)*EF_j["septic"] +
        (ww_open/100)*EF_j["open"]
    )
    N_per_capita = ww_prot * 0.16 * 1.1  # kg N/person/yr (FracNPR=0.16, FNON-CON=1.1)
    N_effluent = population * N_per_capita
    n2o_ww = N_effluent * 0.005 * 44/28   # EF_effluent = 0.005 kgN2O-N/kgN
    b_em["Waste – Wastewater"] = ch4_ww * GWP["CH4"] + n2o_ww * GWP["N2O"]

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 6: AFOLU
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 6. AFOLU")
    formula_note("ΔC_AFOLU = ΔC_FL + ΔC_CL + ΔC_GL + ΔC_WL + ΔC_SL + ΔC_OL")
    formula_note("CH₄_enteric = EF_T × N_T / 10⁶  [IPCC Eq.10.19]")

    with st.expander("6.1 Livestock (head)"):
        af_dairy  = st.number_input("Dairy cattle", 0.0, step=100.0, key="af_dc")
        af_nond   = st.number_input("Non-dairy cattle (adult)", 0.0, step=100.0, key="af_ndc")
        af_buf    = st.number_input("Buffalo (dairy)", 0.0, step=100.0, key="af_bufd")
        af_bufnd  = st.number_input("Buffalo (non-dairy adult)", 0.0, step=100.0, key="af_bufnd")
        af_sheep  = st.number_input("Sheep", 0.0, step=100.0, key="af_sheep")
        af_goat   = st.number_input("Goats", 0.0, step=100.0, key="af_goat")
        af_swine  = st.number_input("Swine", 0.0, step=100.0, key="af_swine")
        af_poult  = st.number_input("Poultry", 0.0, step=1000.0, key="af_poult")

    # EF (kgCH4/head/yr) from IPCC 2019 Table 10.10 South Asia
    EF_live = {
        "dairy": 28, "nond": 23, "buf_d": 43, "buf_nd": 33,
        "sheep": 5, "goat": 5, "swine": 1.5, "poultry": 0.0
    }
    ch4_ent = (
        af_dairy*EF_live["dairy"] + af_nond*EF_live["nond"] +
        af_buf*EF_live["buf_d"] + af_bufnd*EF_live["buf_nd"] +
        af_sheep*EF_live["sheep"] + af_goat*EF_live["goat"] +
        af_swine*EF_live["swine"]
    )  # kg CH4/yr

    with st.expander("6.2–6.8 Land use (ha)"):
        af_forest_d = st.number_input("Dense forest (ha)", 0.0, step=10.0, key="af_fd")
        af_forest_m = st.number_input("Moderately dense forest (ha)", 0.0, step=10.0, key="af_fm")
        af_forest_o = st.number_input("Open forest (ha)", 0.0, step=10.0, key="af_fo")
        af_crop     = st.number_input("Cropland (ha)", 0.0, step=10.0, key="af_crop")
        af_grass    = st.number_input("Grassland (ha)", 0.0, step=10.0, key="af_grass")
        af_wet      = st.number_input("Wetlands / rice paddies (ha)", 0.0, step=10.0, key="af_wet")
        af_settle   = st.number_input("Settlements (ha)", 0.0, step=10.0, key="af_settle")

    # Net biomass growth: 6 t d.m./ha/yr default × 0.47 carbon fraction × 44/12
    C_seq_forest = (af_forest_d * 6 + af_forest_m * 4 + af_forest_o * 2) * 0.47 * 44/12  # t CO2
    # Rice CH4: EF 1.3 kg/ha/day × 120 days cropping season
    ch4_rice = af_wet * 1.3 * 120 / 1000  # t CH4
    afolu_net = (ch4_ent / 1000 * GWP["CH4"]) + (ch4_rice * GWP["CH4"]) - C_seq_forest
    b_em["AFOLU"] = afolu_net

    # ════════════════════════════════════════════════════════════════════════
    # SECTOR 7: IPPU
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### 7. IPPU")
    formula_note("Cement: CO₂ = [Σ(M_ci × C_cli) − Im + Ex] × EF_clc")
    formula_note("Steel: CO₂ = BOF×EF_BOF + EAF×EF_EAF + OHF×EF_OHF")

    with st.expander("7.1–7.4 Mineral processes"):
        ip_clink  = st.number_input("Clinker production (tonne)", 0.0, step=1000.0, key="ip_clink")
        ip_cfrac  = st.selectbox("Cement type (clinker fraction)",
                                 ["OPC (0.95)","PPC (0.75)","PSC (0.65)"], key="ip_cfrac")
        ip_lime   = st.number_input("Lime production — high calcium (tonne)", 0.0, step=100.0, key="ip_lime")
        ip_glass  = st.number_input("Glass production (tonne)", 0.0, step=100.0, key="ip_glass")
        ip_cullet = st.number_input("Cullet ratio (fraction)", 0.0, 1.0, 0.2, 0.01, key="ip_cullet")
        ip_ls     = st.number_input("Limestone consumption (tonne)", 0.0, step=100.0, key="ip_ls")
    ip_cfrac_val = float(ip_cfrac.split("(")[1].replace(")",""))
    co2_cement = ip_clink * ip_cfrac_val * 0.507  # default EF 0.507 t CO2/t clinker
    co2_lime   = ip_lime * 0.754  # default EF for high calcium lime
    co2_glass  = ip_glass * 0.2  * (1 - ip_cullet)
    co2_ls     = ip_ls   * 0.44   # CaCO3 → CaO + CO2

    with st.expander("7.5–7.9 Chemical industry"):
        ip_nh3   = st.number_input("Ammonia production (tonne)", 0.0, step=100.0, key="ip_nh3")
        ip_hno3  = st.number_input("Nitric acid production (tonne)", 0.0, step=100.0, key="ip_hno3")
        ip_soda  = st.number_input("Soda ash production (tonne)", 0.0, step=100.0, key="ip_soda")
    co2_nh3   = ip_nh3  * 1.694   # t CO2/t NH3 default Tier 1
    n2o_hno3  = ip_hno3 * 9.0     # kg N2O/t HNO3 (low pressure plants)
    co2_soda  = ip_soda * 0.138

    with st.expander("7.15–7.18 Iron, steel & metals"):
        ip_bof   = st.number_input("BOF steel (tonne)", 0.0, step=1000.0, key="ip_bof")
        ip_eaf   = st.number_input("EAF steel (tonne)", 0.0, step=1000.0, key="ip_eaf")
        ip_al_pb = st.number_input("Primary Al — prebake (tonne)", 0.0, step=100.0, key="ip_alpb")
        ip_al_so = st.number_input("Primary Al — Søderberg (tonne)", 0.0, step=100.0, key="ip_also")
    co2_steel = ip_bof * 0.26 + ip_eaf * 0.14   # t CO2/t steel Tier 1
    co2_al    = ip_al_pb * 1.6 + ip_al_so * 2.2  # t CO2/t Al Tier 1

    with st.expander("7.36–7.42 Fluorinated gases (F-gases)"):
        ip_hfc_bank = st.number_input("HFC bank (tonne, GWP~2000 avg)", 0.0, step=1.0, key="ip_hfc")
        ip_sf6      = st.number_input("SF₆ equipment charge (tonne, GWP=23500)", 0.0, step=0.1, key="ip_sf6")
    co2e_hfc = ip_hfc_bank * 0.05 * 2000   # 5% annual emission rate assumed
    co2e_sf6 = ip_sf6      * 0.02 * 23500  # 2% annual leakage

    b_em["IPPU"] = (
        co2_cement + co2_lime + co2_glass + co2_ls +
        co2_nh3 + n2o_hno3 * GWP["N2O"] / 1000 + co2_soda +
        co2_steel + co2_al +
        co2e_hfc + co2e_sf6
    )
    st.divider()

    # ════════════════════════════════════════════════════════════════════════
    # SCENARIO STRATEGIES
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("### Scenario Strategies")

    with st.expander("Existing & Planned (EP) — moderate"):
        ep_strategies = {}
        for s in SECTORS:
            default_ep = int(8 if "Buildings" in s else
                             10 if "Road" in s else
                             5)
            ep_strategies[s] = st.slider(s, 0, 30, default_ep, 1,
                                          format="%d%%", key=f"ep_{s}") / 100

    with st.expander("High Ambition (HA) — aggressive", expanded=False):
        ha_strategies = {}
        for s in SECTORS:
            default_ha = int(30 if "Buildings" in s else
                             35 if "Road" in s else
                             20 if "Rail" in s else
                             40 if "Waste" in s else
                             15 if "AFOLU" in s else 20)
            ha_strategies[s] = st.slider(s, 0, 75, default_ha, 1,
                                          format="%d%%", key=f"ha_{s}") / 100

    st.divider()
    st.markdown("### Net-Zero Target")
    target_pct = st.slider("% reduction from BAU by target year",
                            0, 100, 60, 5, format="%d%%", key="tpct")


# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════
base_emissions = {s: max(0.0, v) if s != "AFOLU" else v
                  for s, v in b_em.items()}
n_years    = target_year - base_year
df_ts      = timeseries(base_emissions, growth_rate, base_year,
                        years_list, ep_strategies, ha_strategies)
bdf        = budget_table(base_emissions, ha_strategies, growth_rate, n_years)

base_total = sum(base_emissions.values())
bau_end    = df_ts["Reference"].iloc[-1]
ha_end     = df_ts["High Ambition"].iloc[-1]
ha_saving  = bau_end - ha_end
total_inv  = bdf[bdf["Sector"] == "TOTAL"]["Investment (₹ Crore)"].values[0]
per_capita = base_total / population if population > 0 else 0
per_sqkm   = base_total / area_sqkm  if area_sqkm  > 0 else 0
city_label = f"{sel_district}, {sel_state}"


# ─── HERO ─────────────────────────────────────────────────────────────────────
badges = " ".join([
    f'<span class="badge">{city_label}</span>',
    f'<span class="badge">{tier}</span>',
    f'<span class="badge">{auto_climate}</span>',
    f'<span class="badge">Pop: {population:,}</span>',
    f'<span class="badge">{area_sqkm:,} km²</span>',
    f'<span class="badge">{base_year}→{interim1}→{interim2}→{target_year}</span>',
    '<span class="badge">IPCC 2019 · GPC</span>',
])
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div>
      <div class="hero-title">ASCENT</div>
      <p class="hero-sub">Advanced Scenarios and Carbon Emissions Navigation Tool India</p>
      <div class="hero-badges">{badges}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── EMPTY STATE ──────────────────────────────────────────────────────────────
if abs(base_total) < 1:
    st.markdown("""
    <div class="empty-card">
      <h3>Fill in the Questionnaire to Get Started</h3>
      <p>Enter fuel consumption data in the sector questionnaire on the left.<br>
         The tool auto-calculates GHG emissions using IPCC 2019 Tier 1 factors
         and builds scenario trajectories automatically.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── KPI CARDS ────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.metric("Base Emissions", f"{base_total/1e6:.4f} Mt CO₂e")
with c2: st.metric("Per Capita",     f"{per_capita:.2f} t CO₂e/person")
with c3: st.metric("Per Sq.Km",      f"{per_sqkm/1e3:.2f} kt/km²")
with c4:
    delta = f"+{(bau_end/base_total-1)*100:.0f}% vs base" if base_total != 0 else "—"
    st.metric(f"BAU {target_year}", f"{bau_end/1e6:.4f} Mt", delta, delta_color="inverse")
with c5:
    delta2 = f"{(ha_end/bau_end-1)*100:.0f}% vs BAU" if bau_end != 0 else "—"
    st.metric(f"High Ambition {target_year}", f"{ha_end/1e6:.4f} Mt", delta2)
with c6:
    st.metric("HA Total Investment", f"₹{total_inv:,.0f} Cr")
st.divider()


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Scenarios", "Sub-sector Breakdown", "Budget & Cost",
    "Target Setting", "Sensitivity & Export", "Data Upload"
])

# ── Tab 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.plotly_chart(chart_traj(df_ts, city_label, target_pct, base_year),
                    use_container_width=True)
    ca, cb = st.columns(2)
    with ca:
        st.plotly_chart(chart_wedge(df_ts, "BAU_", "Sector Wedge — Reference (BAU)"),
                        use_container_width=True)
    with cb:
        st.plotly_chart(chart_wedge(df_ts, "HA_", "Sector Wedge — High Ambition"),
                        use_container_width=True)
    st.markdown('<p class="sec-hdr">4-Milestone Summary</p>', unsafe_allow_html=True)
    rows4 = []
    for yr in [base_year, interim1, interim2, target_year]:
        row = df_ts[df_ts["Year"] == yr]
        if not row.empty:
            r_ = row["Reference"].values[0]
            h_ = row["High Ambition"].values[0]
            rows4.append({
                "Year": yr,
                "Reference (Mt)":          round(r_ / 1e6, 4),
                "Existing & Planned (Mt)": round(row["Existing & Planned"].values[0] / 1e6, 4),
                "High Ambition (Mt)":      round(h_ / 1e6, 4),
                "HA vs BAU": f"{(h_/r_-1)*100:.1f}%" if r_ != 0 else "—",
            })
    st.dataframe(pd.DataFrame(rows4), use_container_width=True, hide_index=True)


# ── Tab 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    ca, cb = st.columns(2)
    with ca:
        st.plotly_chart(chart_pie(base_emissions), use_container_width=True)
    with cb:
        # Bar by sector group
        grp_map = {
            "Buildings": ["Buildings – Residential","Buildings – Commercial",
                          "Buildings – Public & Inst.","Buildings – Industrial"],
            "Electricity": ["Electricity Generation"],
            "Transport":   ["Transport – Road","Transport – Rail","Transport – Water/Aviation"],
            "Waste":       ["Waste – Solid Waste","Waste – Biological","Waste – Wastewater"],
            "AFOLU":       ["AFOLU"],
            "IPPU":        ["IPPU"],
        }
        grps, vals, cols = [], [], []
        for grp, slist in grp_map.items():
            tot = sum(base_emissions.get(s, 0) for s in slist) / 1e6
            grps.append(grp); vals.append(round(tot, 4))
            cols.append(SECTOR_COLORS.get(slist[0], "#888"))
        fig_bar = go.Figure(go.Bar(x=grps, y=vals, marker_color=cols,
            text=[f"{v:.4f}" for v in vals], textposition="outside",
            marker_line=dict(width=0)))
        fig_bar.update_layout(title="<b>Emissions by Sector Group (Mt CO₂e)</b>",
                              yaxis_title="Mt CO₂e", height=360, **CT)
        st.plotly_chart(cax(fig_bar), use_container_width=True)

    st.markdown('<p class="sec-hdr">Sub-sector Detail — Base Year</p>', unsafe_allow_html=True)
    det = []
    for s, v in base_emissions.items():
        det.append({
            "Sub-sector": s,
            "Emissions (t CO₂e)": round(v),
            "Share (%)": round(v / base_total * 100, 2) if base_total != 0 else 0,
        })
    st.dataframe(pd.DataFrame(det).style.format({
        "Emissions (t CO₂e)": "{:,.0f}", "Share (%)": "{:.2f}%"
    }), use_container_width=True, hide_index=True)

    st.markdown('<p class="sec-hdr">Emission Factor Reference (IPCC 2019)</p>',
                unsafe_allow_html=True)
    ef_rows = [(k,) + v[:3] + (str(v[4]) + " t/kL" if v[4] else "—",)
               for k, v in FUEL_EF.items()]
    st.dataframe(pd.DataFrame(ef_rows,
                 columns=["Fuel","CO₂ (t/TJ)","CH₄ (t/TJ)","N₂O (t/TJ)","Density"]),
                 use_container_width=True, hide_index=True)


# ── Tab 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    ca, cb = st.columns(2)
    with ca:
        st.plotly_chart(chart_budget(bdf), use_container_width=True)
    with cb:
        df_ce = bdf[(bdf["Sector"] != "TOTAL") & (bdf["GHG Reduced (t CO₂e)"] > 0)].copy()
        if not df_ce.empty:
            df_ce["₹/tonne"] = (df_ce["Investment (₹ Crore)"] * 1e7 /
                                 df_ce["GHG Reduced (t CO₂e)"]).round(0)
            df_ce = df_ce.sort_values("₹/tonne")
            fig_ce = go.Figure(go.Bar(
                x=df_ce["Sector"], y=df_ce["₹/tonne"],
                marker_color=[SECTOR_COLORS.get(s, "#888") for s in df_ce["Sector"]],
                text=df_ce["₹/tonne"].apply(lambda x: f"₹{x:,.0f}"),
                textposition="outside", marker_line=dict(width=0), opacity=0.9,
            ))
            fig_ce.update_layout(title="<b>Cost-Effectiveness (₹/tonne CO₂e avoided)</b>",
                                  yaxis_title="₹ per tonne CO₂e", height=360, **CT)
            st.plotly_chart(cax(fig_ce), use_container_width=True)

    st.markdown('<p class="sec-hdr">Investment Breakdown — High Ambition</p>',
                unsafe_allow_html=True)
    st.dataframe(
        bdf.style.apply(
            lambda row: ["background-color:#E6F4EA;font-weight:700;color:#1B4332"
                         if row["Sector"]=="TOTAL" else "" for _ in row], axis=1
        ).format({
            "BAU (t CO₂e)":         "{:,.0f}",
            "GHG Reduced (t CO₂e)": "{:,.0f}",
            "Investment (₹ Crore)": "₹{:,.1f}",
        }),
        use_container_width=True, hide_index=True
    )
    if bau_end != 0:
        st.info(
            f"**Total HA investment: ₹{total_inv:,.0f} Crore** "
            f"to avoid **{ha_saving/1e6:.4f} Mt CO₂e** "
            f"— **{ha_saving/bau_end*100:.1f}% below BAU** by {target_year}."
        )


# ── Tab 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="sec-hdr">Net-Zero Pathway — Milestone Tracking</p>',
                unsafe_allow_html=True)
    if base_total != 0 and n_years > 0:
        tgt_rows = []
        for yr in [interim1, interim2, target_year]:
            row = df_ts[df_ts["Year"] == yr]
            if not row.empty:
                bau_yr = row["Reference"].values[0]
                ha_yr  = row["High Ambition"].values[0]
                pct_req = target_pct * (yr - base_year) / n_years
                tgt_abs = bau_yr * (1 - pct_req / 100)
                ach     = (1 - ha_yr / bau_yr) * 100 if bau_yr != 0 else 0
                tgt_rows.append({
                    "Milestone": yr,
                    "BAU (Mt)":           round(bau_yr / 1e6, 4),
                    "Target (Mt)":        round(tgt_abs / 1e6, 4),
                    "High Ambition (Mt)": round(ha_yr   / 1e6, 4),
                    "Required %":         f"{pct_req:.1f}%",
                    "HA Achieves %":      f"{ach:.1f}%",
                    "Status": "On Track" if ach >= pct_req else "Gap",
                })
        st.dataframe(pd.DataFrame(tgt_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Enter base year emissions and configure years in the sidebar.")

    st.markdown('<p class="sec-hdr">Mitigation Strategy Reference (ASCENT Appendix D)</p>',
                unsafe_allow_html=True)
    strat_df = pd.DataFrame([
        ("Buildings",  "Star-rated appliances, LED, solar rooftops, BLDC fans"),
        ("Electricity","Transition fossil → RE (solar, wind, hydel)"),
        ("Transport",  "Fuel switch; ICE → EV; mode share shift to public transport"),
        ("Solid waste","Composting, anaerobic digestion, recycling, landfill gas capture"),
        ("Wastewater", "Treatment switch (aerobic → UASB); biogas end-use"),
        ("AFOLU",      "Feeding supplements; community biogas; afforestation"),
        ("IPPU",       "Clinker-cement ratio; CCS; electrification; green hydrogen"),
    ], columns=["Sector","Key Strategies"])
    st.dataframe(strat_df, use_container_width=True, hide_index=True)


# ── Tab 5 ─────────────────────────────────────────────────────────────────────
with tab5:
    st.plotly_chart(
        chart_sensitivity(base_emissions, ha_strategies, growth_rate, base_year, target_year),
        use_container_width=True
    )
    st.markdown('<p class="sec-hdr">Year-by-Year Data Export</p>', unsafe_allow_html=True)
    exp = df_ts.copy()
    exp["Reference (Mt)"]          = (exp["Reference"] / 1e6).round(4)
    exp["Existing & Planned (Mt)"] = (exp["Existing & Planned"] / 1e6).round(4)
    exp["High Ambition (Mt)"]      = (exp["High Ambition"] / 1e6).round(4)
    st.dataframe(exp[["Year","Reference (Mt)","Existing & Planned (Mt)","High Ambition (Mt)"]],
                 use_container_width=True, hide_index=True)
    ca, cb = st.columns(2)
    with ca:
        csv1 = exp[["Year","Reference (Mt)","Existing & Planned (Mt)",
                    "High Ambition (Mt)"]].to_csv(index=False).encode("utf-8")
        st.download_button("Download Scenario Data (CSV)", csv1,
                            f"ascent_{sel_district}_scenarios.csv", "text/csv")
    with cb:
        csv2 = bdf.to_csv(index=False).encode("utf-8")
        st.download_button("Download Budget Breakdown (CSV)", csv2,
                            f"ascent_{sel_district}_budget.csv", "text/csv")


# ── Tab 6 ─────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown('<p class="sec-hdr">Upload City GHG Data — Standard Format</p>',
                unsafe_allow_html=True)
    TEMPLATE = {
        "city_name": "Your City", "state": "Gujarat", "district": "Surat",
        "governance_tier": "City / ULB", "climate_zone": "Hot and Dry",
        "population": 500000, "area_sqkm": 150, "avg_rainfall_mm": 700, "gdp_crore": 5000,
        "base_year": 2025, "interim_year_1": 2030, "interim_year_2": 2040, "target_year": 2050,
        "population_growth_rate_pct": 2.0,
        "emissions_tCO2e": {s: 0 for s in SECTORS},
        "ep_strategies_pct": {s: 8 for s in SECTORS},
        "ha_strategies_pct": {s: 25 for s in SECTORS},
    }
    col_tpl, col_ex = st.columns(2)
    with col_tpl:
        st.markdown("**Download template:**")
        st.download_button("Download JSON Template",
                            json.dumps(TEMPLATE, indent=2).encode("utf-8"),
                            "ascent_template.json", "application/json")
    with col_ex:
        st.markdown("**Sector keys in JSON:**")
        st.code("\n".join(SECTORS), language="text")

    st.divider()
    uploaded_file = st.file_uploader("Upload filled JSON", type=["json"])
    if uploaded_file is not None:
        try:
            raw = json.load(uploaded_file)
            em = raw.get("emissions_tCO2e", {})
            total_em = sum(em.values())
            st.success("File loaded successfully!")
            col_a, col_b = st.columns(2)
            with col_a:
                info_df = pd.DataFrame([
                    ("City", raw.get("city_name","—")),
                    ("State", raw.get("state","—")),
                    ("District", raw.get("district","—")),
                    ("Tier", raw.get("governance_tier","—")),
                    ("Climate", raw.get("climate_zone","—")),
                    ("Population", f"{raw.get('population',0):,}"),
                    ("Base Year", str(raw.get("base_year","—"))),
                    ("Target Year", str(raw.get("target_year","—"))),
                ], columns=["Field","Value"])
                st.dataframe(info_df, use_container_width=True, hide_index=True)
            with col_b:
                em_rows = [(k, f"{v:,.0f}",
                            f"{v/total_em*100:.1f}%" if total_em else "—")
                           for k, v in em.items()]
                st.dataframe(pd.DataFrame(em_rows,
                             columns=["Sub-sector","t CO₂e/yr","Share"]),
                             use_container_width=True, hide_index=True)
            if total_em != 0:
                _up_gr  = raw.get("population_growth_rate_pct", 2.0) / 100
                _up_by  = raw.get("base_year", 2025)
                _up_ty  = raw.get("target_year", 2050)
                _up_i1  = raw.get("interim_year_1", _up_by + 5)
                _up_i2  = raw.get("interim_year_2", _up_by + 15)
                _up_yrs = sorted(set([_up_by, _up_i1, _up_i2, _up_ty] +
                                      list(range(_up_by, _up_ty + 1))))
                _up_ep  = {k: v/100 for k, v in raw.get("ep_strategies_pct", {}).items()}
                _up_ha  = {k: v/100 for k, v in raw.get("ha_strategies_pct", {}).items()}
                for s in SECTORS:
                    _up_ep.setdefault(s, 0.08)
                    _up_ha.setdefault(s, 0.25)
                _up_df = timeseries(em, _up_gr, _up_by, _up_yrs, _up_ep, _up_ha)
                st.plotly_chart(
                    chart_traj(_up_df, raw.get("city_name","Uploaded City"), 60, _up_by),
                    use_container_width=True
                )
                csv_up = _up_df[["Year"]].copy()
                csv_up["Reference (Mt)"]          = (_up_df["Reference"]/1e6).round(4)
                csv_up["High Ambition (Mt)"]       = (_up_df["High Ambition"]/1e6).round(4)
                st.download_button("Download Results (CSV)",
                                    csv_up.to_csv(index=False).encode("utf-8"),
                                    f"ascent_{raw.get('city_name','city')}_results.csv", "text/csv")
        except Exception as e:
            st.error(f"Error reading file: {e}")


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="footer">ASCENT &nbsp;·&nbsp; WRI India &nbsp;·&nbsp; {city_label} &nbsp;·&nbsp; '
    f'{auto_climate} &nbsp;·&nbsp; IPCC 2019 Guidelines &amp; GPC Protocol &nbsp;·&nbsp; '
    f'Emission Factors: CEA 2023, IPCC AR6 GWPs</div>',
    unsafe_allow_html=True
)

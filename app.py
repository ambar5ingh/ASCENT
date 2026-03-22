"""
ASCENT — Advanced Scenario Carbon Emissions Navigation Tool
Streamlit Web App | WRI India
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ASCENT — Carbon Emissions Tool",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hero header */
.ascent-hero {
    background: linear-gradient(135deg, #0d3b2e 0%, #145a3c 50%, #1a7a52 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.ascent-hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.ascent-hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.72);
    margin: 0 0 1.2rem 0;
    font-weight: 300;
}
.hero-badges {
    display: flex; gap: 10px; flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    backdrop-filter: blur(4px);
}

/* KPI cards */
.kpi-row { display: flex; gap: 16px; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1;
    background: #fff;
    border: 1px solid #e8f0ec;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.kpi-label {
    font-size: 0.75rem;
    color: #6b7c74;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #0d3b2e;
    line-height: 1;
}
.kpi-delta {
    font-size: 0.8rem;
    margin-top: 4px;
    font-weight: 500;
}
.kpi-delta.good { color: #1a7a52; }
.kpi-delta.warn { color: #c05c1a; }
.kpi-delta.bad  { color: #c0341a; }

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #0d3b2e;
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e0ede6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #f5faf7;
    border-right: 1px solid #dceae3;
}
[data-testid="stSidebar"] .sidebar-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0d3b2e;
    margin-bottom: 0.3rem;
}

/* Streamlit overrides */
div[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid #e8f0ec;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
.stSelectbox label, .stSlider label { font-weight: 500; color: #2d4a3e; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

SECTORS = ["Buildings & Energy", "Transport", "MSW", "Wastewater", "IPPU", "AFOLU"]

SECTOR_COLORS = {
    "Buildings & Energy": "#E63946",
    "Transport":          "#F4A261",
    "MSW":                "#2A9D8F",
    "Wastewater":         "#457B9D",
    "IPPU":               "#8338EC",
    "AFOLU":              "#3A862B"
}

SAMPLE_CITIES = {
    "Surat (City)": {
        "tier": "City", "population": 7_200_000,
        "base_year": 2019, "target_year": 2030,
        "pop_growth_rate": 0.028, "gdp_growth_rate": 0.065,
        "base_emissions": {
            "Buildings & Energy": 4850, "Transport": 2900,
            "MSW": 420, "Wastewater": 180, "IPPU": 310, "AFOLU": 0
        }
    },
    "Nashik (City)": {
        "tier": "City", "population": 1_490_000,
        "base_year": 2019, "target_year": 2030,
        "pop_growth_rate": 0.021, "gdp_growth_rate": 0.055,
        "base_emissions": {
            "Buildings & Energy": 980, "Transport": 560,
            "MSW": 95, "Wastewater": 42, "IPPU": 75, "AFOLU": 0
        }
    },
    "Wayanad District (Kerala)": {
        "tier": "District", "population": 820_000,
        "base_year": 2019, "target_year": 2030,
        "pop_growth_rate": 0.008, "gdp_growth_rate": 0.045,
        "base_emissions": {
            "Buildings & Energy": 320, "Transport": 210,
            "MSW": 38, "Wastewater": 15, "IPPU": 22, "AFOLU": -95
        }
    },
    "✏️ Enter my own data": None
}

UNIT_COST = {
    "Buildings & Energy": 12.5,
    "Transport": 18.0,
    "MSW": 8.0,
    "Wastewater": 9.5,
    "IPPU": 22.0,
    "AFOLU": 3.5
}

DEFAULT_EP = {s: v for s, v in zip(SECTORS, [0.08, 0.10, 0.12, 0.08, 0.06, 0.05])}
DEFAULT_HA = {s: v for s, v in zip(SECTORS, [0.30, 0.35, 0.40, 0.25, 0.20, 0.15])}

# ─────────────────────────────────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def project_bau(base: dict, r: float, n: int) -> dict:
    return {s: e * (1 + r) ** n for s, e in base.items()}

def apply_mitigation(bau: dict, strategies: dict) -> dict:
    return {s: bau[s] * (1 - strategies.get(s, 0)) for s in bau}

def timeseries(base: dict, r: float, by: int, ty: int,
               ep: dict, ha: dict) -> pd.DataFrame:
    rows = []
    for yr in range(by, ty + 1):
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
            **{f"EP_{s}":  v for s, v in e.items()},
            **{f"HA_{s}":  v for s, v in h.items()},
        })
    return pd.DataFrame(rows)

def budget_table(base: dict, ha: dict, r: float, n: int) -> pd.DataFrame:
    bau = project_bau(base, r, n)
    rows = []
    for s, frac in ha.items():
        red = bau[s] * frac
        rows.append({
            "Sector": s,
            "BAU (Gg CO₂e)": round(bau[s], 1),
            "Reduction": f"{frac*100:.0f}%",
            "GHG Reduced (Gg)": round(red, 1),
            "Investment (₹ Crore)": round(red * UNIT_COST[s], 1)
        })
    df = pd.DataFrame(rows)
    total = pd.DataFrame([{
        "Sector": "TOTAL",
        "BAU (Gg CO₂e)": round(df["BAU (Gg CO₂e)"].sum(), 1),
        "Reduction": "",
        "GHG Reduced (Gg)": round(df["GHG Reduced (Gg)"].sum(), 1),
        "Investment (₹ Crore)": round(df["Investment (₹ Crore)"].sum(), 1)
    }])
    return pd.concat([df, total], ignore_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

CHART_THEME = dict(template="plotly_white", font_family="DM Sans",
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

def chart_trajectories(df, city):
    fig = go.Figure()
    specs = {
        "Reference":          ("#C0341A", "solid",    3.0),
        "Existing & Planned": ("#E07B2A", "dash",     2.2),
        "High Ambition":      ("#1a7a52", "longdash", 2.2),
    }
    for name, (color, dash, width) in specs.items():
        fig.add_trace(go.Scatter(
            x=df["Year"], y=df[name].round(1), name=name,
            mode="lines+markers",
            line=dict(color=color, dash=dash, width=width),
            marker=dict(size=5, color=color)
        ))
    fig.update_layout(
        title=f"<b>GHG Emission Scenarios — {city}</b>",
        xaxis_title="Year", yaxis_title="GHG Emissions (Gg CO₂e)",
        hovermode="x unified", height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CHART_THEME
    )
    return fig

def chart_wedge(df, prefix, label, city):
    fig = go.Figure()
    for s in SECTORS:
        col = f"{prefix}{s}"
        if col not in df.columns:
            continue
        fig.add_trace(go.Scatter(
            x=df["Year"], y=df[col].clip(lower=0).round(1),
            name=s, mode="lines", stackgroup="one",
            fillcolor=SECTOR_COLORS[s],
            line=dict(color=SECTOR_COLORS[s], width=0.5)
        ))
    fig.update_layout(
        title=f"<b>Sector Wedge — {label}</b>",
        xaxis_title="Year", yaxis_title="GHG Emissions (Gg CO₂e)",
        hovermode="x unified", height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CHART_THEME
    )
    return fig

def chart_pie(base, city):
    pos = {s: v for s, v in base.items() if v > 0}
    fig = go.Figure(go.Pie(
        labels=list(pos.keys()),
        values=[round(v, 1) for v in pos.values()],
        marker_colors=[SECTOR_COLORS[s] for s in pos],
        hole=0.42, textinfo="label+percent",
        textfont_size=12
    ))
    fig.update_layout(
        title=f"<b>Base Year Emission Profile</b>",
        height=360, **CHART_THEME
    )
    return fig

def chart_budget(bdf):
    df = bdf[bdf["Sector"] != "TOTAL"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df["Sector"], y=df["Investment (₹ Crore)"],
        name="Investment (₹ Cr)",
        marker_color=[SECTOR_COLORS[s] for s in df["Sector"]],
        opacity=0.85
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["Sector"], y=df["GHG Reduced (Gg)"],
        name="GHG Reduced (Gg)", mode="lines+markers",
        line=dict(color="#0d3b2e", width=2.5),
        marker=dict(size=9, color="#0d3b2e")
    ), secondary_y=True)
    fig.update_layout(
        title="<b>Investment vs GHG Reduction (High Ambition)</b>",
        height=380, **CHART_THEME
    )
    fig.update_yaxes(title_text="Investment (₹ Crore)",  secondary_y=False)
    fig.update_yaxes(title_text="GHG Reduced (Gg CO₂e)", secondary_y=True)
    return fig

def chart_cost_effectiveness(bdf):
    df = bdf[bdf["Sector"] != "TOTAL"].copy()
    df["₹ per tonne"] = (
        df["Investment (₹ Crore)"] * 1e7 /
        (df["GHG Reduced (Gg)"] * 1e6)
    ).round(0)
    df = df.sort_values("₹ per tonne")
    fig = go.Figure(go.Bar(
        x=df["Sector"], y=df["₹ per tonne"],
        marker_color=[SECTOR_COLORS[s] for s in df["Sector"]],
        text=df["₹ per tonne"].apply(lambda x: f"₹{x:,.0f}"),
        textposition="outside", opacity=0.85
    ))
    fig.update_layout(
        title="<b>Cost-Effectiveness (₹ per tonne CO₂e avoided)</b>",
        xaxis_title="Sector", yaxis_title="₹ per tonne CO₂e",
        height=360, **CHART_THEME
    )
    return fig

def chart_sensitivity(base, default_ha, by, ty):
    rates = np.arange(0.005, 0.101, 0.005)
    n = ty - by
    bau_vals, ha_vals = [], []
    for gr in rates:
        b = project_bau(base, gr, n)
        h = apply_mitigation(b, default_ha)
        bau_vals.append(sum(b.values()))
        ha_vals.append(sum(h.values()))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rates, y=[round(v,1) for v in bau_vals],
        name="BAU", mode="lines+markers",
        line=dict(color="#C0341A", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=rates, y=[round(v,1) for v in ha_vals],
        name="High Ambition", mode="lines+markers",
        line=dict(color="#1a7a52", dash="dash", width=2.5),
        fill="tonexty", fillcolor="rgba(26,122,82,0.10)"
    ))
    fig.update_layout(
        title=f"<b>Sensitivity to Growth Rate (target year: {ty})</b>",
        xaxis=dict(title="Annual Growth Rate", tickformat=".1%"),
        yaxis_title="GHG Emissions (Gg CO₂e)",
        hovermode="x unified", height=360, **CHART_THEME
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="sidebar-title">🌿 ASCENT</p>', unsafe_allow_html=True)
    st.caption("Advanced Scenario Carbon Emissions Navigation Tool · WRI India")
    st.divider()

    # City / governance tier
    st.markdown("**📍 Geography**")
    city_choice = st.selectbox("Select city or tier", list(SAMPLE_CITIES.keys()), label_visibility="collapsed")

    if city_choice == "✏️ Enter my own data":
        st.markdown("**Enter base year emissions (Gg CO₂e)**")
        custom_emissions = {}
        for s in SECTORS:
            custom_emissions[s] = st.number_input(s, value=100.0 if s != "AFOLU" else 0.0,
                                                   step=10.0, key=f"em_{s}")
        base_year    = st.number_input("Base year",   value=2022, step=1)
        target_year  = st.number_input("Target year", value=2035, step=1)
        growth_rate  = st.slider("Annual growth rate", 0.005, 0.10, 0.025, 0.005,
                                 format="%.1f%%") / 100
        city_label   = "Custom City"
        tier_label   = "Custom"
        population   = st.number_input("Population", value=500_000, step=10_000)
    else:
        cd          = SAMPLE_CITIES[city_choice]
        custom_emissions = cd["base_emissions"]
        base_year   = cd["base_year"]
        target_year = cd["target_year"]
        growth_rate = st.slider("Annual growth rate", 0.005, 0.10,
                                cd["pop_growth_rate"], 0.005, format="%.1f%%") / 100
        city_label  = city_choice
        tier_label  = cd["tier"]
        population  = cd["population"]

    st.divider()
    st.markdown("**🔧 High Ambition Targets**")
    st.caption("% reduction from BAU by target year")
    ha_strategies = {}
    for s in SECTORS:
        ha_strategies[s] = st.slider(
            s, 0, 75, int(DEFAULT_HA[s] * 100), 1, format="%d%%",
            key=f"ha_{s}"
        ) / 100

    st.divider()
    st.markdown("**⚡ Existing & Planned Targets**")
    st.caption("Conservative, policy-driven reductions")
    ep_strategies = {}
    with st.expander("Adjust EP strategies"):
        for s in SECTORS:
            ep_strategies[s] = st.slider(
                s, 0, 40, int(DEFAULT_EP[s] * 100), 1, format="%d%%",
                key=f"ep_{s}"
            ) / 100
    ep_strategies = ep_strategies or DEFAULT_EP

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────────────────────────────────────

n_years = target_year - base_year
df_ts   = timeseries(custom_emissions, growth_rate, base_year, target_year,
                     ep_strategies, ha_strategies)
bdf     = budget_table(custom_emissions, ha_strategies, growth_rate, n_years)

base_total = sum(custom_emissions.values())
bau_end    = df_ts["Reference"].iloc[-1]
ep_end     = df_ts["Existing & Planned"].iloc[-1]
ha_end     = df_ts["High Ambition"].iloc[-1]
ha_saving  = bau_end - ha_end
total_inv  = bdf[bdf["Sector"] == "TOTAL"]["Investment (₹ Crore)"].values[0]

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="ascent-hero">
  <p class="hero-title">ASCENT</p>
  <p class="hero-subtitle">Advanced Scenario Carbon Emissions Navigation Tool &nbsp;·&nbsp; WRI India</p>
  <div class="hero-badges">
    <span class="badge">📍 {city_label}</span>
    <span class="badge">🏛 {tier_label}</span>
    <span class="badge">👥 {population:,} people</span>
    <span class="badge">📅 {base_year} → {target_year}</span>
    <span class="badge">IPCC 2019 Guidelines</span>
    <span class="badge">GPC Protocol</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Base Year Emissions", f"{base_total:,.0f} Gg CO₂e")
with c2:
    delta_bau = f"+{(bau_end/base_total - 1)*100:.0f}% from base"
    st.metric(f"BAU {target_year}", f"{bau_end:,.0f} Gg CO₂e", delta_bau, delta_color="inverse")
with c3:
    delta_ha = f"{(ha_end/bau_end - 1)*100:.0f}% vs BAU"
    st.metric(f"High Ambition {target_year}", f"{ha_end:,.0f} Gg CO₂e", delta_ha)
with c4:
    st.metric("HA Investment Required", f"₹{total_inv:,.0f} Cr")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Scenarios",
    "🏭 Sector Breakdown",
    "💰 Budget & Cost",
    "🔍 Sensitivity",
    "📊 Data Tables"
])

# ── Tab 1: Scenarios ──────────────────────────────────────────────────────────
with tab1:
    st.plotly_chart(chart_trajectories(df_ts, city_label), use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(chart_wedge(df_ts, "BAU_", "Reference (BAU)", city_label),
                        use_container_width=True)
    with col_b:
        st.plotly_chart(chart_wedge(df_ts, "HA_", "High Ambition", city_label),
                        use_container_width=True)

# ── Tab 2: Sector Breakdown ────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.plotly_chart(chart_pie(custom_emissions, city_label), use_container_width=True)
    with col_b:
        st.plotly_chart(chart_wedge(df_ts, "EP_", "Existing & Planned", city_label),
                        use_container_width=True)

    st.markdown('<p class="section-header">Sector Applicability by Governance Tier</p>',
                unsafe_allow_html=True)
    tier_matrix = pd.DataFrame({
        "Tier":               ["State", "District", "City", "Gram Panchayat"],
        "Buildings & Energy": ["✓", "✓", "✓", "✓"],
        "Electricity Gen.":   ["✓", "✗", "✗", "✗"],
        "Transport":          ["✓", "✓", "✓", "✓"],
        "MSW":                ["✓", "✓", "✓", "✓"],
        "Wastewater":         ["✓", "✓", "✓", "✓"],
        "IPPU":               ["✓", "✓", "✗", "✗"],
        "AFOLU":              ["✓", "✓", "✗", "✓"],
    }).set_index("Tier")
    st.dataframe(tier_matrix, use_container_width=True)

# ── Tab 3: Budget & Cost ───────────────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(chart_budget(bdf), use_container_width=True)
    with col_b:
        st.plotly_chart(chart_cost_effectiveness(bdf), use_container_width=True)

    st.markdown('<p class="section-header">Investment Breakdown (High Ambition)</p>',
                unsafe_allow_html=True)

    styled = bdf.style.apply(
        lambda row: ["background-color: #e8f5ee; font-weight: 600" if row["Sector"] == "TOTAL"
                     else "" for _ in row], axis=1
    ).format({
        "BAU (Gg CO₂e)": "{:,.1f}",
        "GHG Reduced (Gg)": "{:,.1f}",
        "Investment (₹ Crore)": "₹{:,.1f}"
    })
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Financing gap summary
    st.info(
        f"💡 Total estimated investment for High Ambition scenario: "
        f"**₹{total_inv:,.0f} Crore** to avoid **{ha_saving:,.0f} Gg CO₂e** "
        f"({ha_saving/bau_end*100:.1f}% below BAU by {target_year})."
    )

# ── Tab 4: Sensitivity ─────────────────────────────────────────────────────────
with tab4:
    st.plotly_chart(chart_sensitivity(custom_emissions, ha_strategies, base_year, target_year),
                    use_container_width=True)
    st.caption(
        "The shaded area shows the mitigation potential — the gap between BAU and High Ambition — "
        "across different growth rate assumptions. A wider band means mitigation strategies have "
        "greater impact at higher growth rates."
    )

    st.markdown('<p class="section-header">IPCC Tier Framework</p>', unsafe_allow_html=True)
    ipcc = pd.DataFrame({
        "IPCC Tier": ["Tier 1", "Tier 2", "Tier 3"],
        "Description": [
            "Default emission factors — least accurate, most accessible",
            "Region/fuel-specific data — more accurate than Tier 1",
            "Site-specific measurements & process-level data — highest accuracy"
        ],
        "Use case": [
            "Gram panchayats, small ULBs with limited data",
            "Cities and districts with sector-level data",
            "States with comprehensive reporting infrastructure"
        ]
    })
    st.dataframe(ipcc, use_container_width=True, hide_index=True)

# ── Tab 5: Data Tables ─────────────────────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-header">Year-by-Year Scenario Emissions</p>',
                unsafe_allow_html=True)

    display_cols = ["Year", "Reference", "Existing & Planned", "High Ambition"]
    st.dataframe(
        df_ts[display_cols].round(1).style.format({
            "Reference": "{:,.1f}",
            "Existing & Planned": "{:,.1f}",
            "High Ambition": "{:,.1f}"
        }),
        use_container_width=True, hide_index=True
    )

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv_ts = df_ts[display_cols].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download scenario data (CSV)", csv_ts,
                           "ascent_scenarios.csv", "text/csv")
    with col_dl2:
        csv_bd = bdf.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download budget breakdown (CSV)", csv_bd,
                           "ascent_budget.csv", "text/csv")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "ASCENT · WRI India · Built on IPCC 2019 Guidelines & GPC Protocol · "
    "Emission factors: IPCC, CO₂ Baseline Database for Indian Power Sector, peer-reviewed literature"
)

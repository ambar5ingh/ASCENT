# ASCENT — Streamlit Web App

Advanced Scenario Carbon Emissions Navigation Tool  
**WRI India** · IPCC 2019 Guidelines · GPC Protocol

---

## Run Locally

```bash
# 1. Clone / download this folder
cd ascent_app

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Deploy for Free — Streamlit Community Cloud

1. Push this folder to a **GitHub repository** (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set `app.py` as the main file
4. Click **Deploy** — your app gets a public URL in ~2 minutes

That's it. No server management, no cost.

---

## Project Structure

```
ascent_app/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml         ← Theme & server settings
└── README.md
```

---

## Features

| Feature | Description |
|---------|-------------|
| 📍 City selector | 3 pre-loaded Indian cities + custom data entry |
| 📈 Scenario modelling | Reference (BAU), Existing & Planned, High Ambition |
| 🔧 Interactive sliders | Tune HA & EP reduction targets per sector live |
| 🏭 Sector wedge charts | Stacked area charts showing sector contributions |
| 💰 Budget estimation | Investment vs GHG reduction, cost-effectiveness |
| 🔍 Sensitivity analysis | How results shift across growth rate assumptions |
| ⬇️ CSV export | Download scenario data and budget tables |

---

## Methodology

- **Projection formula**: `GHG_target = GHG_base × (1 + r)^n`
- **Sectors**: Buildings & Energy, Transport, MSW, Wastewater, IPPU, AFOLU
- **Scenarios**: Reference · Existing & Planned · High Ambition
- **Standards**: IPCC 2019 · GPC Protocol (Fong et al. 2021)

---

## Customising with Real Data

Edit the `SAMPLE_CITIES` dictionary in `app.py` to add your city, or use the  
**"✏️ Enter my own data"** option in the sidebar to input live figures.

Unit costs (₹ Crore per Gg CO₂e) are in the `UNIT_COST` dict — update these  
from Appendix E of the ASCENT Technical Note for the latest figures.

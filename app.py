"""
ASCENT — Advanced Scenario Carbon Emissions Navigation Tool
Streamlit Web App | WRI India
Full upgrade: 699 Indian cities, climate zones, sub-sectors,
4 time points, target-setting, real EFs, specific mitigation actions
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="ASCENT — Carbon Emissions Tool",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.ascent-hero {
    background: linear-gradient(135deg, #0d3b2e 0%, #145a3c 50%, #1a7a52 100%);
    border-radius: 16px; padding: 2.2rem 3rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-title { font-family:'DM Serif Display',serif; font-size:2.4rem; color:#fff; margin:0 0 0.2rem 0; }
.hero-subtitle { font-size:0.95rem; color:rgba(255,255,255,0.72); margin:0 0 1rem 0; font-weight:300; }
.hero-badges { display:flex; gap:8px; flex-wrap:wrap; }
.badge { background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:3px 12px; border-radius:20px; font-size:0.76rem; font-weight:500; }
.section-header { font-family:'DM Serif Display',serif; font-size:1.3rem; color:#0d3b2e; margin:1.5rem 0 0.6rem 0; padding-bottom:6px; border-bottom:2px solid #e0ede6; }
.climate-badge { display:inline-block; padding:4px 14px; border-radius:20px; font-size:0.82rem; font-weight:600; margin-bottom:8px; }
.hot-dry    { background:#fff3cd; color:#856404; }
.warm-humid { background:#d1ecf1; color:#0c5460; }
.composite  { background:#d4edda; color:#155724; }
.cold       { background:#cce5ff; color:#004085; }
.temperate  { background:#e2d9f3; color:#4a235a; }
[data-testid="stSidebar"] { background:#f5faf7; border-right:1px solid #dceae3; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e8f0ec; border-radius:12px; padding:1rem 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 699 INDIAN DISTRICTS WITH CLIMATE ZONES (ASCENT City_master sheet)
# ─────────────────────────────────────────────────────────────────────────────
INDIA_CITIES = [
 {"state":"Andaman & Nicobar Islands","district":"South Andaman","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Anakapalli","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Anantapur","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Annamayya","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Bapatla","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Chittoor","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"East Godavari","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Eluru","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Guntur","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Kadapa","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Kakinada","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Konaseema","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Krishna","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Kurnool","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Manyam","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"NTR","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Nandyal","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Nellore","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Palnadu","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Prakasam","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Sri Satyasai","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Srikakulam","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Tirupati","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Visakhapatnam","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"Vizianagaram","climate":"Warm & humid"},
 {"state":"Andhra Pradesh","district":"West Godavari","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Anjaw","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Changlang","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Dibang Valley","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"East Kameng","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"East Siang","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Karung Kumey","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"Kra Dadi","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"Lohit","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Longding","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Lower Dibang Valley","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Lower Subansari","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Pakke Kesan","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Papum Pare","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Shi Yomi","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"Tawang","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"Tirap","climate":"Warm & humid"},
 {"state":"Arunachal Pradesh","district":"Upper Siang","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"Upper Subansiri","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"West Kameng","climate":"Cold"},
 {"state":"Arunachal Pradesh","district":"West Siang","climate":"Cold"},
 {"state":"Assam","district":"Baksa","climate":"Warm & humid"},
 {"state":"Assam","district":"Barpeta","climate":"Warm & humid"},
 {"state":"Assam","district":"Bongaigaon","climate":"Warm & humid"},
 {"state":"Assam","district":"Cachar","climate":"Warm & humid"},
 {"state":"Assam","district":"Darrang","climate":"Cold"},
 {"state":"Assam","district":"Dhemaji","climate":"Warm & humid"},
 {"state":"Assam","district":"Dhubri","climate":"Warm & humid"},
 {"state":"Assam","district":"Dibrugarh","climate":"Warm & humid"},
 {"state":"Assam","district":"Dima Hasao","climate":"Warm & humid"},
 {"state":"Assam","district":"Goalpara","climate":"Warm & humid"},
 {"state":"Assam","district":"Golaghat","climate":"Warm & humid"},
 {"state":"Assam","district":"Hailakandi","climate":"Warm & humid"},
 {"state":"Assam","district":"Jorhat","climate":"Warm & humid"},
 {"state":"Assam","district":"Kamrup","climate":"Warm & humid"},
 {"state":"Assam","district":"Karbi Anlong","climate":"Warm & humid"},
 {"state":"Assam","district":"Karimganj","climate":"Warm & humid"},
 {"state":"Assam","district":"Kokrajhar","climate":"Warm & humid"},
 {"state":"Assam","district":"Marigaon","climate":"Cold"},
 {"state":"Assam","district":"Nagaon","climate":"Warm & humid"},
 {"state":"Assam","district":"Nalbari","climate":"Warm & humid"},
 {"state":"Assam","district":"North Lakhimpur","climate":"Warm & humid"},
 {"state":"Assam","district":"Sibsagar","climate":"Warm & humid"},
 {"state":"Assam","district":"Sonitpur","climate":"Warm & humid"},
 {"state":"Assam","district":"Tinsukia","climate":"Warm & humid"},
 {"state":"Assam","district":"Udalguri","climate":"Warm & humid"},
 {"state":"Bihar","district":"Araria","climate":"Warm & humid"},
 {"state":"Bihar","district":"Arwal","climate":"Composite"},
 {"state":"Bihar","district":"Aurangabad","climate":"Composite"},
 {"state":"Bihar","district":"Banka","climate":"Composite"},
 {"state":"Bihar","district":"Begusarai","climate":"Composite"},
 {"state":"Bihar","district":"Bhagalpur","climate":"Warm & humid"},
 {"state":"Bihar","district":"Bhojpur","climate":"Composite"},
 {"state":"Bihar","district":"Buxar","climate":"Composite"},
 {"state":"Bihar","district":"Darbhanga","climate":"Warm & humid"},
 {"state":"Bihar","district":"Gaya","climate":"Composite"},
 {"state":"Bihar","district":"Gopalganj","climate":"Composite"},
 {"state":"Bihar","district":"Jahanabad","climate":"Composite"},
 {"state":"Bihar","district":"Jamui","climate":"Composite"},
 {"state":"Bihar","district":"Kaimur(Bhabua)","climate":"Composite"},
 {"state":"Bihar","district":"Katihar","climate":"Warm & humid"},
 {"state":"Bihar","district":"Khagariya","climate":"Composite"},
 {"state":"Bihar","district":"Kishanganj","climate":"Warm & humid"},
 {"state":"Bihar","district":"Lakhisarai","climate":"Composite"},
 {"state":"Bihar","district":"Madhepura","climate":"Warm & humid"},
 {"state":"Bihar","district":"Madhubani","climate":"Warm & humid"},
 {"state":"Bihar","district":"Munger","climate":"Composite"},
 {"state":"Bihar","district":"Muzaffarpur","climate":"Composite"},
 {"state":"Bihar","district":"Nalanda","climate":"Composite"},
 {"state":"Bihar","district":"Nawada","climate":"Composite"},
 {"state":"Bihar","district":"Paschim Champaran","climate":"Composite"},
 {"state":"Bihar","district":"Patna","climate":"Composite"},
 {"state":"Bihar","district":"Purnia","climate":"Composite"},
 {"state":"Bihar","district":"Purvi Champaran","climate":"Warm & humid"},
 {"state":"Bihar","district":"Rohtas","climate":"Composite"},
 {"state":"Bihar","district":"Saharsa","climate":"Warm & humid"},
 {"state":"Bihar","district":"Samastipur","climate":"Composite"},
 {"state":"Bihar","district":"Saran","climate":"Composite"},
 {"state":"Bihar","district":"Sheikhpura","climate":"Composite"},
 {"state":"Bihar","district":"Sheohar","climate":"Warm & humid"},
 {"state":"Bihar","district":"Sitamarhi","climate":"Warm & humid"},
 {"state":"Bihar","district":"Siwan","climate":"Composite"},
 {"state":"Bihar","district":"Supaul","climate":"Warm & humid"},
 {"state":"Bihar","district":"Vaishali","climate":"Composite"},
 {"state":"Chandigarh","district":"Chandigarh","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Balod","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Bilaspur","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Durg","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Raipur","climate":"Composite"},
 {"state":"Chhattisgarh","district":"Rajnandgaon","climate":"Composite"},
 {"state":"Delhi","district":"New Delhi","climate":"Composite"},
 {"state":"Delhi","district":"South Delhi","climate":"Composite"},
 {"state":"Goa","district":"North Goa","climate":"Warm & humid"},
 {"state":"Goa","district":"South Goa","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Ahmedabad","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Amreli","climate":"Composite"},
 {"state":"Gujarat","district":"Anand","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Bharuch","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Bhavnagar","climate":"Composite"},
 {"state":"Gujarat","district":"Gandhinagar","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Jamnagar","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Junagadh","climate":"Warm & humid"},
 {"state":"Gujarat","district":"Kachchh","climate":"Composite"},
 {"state":"Gujarat","district":"Mahesana","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Rajkot","climate":"Composite"},
 {"state":"Gujarat","district":"Surat","climate":"Hot and Dry"},
 {"state":"Gujarat","district":"Vadodara","climate":"Hot and Dry"},
 {"state":"Haryana","district":"Ambala","climate":"Composite"},
 {"state":"Haryana","district":"Faridabad","climate":"Composite"},
 {"state":"Haryana","district":"Gurgaon","climate":"Composite"},
 {"state":"Haryana","district":"Hisar","climate":"Composite"},
 {"state":"Haryana","district":"Karnal","climate":"Composite"},
 {"state":"Haryana","district":"Panipat","climate":"Composite"},
 {"state":"Himachal Pradesh","district":"Shimla","climate":"Cold"},
 {"state":"Himachal Pradesh","district":"Kangra","climate":"Cold"},
 {"state":"Himachal Pradesh","district":"Mandi","climate":"Cold"},
 {"state":"Jammu & Kashmir","district":"Jammu","climate":"Composite"},
 {"state":"Jammu & Kashmir","district":"Srinagar","climate":"Cold"},
 {"state":"Jharkhand","district":"Dhanbad","climate":"Composite"},
 {"state":"Jharkhand","district":"Ranchi","climate":"Composite"},
 {"state":"Jharkhand","district":"Bokaro","climate":"Composite"},
 {"state":"Jharkhand","district":"Jamshedpur","climate":"Composite"},
 {"state":"Karnataka","district":"Bagalkot","climate":"Composite"},
 {"state":"Karnataka","district":"Bangalore Rural","climate":"Composite"},
 {"state":"Karnataka","district":"Bangalore Urban","climate":"Composite"},
 {"state":"Karnataka","district":"Belagavi","climate":"Composite"},
 {"state":"Karnataka","district":"Bellary","climate":"Hot and Dry"},
 {"state":"Karnataka","district":"Bidar","climate":"Composite"},
 {"state":"Karnataka","district":"Chamarajanagar","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Chikkaballapur","climate":"Composite"},
 {"state":"Karnataka","district":"Chikkamagaluru","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Chitradurga","climate":"Composite"},
 {"state":"Karnataka","district":"Dakshina Kannada","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Davanagere","climate":"Composite"},
 {"state":"Karnataka","district":"Dharwad","climate":"Composite"},
 {"state":"Karnataka","district":"Gadag","climate":"Composite"},
 {"state":"Karnataka","district":"Hassan","climate":"Composite"},
 {"state":"Karnataka","district":"Haveri","climate":"Composite"},
 {"state":"Karnataka","district":"Kalaburagi","climate":"Composite"},
 {"state":"Karnataka","district":"Kodagu","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Kolar","climate":"Composite"},
 {"state":"Karnataka","district":"Koppal","climate":"Hot and Dry"},
 {"state":"Karnataka","district":"Mandya","climate":"Composite"},
 {"state":"Karnataka","district":"Mysore","climate":"Composite"},
 {"state":"Karnataka","district":"Raichur","climate":"Hot and Dry"},
 {"state":"Karnataka","district":"Ramanagara","climate":"Composite"},
 {"state":"Karnataka","district":"Shivamogga","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Tumkur","climate":"Composite"},
 {"state":"Karnataka","district":"Udupi","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Uttara Kannada","climate":"Warm & humid"},
 {"state":"Karnataka","district":"Vijayapura","climate":"Composite"},
 {"state":"Karnataka","district":"Yadgir","climate":"Hot and Dry"},
 {"state":"Kerala","district":"Alappuzha","climate":"Warm & humid"},
 {"state":"Kerala","district":"Ernakulam","climate":"Warm & humid"},
 {"state":"Kerala","district":"Idukki","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kannur","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kasaragod","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kollam","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kottayam","climate":"Warm & humid"},
 {"state":"Kerala","district":"Kozhikode","climate":"Warm & humid"},
 {"state":"Kerala","district":"Malappuram","climate":"Warm & humid"},
 {"state":"Kerala","district":"Palakkad","climate":"Warm & humid"},
 {"state":"Kerala","district":"Pathanamthitta","climate":"Warm & humid"},
 {"state":"Kerala","district":"Thiruvananthapuram","climate":"Warm & humid"},
 {"state":"Kerala","district":"Thrissur","climate":"Warm & humid"},
 {"state":"Kerala","district":"Wayanad","climate":"Warm & humid"},
 {"state":"Ladakh","district":"Kargil","climate":"Cold"},
 {"state":"Ladakh","district":"Leh","climate":"Cold"},
 {"state":"Madhya Pradesh","district":"Bhopal","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Gwalior","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Indore","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Jabalpur","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Rewa","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Sagar","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Satna","climate":"Composite"},
 {"state":"Madhya Pradesh","district":"Ujjain","climate":"Composite"},
 {"state":"Maharashtra","district":"Ahmednagar","climate":"Composite"},
 {"state":"Maharashtra","district":"Akola","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Amravati","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Aurangabad","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Beed","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Chandrapur","climate":"Composite"},
 {"state":"Maharashtra","district":"Dhule","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Jalgaon","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Kolhapur","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Latur","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Mumbai City","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Mumbai Suburban","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Nagpur","climate":"Composite"},
 {"state":"Maharashtra","district":"Nanded","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Nashik","climate":"Composite"},
 {"state":"Maharashtra","district":"Pune","climate":"Composite"},
 {"state":"Maharashtra","district":"Raigad","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Ratnagiri","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Sangli","climate":"Composite"},
 {"state":"Maharashtra","district":"Satara","climate":"Composite"},
 {"state":"Maharashtra","district":"Sindhudurg","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Solapur","climate":"Hot and Dry"},
 {"state":"Maharashtra","district":"Thane","climate":"Warm & humid"},
 {"state":"Maharashtra","district":"Wardha","climate":"Composite"},
 {"state":"Maharashtra","district":"Yavatmal","climate":"Hot and Dry"},
 {"state":"Manipur","district":"Bishnupur","climate":"Warm & humid"},
 {"state":"Manipur","district":"Imphal East","climate":"Warm & humid"},
 {"state":"Manipur","district":"Imphal West","climate":"Warm & humid"},
 {"state":"Meghalaya","district":"East Khasi Hills","climate":"Warm & humid"},
 {"state":"Meghalaya","district":"West Garo Hills","climate":"Warm & humid"},
 {"state":"Mizoram","district":"Aizawl","climate":"Warm & humid"},
 {"state":"Nagaland","district":"Dimapur","climate":"Warm & humid"},
 {"state":"Nagaland","district":"Kohima","climate":"Warm & humid"},
 {"state":"Odisha","district":"Angul","climate":"Composite"},
 {"state":"Odisha","district":"Balasore","climate":"Warm & humid"},
 {"state":"Odisha","district":"Cuttack","climate":"Warm & humid"},
 {"state":"Odisha","district":"Ganjam","climate":"Warm & humid"},
 {"state":"Odisha","district":"Khordha","climate":"Warm & humid"},
 {"state":"Odisha","district":"Puri","climate":"Warm & humid"},
 {"state":"Odisha","district":"Sambalpur","climate":"Composite"},
 {"state":"Odisha","district":"Sundargarh","climate":"Composite"},
 {"state":"Puducherry","district":"Puducherry","climate":"Warm & humid"},
 {"state":"Punjab","district":"Amritsar","climate":"Composite"},
 {"state":"Punjab","district":"Bathinda","climate":"Composite"},
 {"state":"Punjab","district":"Jalandhar","climate":"Composite"},
 {"state":"Punjab","district":"Ludhiana","climate":"Composite"},
 {"state":"Punjab","district":"Patiala","climate":"Composite"},
 {"state":"Rajasthan","district":"Ajmer","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Alwar","climate":"Composite"},
 {"state":"Rajasthan","district":"Barmer","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Bharatpur","climate":"Composite"},
 {"state":"Rajasthan","district":"Bikaner","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Jaipur","climate":"Composite"},
 {"state":"Rajasthan","district":"Jaisalmer","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Jodhpur","climate":"Hot and Dry"},
 {"state":"Rajasthan","district":"Kota","climate":"Composite"},
 {"state":"Rajasthan","district":"Udaipur","climate":"Hot and Dry"},
 {"state":"Sikkim","district":"East Sikkim","climate":"Cold"},
 {"state":"Sikkim","district":"North Sikkim","climate":"Cold"},
 {"state":"Sikkim","district":"South Sikkim","climate":"Temperate"},
 {"state":"Sikkim","district":"West Sikkim","climate":"Temperate"},
 {"state":"Tamil Nadu","district":"Chennai","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Coimbatore","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Cuddalore","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Dharmapuri","climate":"Hot and Dry"},
 {"state":"Tamil Nadu","district":"Erode","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Madurai","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Nagapattinam","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Namakkal","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Nilgiris","climate":"Temperate"},
 {"state":"Tamil Nadu","district":"Salem","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Thanjavur","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Tiruchirappalli","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Tirunelveli","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Tiruppur","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Vellore","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Villupuram","climate":"Warm & humid"},
 {"state":"Tamil Nadu","district":"Virudhunagar","climate":"Warm & humid"},
 {"state":"Telangana","district":"Adilabad","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Hyderabad","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Karimnagar","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Khammam","climate":"Composite"},
 {"state":"Telangana","district":"Mahabubnagar","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Medak","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Nalgonda","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Nizamabad","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Rangareddy","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Sangareddy","climate":"Hot and Dry"},
 {"state":"Telangana","district":"Warangal Urban","climate":"Hot and Dry"},
 {"state":"Tripura","district":"North Tripura","climate":"Warm & humid"},
 {"state":"Tripura","district":"South Tripura","climate":"Warm & humid"},
 {"state":"Tripura","district":"West Tripura","climate":"Warm & humid"},
 {"state":"Uttar Pradesh","district":"Agra","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Allahabad","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Bareilly","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Ghaziabad","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Gorakhpur","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Jhansi","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Kanpur Nagar","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Lucknow","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Mathura","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Meerut","climate":"Composite"},
 {"state":"Uttar Pradesh","district":"Varanasi","climate":"Composite"},
 {"state":"Uttarakhand","district":"Almora","climate":"Cold"},
 {"state":"Uttarakhand","district":"Dehradun","climate":"Composite"},
 {"state":"Uttarakhand","district":"Haridwar","climate":"Composite"},
 {"state":"Uttarakhand","district":"Nainital","climate":"Cold"},
 {"state":"West Bengal","district":"Bankura","climate":"Composite"},
 {"state":"West Bengal","district":"Birbhum","climate":"Composite"},
 {"state":"West Bengal","district":"Cooch Behar","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Darjeeling","climate":"Cold"},
 {"state":"West Bengal","district":"Hooghly","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Howrah","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Jalpaiguri","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Kolkata","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Malda","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Murshidabad","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Nadia","climate":"Warm & humid"},
 {"state":"West Bengal","district":"North 24 Parganas","climate":"Warm & humid"},
 {"state":"West Bengal","district":"Purulia","climate":"Composite"},
 {"state":"West Bengal","district":"South 24 Parganas","climate":"Warm & humid"},
]

# ─────────────────────────────────────────────────────────────────────────────
# REAL AHMEDABAD DATA (from ASCENT Excel Dashboard Data sheet)
# ─────────────────────────────────────────────────────────────────────────────
AHMEDABAD_EMISSIONS = {
    "Buildings – Residential":     9_373_165,
    "Buildings – Commercial":      5_823_579,
    "Buildings – Public & Inst.":    474_687,
    "Buildings – Industrial":        126_683,
    "Transport – On Road":         3_856_050,
    "Transport – Railway":           794_522,
    "Transport – Water/Aviation":          0,
    "Waste – Solid Waste":         3_164_359,
    "Waste – Organic Treatment":         698,
    "Waste – Wastewater":            845_573,
    "IPPU":                                0,
    "AFOLU":                               0,
}

# ─────────────────────────────────────────────────────────────────────────────
# EMISSION FACTORS (from ASCENT Emission Factor sheet)
# ─────────────────────────────────────────────────────────────────────────────
EMISSION_FACTORS = {
    "Electricity (t/MWh)":        0.823,
    "LPG (t/TJ)":                 63.1,
    "PNG/City Gas (t/TJ)":        56.1,
    "Kerosene (t/TJ)":            71.9,
    "Firewood (t/TJ)":           112.0,
    "Coal/Charcoal (t/TJ)":      112.0,
    "Diesel Gen-set (t/TJ)":      74.1,
    "Petrol/Gasoline (t/TJ)":     69.3,
    "Diesel (Transport, t/TJ)":   74.1,
    "CNG (Transport, t/TJ)":      56.1,
}

SECTORS_DETAILED = [
    "Buildings – Residential","Buildings – Commercial",
    "Buildings – Public & Inst.","Buildings – Industrial",
    "Transport – On Road","Transport – Railway","Transport – Water/Aviation",
    "Waste – Solid Waste","Waste – Organic Treatment","Waste – Wastewater",
    "IPPU","AFOLU"
]
SECTOR_GROUPS = {
    "Buildings & Energy": ["Buildings – Residential","Buildings – Commercial","Buildings – Public & Inst.","Buildings – Industrial"],
    "Transport":          ["Transport – On Road","Transport – Railway","Transport – Water/Aviation"],
    "Waste":              ["Waste – Solid Waste","Waste – Organic Treatment","Waste – Wastewater"],
    "IPPU":               ["IPPU"],
    "AFOLU":              ["AFOLU"],
}
SECTOR_COLORS = {
    "Buildings – Residential":    "#E63946",
    "Buildings – Commercial":     "#FF6B6B",
    "Buildings – Public & Inst.": "#FF9F9F",
    "Buildings – Industrial":     "#FFC4C4",
    "Transport – On Road":        "#F4A261",
    "Transport – Railway":        "#E76F51",
    "Transport – Water/Aviation": "#FFBA75",
    "Waste – Solid Waste":        "#2A9D8F",
    "Waste – Organic Treatment":  "#52C9BB",
    "Waste – Wastewater":         "#457B9D",
    "IPPU":                       "#8338EC",
    "AFOLU":                      "#3A862B",
}
UNIT_COST = {   # ₹ Crore per Mt CO₂e reduced
    "Buildings – Residential":    10.0,
    "Buildings – Commercial":     11.0,
    "Buildings – Public & Inst.":  9.0,
    "Buildings – Industrial":     14.0,
    "Transport – On Road":        18.0,
    "Transport – Railway":        15.0,
    "Transport – Water/Aviation": 12.0,
    "Waste – Solid Waste":         8.0,
    "Waste – Organic Treatment":   6.0,
    "Waste – Wastewater":          9.5,
    "IPPU":                       22.0,
    "AFOLU":                       3.5,
}
MITIGATION_ACTIONS = {
    "Buildings – Residential":    ["LED Lights","5-star appliances","5-star AC","BLDC fans","Rooftop solar PV","ECBC green building"],
    "Buildings – Commercial":     ["LED Lights (commercial)","3-star appliances","5-star AC (commercial)","BLDC fans","Green building cert."],
    "Buildings – Public & Inst.": ["LED streetlights","Solar on public buildings","Energy audits & retrofits"],
    "Buildings – Industrial":     ["Energy efficiency measures","Captive renewable energy","Waste heat recovery"],
    "Transport – On Road":        ["Electric vehicles (2W/3W)","Electric buses","BRTS/BRT","Non-motorised transport","Fuel efficiency standards","CNG conversion"],
    "Transport – Railway":        ["Rail electrification","Modal shift to rail"],
    "Transport – Water/Aviation": ["LNG/biofuel for vessels","Carbon offset schemes"],
    "Waste – Solid Waste":        ["Biomethanation plant","Waste-to-energy","Landfill gas capture","Segregation & composting"],
    "Waste – Organic Treatment":  ["Anaerobic digestion","Vermicomposting"],
    "Waste – Wastewater":         ["Sludge-to-energy","Methane capture from STPs","Secondary/tertiary treatment"],
    "IPPU":                       ["Process optimisation","Material efficiency","CCS pilot"],
    "AFOLU":                      ["Agroforestry","Afforestation / urban greening","Sustainable agriculture","Reduce deforestation"],
}
CLIMATE_STYLES = {
    "Hot and Dry":  ("hot-dry",   "🔆"),
    "Warm & humid": ("warm-humid","💧"),
    "Composite":    ("composite", "🌤"),
    "Cold":         ("cold",      "❄️"),
    "Temperate":    ("temperate", "🌿"),
}
CHART_THEME = dict(template="plotly_white", font_family="DM Sans",
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

# ─────────────────────────────────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def project_bau(base, r, n):
    return {s: max(e,0)*(1+r)**n for s,e in base.items()}

def apply_mitigation(bau, strategies):
    return {s: bau[s]*(1-strategies.get(s,0)) for s in bau}

def timeseries(base, r, by, years_list, ep, ha):
    rows = []
    for yr in years_list:
        n = yr - by
        b = project_bau(base, r, n)
        e = apply_mitigation(b, ep)
        h = apply_mitigation(b, ha)
        rows.append({
            "Year": yr,
            "Reference": sum(b.values()),
            "Existing & Planned": sum(e.values()),
            "High Ambition": sum(h.values()),
            **{f"BAU_{s}": v for s,v in b.items()},
            **{f"HA_{s}":  v for s,v in h.items()},
        })
    return pd.DataFrame(rows)

def budget_table(base, ha, r, n):
    bau = project_bau(base, r, n)
    rows = []
    for s,frac in ha.items():
        red = bau[s]*frac
        rows.append({
            "Sector": s,
            "BAU (t CO₂e)": round(bau[s]),
            "Reduction": f"{frac*100:.0f}%",
            "GHG Reduced (t CO₂e)": round(red),
            "Investment (₹ Crore)": round(red/1e6*UNIT_COST[s], 1)
        })
    df = pd.DataFrame(rows)
    total = pd.DataFrame([{
        "Sector": "TOTAL",
        "BAU (t CO₂e)": round(df["BAU (t CO₂e)"].sum()),
        "Reduction": "",
        "GHG Reduced (t CO₂e)": round(df["GHG Reduced (t CO₂e)"].sum()),
        "Investment (₹ Crore)": round(df["Investment (₹ Crore)"].sum(), 1)
    }])
    return pd.concat([df, total], ignore_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────
def chart_trajectories(df, city, target_pct, base_year):
    fig = go.Figure()
    specs = {
        "Reference":          ("#C0341A","solid",    3.0),
        "Existing & Planned": ("#E07B2A","dash",     2.2),
        "High Ambition":      ("#1a7a52","longdash", 2.2),
    }
    for name,(color,dash,width) in specs.items():
        fig.add_trace(go.Scatter(
            x=df["Year"], y=(df[name]/1e6).round(3), name=name,
            mode="lines+markers",
            line=dict(color=color,dash=dash,width=width),
            marker=dict(size=7,color=color)
        ))
    if target_pct > 0:
        bau_base = df[df["Year"]==base_year]["Reference"].values
        if len(bau_base):
            tval = bau_base[0]*(1-target_pct/100)/1e6
            fig.add_hline(y=tval, line_dash="dot", line_color="#8338EC",
                          annotation_text=f" Net-zero target ({target_pct:.0f}% reduction)",
                          annotation_font_color="#8338EC")
    fig.update_layout(
        title="<b>GHG Emission Scenarios — All 4 Time Points</b>",
        xaxis_title="Year", yaxis_title="GHG Emissions (Mt CO₂e)",
        hovermode="x unified", height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CHART_THEME)
    return fig

def chart_wedge(df, prefix, label):
    fig = go.Figure()
    for s in SECTORS_DETAILED:
        col = f"{prefix}{s}"
        if col not in df.columns: continue
        fig.add_trace(go.Scatter(
            x=df["Year"], y=(df[col].clip(lower=0)/1e6).round(3),
            name=s, mode="lines", stackgroup="one",
            fillcolor=SECTOR_COLORS[s],
            line=dict(color=SECTOR_COLORS[s], width=0.5)
        ))
    fig.update_layout(
        title=f"<b>Sector Wedge — {label}</b>",
        xaxis_title="Year", yaxis_title="Mt CO₂e",
        hovermode="x unified", height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CHART_THEME)
    return fig

def chart_pie(base):
    pos = {s:v for s,v in base.items() if v>0}
    fig = go.Figure(go.Pie(
        labels=list(pos.keys()),
        values=[round(v/1e3,1) for v in pos.values()],
        marker_colors=[SECTOR_COLORS[s] for s in pos],
        hole=0.42, textinfo="label+percent", textfont_size=11
    ))
    fig.update_layout(title="<b>Base Year Emission Profile (kt CO₂e)</b>",
                      height=400, **CHART_THEME)
    return fig

def chart_subsector_bar(base):
    groups,vals,colors = [],[],[]
    for grp,slist in SECTOR_GROUPS.items():
        total = sum(base.get(s,0) for s in slist)/1e6
        if total > 0:
            groups.append(grp); vals.append(round(total,3))
            colors.append(SECTOR_COLORS[slist[0]])
    fig = go.Figure(go.Bar(x=groups, y=vals, marker_color=colors,
        text=[f"{v:.3f} Mt" for v in vals], textposition="outside"))
    fig.update_layout(title="<b>Emissions by Sector Group (Mt CO₂e)</b>",
                      yaxis_title="Mt CO₂e", height=360, **CHART_THEME)
    return fig

def chart_budget(bdf):
    df = bdf[bdf["Sector"]!="TOTAL"]
    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=df["Sector"], y=df["Investment (₹ Crore)"],
        name="Investment (₹ Cr)",
        marker_color=[SECTOR_COLORS[s] for s in df["Sector"]], opacity=0.85),
        secondary_y=False)
    fig.add_trace(go.Scatter(x=df["Sector"], y=df["GHG Reduced (t CO₂e)"]/1e6,
        name="GHG Reduced (Mt)", mode="lines+markers",
        line=dict(color="#0d3b2e",width=2.5), marker=dict(size=8)),
        secondary_y=True)
    fig.update_layout(title="<b>Investment vs GHG Reduction (High Ambition)</b>",
                      height=380, **CHART_THEME)
    fig.update_yaxes(title_text="Investment (₹ Crore)", secondary_y=False)
    fig.update_yaxes(title_text="GHG Reduced (Mt CO₂e)", secondary_y=True)
    return fig

def chart_cost_eff(bdf):
    df = bdf[(bdf["Sector"]!="TOTAL") & (bdf["GHG Reduced (t CO₂e)"]>0)].copy()
    df["₹ per tonne"] = (df["Investment (₹ Crore)"]*1e7/df["GHG Reduced (t CO₂e)"]).round(0)
    df = df.sort_values("₹ per tonne")
    fig = go.Figure(go.Bar(x=df["Sector"], y=df["₹ per tonne"],
        marker_color=[SECTOR_COLORS[s] for s in df["Sector"]],
        text=df["₹ per tonne"].apply(lambda x:f"₹{x:,.0f}"),
        textposition="outside", opacity=0.85))
    fig.update_layout(title="<b>Cost-Effectiveness (₹ per tonne CO₂e)</b>",
                      height=360, **CHART_THEME)
    return fig

def chart_sensitivity(base, ha, by, ty):
    rates = np.arange(0.005,0.101,0.005)
    n = ty-by
    bau_v,ha_v = [],[]
    for gr in rates:
        b = project_bau(base,gr,n)
        h = apply_mitigation(b,ha)
        bau_v.append(sum(b.values())/1e6)
        ha_v.append(sum(h.values())/1e6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rates, y=[round(v,3) for v in bau_v],
        name="BAU", mode="lines+markers", line=dict(color="#C0341A",width=2.5)))
    fig.add_trace(go.Scatter(x=rates, y=[round(v,3) for v in ha_v],
        name="High Ambition", mode="lines+markers",
        line=dict(color="#1a7a52",dash="dash",width=2.5),
        fill="tonexty", fillcolor="rgba(26,122,82,0.10)"))
    fig.update_layout(
        title=f"<b>Sensitivity to Growth Rate (target year: {ty})</b>",
        xaxis=dict(title="Annual Growth Rate",tickformat=".1%"),
        yaxis_title="Mt CO₂e", hovermode="x unified", height=360, **CHART_THEME)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 ASCENT")
    st.caption("Advanced Scenario Carbon Emissions Navigation Tool · WRI India")
    st.divider()

    # Step 1: State
    st.markdown("**📍 Step 1 — State**")
    all_states = sorted(set(c["state"] for c in INDIA_CITIES))
    sel_state = st.selectbox("State", all_states,
                             index=all_states.index("Gujarat"),
                             label_visibility="collapsed")

    # Step 2: District
    st.markdown("**🏙 Step 2 — District**")
    districts_in_state = sorted([c for c in INDIA_CITIES if c["state"]==sel_state],
                                 key=lambda x: x["district"])
    district_names = [c["district"] for c in districts_in_state]
    default_d = "Ahmedabad" if "Ahmedabad" in district_names else district_names[0]
    sel_district = st.selectbox("District", district_names,
                                index=district_names.index(default_d),
                                label_visibility="collapsed")

    sel_info   = next(c for c in districts_in_state if c["district"]==sel_district)
    auto_climate = sel_info["climate"]
    cstyle, cicon = CLIMATE_STYLES.get(auto_climate, ("composite","🌤"))
    st.markdown(f'<span class="climate-badge {cstyle}">{cicon} {auto_climate} climate zone</span>',
                unsafe_allow_html=True)

    st.divider()

    # Step 3: Geography
    st.markdown("**🗺 Step 3 — Geography & Demographics**")
    tier       = st.selectbox("Governance Tier",["City / ULB","District","State","Gram Panchayat"])
    population = st.number_input("Population", value=1_000_000, step=50_000, format="%d")
    area_sqkm  = st.number_input("Area (sq. km)", value=200, step=10)
    avg_rainfall = st.number_input("Avg. Annual Rainfall (mm/yr)", value=800, step=50)
    city_gdp   = st.number_input("City/District GDP (₹ Crore)", value=10_000, step=500)

    st.divider()

    # Step 4: Years & Growth
    st.markdown("**📅 Step 4 — Years & Growth Rate**")
    base_year   = st.number_input("Base Year",      value=2025, step=1)
    interim1    = st.number_input("Interim Year 1", value=2030, step=1)
    interim2    = st.number_input("Interim Year 2", value=2040, step=1)
    target_year = st.number_input("Target Year",    value=2050, step=1)
    years_list  = sorted(set(
        [base_year, interim1, interim2, target_year] +
        list(range(int(base_year), int(target_year)+1))
    ))

    growth_mode = st.radio("Growth driver",["Population","GDP","Population + GDP"],horizontal=True)
    pop_rate = st.slider("Population growth rate", 0.5, 10.0, 2.0, 0.1, format="%.1f%%") / 100
    gdp_rate = (st.slider("GDP growth rate", 0.5, 12.0, 5.0, 0.1, format="%.1f%%") / 100
                if "GDP" in growth_mode else 0.0)
    growth_rate = (pop_rate if growth_mode=="Population"
                   else gdp_rate if growth_mode=="GDP"
                   else (pop_rate+gdp_rate)/2)

    st.divider()

    # Step 5: Base Year Emissions
    is_ahmedabad = (sel_state=="Gujarat" and sel_district=="Ahmedabad")
    st.markdown("**⚡ Step 5 — Base Year Emissions (t CO₂e)**")
    st.caption("✅ Real Ahmedabad data from ASCENT Excel" if is_ahmedabad
               else "Enter emissions per sub-sector below")

    base_emissions = {}
    with st.expander("📋 Sub-sector emissions", expanded=False):
        for s in SECTORS_DETAILED:
            defval = float(AHMEDABAD_EMISSIONS.get(s,0)) if is_ahmedabad else 0.0
            base_emissions[s] = st.number_input(s, value=defval, step=1000.0,
                                                format="%.0f", key=f"be_{s}")

    if is_ahmedabad and all(v==0 for v in base_emissions.values()):
        base_emissions = dict(AHMEDABAD_EMISSIONS)

    st.divider()

    # Step 6: Mitigation Actions
    st.markdown("**🔧 Step 6 — Mitigation Actions**")
    ha_strategies, ep_strategies = {}, {}
    with st.expander("Configure actions & targets"):
        for s in SECTORS_DETAILED:
            st.markdown(f"**{s}**")
            acts = MITIGATION_ACTIONS.get(s,[])
            if acts:
                st.multiselect("Actions", acts, key=f"act_{s}",
                               label_visibility="collapsed")
            default_ha = (30 if "Buildings" in s else 35 if "On Road" in s
                         else 20 if "Railway" in s else 40 if "Waste" in s
                         else 15 if "AFOLU" in s else 20)
            default_ep = (8 if "Buildings" in s else 10 if "On Road" in s else 5)
            ha_strategies[s] = st.slider(f"HA %", 0,75,default_ha,1,
                                         format="%d%%",key=f"ha_{s}") / 100
            ep_strategies[s] = st.slider(f"EP %", 0,30,default_ep,1,
                                         format="%d%%",key=f"ep_{s}") / 100

    st.divider()

    # Step 7: Target
    st.markdown("**🎯 Step 7 — Net-Zero Target**")
    target_pct = st.slider("Reduction from BAU by target year (%)",
                           0, 100, 60, 5, format="%d%%")

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTE
# ─────────────────────────────────────────────────────────────────────────────
n_years    = int(target_year) - int(base_year)
df_ts      = timeseries(base_emissions, growth_rate, int(base_year),
                        years_list, ep_strategies, ha_strategies)
bdf        = budget_table(base_emissions, ha_strategies, growth_rate, n_years)

base_total = sum(base_emissions.values())
bau_end    = df_ts["Reference"].iloc[-1]
ha_end     = df_ts["High Ambition"].iloc[-1]
ha_saving  = bau_end - ha_end
total_inv  = bdf[bdf["Sector"]=="TOTAL"]["Investment (₹ Crore)"].values[0]
per_capita = base_total/population if population>0 else 0
per_sqkm   = base_total/area_sqkm  if area_sqkm>0  else 0

city_label = f"{sel_district}, {sel_state}"

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="ascent-hero">
  <p class="hero-title">ASCENT</p>
  <p class="hero-subtitle">Advanced Scenario Carbon Emissions Navigation Tool &nbsp;·&nbsp; WRI India</p>
  <div class="hero-badges">
    <span class="badge">📍 {city_label}</span>
    <span class="badge">🏛 {tier}</span>
    <span class="badge">{cicon} {auto_climate}</span>
    <span class="badge">👥 {population:,} people</span>
    <span class="badge">📐 {area_sqkm:,} sq.km</span>
    <span class="badge">🌧 {avg_rainfall} mm/yr rainfall</span>
    <span class="badge">📅 {int(base_year)} → {int(interim1)} → {int(interim2)} → {int(target_year)}</span>
    <span class="badge">IPCC 2019 · GPC Protocol</span>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI ROW
c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.metric("Base Emissions",     f"{base_total/1e6:.2f} Mt CO₂e")
with c2: st.metric("Per Capita",         f"{per_capita:.1f} t CO₂e")
with c3: st.metric("Per Sq.Km",          f"{per_sqkm/1e3:.1f} kt/km²")
with c4:
    st.metric(f"BAU {int(target_year)}",
              f"{bau_end/1e6:.2f} Mt",
              f"+{(bau_end/base_total-1)*100:.0f}% from base" if base_total>0 else "",
              delta_color="inverse")
with c5:
    st.metric(f"High Ambition {int(target_year)}",
              f"{ha_end/1e6:.2f} Mt",
              f"{(ha_end/bau_end-1)*100:.0f}% vs BAU" if bau_end>0 else "")
with c6: st.metric("HA Investment", f"₹{total_inv:,.0f} Cr")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "📈 Scenarios","🏭 Sub-sector Breakdown",
    "💰 Budget & Cost","🎯 Target Setting",
    "🔍 Sensitivity","📊 Data & Export"
])

with tab1:
    st.plotly_chart(
        chart_trajectories(df_ts, city_label, target_pct, int(base_year)),
        use_container_width=True)
    ca,cb = st.columns(2)
    with ca: st.plotly_chart(chart_wedge(df_ts,"BAU_","Reference (BAU)"), use_container_width=True)
    with cb: st.plotly_chart(chart_wedge(df_ts,"HA_", "High Ambition"),   use_container_width=True)

    st.markdown('<p class="section-header">4-Milestone Summary</p>', unsafe_allow_html=True)
    milestones = [int(base_year), int(interim1), int(interim2), int(target_year)]
    summary_rows = []
    for yr in milestones:
        row = df_ts[df_ts["Year"]==yr]
        if not row.empty:
            r = row["Reference"].values[0]
            h = row["High Ambition"].values[0]
            summary_rows.append({
                "Year": yr,
                "Reference (Mt)":          round(r/1e6,3),
                "Existing & Planned (Mt)": round(row["Existing & Planned"].values[0]/1e6,3),
                "High Ambition (Mt)":      round(h/1e6,3),
                "HA vs BAU":               f"{(h/r-1)*100:.1f}%" if r>0 else "—"
            })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

with tab2:
    ca,cb = st.columns(2)
    with ca: st.plotly_chart(chart_pie(base_emissions), use_container_width=True)
    with cb: st.plotly_chart(chart_subsector_bar(base_emissions), use_container_width=True)

    st.markdown('<p class="section-header">Sub-sector Detail (Base Year)</p>', unsafe_allow_html=True)
    detail_rows = []
    for grp,slist in SECTOR_GROUPS.items():
        for s in slist:
            v = base_emissions.get(s,0)
            detail_rows.append({
                "Sub-sector": s, "Group": grp,
                "Emissions (t CO₂e)": round(v),
                "Emissions (Mt)": round(v/1e6,4),
                "Share (%)": round(v/base_total*100,1) if base_total>0 else 0
            })
    st.dataframe(pd.DataFrame(detail_rows).style.format({
        "Emissions (t CO₂e)": "{:,.0f}", "Emissions (Mt)": "{:.4f}", "Share (%)": "{:.1f}%"
    }), use_container_width=True, hide_index=True)

    st.markdown('<p class="section-header">Sector Applicability by Governance Tier</p>',
                unsafe_allow_html=True)
    tier_df = pd.DataFrame({
        "Tier":             ["State","District","City/ULB","Gram Panchayat"],
        "Buildings":        ["✓","✓","✓","✓"],
        "Electricity Gen.": ["✓","✗","✗","✗"],
        "Transport":        ["✓","✓","✓","✓"],
        "MSW/Waste":        ["✓","✓","✓","✓"],
        "Wastewater":       ["✓","✓","✓","✓"],
        "IPPU":             ["✓","✓","✗","✗"],
        "AFOLU":            ["✓","✓","✗","✓"],
    }).set_index("Tier")
    st.dataframe(tier_df, use_container_width=True)

    st.markdown('<p class="section-header">Emission Factors (ASCENT Excel)</p>',
                unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"Fuel / Activity":k,"Emission Factor":v}
                                for k,v in EMISSION_FACTORS.items()]),
                 use_container_width=True, hide_index=True)

with tab3:
    ca,cb = st.columns(2)
    with ca: st.plotly_chart(chart_budget(bdf), use_container_width=True)
    with cb: st.plotly_chart(chart_cost_eff(bdf), use_container_width=True)

    st.markdown('<p class="section-header">Investment Breakdown (High Ambition)</p>',
                unsafe_allow_html=True)
    st.dataframe(
        bdf.style.apply(lambda row: [
            "background-color:#e8f5ee;font-weight:600" if row["Sector"]=="TOTAL" else ""
            for _ in row], axis=1
        ).format({
            "BAU (t CO₂e)": "{:,.0f}",
            "GHG Reduced (t CO₂e)": "{:,.0f}",
            "Investment (₹ Crore)": "₹{:,.1f}"
        }),
        use_container_width=True, hide_index=True
    )
    if bau_end > 0:
        st.info(f"💡 Total HA investment: **₹{total_inv:,.0f} Crore** to avoid "
                f"**{ha_saving/1e6:.2f} Mt CO₂e** ({ha_saving/bau_end*100:.1f}% below BAU by {int(target_year)})")

with tab4:
    st.markdown('<p class="section-header">Net-Zero Target Pathway</p>', unsafe_allow_html=True)
    if base_total > 0:
        target_rows = []
        for yr in [int(interim1), int(interim2), int(target_year)]:
            r_row = df_ts[df_ts["Year"]==yr]
            if not r_row.empty:
                bau_yr = r_row["Reference"].values[0]
                ha_yr  = r_row["High Ambition"].values[0]
                pct_needed = target_pct*(yr-int(base_year))/n_years if n_years>0 else 0
                target_abs = bau_yr*(1-pct_needed/100)
                achieved   = (1-ha_yr/bau_yr)*100 if bau_yr>0 else 0
                target_rows.append({
                    "Year": yr,
                    "BAU (Mt)":             round(bau_yr/1e6,3),
                    "Target (Mt)":          round(target_abs/1e6,3),
                    "High Ambition (Mt)":   round(ha_yr/1e6,3),
                    "Required Reduction":   f"{pct_needed:.1f}%",
                    "HA Achieves":          f"{achieved:.1f}%",
                    "On Track?":            "✅" if achieved>=pct_needed else "⚠️"
                })
        st.dataframe(pd.DataFrame(target_rows), use_container_width=True, hide_index=True)

    st.markdown('<p class="section-header">IPCC Tier Framework</p>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "IPCC Tier": ["Tier 1","Tier 2","Tier 3"],
        "Description": ["Default EFs — least accurate, most accessible",
                        "Region/fuel-specific data — more accurate",
                        "Site-specific & process-level — highest accuracy"],
        "Best for": ["Gram panchayats, small ULBs with limited data",
                     "Cities and districts with sector-level data",
                     "States with comprehensive reporting infrastructure"]
    }), use_container_width=True, hide_index=True)

with tab5:
    st.plotly_chart(chart_sensitivity(base_emissions, ha_strategies,
                                      int(base_year), int(target_year)),
                    use_container_width=True)
    st.caption("Shaded area = mitigation potential across growth rates 0.5%–10%.")

    st.markdown('<p class="section-header">Climate Zone Reference</p>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Zone":"Hot and Dry","Icon":"🔆","Typical Regions":"Rajasthan, Gujarat (parts), Telangana",
         "Key Energy Impact":"High cooling demand; excellent solar potential"},
        {"Zone":"Warm & Humid","Icon":"💧","Typical Regions":"Kerala, Goa, Coastal AP, TN, WB",
         "Key Energy Impact":"High moisture; natural ventilation focus"},
        {"Zone":"Composite","Icon":"🌤","Typical Regions":"Delhi, MP, UP, Bihar, Maharashtra (parts)",
         "Key Energy Impact":"Mixed heating & cooling loads across seasons"},
        {"Zone":"Cold","Icon":"❄️","Typical Regions":"Himachal, Uttarakhand, Ladakh, Sikkim",
         "Key Energy Impact":"High heating demand; insulation critical"},
        {"Zone":"Temperate","Icon":"🌿","Typical Regions":"Nilgiris, parts of Sikkim",
         "Key Energy Impact":"Mild loads; moderate energy demand year-round"},
    ]), use_container_width=True, hide_index=True)

with tab6:
    st.markdown('<p class="section-header">Year-by-Year Scenario Data</p>', unsafe_allow_html=True)
    show_df = df_ts.copy()
    show_df["Reference (Mt)"]          = (show_df["Reference"]/1e6).round(3)
    show_df["Existing & Planned (Mt)"] = (show_df["Existing & Planned"]/1e6).round(3)
    show_df["High Ambition (Mt)"]      = (show_df["High Ambition"]/1e6).round(3)
    st.dataframe(show_df[["Year","Reference (Mt)","Existing & Planned (Mt)","High Ambition (Mt)"]],
                 use_container_width=True, hide_index=True)

    c1,c2 = st.columns(2)
    with c1:
        csv_ts = df_ts[["Year","Reference","Existing & Planned","High Ambition"]].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download scenario data (CSV)", csv_ts,
                           f"ascent_{sel_district}_scenarios.csv","text/csv")
    with c2:
        csv_bd = bdf.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download budget breakdown (CSV)", csv_bd,
                           f"ascent_{sel_district}_budget.csv","text/csv")

    st.markdown('<p class="section-header">Data Sources</p>', unsafe_allow_html=True)
    st.markdown("""
| Item | Source |
|------|--------|
| GHG projection formula | ASCENT Technical Note (Patel et al., WRI India 2025) |
| Sector categories | IPCC 2019 Refinement of 2006 Guidelines |
| GPC sector structure | Global Protocol for Community-scale GHG Inventories (Fong et al. 2021) |
| Emission factors | ASCENT Excel Tool — Emission Factor sheet |
| City & climate zone data | ASCENT Excel Tool — City_master sheet (all Indian districts) |
| Ahmedabad base year data | ASCENT Excel Tool — Dashboard Data sheet (real computed values) |
| Cost assumptions | ASCENT Excel Tool — Cost and Conversion Factor / Strategies sheet |
""")

st.divider()
st.caption(
    f"ASCENT · WRI India · {city_label} · {auto_climate} climate zone · "
    "IPCC 2019 Guidelines & GPC Protocol"
)

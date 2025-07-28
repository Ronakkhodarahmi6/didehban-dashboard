
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🛡️ DIDEHBAN – Wildlife Risk Monitor", layout="wide")
st.title("🛡️ DIDEHBAN: AI-Powered Wildlife & Wetland Protection Dashboard")

st.markdown("#### A regional decision-support tool for Middle Eastern wetlands 🌍")
st.markdown("🔬 *Focus: Climate stress, animal migration, poaching risk, smart recommendations, and real-time insights*")
st.markdown("👩‍💻 *Project Lead:* **Ronak Khodarahmi**")

# Wetland locations
wetlands_coords = {
    "Khor Kalba (UAE)": (25.0200, 56.3600),
    "Ras Al Khor (UAE)": (25.1800, 55.3200),
    "Gavkhouni (Iran)": (32.3833, 52.7666),
    "Hamoun (Iran)": (31.1000, 61.5000),
    "Bakhtegan (Iran)": (29.6181, 53.8244),
    "Hawizeh Marshes (Iraq)": (31.5000, 47.0000),
    "Azraq Wetland (Jordan)": (31.8333, 36.8166),
    "Salalah Wetlands (Oman)": (17.0500, 54.1000)
}

wetland = st.selectbox("📍 Select Wetland Site:", list(wetlands_coords.keys()))
lat, lon = wetlands_coords[wetland]

# Fetch weather data from Open-Meteo
@st.cache_data
def fetch_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": ["precipitation_sum", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto"
    }
    res = requests.get(url, params=params)
    return res.json()

weather_data = fetch_weather(lat, lon)

if "current_weather" in weather_data:
    current_temp = weather_data["current_weather"]["temperature"]
    st.metric("🌡️ Current Temperature (°C)", current_temp)

    today = weather_data["daily"]["time"][0]
    temp_max = weather_data["daily"]["temperature_2m_max"][0]
    temp_min = weather_data["daily"]["temperature_2m_min"][0]
    rainfall = weather_data["daily"]["precipitation_sum"][0]

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Max Temp Today", f"{temp_max} °C")
    col2.metric("📉 Min Temp Today", f"{temp_min} °C")
    col3.metric("🌧️ Precipitation Today", f"{rainfall} mm")

    # Risk Assessment
    st.markdown("---")
    st.subheader("📊 Risk Assessment")

    stress_level = "Low"
    migration_risk = "Low"

    if current_temp > 40 or rainfall < 5:
        stress_level = "High"
        migration_risk = "High"
    elif current_temp > 35 or rainfall < 10:
        stress_level = "Moderate"
        migration_risk = "Moderate"

    weekend = datetime.now().weekday() in [4, 5]
    near_road = st.checkbox("🛣️ Wetland is near roads or human settlements?", value=True)

    if near_road and weekend:
        poaching_risk = "High"
    elif near_road:
        poaching_risk = "Moderate"
    else:
        poaching_risk = "Low"

    # Display risk alerts and recommendations
    st.markdown("### 🦠 Environmental Stress Level")
    if stress_level == "High":
        st.error("🔥 High stress due to extreme heat or drought")
        st.markdown("**Recommendation:** Provide artificial shade and temporary water sources. Reduce human activity near habitats.")
    elif stress_level == "Moderate":
        st.warning("🌡️ Moderate stress – monitor closely")
        st.markdown("**Recommendation:** Increase environmental monitoring. Prepare backup water supply.")
    else:
        st.success("✅ Low environmental stress")
        st.markdown("**Recommendation:** Maintain current management. Conditions are stable.")

    st.markdown("### 🕊️ Animal Migration Risk")
    if migration_risk == "High":
        st.error("🛑 High risk of early animal migration")
        st.markdown("**Recommendation:** Track movements via GPS tags. Strengthen ecological corridors.")
    elif migration_risk == "Moderate":
        st.warning("🔄 Moderate migration potential")
        st.markdown("**Recommendation:** Coordinate with nearby reserves. Prepare for population shifts.")
    else:
        st.success("🦌 Stable habitat conditions")
        st.markdown("**Recommendation:** No immediate actions needed. Maintain current observations.")

    st.markdown("### 🎯 Poaching Risk")
    if poaching_risk == "High":
        st.error("🚨 High poaching risk – critical alert!")
        st.markdown("**Recommendation:** Deploy ranger teams. Install camera traps. Increase night patrols.")
    elif poaching_risk == "Moderate":
        st.warning("🧐 Moderate poaching risk")
        st.markdown("**Recommendation:** Inform nearby communities. Set up temporary check-points.")
    else:
        st.success("🔒 Poaching risk is low")
        st.markdown("**Recommendation:** Continue routine surveillance.")

    st.markdown("---")
    st.caption("© 2025, DIDEHBAN | Lead: Ronak Khodarahmi")
    st.markdown("---")
    st.markdown("🕊️ *This project is humbly dedicated to the memory of* **Heydarollah Didehban**, *an Iranian ranger who gave his life protecting nature. May his legacy live on through every effort to preserve our planet.*")
    
else:
    st.error("⚠️ Failed to fetch weather data. Try again later.")

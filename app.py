import streamlit as st
import requests
import pandas as pd

# Backend API URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Traffic Smart Analytics", layout="wide")

st.title("🚦 Traffic & Smart City Analytics Dashboard")

# -------------------------------
# Sidebar Menu
# -------------------------------
menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "View Data",
        "Traffic Trends",
        "Peak Hours",
        "Weather Impact",
        "Traffic Prediction",
        "Route Suggestion"
    ]
)

# -------------------------------
# 1. View Full Dataset
# -------------------------------
if menu == "View Data":
    st.header("📊 Full Traffic Dataset")

    res = requests.get(f"{BASE_URL}/data")
    data = res.json()

    df = pd.DataFrame(data)

    st.dataframe(df)


# -------------------------------
# 2. Traffic Trends Visualization
# -------------------------------
elif menu == "Traffic Trends":
    st.header("📈 Traffic Trend Over Time")

    res = requests.get(f"{BASE_URL}/data")
    data = res.json()

    df = pd.DataFrame(data)

    df['datetime'] = pd.to_datetime(df['datetime'])
    df_sorted = df.sort_values("datetime")

    st.line_chart(df_sorted.set_index("datetime")["vehicle_count"])


# -------------------------------
# 3. Peak Congestion Hours
# -------------------------------
elif menu == "Peak Hours":
    st.header("🚨 Peak Congestion Hours")

    res = requests.get(f"{BASE_URL}/peak-hours")
    data = res.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

    st.subheader("📊 Traffic by Hour")
    st.bar_chart(df.set_index("hour"))

    peak_hour = df.iloc[0]["hour"]
    st.success(f"🚨 Peak congestion occurs at: {int(peak_hour)}:00")


# -------------------------------
# 4. Weather Impact
# -------------------------------
elif menu == "Weather Impact":
    st.header("🌦️ Weather Impact on Traffic")

    res = requests.get(f"{BASE_URL}/weather-analysis")
    data = res.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

    st.subheader("📊 Traffic vs Weather")
    st.bar_chart(df.set_index("weather"))


# -------------------------------
# 5. Traffic Prediction
# -------------------------------
elif menu == "Traffic Prediction":
    st.header("🚦 Predict Traffic Level")

    vehicle_count = st.number_input("Vehicle Count", min_value=0, value=100)
    avg_speed = st.number_input("Average Speed", min_value=0.0, value=30.0)

    if st.button("Predict"):
        payload = {
            "vehicle_count": vehicle_count,
            "avg_speed": avg_speed
        }

        res = requests.post(f"{BASE_URL}/predict", json=payload)
        result = res.json()

        level = result["traffic_level"]

        if level == "High":
            st.error(f"🚨 Traffic Level: {level}")
        elif level == "Medium":
            st.warning(f"⚠️ Traffic Level: {level}")
        else:
            st.success(f"✅ Traffic Level: {level}")


# -------------------------------
# 6. Route Optimization
# -------------------------------
elif menu == "Route Suggestion":
    st.header("🛣️ Route Optimization")

    junction_id = st.selectbox("Select Junction", ["J1", "J2", "J3", "J4", "J5"])

    if st.button("Get Best Route"):
        payload = {"junction_id": junction_id}

        res = requests.post(f"{BASE_URL}/route-suggestion", json=payload)
        result = res.json()

        if "message" in result:
            st.error(result["message"])
        else:
            df_best = pd.DataFrame(result)

            # Get all junction data for comparison
            res_all = requests.get(f"{BASE_URL}/junction-analysis")
            df_all = pd.DataFrame(res_all.json())

            st.subheader("📊 Junction Traffic Comparison")
            st.bar_chart(df_all.set_index("junction_id"))

            st.subheader("✅ Best Route Details")
            st.dataframe(df_best)

            st.success("Recommended route based on low traffic and high speed")


# -------------------------------
# Footer
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.write("🚀 Built with FastAPI + Streamlit")
import streamlit as st
import pandas as pd
import os
import datetime
import subprocess
from streamlit_autorefresh import st_autorefresh
import random

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(page_title="Smart City Traffic Dashboard", layout="wide")
st_autorefresh(interval=2000, key="refresh")
st.title("🚦 AI-Enabled Smart Traffic Density Monitoring System")
st.subheader("📍 Jaidev Vihar")

# -----------------------------------------
# CONTROL BUTTONS
# -----------------------------------------
header_col1, header_col2, header_col3 = st.columns([8,1,1])

with header_col2:
    step_btn = st.button("▶ START YOLO")

with header_col3:
    pause_btn = st.button("⏸ PAUSE")

# -----------------------------------------
# SESSION STATE
# -----------------------------------------
if "running" not in st.session_state:
    st.session_state.running = False

# -----------------------------------------
# YOLO START / PAUSE CONTROL
# -----------------------------------------

if "yolo_process" not in st.session_state:
    st.session_state.yolo_process = None

if step_btn:
    if st.session_state.yolo_process is None:

        st.session_state.yolo_process = subprocess.Popen(
            ["python", "yolo_detection.py"]
        )

    st.session_state.running = True

if pause_btn:
    if st.session_state.yolo_process is not None:

        st.session_state.yolo_process.terminate()
        st.session_state.yolo_process = None

    st.session_state.running = False

if st.session_state.running:
    st.success("🟢 YOLO Detection Running")
else:
    st.warning("🔴 YOLO Detection Stopped")


# -----------------------------------------
# READ YOLO TRAFFIC DATA
# -----------------------------------------

CSV_PATH = "data/traffic_data.csv"

if os.path.exists(CSV_PATH):

    df = pd.read_csv(CSV_PATH)

    if not df.empty and "vehicle_count" in df.columns:

        latest_vehicle_count = int(df["vehicle_count"].iloc[-1])

        # Calculate traffic density from YOLO vehicle count
        if latest_vehicle_count < 10:
            latest_density = "Low"
        elif latest_vehicle_count <= 25:
            latest_density = "Medium"
        else:
            latest_density = "High"

    else:
        latest_vehicle_count = 0
        latest_density = "Low"

else:

    df = pd.DataFrame()

    latest_vehicle_count = 0
    latest_density = "Low"


# df = pd.read_csv("data/traffic_data.csv")
# simulated_vehicle_count = df["Vehicle_Count"].iloc[-1]

# -----------------------------------------
# MAIN DASHBOARD
# -----------------------------------------
col1, col2 = st.columns(2)

# -----------------------------------------
# LEFT SIDE - YOLO DATA
# -----------------------------------------
with col1:

    st.subheader("📊 Live YOLO Traffic Feed")

    if not df.empty:

        # Show latest 10 records
        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

        # Vehicle count chart
        st.subheader("📈 Vehicle Count Trend")

        st.line_chart(
            df["vehicle_count"].tail(30)
        )

    else:
        st.info("No YOLO traffic data found.")
# -----------------------------------------
# RIGHT SIDE - AI ANALYSIS
# -----------------------------------------
with col2:

    st.subheader("🧠 AI Traffic Analysis")

    # Live vehicle count detected by YOLO
    st.metric(
        "🚗 Live Vehicle Count",
        latest_vehicle_count
    )

    st.write("### Predicted Traffic State")

    if latest_density == "High":

        st.error("🔴 HIGH DENSITY - CONGESTION WARNING")

        st.warning(
            "High congestion detected! "
            "Activate adaptive signal control and divert traffic."
        )

    elif latest_density == "Medium":

        st.warning("🟡 MEDIUM CONGESTION")

        st.info(
            "Moderate traffic detected. "
            "Optimize signal timing and monitor traffic flow."
        )

    else:

        st.success("🟢 LOW DENSITY")

        st.info(
            "Traffic flow is normal. "
            "Maintain current signal timing."
        )

# -----------------------------------------
# TRAFFIC MANAGEMENT RECOMMENDATION
# -----------------------------------------

st.subheader("🚦 Traffic Management Recommendation")

if latest_density == "High":

    st.error(
        "🚨 High congestion detected! "
        "Activate adaptive signal control and divert traffic."
    )

elif latest_density == "Medium":

    st.warning(
        "⚠️ Moderate traffic detected! "
        "Optimize signal timing and monitor traffic flow."
    )

else:

    st.success(
        "🟢 Traffic flow is normal. "
        "Maintain current signal timing."
    )

st.sidebar.success("YOLOv8 Vehicle Detection Active")
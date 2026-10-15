import streamlit as st
import pandas as pd
import datetime
import os
import base64

# Page Configuration
st.set_page_config(page_title="Drone Surveillance System", layout="wide")

# Custom CSS for Full Edge-to-Edge Width and Full Image Display (No Cropping)
st.markdown("""
    <style>
    /* Main Background & Font Styling (White & Warm Brown) */
    .stApp {
        background-color: #FFFFFF;
        color: #3E2723;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Remove Streamlit default dark header bar and top/side padding */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        visibility: visible;
    }
    
    .block-container, [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    #MainMenu {visibility: visible;}
    footer {visibility: hidden;}
    
    /* Top White Header Bar for Logo */
    .top-header {
        background-color: #FFFFFF;
        padding: 12px 30px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #E0D7D0;
        width: 100vw;
    }
    
    /* True Edge-to-Edge Viewport Breakout for Banner without Cropping */
    .hero-banner-wrapper {
        position: relative;
        width: 100vw;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        overflow: hidden;
        margin-bottom: 25px;
        background-color: #000000;
    }
    
    .hero-banner-wrapper img {
        width: 100vw;
        height: auto; /* Displays the entire image proportionally without cutting the top */
        display: block;
    }
    
    /* Heading and Subtitle Styling */
    .section-title {
        text-align: center;
        color: #4A3525;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 20px 0 10px 0;
    }
    
    .sub-welcome {
        text-align: center;
        color: #6D4C41;
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 30px;
    }
    
    /* Padded wrapper for dashboard content so widgets have breathing room */
    .dashboard-content {
        padding: 0 3rem;
    }
    
    /* Professional Section Headers */
    h3 {
        color: #4A3525 !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #D7CCC8;
        padding-bottom: 4px;
        margin-bottom: 12px;
    }
    
    /* Style Button Text to White with Coffee-Brown Background */
    div.stButton > button {
        color: #FFFFFF !important;
        background-color: #6D4C41 !important;
        border: none;
        font-weight: 600;
        border-radius: 6px;
    }
    
    div.stButton > button:hover {
        background-color: #5C4033 !important;
        color: #FFFFFF !important;
    }
    
    /* Highlight Metrics */
    [data-testid="stMetricValue"] {
        color: #4A3525 !important;
    }
    
    /* Custom Styling for Dataframe / Event Table */
    [data-testid="stDataFrame"] {
        border: 1px solid #D7CCC8;
        border-radius: 8px;
        padding: 5px;
        background-color: #FAF8F5;
    }
    
    /* Ensure Status Alert Text is Dark and Readable */
    .stSuccess p, .stWarning p, .stError p {
        color: #1A1A1A !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Top White Header Bar with Logo on the Left
logo_html = ""
if os.path.exists("logo.jpeg"):
    with open("logo.jpeg", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height: 52px; object-fit: contain;">'

st.markdown(f"""
    <div class="top-header">
        {logo_html}
    </div>
""", unsafe_allow_html=True)

# 2. True Edge-to-Edge Banner Image (Proportional display without top/bottom cropping)
if os.path.exists("drone.jpg"):
    with open("drone.jpg", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
        <div class="hero-banner-wrapper">
            <img src="data:image/jpeg;base64,{img_base64}">
        </div>
    """, unsafe_allow_html=True)

# 3. Heading and Subtitle Below Banner
st.markdown('<h1 class="section-title">Drone Surveillance System</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-welcome">Active Operational Monitoring Dashboard</div>', unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #D7CCC8; margin: 0 3rem 30px 3rem;'>", unsafe_allow_html=True)

# 4. Padded Dashboard Content Container
st.markdown('<div class="dashboard-content">', unsafe_allow_html=True)

# Layout: Two columns (Video on left, Status on right)
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("LIVE VIDEO FEED")
    video_placeholder = st.empty()
    
    with video_placeholder.container():
        st.info("Waiting for live video stream from YOLO module...")

with right_col:
    st.subheader("SYSTEM TELEMETRY")
    
    drone_id = st.selectbox("Select Drone ID", ["Drone01", "Drone02", "Drone03"])
    
    conf_score = "0.91" if drone_id == "Drone01" else "0.85" if drone_id == "Drone02" else "0.96"
    status_text = "MONITOR" if drone_id == "Drone01" else "REVIEW" if drone_id == "Drone02" else "ALERT"
    
    st.metric(label="Active Drone ID", value=drone_id)
    st.metric(label="Confidence Score", value=conf_score)
    
    if status_text == "MONITOR":
        st.success(f"Status: {status_text}")
    elif status_text == "REVIEW":
        st.warning(f"Status: {status_text}")
    else:
        st.error(f"Status: {status_text}")
        
    st.markdown("---")
    st.write(f"**Assessment:** Active tracking for {drone_id}. Stable flight path with telemetry feed locked.")

st.markdown("---")

# Bottom Section: Event Logging (CSV-backed)
st.subheader("EVENT LOG")

LOG_FILE = "drone_events.csv"

if not os.path.exists(LOG_FILE):
    initial_data = pd.DataFrame(columns=["Timestamp", "Drone ID", "Payload", "Zone", "Assessment"])
    sample_row = {"Timestamp": "10:31:02", "Drone ID": "Drone_01", "Payload": "No", "Zone": "No", "Assessment": "Monitor"}
    initial_data = pd.concat([initial_data, pd.DataFrame([sample_row])], ignore_index=True)
    initial_data.to_csv(LOG_FILE, index=False)

log_df = pd.read_csv(LOG_FILE)

if st.button("Simulate Event Entry"):
    new_row = {
        "Timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "Drone ID": drone_id,
        "Payload": "Yes" if status_text != "MONITOR" else "No",
        "Zone": "Yes" if status_text != "MONITOR" else "No",
        "Assessment": status_text.capitalize()
    }
    log_df = pd.concat([log_df, pd.DataFrame([new_row])], ignore_index=True)
    log_df.to_csv(LOG_FILE, index=False)
    st.rerun()

st.dataframe(log_df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
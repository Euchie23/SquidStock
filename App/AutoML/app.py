# =========================================================
# 📦 STANDARD LIBRARIES
# =========================================================
import io
import time
import calendar
from datetime import datetime
from pathlib import Path
import warnings

# =========================================================
# ⚙️ DATA & NUMERICAL PROCESSING
# =========================================================
import numpy as np
import pandas as pd
import joblib

# =========================================================
# 🌊 DATA SOURCING
# =========================================================
import gspread
from google.oauth2.service_account import Credentials
from utils.preprocess import load_weekly_dataset  # local utility function

# =========================================================
# 🎨 VISUALIZATION
# =========================================================
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# 🌐 WEB & INTERACTIVITY
# =========================================================
import streamlit as st

# =========================================================
# ⚠️ WARNINGS
# =========================================================
warnings.filterwarnings("ignore")


# ============================
# 2️⃣ CUSTOM CSS 
# ============================
st.markdown("""
<style>

/* ---------------------- Sidebar ---------------------- */
[data-testid="stSidebar"] > div:first-child {
    top: 0;
    left: 0;
    bottom: 0;
    width: inherit;
    overflow-y: auto;        /* allows scrolling */
    min-height: 100vh;
    padding-top: 0.5rem !important;
    color: #E1EAF2;
    
    /* Combine background image + overlay so it scrolls with content */
    background:
        linear-gradient(rgba(0, 31, 63, 0.6), rgba(0, 31, 63, 0.6)),
        url("https://thumbs.dreamstime.com/b/underwater-seascape-ocean-coral-reef-deep-sea-bottom-swimming-under-water-marine-corals-background-vector-seaweed-algae-354608779.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

# [data-testid="stSidebar"] {
#     width: 370px !important;
# }

section[data-testid="stSidebar"][aria-expanded="true"] {
    width: 370px !important;
}

/* Ensure sidebar content is above overlay */
[data-testid="stSidebar"] > div:first-child > * {
    position: relative;
    z-index: 1;
}


# /* Sidebar titles and headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #39FF14 !important;
    margin-top: 4px !important;
}

# /* Sidebar 'Tabs' section header */
[data-testid="stSidebar"] [data-testid="stRadioGroupLabel"] p {
    font-size: 25px !important;
    font-weight: 800 !important;
    color: #FFD700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-align: center !important;
    margin-bottom: 10px !important;
}

/* Sidebar radio button text */
[data-testid="stSidebar"] [role="radiogroup"] label p {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #E1EAF2 !important;
}

# /* Sidebar links */
[data-testid="stSidebar"] a {
    font-size: 20px !important;
    color: #39FF14 !important;
}

# /* Sidebar footer */
.sidebar-footer {
    position: absolute;
    bottom: 10px;
    width: 100%;
    padding: 10px;
}
            
# /* Make the sidebar background extend the full height */
section[data-testid="stSidebar"] {
    min-height: 100vh !important;
}

# /* Optional: adjust padding for expanders inside sidebar */
section[data-testid="stSidebar"] .st-expander {
    margin-bottom: 1rem;
}
            
# /* Disable sidebar resize handle */
div[data-testid="stSidebarResizer"] {
    display: none !important;
    pointer-events: none !important;
}


/* ---------------------- Main panel ---------------------- */
.stApp {
    position: relative;
    background-image: url("https://images.unsplash.com/photo-1530951980629-fbeef86f69a1?q=80&w=2768&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    color: #E1EAF2;
}
.stApp::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(10, 47, 68, 0.7);
    z-index: 0;
}
.stApp > * {
    position: relative;
    z-index: 1;
}

# [data-testid="stAppViewContainer"] > .main {
#     margin-left: 370px !important;
#     margin-top: 0 !important;      /* flush with top */
#     transition: margin-left 0.3s ease;
# }



/* ---------------------- Titles ---------------------- */
h1, .stTitle {
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #39FF14 !important;
}

/* Markdown text */
.stMarkdown, .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li, .stCaption {
    font-size: 20px !important;
    line-height: 1.8 !important;
    color: #E1EAF2 !important;
}
            
 /* Allow emojis to render using system default emoji font */
h1 span.emoji, 
h2 span.emoji,
h3 span.emoji,
p span.emoji {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif !important;
    font-weight: 400 !important;   /* emojis don’t like bold */
}

            
/* ---------------------- 🟢 Markdown Headers Fix ---------------------- */

/* Ensure Markdown titles keep the right color and size across the app */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.block-container h1, .block-container h2, .block-container h3,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #39FF14 !important;
    font-weight: 800 !important;
    margin-top: 6px !important;
    margin-bottom: 6px !important;
}

/* Header sizes */
.stMarkdown h1, .block-container h1,
[data-testid="stSidebar"] .stMarkdown h1 {
    font-size: 34px !important;
}
.stMarkdown h2, .block-container h2,
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 28px !important;
}
.stMarkdown h3, .block-container h3,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 24px !important;
}

/* Sidebar paragraph text */
[data-testid="stSidebar"] .stMarkdown p {
    color: #E1EAF2 !important;
    font-size: 18px !important;
    line-height: 1.6 !important;
}

/* ---------------------- Tabs ---------------------- */
.stTabs [data-baseweb="tab"] {
    font-size: 20px !important;
    padding: 12px 20px !important;
    font-weight: 600 !important;
    color: #E1EAF2 !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #FFD700 !important;
    border-bottom: 3px solid #FFD700 !important;
}

/* ---------------------- DataFrames ---------------------- */
[data-testid="stDataFrame"] {
    width: 100% !important;
    margin-bottom: 1.5rem !important;
}
[data-testid="stDataFrame"] table {
    font-size: 19px !important;
    line-height: 1.4 !important;
    border-collapse: collapse !important;
}
[data-testid="stDataFrame"] th {
    font-weight: 700 !important;
    background-color: rgba(0, 31, 63, 0.8) !important;
    color: #39FF14 !important;
    padding: 8px !important;
}
[data-testid="stDataFrame"] td {
    color: #E1EAF2 !important;
    padding: 6px !important;
}
        

/* ---------------------- Sidebar + Main Layout Fix ---------------------- */

header[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

# [data-testid="stSidebar"] {
#     top: 0 !important;
#     height: 100vh !important;
# }

[data-testid="stSidebar"] {
    width: 370px !important;
}

section[data-testid="stSidebar"] {
    flex-shrink: 0 !important;
}

div[data-testid="stAppViewContainer"] {
    margin-top: 0 !important;
}

/* Sidebar fixed below top bar */
# [data-testid="stSidebar"] {
#     position: fixed !important;
#     top: 0rem !important;      /* below top bar */
#     left: 0 !important;
#     width: 370px !important;
#     height: 100vh !important;
#     overflow-y: auto !important;
#     z-index: 100 !important;
# }

/* Main content shifted to the right and below top bar */
# [data-testid="stAppViewContainer"] {
#     margin-left: 370px !important;  /* match sidebar width */
#     margin-top: 0rem !important;  /* below top bar */
#     padding: 0 2rem !important;
# }

/* Block container inside main content */
.block-container {
    padding: 2rem !important;
    margin: 0 !important;
    max-width: 100% !important;
}


/* Responsive adjustments for smaller screens */
@media (max-width: 992px) {
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
    }
    [data-testid="stSidebar"] {
        position: relative !important;
        width: 100% !important;
        top: 0 !important;
        height: auto !important;
    }
}


/* ---------------------- Buttons & Sliders ---------------------- */
div.stButton > button:first-child {
    background-color: #39FF14 !important;
    color: #001f3f !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    display: block !important;
    margin: 0 auto !important;
}
div.stButton > button:first-child:hover {
    background-color: #32CD32 !important;
    color: #FFD700 !important;
}
            
div[data-testid="stSlider"] label p {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================
# 3️⃣ SIDEBAR NAVIGATION
# ============================
# Title
st.sidebar.markdown("""
<h1 style="font-size: 32px; font-weight: 800; text-align: center;">
    <img src="https://twemoji.maxcdn.com/v/latest/72x72/1f916.png" width="32" style="vertical-align:middle;"> 
    Predictive Catch Models 
    <img src="https://twemoji.maxcdn.com/v/latest/72x72/1f991.png" width="32" style="vertical-align:middle;">
</h1>
""", unsafe_allow_html=True)

# Tabs
tabs = [
    "Overview",
    "Data Exploration",
    "Feature Engineering",
    "Anomaly Detection",
    "Model Evaluation",
    "Classification",
    "Regression",
    "Predict Scenarios",
    "Logbook"  # add logbook tab
]

# Custom "Tabs" header in the sidebar
st.sidebar.markdown("""
<div style="
    font-size: 23px;
    font-weight: 800;
    color: #FFD700;
    text-align: justify;
    margin-bottom: 10px;
">
    Tabs:
</div>
""", unsafe_allow_html=True)

# =========================================================
# INITIALIZE SESSION STATE
# =========================================================

# ---------------- Page & Tabs ----------------
if "page" not in st.session_state:
    st.session_state.page = tabs[0]  # default to first tab

# ---------------- Notes ----------------
if "notes" not in st.session_state:
    # Initialize notes dict with empty lists for all tabs except Logbook
    st.session_state.notes = {tab: [] for tab in tabs if tab != "Logbook"}

# Ensure current page has a list
if st.session_state.page not in st.session_state.notes:
    st.session_state.notes[st.session_state.page] = []

# ---------------- Note Input & Edit Mode ----------------
if "note_input" not in st.session_state:
    st.session_state.note_input = ""

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {"active": False, "tab": None, "index": None}

if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = {}

if "auto_expand_notes" not in st.session_state:
    st.session_state.auto_expand_notes = False

if "notes_expanded" not in st.session_state:
    st.session_state.notes_expanded = False  # collapsed by default

if "clear_note_input" not in st.session_state:
    st.session_state.clear_note_input = False  # ✅ added for safe clearing

if "tab_extra_params" not in st.session_state:
    st.session_state.tab_extra_params = {}
tab_extra_params = st.session_state.tab_extra_params

# ---------------- Toast Message ----------------
if "toast_message" in st.session_state and st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = ""


# ---------------- Page Selection ----------------

# Determine which pages are available
if st.session_state.edit_mode["active"]:
    available_tabs = [st.session_state.edit_mode["tab"]]  # only allow editing tab
    disabled_radio = True
else:
    available_tabs = tabs
    disabled_radio = False

# Determine the selected index
selected_index = available_tabs.index(st.session_state.page) if st.session_state.page in available_tabs else 0

# Single radio with dynamic lock
page = st.sidebar.radio(
    "Select tab",
    available_tabs,
    index=selected_index,
    key="page",
    disabled=disabled_radio
)

# Reset toast flags for other tabs when switching tabs
for tab in tabs:
    if tab != page:
        st.session_state[f"toast_shown_{tab}"] = False


# Optional warning
if st.session_state.edit_mode["active"]:
    st.warning("⚠️ You are editing a reloaded note. You must save before switching tabs.")


      # Use columns to center the button
    col1, col2, col3 = st.columns([1, 1, 1])  # Adjust the middle column width

    with col2:
        if st.button("❌ Exit Edit Mode"):
            st.session_state.redirect_page = st.session_state.edit_mode["tab"]
            st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
            st.session_state.preload_note_input = ""
            st.session_state.auto_expand_notes = False
            st.rerun()


# ---------------- Safe Clear Trigger ----------------
if st.session_state.clear_note_input:
    st.session_state.note_input = ""
    st.session_state.clear_note_input = False


# Keep notes panel expander open if typing or editing
st.session_state.notes_expanded = bool(st.session_state.note_input.strip()) or st.session_state.edit_mode["active"]


# 🔹 Keep expander open if user is editing or typing
st.session_state.notes_expanded = (
    bool(st.session_state.note_input.strip())
    or st.session_state.edit_mode["active"]
    or st.session_state.auto_expand_notes
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

#For how saved notes are displayed in the logbook tab and the downloads
TABS_WITH_PARAMS = ["Data Exploration", "Feature Engineering", "Anomaly Detection", "Model Evaluation", "Classification", "Regression", "Predict Scenarios"]

def format_note_display(note, tab_name):

    timestamp = note.get("timestamp")
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown time"
    content = note.get("notes", "")

    # Pull parameters
    inputs = note.get("inputs", {})
    feature = note.get("feature")  # Only for Feature Engineering
    variable = inputs.get("variable")  # Only for Data Exploration

    # Build tab-specific label text
    if tab_name == "Data Exploration":
        extra = f"**Variable:** {variable}" if variable else ""

    elif tab_name == "Feature Engineering":
        extra = f"**Feature:** {feature}" if feature else ""

    elif tab_name == "Anomaly Detection":
        sel = inputs.get("selected_var_display", "N/A")
        thr = inputs.get("threshold", "N/A")  # Now already formatted with units
        extra = f"**Parameters:** {sel} > {thr}"

    elif tab_name in ["Classification", "Regression"]:
        week = inputs.get("Week", "N/A")
        extra = f"**Week:** {week}"

    elif tab_name == "Predict Scenarios":
        week = inputs.get("Week", "N/A")
        env_text = inputs.get("Environmental_Display", "None")
        
        baseline_regime = inputs.get("Baseline_Regime", "N/A")
        baseline_cpue = inputs.get("Baseline_CPUE", 0.0)
        modified_cpue = inputs.get("Modified_CPUE", 0.0)

        extra = (
            f"**Week:** {week} | "
            f"**Baseline Regime:** {baseline_regime} | "
            f"**Baseline CPUE:** {baseline_cpue:,.0f} kg | "
            f"**Modified CPUE:** {modified_cpue:,.0f} kg | "
            f"**Environmental:** {env_text}"
        )

    else:
        extra = ""

    formatted = (
        f"🕒 {timestamp_str} | 📍 Source: {tab_name} |  {extra}\n\n"
        f"🗒️ Notes: {content}\n\n"
        f"{'-'*50}\n\n"
    )
    return formatted

# For Feature Engineering
def get_readable_name(feature):
    base_names = {
        "WeekStart": "Week Start Date",
        "Year": "Year",
        "Month": "Month",
        "WeekOfYear": "Week of Year",
        "Avg_weekly_Lat": "Average Weekly Latitude",
        "Avg_weekly_Lon": "Average Weekly Longitude",
        "total_weekly_catch_kg": "Total Weekly Catch",
        "weekly_effort": "Weekly Effort",
        "Avg_weekly_Depth": "Average Weekly Depth",
        "Avg_weekly_WaterTemp": "Average Weekly Water Temperature",
        "weekly_CPUE_per_effort": "CPUE per Effort",
        "Chlor_a_mg_m3": "Chlorophyll-a",
        "SSH": "Sea Surface Height",
    }

    # Add rolling suffixes without repeating unit
    rolling_suffixes = ["2wk", "3wk", "5wk"]
    for suffix in rolling_suffixes:
        if feature.endswith(f"_{suffix}"):
            parent = feature.replace(f"_{suffix}", "")
            base = base_names.get(parent, parent)
            return f"{base} — {suffix}"

    # Interaction names
    interactions = {
        "Temp_x_Depth": "Temperature × Depth",
        "Temp_x_Depth_2wk": "Temperature × Depth (2wk)",
        "Temp_x_Depth_3wk": "Temperature × Depth (3wk)",
        "Temp_x_Depth_5wk": "Temperature × Depth (5wk)",
        "Temp_x_Chlor": "Temperature × Chlorophyll",
        "Depth_x_Chlor": "Depth × Chlorophyll",
        "Temp_x_SSH": "Temperature × SSH",
    }
    if feature in interactions:
        return interactions[feature]

    return base_names.get(feature, feature)


# For inputing readable names for variables in dropdown lists and app in general so instead of SSH we will have Sea Surface Height
def selectbox_box_readable_names(feature):
    base = {
        "WeekStart": "Week Start Date",
        "Year": "Year",
        "Month": "Month",
        "WeekOfYear": "Week of Year",
        "Avg_weekly_Lat": "Average Weekly Latitude",
        "Avg_weekly_Lon": "Average Weekly Longitude",
        "total_weekly_catch_kg": "Total Weekly Catch",
        "weekly_effort": "Weekly Effort",
        "Avg_weekly_Depth": "Average Weekly Depth",
        "Avg_weekly_WaterTemp": "Average Weekly Water/Sea Surface Temperature",
        "weekly_CPUE_per_effort": "CPUE per Effort",
        "Chlor_a_mg_m3": "Chlorophyll-a",
        "SSH": "Sea Surface Height",
    }

    name = base.get(feature, feature)
    unit = get_unit(feature)

    return f"{name} ({unit})" if unit else name

# For adding Units to variables for readbility e.g Depth (m)
def get_unit(feature):
    env_vars = ["Lat", "Lon", "Depth", "WaterTemp", "Chlor_a", "SSH"]
    for v in env_vars:
        if v in feature:
            if "Lat" in feature or "Lon" in feature:
                return "°"
            elif "Depth" in feature:
                return "m"
            elif "WaterTemp" in feature:
                return "°C"
            elif "Chlor_a" in feature:
                return "mg/m³"
            elif "SSH" in feature:
                return "m"
    if feature in ["total_weekly_catch_kg"]:
        return "tons"
    if feature in ["weekly_effort"]:
        return "days"
    if feature in ["weekly_CPUE_per_effort"]:
        return "kg/day"
    return ""


#For brief general figure descriptions
def get_caption(feature):
    captions = {
        "WeekStart": "ℹ️ Each bar shows one week. Some weeks may be combined; only the latest date is labeled.",
        "Year": "ℹ️ Year of observation.",
        "Month": "ℹ️ Month of observation.",
        "Avg_weekly_Lat": "ℹ️ Average location (latitude) in degrees.",
        "Avg_weekly_Lon": "ℹ️ Average location (longitude) in degrees.",
        "total_weekly_catch_kg": "ℹ️ Weekly catch in tons for readability (1 ton = 1000 kg).",
        "weekly_effort": "ℹ️ Number of fishing days in the week. Higher bars = more days fished.",
        "Avg_weekly_Depth": "ℹ️ Average depth fished in meters.",
        "Avg_weekly_WaterTemp": "ℹ️ Average water/ sea Surface temperature in °C.",
        "weekly_CPUE_per_effort": "ℹ️ CPUE per Effort shows how many tons of squid were caught per day of fishing. Higher bars = more catch per day.",
        "Chlor_a_mg_m3": "ℹ️ Chlorophyll concentration in water (mg/m³).",
        "SSH": "ℹ️ Sea surface height in meters.",
        "sin_week": "ℹ️ Seasonal value 0–1, peaks = mid-year weeks; low = start of year.",
        "cos_week": "ℹ️ Seasonal value -1 to 1, peaks = start or mid-year weeks.",
        "Depth_bin": "ℹ️ Depth categories ordered shallow → mid → deep → very deep.",
        "WaterTemp_bin": "ℹ️ Temperature categories ordered cold → moderate → warm → very warm.",
        "Chlor_a_bin": "ℹ️ Chlorophyll categories ordered low → moderate → high → very high.",
        "SSH_bin": "ℹ️ SSH categories ordered very low → low → neutral → high → very high.",
        "CPUE_level": "ℹ️ CPUE Level: Low → Medium → High, showing catch per day categories."
    }

    # Handle rolling versions like "_2wk", "_3wk", "_5wk"
    rolling_suffixes = ["2wk", "3wk", "5wk"]
    for suffix in rolling_suffixes:
        if feature.endswith(f"_{suffix}"):
            parent = feature.replace(f"_{suffix}", "")
            return captions.get(parent, "")
    
    return captions.get(feature, "")



# For identifying raw, real variables
rolling_suffixes = ("_2wk", "_3wk", "_5wk")
engineered_patterns = ("_x_", "_bin")
engineered_exact = {"CPUE_level", "sin_week", "cos_week"}
qc_columns = {"anomaly_flag"}

def is_raw_feature(name: str) -> bool:
    """Return True if the variable is a real, raw, interpretable feature."""
    if name.endswith(rolling_suffixes):    # rolling windows
        return False
    if any(p in name for p in engineered_patterns):  # interactions, bins
        return False
    if name in engineered_exact:           # engineered exact features
        return False
    if name in qc_columns:                 # QC or anomaly flags
        return False
    return True


#For Classification, Regression and Predict Scenario Tabs
def apply_modifications(row, deltas, bin_choice):
    """Apply user modifications and recalc interaction features."""
    row_mod = row.copy()
    
    # Base features
    row_mod["Avg_weekly_WaterTemp_3wk"] += deltas.get("temp", 0.0)
    row_mod["Avg_weekly_Depth_3wk"] += deltas.get("depth", 0.0)
    row_mod["Chlor_a_mg_m3_5wk"] += deltas.get("chlor", 0.0)
    if bin_choice == "Medium":
        row_mod["SSH_5wk"] += deltas.get("ssh", 0.0)

    # Recalculate interactions
    row_mod["Temp_x_Depth_3wk"] = row_mod["Avg_weekly_WaterTemp_3wk"] * row_mod["Avg_weekly_Depth_3wk"]
    row_mod["Temp_x_Chlor"] = row_mod["Avg_weekly_WaterTemp_3wk"] * row_mod["Chlor_a_mg_m3_5wk"]
    row_mod["Depth_x_Chlor"] = row_mod["Avg_weekly_Depth_3wk"] * row_mod["Chlor_a_mg_m3_5wk"]
    if bin_choice == "Medium":
        row_mod["Temp_x_SSH"] = row_mod["Avg_weekly_WaterTemp_3wk"] * row_mod["SSH_5wk"]

    return row_mod

def prepare_row_for_model(row, features):
    """Keep only model features and convert to numeric."""
    row_model = pd.DataFrame({f: row[f] if f in row else 0 for f in features}, index=[0])
    return row_model.apply(pd.to_numeric, errors="coerce").fillna(0)

def predict_cpue(row_model, models):
    """Predict classification bin and CPUE (kg and tons)."""
    # Predict classification
    clf = models["clf_top1"]
    classification = clf.predict(row_model)[0]

    # Select regressor
    regressor = {
        "Low": models["reg_low"],
        "Medium": models["reg_med"],
        "High": models["reg_high"]
    }[classification]

    # Prepare row for regression
    reg_features = [f for f in regressor.feature_names_in_ if f != "CPUE_log1p"]
    row_reg = prepare_row_for_model(row_model, reg_features)

    cpue_pred_log = regressor.predict(row_reg)[0]
    cpue_pred_kg = np.expm1(cpue_pred_log)
    cpue_pred_tons = cpue_pred_kg / 1000

    return classification, cpue_pred_kg, cpue_pred_tons


def display_cpue(classification, cpue_kg, cpue_tons):
    """Display CPUE with color coding and interpretation."""
    bin_colors = {"Low": "red", "Medium": "orange", "High": "green"}
    
    st.subheader("Scenario Prediction")
    st.markdown(f"**Classification Bin:** {classification} CPUE ({'low catch' if classification=='Low' else 'moderate catch' if classification=='Medium' else 'high catch'})")
    st.markdown(f"""
    ### Predicted CPUE
    <span style='color:{bin_colors[classification]}; font-size:24px'>
    {cpue_kg:.0f} kg ({cpue_tons:.1f} tons)
    </span>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    **Interpretation / Advice (if predictions were accurate):**  
    - **Low CPUE:** anticipate few catches; may consider adjusting fishing effort.  
    - **Medium CPUE:** moderate catch expected; plan operations accordingly.  
    - **High CPUE:** high catch expected; could be an opportunity for larger harvest, but beware of overfishing risks.  
    - Predictions are approximate; rolling averages and interactions were recalculated heuristically.
    """)


# For global week syncing between classification, regression and predict scenarios tab
df_global = load_weekly_dataset()

# Only show week slider on these pages
if page in ["Classification", "Regression", "Predict Scenarios"]:

    if "week_index" not in st.session_state:
        st.session_state["week_index"] = 1

    st.sidebar.markdown("### 📅 Select Week")
    st.sidebar.write("Controls Classification, Regression, and Scenario tabs.")

    week_selected = st.sidebar.slider(
        "Simulation Week:",
        1,
        len(df_global),
        st.session_state["week_index"],
        help="Select the simulation week index (weeks 1–468 across 20 years of data)"
    )

    st.session_state["week_index"] = week_selected


# =========================================================
# LOGBOOK TAB
# =========================================================

# ---------------- Notes Panel ----------------
if page != "Logbook":
    with st.sidebar:
        # --- Divider ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>", unsafe_allow_html=True)

        # --- Ensure session defaults exist ---
        if "params" not in st.session_state:
            st.session_state.params = {}
        if "notes" not in st.session_state:
            st.session_state.notes = {t: [] for t in tabs}
        if "note_input" not in st.session_state:
            st.session_state.note_input = ""
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
        if "delete_confirm" not in st.session_state:
            st.session_state.delete_confirm = {}

        params = st.session_state.params
        st.markdown("### 🗒️ Notes Panel")

        with st.expander(f"💬 Notes for {page}", expanded=st.session_state.notes_expanded):
            st.session_state.auto_expand_notes = False
            note_text = st.text_area(
                "Write your note here:",
                key="note_input",
                height=150,
                placeholder="Type your note..."
            )

            # Tabs that store parameter snapshots
            TABS_WITH_PARAMS = ["Data Exploration", "Feature Engineering", "Anomaly Detection", "Model Evaluation", "Classification", "Regression", "Predict Scenarios"]

            # --- Save Button ---
            if st.button("💾 Save Note", key=f"save_{page}"):
                content = note_text.strip()
                if content:
                    new_entry = {
                        "timestamp": datetime.now(),
                        "notes": content,
                        "inputs": params.copy() if page in TABS_WITH_PARAMS else {},
                    }
                    # ---------------- Saving a note ----------------
                    tab_extra_params = {}

                    if page == "Data Exploration":
                        selected_feature = st.session_state.get("selected_feature", None)

                        if selected_feature:
                            readable_feature = selectbox_box_readable_names(selected_feature)
                        else:
                            readable_feature = None

                        tab_extra_params["variable"] = readable_feature

                    elif page == "Feature Engineering":
                        feature_raw = st.session_state.get("selected_feature_eng")

                        if feature_raw:
                            # Rolling suffixes
                            rolling_suffix = ""
                            for s in ["_2wk", "_3wk", "_5wk"]:
                                if feature_raw.endswith(s):
                                    rolling_suffix = f" — {s.replace('_',' ')}"
                                    break

                            # Binned features mapping
                            binned_map = {
                                "Chlor_a_bin": "Chlorophyll a binned",
                                "Depth_bin": "Depth binned",
                                "WaterTemp_bin": "Sea Surface Temperature binned",
                                "SSH_bin": "Sea Surface Height binned",
                                "CPUE_level": "Catch Per Unit Effort Levels",
                            }

                            if feature_raw in binned_map:
                                base_name = binned_map[feature_raw]
                            elif feature_raw in ["sin_week", "cos_week"]:
                                base_name = "Seasonal Week (sin)" if feature_raw == "sin_week" else "Seasonal Week (cos)"
                            else:
                                base_name = get_readable_name(feature_raw)

                            # Interaction features: remove units
                            # --- Interaction features ---
                            if "_x_" in feature_raw:
                                parts = feature_raw.split("_x_")
                                
                                interaction_mapping = {
                                    "Temp": "Sea Surface Temperature",
                                    "Avg_weekly_WaterTemp": "Sea Surface Temperature",
                                    "Depth": "Depth",
                                    "Avg_weekly_Depth": "Depth",
                                    "Chlor": "Chlorophyll a",
                                    "Chlor_a": "Chlorophyll a",
                                    "Chlor_a_mg_m3": "Chlorophyll a",
                                    "SSH": "Sea Surface Height",
                                }

                                readable_parts = []
                                for p in parts:
                                    # strip rolling suffix for individual part
                                    for s in ["_2wk", "_3wk", "_5wk"]:
                                        if p.endswith(s):
                                            p = p[:-len(s)]
                                            break
                                    readable_parts.append(interaction_mapping.get(p, get_readable_name(p)))

                                saved_feature_str = " × ".join(readable_parts) + rolling_suffix
                            else:
                                unit = get_unit(feature_raw)
                                saved_feature_str = f"{base_name}({unit})" if unit else f"{base_name}{rolling_suffix}"

                            extra = f"**Feature:** {saved_feature_str}"

                            # Save for logging/edit
                            tab_extra_params["feature_raw"] = feature_raw
                            tab_extra_params["feature"] = saved_feature_str
                        else:
                            extra = ""

                    elif page == "Anomaly Detection":
                        selected_var = st.session_state.get("selected_var", None)
                        threshold_val = st.session_state.get("threshold", None)

                        int_vars_no_unit = ["year", "month", "weekofyear", "day"]

                        saved_threshold_str = "N/A"

                        if selected_var is not None and threshold_val is not None:
                            
                            # 0) If threshold_val is a string (coming from EDIT mode), extract the numeric part
                            if isinstance(threshold_val, str):
                                num_str = threshold_val.split(" ")[0]  # split off units
                                try:
                                    threshold_val = float(num_str)
                                except:
                                    threshold_val = None

                            unit = get_unit(selected_var)

                            # 1) pure integer vars, no unit
                            if selected_var.lower() in int_vars_no_unit:
                                saved_threshold_str = f"{int(threshold_val)}"

                            # 2) integer physically meaningful vars with unit (weekly_effort)
                            elif unit != "" and float(threshold_val).is_integer():
                                saved_threshold_str = f"{int(threshold_val)} ({unit})"

                            # 3) continuous numeric vars with unit
                            else:
                                saved_threshold_str = f"{float(threshold_val):.2f} ({unit})"
                        tab_extra_params["selected_var_display"] = selectbox_box_readable_names(selected_var)

                        # Save the raw variable name for restoring the selectbox and slider
                        tab_extra_params["selected_var_raw"] = selected_var 
                        tab_extra_params["threshold"] = saved_threshold_str

                    elif page in ["Classification", "Regression"]:
                        tab_extra_params["Week"] = st.session_state.get("week_index", 1)

                    elif page == "Predict Scenarios":
                        # 1️⃣ Reset inactive sliders
                        if not params.get("medium_cpue", False):
                            params["delta_SSH"] = 0.0

                        # 2️⃣ Build display dictionary
                        environmental_display = {
                            "Temperature (°C)": params.get("delta_T", "N/A"),
                            "Chlorophyll a (mg/m³)": params.get("delta_Chlor_a", "N/A"),
                            "Depth (m)": params.get("depth", 0.0)   # Depth always allowed
                        }

                        # Add SSH ONLY for Medium CPUE AND when non-zero
                        if params.get("medium_cpue", False):
                            ssh_val = params.get("delta_SSH", 0.0)
                            environmental_display["Sea Surface Height (m)"] = ssh_val
                            # if ssh_val != 0.0:
                            #     

                        # 3️⃣ Prepare comma-separated string for logbook
                        environmental_display_str = ",  ".join(f"{k}: {v}" for k, v in environmental_display.items())

                        # 4️⃣ Internal dict for edit mode
                        environmental_internal = {
                            "delta_T": params.get("delta_T", 0.0),
                            "delta_Chlor_a": params.get("delta_Chlor_a", 0.0),
                            "depth": params.get("depth", 0.0),
                            "delta_SSH": params.get("delta_SSH", 0.0),
                            "medium_cpue": params.get("medium_cpue", False)
                        }

                        # 5️⃣ Tab extra params
                        tab_extra_params = {
                            "Week": params.get("week_index", "N/A"),
                            "Baseline_Regime": params.get("Baseline_Regime", "N/A"),
                            "Baseline_CPUE": params.get("Baseline_CPUE", 0.0),
                            "Modified_CPUE": params.get("Modified_CPUE", 0.0),
                            "Environmental": environmental_display,
                            "Environmental_Display": environmental_display_str,
                            "Environmental_Internal": environmental_internal
                        }

                    new_entry = {
                        "timestamp": datetime.now(),
                        "inputs": tab_extra_params,
                        "notes": st.session_state.note_input.strip(),
                        "feature": tab_extra_params.get("feature") if page == "Feature Engineering" else None
                    }


                    if st.session_state.edit_mode["active"] and st.session_state.edit_mode["tab"] == page:
                        idx = st.session_state.edit_mode["index"]
                        st.session_state.notes[page][idx] = new_entry
                        st.session_state.toast_message = f"✏️ Note updated in {page}!"
                        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
                    else:
                        st.session_state.notes[page].append(new_entry)
                        st.session_state.toast_message = f"✅ Note saved to Logbook!"

                    # ✅ Trigger the safe clear for next rerun
                    st.session_state.clear_note_input = True
                    st.rerun()
                else:
                    st.toast("⚠️ Nothing to save (note is empty).")


# ---------------- Logbook ----------------
else:
    st.title("📔 Logbook")

    notes_exist = any(st.session_state.notes[tab] for tab in st.session_state.notes)
    if not notes_exist:
        st.info("No notes yet. Go to any tab to add some notes!")
    else:
        for tab_name, notes in st.session_state.notes.items():
            if not notes:
                continue
                
             # Check if the expander should be open
            expander_state_key = f"expander_state_{tab_name}"
            if expander_state_key not in st.session_state:
                st.session_state[expander_state_key] = False

            with st.expander(f"🗂 {tab_name} ({len(notes)} notes)", expanded=st.session_state[expander_state_key]):
                for i, note in enumerate(notes):
                    col1, col2, col3 = st.columns([6, 1, 1])
                    with col1:
                        st.markdown(format_note_display(note, tab_name))
                    with col2:
                        if st.button("✏️", key=f"edit_{tab_name}_{i}"):
                            #entry = note
                            entry = st.session_state.notes[tab_name][i]

                            # Restore note text
                            st.session_state.note_input = entry.get("notes", "")

                            # Restore tab-specific parameters
                            inputs = entry.get("inputs", {})

                            # --- Data Exploration ---
                            if tab_name == "Data Exploration":
                                if "variable" in inputs:
                                     st.session_state.inputs = inputs 

                            # --- Feature Engineering ---
                            elif tab_name == "Feature Engineering":

                                # 1️⃣ Restore the raw feature used in the snapshot
                                feature_raw = inputs.get("feature_raw")

                                if feature_raw:
                                    # Set it into session state so the selectbox updates on page reload
                                    st.session_state.selected_feature_eng = feature_raw
                                  
                                    # Rolling suffix
                                    rolling_suffix = ""
                                    for s in ["_2wk", "_3wk", "_5wk"]:
                                        if feature_raw.endswith(s):
                                            rolling_suffix = f" — {s.replace('_',' ')}"
                                            break

                                    # Binned features
                                    binned_map = {
                                        "Chlor_a_bin": "Chlorophyll a binned",
                                        "Depth_bin": "Depth binned",
                                        "WaterTemp_bin": "Sea Surface Temperature binned",
                                        "SSH_bin": "Sea Surface Height binned",
                                        "CPUE_level": "Catch Per Unit Effort Levels",
                                    }

                                    if feature_raw in binned_map:
                                        base_name = binned_map[feature_raw]

                                    # Seasonal features
                                    elif feature_raw == "sin_week":
                                        base_name = "Seasonal Week (sin)"
                                    elif feature_raw == "cos_week":
                                        base_name = "Seasonal Week (cos)"

                                    # Normal features
                                    else:
                                        base_name = get_readable_name(feature_raw)

                                    # Interaction features (NO UNIT)
                                    if "_x_" in feature_raw:
                                        parts = feature_raw.split("_x_")
                                        saved_feature_str = " × ".join([get_readable_name(p) for p in parts])

                                    # Non-interactions
                                    else:
                                        unit = get_unit(feature_raw)
                                        saved_feature_str = f"{base_name}{rolling_suffix} ({unit})" if unit else f"{base_name}{rolling_suffix}"

                                    # Commit the logbook display string
                                    extra = f"**Feature:** {saved_feature_str}"

                                else:
                                    extra = ""

                            # --- Anomaly Detection ---
                            elif tab_name == "Anomaly Detection":
                                st.session_state.anomaly_edit_mode = True

                                if "selected_var_raw" in inputs:
                                    st.session_state.selected_var = inputs["selected_var_raw"]

                                # threshold is stored WITH units, so we must extract numeric part
                                saved_thr = inputs.get("threshold")
                                if saved_thr:
                                    numeric_part = saved_thr.split()[0]
                                    try:
                                        st.session_state.threshold = float(numeric_part)
                                        print(numeric_part)
                                    except:
                                        st.session_state.threshold = None

                            # --- Model Evaluation ---
                            elif tab_name == "Model Evaluation":
                                # Restore any parameters saved in this tab
                                for k, v in inputs.items():
                                    st.session_state.params[k] = v

                            elif tab_name in ["Classification", "Regression"]:
                                if "Week" in inputs:
                                    st.session_state.week_index = inputs["Week"]


                            elif tab_name == "Predict Scenarios":

                                st.session_state.pred_scen_edit_mode = True

                                # Reload week
                                st.session_state.week_index = inputs.get("Week", 1)

                                # Internal environment dict
                                env = inputs.get("Environmental_Internal", {})

                                st.session_state.params["delta_T"] = env.get("delta_T", 0.0)
                                st.session_state.params["delta_Chlor_a"] = env.get("delta_Chlor_a", 0.0)
                                st.session_state.params["depth"] = env.get("depth", 0.0)
                                st.session_state.params["delta_SSH"] = env.get("delta_SSH", 0.0)

                                # Preserve SSH vs Depth mode
                                st.session_state.params["medium_cpue"] = env.get("medium_cpue", False)


                            st.session_state.edit_mode = {"active": True, "tab": tab_name, "index": i}
                            st.session_state.toast_message = f"📸 Snapshot reloaded for {tab_name}. Please save again after editing."
                            #st.session_state.page = tab_name

                            # ✅ Force notes panel to auto-expand after rerun
                            st.session_state.auto_expand_notes = True
                            st.rerun()

                    with col3:
                        delete_key = f"{tab_name}_{i}"
                        if not st.session_state.delete_confirm.get(delete_key, False):
                            if st.button("🗑", key=f"delete_{tab_name}_{i}"):
                                st.session_state.delete_confirm[delete_key] = True
                                st.session_state[expander_state_key] = True
                                st.rerun()
                        else:
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("✅", key=f"confirm_del_{tab_name}_{i}"):
                                    del st.session_state.notes[tab_name][i]
                                    st.session_state.delete_confirm.pop(delete_key, None)
                                    st.session_state.toast_message = f"🗑 Deleted note {i+1} from {tab_name}"
                                    st.session_state[expander_state_key] = True
                                    st.rerun()
                            with c2:
                                if st.button("❌", key=f"cancel_del_{tab_name}_{i}"):
                                    st.session_state.delete_confirm[delete_key] = False
                                    st.session_state[expander_state_key] = True
                                    st.rerun()
                                    
                if 'auto_expand_notes' in st.session_state:
                    st.session_state[expander_state_key] = st.session_state.auto_expand_notes
    # --- Final Observation + Download ---
    st.subheader("🧾 Final Observation")
    st.session_state.final_observation = st.text_area(
        "Write your final observation here:",
        value=st.session_state.get("final_observation", ""),
        height=150,
        placeholder="Summarize your findings..."
    )

    st.markdown("---")
    st.warning(
        "⚠️ **Important:** Your notes are stored only for this session. "
        "If you leave or refresh the app, they will be lost.\n\n"
        "💾 Please download them to your computer if you wish to keep a copy."
    )

    # --- Step 1: Prepare content only when clicked ---
    if st.button("🧩 Prepare Logbook for Download"):
        all_notes_text = f"📝 FINAL OBSERVATION:\n{st.session_state.final_observation}\n\n📔 INDIVIDUAL NOTES:\n\n"
        for tab, notes in st.session_state.notes.items():
            if notes:
                all_notes_text += f"{tab} ({len(notes)} notes):\n"
                for note in notes:
                    all_notes_text += format_note_display(note, tab)
                all_notes_text += "\n"

        st.session_state.all_notes_text = all_notes_text
        st.success("✅ Logbook is ready to download!")

    if "all_notes_text" in st.session_state and st.session_state.all_notes_text:
        buffer = io.BytesIO(st.session_state.all_notes_text.encode("utf-8"))

        # Current datetime string
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"logbook_{timestamp}.txt"
        st.download_button(
            label="📥 Download Logbook (.txt)",
            data=buffer,
            file_name=file_name,
            mime="text/plain"
        )
    # 📤 Send to Host Section (appears after download)
    
    # --- Define the function ---
    def send_notes_to_host(all_notes_text, tab_name="predictive_catch_models"):
        try:
            # Authenticate with Google Sheets
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],  scopes=["https://www.googleapis.com/auth/spreadsheets"])
            client = gspread.authorize(creds)

            # Open the target sheet by ID (no need for an extra ["google_sheets"] key)
            sheet = client.open_by_key("1mLnW5UHnRU8Cs5tD1NKtvr-ODlFPdFOoZi0lqXTEj10").worksheet(tab_name)

            # Append a new anonymous submission
            sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), all_notes_text])

            return True
        except Exception as e:
            st.error(f"Error sending notes: {e}")
            return False


    # --- In your Logbook section, keep all this under the same indentation ---
    st.markdown("---")
    st.subheader("📤 Send to Host (Optional)")
    st.info(
        "🧠 By sharing your notes *anonymously*, you help the host improve their "
        "data interpretation, statistical analysis, and app development skills.\n\n"
        "No personal information is collected — only your text notes are shared.\n\n"
        "*It may take a few seconds to confirm whether your notes were successfully sent to the host. Thank you for your patience 🙂*"
    )

    send_to_host = st.checkbox("Send my notes to the host (optional)")

    if send_to_host:
        if st.button("📤 Confirm & Send"):
            # Gather all notes + final observation into one text block
            all_notes_text = "📝 FINAL OBSERVATION:\n" + st.session_state.final_observation + "\n\n"
            all_notes_text += "📔 INDIVIDUAL NOTES:\n\n"
            for tab_name, notes in st.session_state.notes.items():
                if notes:
                    all_notes_text += f"[{tab_name}] ({len(notes)} notes):\n"
                    for note in notes:
                        all_notes_text += format_note_display(note, tab_name)
                    all_notes_text += "\n"
            
            
            # Show spinner while sending
            with st.spinner("⏳ Connecting to Google Sheets... This may take a few seconds."):
                    # Send to Google Sheets
                    success = send_notes_to_host(all_notes_text)

            if success:
                st.success("✅ Upload to Google Sheets successful! Your notes were sent anonymously. Thank you!")
            else:
                st.error("❌ Failed to send notes. Please try again later.")

    st.markdown("---")

    st.markdown("<h3 style='text-align:center'>🚀 Looking Ahead</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center'>It’s bittersweet to wrap up the SquidStock series 😔 — thank you for exploring these insights with me. Your feedback, suggestions, and ideas have been invaluable in helping improve the apps in the repository and their analyses.</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center'>For those curious to dive deeper, feel free to explore the:</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center'>1) <a href='https://github.com/Euchie23/SquidStack/' target='_blank' style='color:#39FF14; font-weight:600;'>SquidStack Repository</a> – Extends the SquidStock series by diving deeper into specific modules, analyzing 2019–2021 squid data to uncover shifts in marine environmental health and pollutant trends, including the impacts of the COVID-19 lockdown. This focused, year-specific lens complements the broader SquidStock analyses and highlights how global events can influence local ecosystems.</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center'>2) <a href='https://github.com/Euchie23/GeoTentacles/' target='_blank' style='color:#39FF14; font-weight:600;'>GeoTentacles Repository</a> – Builds on both SquidStock and SquidStack datasets for spatial exploration. It visualizes catch hotspots, predicts swarming behavior, and maps pollution impacts using PostgreSQL/PostGIS, QGIS, and ML techniques — bridging temporal trends with spatial insights for a comprehensive understanding of marine dynamics.</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center'>With that said, our SquidStock journey continues with ambitions in scalable ML deployment, versioning, and operational workflows. Together, we’ve built a foundation for meaningful, real-world impact. Stay tuned — the next adventure awaits! Don’t miss it!!😁 </p>", unsafe_allow_html=True)


    # 🔹 Centered "Coming Soon" button (functional version)
st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR FOOTER INFORMATION
# =========================================================

st.sidebar.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# --- Divider Line ---
st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>", unsafe_allow_html=True)

# --- Contact Block ---
st.sidebar.markdown("""
<div style="margin-top: 20px; color: white;">
  <p style="color: #39FF14; font-weight: bold; font-size: 22px;">📬 Want to connect or collaborate?</p>
  <ul style="list-style-type: none; padding-left: 0; line-height: 1.7;">
    <li style="font-size: 16px; font-weight: bold;">📧 Email: 
      <a href="mailto:euchiejnpierre@gmail.com" style="color: #39FF14; text-decoration: none;">Euchie</a>
    </li>
    <li style="font-size: 16px; font-weight: bold;">💼 LinkedIn: 
      <a href="https://www.linkedin.com/in/euchiejnpierre/" target="_blank" style="color: #39FF14; text-decoration: none;">Visit Profile</a>
    </li>
    <li style="font-size: 16px; font-weight: bold;">🌍 GitHub: 
      <a href="https://github.com/Euchie23" target="_blank" style="color: #39FF14; text-decoration: none;">More About Me</a>
    </li>
    <li style="font-size: 16px; font-weight: bold;">💬 Share Your Thoughts: 
      <a href="https://github.com/Euchie23/SquidStock/issues/new" target="_blank" style="color: #39FF14; text-decoration: none;">Open an Issue</a>
    </li>
  </ul>
</div>
""", unsafe_allow_html=True)


# ========================================
#  LOAD DATA
# ========================================
from pathlib import Path
import pandas as pd
import joblib
import streamlit as st
import requests

# Base directory relative to app.py
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"


# Load cleaned weekly dataset
@st.cache_data
def load_weekly_dataset():
    """Loads your cleaned dataset."""
    return pd.read_csv(DATA_DIR / "weekly_processed.csv")
  

@st.cache_data
def build_feature_row(df_weekly, week_index, overrides=None):
    """Extract a weekly row, apply overrides, recompute interactions, and return ONLY model features."""
    
    row = df_weekly.iloc[week_index].copy()

    # Remove target if present
    if "CPUE_level" in row.index:
        row = row.drop(labels=["CPUE_level"])

    # Apply overrides
    if overrides:
        for k, v in overrides.items():
            if k in row.index:
                row[k] = v

    # Recompute interactions
    row["Temp_x_Depth"] = row["Avg_weekly_WaterTemp_3wk"] * row["Avg_weekly_Depth_3wk"]
    row["Temp_x_Chlor"] = row["Avg_weekly_WaterTemp_3wk"] * row["Chlor_a_mg_m3_5wk"]
    row["Depth_x_Chlor"] = row["Avg_weekly_Depth_3wk"] * row["Chlor_a_mg_m3_5wk"]
    row["Temp_x_SSH"]   = row["Avg_weekly_WaterTemp_3wk"] * row["SSH_5wk"]

    return row



# Load all models
MODEL_URLS = {
    "anom": "https://drive.google.com/uc?export=download&id=1WpzTiik2KWvfmx5P7ZOPRZOxMoyrpNqq",
    "clf_top1": "https://drive.google.com/uc?export=download&id=1XhKt8O3fLs_ds_A1zypmQYmMbpdvsSi5",
    "clf_top2": "https://drive.google.com/uc?export=download&id=15xOGE6omuUjuvm7kcxW-h6cJ2I5NosFc",
    "clf_top3": "https://drive.google.com/uc?export=download&id=1IIuxBkWLa4hUGp0ect3KeN8FTpDCDd-o",
    "reg_low": "https://drive.google.com/uc?export=download&id=1Y1E5HNyJBsk30JGpP3RqUEamB5W3Bqj-",
    "reg_med": "https://drive.google.com/uc?export=download&id=1boLCLCMKNjPaZIn2TYrgs9xXH_yW-ZRh",
    "reg_high": "https://drive.google.com/uc?export=download&id=1qIDfvuLhUAGrbLeoJBsq5ESfup2kEI8H",
}


@st.cache_data
def download_model(url: str, save_as: str):
    """Download a file from a URL and save it locally."""
    r = requests.get(url)
    with open(save_as, "wb") as f:
        f.write(r.content)
    return save_as

@st.cache_resource
def load_model(path: str):
    """Load a model from a local path."""
    return joblib.load(path)



@st.cache_resource
def load_all_models():
    """Loads every model required for classification, regression, anomaly detection."""
    loaded = {}
    
    for name, url in MODEL_URLS.items():
        local_filename = f"{name}.pkl"     # e.g., anom.pkl, clf_top1.pkl
        path = download_model(url, local_filename)
        loaded[name] = load_model(path)
    
    return loaded



# Make weekly dataset from daily data
@st.cache_data
def make_weekly(df):
    df['Date'] = pd.to_datetime(df[['Year','Month','Day']])
    df['WeekStart'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly = df.groupby('WeekStart').agg({
        'CPUE':'sum', 'CTNO':'nunique', 'Lat':'mean', 'Lon':'mean',
        'WaterTemp':'mean','Depth':'mean'
    }).rename(columns={'CPUE':'total_weekly_catch_kg','CTNO':'weekly_effort',
                       'WaterTemp':'Avg_weekly_WaterTemp','Depth':'Avg_weekly_Depth'}).reset_index()
    weekly['weekly_CPUE_per_effort'] = weekly['total_weekly_catch_kg'] / weekly['weekly_effort']
    return weekly


# Feature engineering
@st.cache_data
def feature_engineer(weekly):
    weekly = weekly.sort_values('WeekStart')
    weekly['WeekOfYear'] = weekly['WeekStart'].dt.isocalendar().week
    weekly['Year'] = weekly['WeekStart'].dt.year
    weekly['Avg_weekly_WaterTemp_5wk'] = weekly['Avg_weekly_WaterTemp'].rolling(5, min_periods=1).mean()
    weekly['Avg_weekly_Depth_5wk'] = weekly['Avg_weekly_Depth'].rolling(5, min_periods=1).mean()
    # merge monthly chlor/ssh if available
    return weekly




# ========================================
#  TAB 1: OVERVIEW
# ========================================
if page == "Overview":
   # -------------------- Page Title & Welcome Text --------------------
    st.title("🦑 Squid Stock Assessment & Forecasting Engine ⚙️")

    st.markdown("""
    ### 🧭 Problem Framing & Decision Context
    
    Weekly CPUE predictions are often requested for operational planning, yet short-lived squid populations
    exhibit extreme ecological variability. CPUE is strongly influenced by environmental conditions,
    fishing effort, spatial targeting, and unobserved ecological drivers, making raw weekly trends
    noisy and unreliable for immediate operational decisions.
    
    This module applies **distribution-aware, regime-sensitive machine learning models** to
    separate meaningful ecological signals from ephemeral noise. By combining classification of CPUE
    regimes (Low / Medium / High) with class-conditioned regression, along with anomaly and feature
    drift detection, the workflow produces **interpretable weekly forecasts and alerts**. 
    
    These outputs help fisheries managers focus on **regime-level trends and adaptive decision-making**, 
    rather than overreacting to short-term fluctuations that carry high irreducible uncertainty.
    """)


    st.markdown("""
    Welcome to the integrated AI-based forecasting system for weekly **squid CPUE prediction**.  
    Navigate the pages on the left to explore environmental features, anomaly signals,  
    model diagnostics, and scenario-based forecasting tools.

    These pages include:

    - 📊 **Overview**
    - 🧬 **Feature Engineering**
    - 🤖 **Model Evaluation**
    - 🎯 **Classification (Low / Medium / High CPUE)**
    - 📈 **Regression (CPUE prediction)**
    - 🔮 **Predictive Scenario Simulator**
    """)

    # -------------------- Overview Section --------------------
    st.markdown("## 📌 Overview")

    df = load_weekly_dataset()

    st.markdown("""
    This dashboard summarizes the full modeling pipeline for weekly squid CPUE forecasting.
    """)

    st.subheader("Preview of Weekly Dataset")
    st.dataframe(df.head())
    
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    # 💬 Justified body with both working links
        # ⚓ Centered title for navigation
    st.markdown(
        "<h3 style='text-align: center; color: #E1EAF2;'>⚓ Continue Your Journey</h3>",
        unsafe_allow_html=True
    )
    
    html_links = """
    <div style="text-align: center; color: #E1EAF2; font-size: 20px; line-height: 1.6;">
    If you'd like to learn more about the methods, predictive catch models, and datasets used in this stage of the voyage:<br>
    👉 <a href="https://github.com/Euchie23/SquidStock/tree/main/notebooks/AutoML" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration: underline;">Explore the AutoML Notebook</a><br><br>
    Or, explore the entire <b>SquidStock Expedition</b> — see how this stage connects to the full storyline:<br>
    🌊 <a href="https://github.com/Euchie23/SquidStock" target="_blank" style="color:#FFD700; font-weight:bold; text-decoration: underline;">Visit the SquidStock Repository</a>
    </div>
    """

    st.markdown(html_links, unsafe_allow_html=True)



# ========================================
#  TAB 2: DATA EXPLORATION
# ========================================

elif page == "Data Exploration":
    
    from matplotlib.ticker import StrMethodFormatter

    st.title("🔎 Data Exploration")

    df = load_weekly_dataset()

    st.markdown("""
    ### 🔍 What this page shows  
    This page allows you to explore the **raw features** collected on a weekly basis in the squid fisheries dataset.  
    These features represent the original observations before any feature engineering or interactions are applied.

    They include:

    - Weekly aggregation metrics (CPUE, effort, catch)
    - Environmental indicators (e.g., water temperature, depth, chlorophyll-a, sea surface height)
    - Temporal information (week start, month, year)
    - Geographic location (latitude, longitude)

    Use this section to inspect distributions and trends in the **original observed data**.
    """)

    # Preview raw data
    st.markdown("### Preview of raw features:")
    st.dataframe(df.head())

    # Feature Distribution Explorer
    st.subheader("📊 Raw Feature Distribution Explorer")

    # Filter dataframe for raw features automatically
# --- Step 1: Get available raw features ---
    raw_features_available = [col for col in df.columns if is_raw_feature(col)]

    if raw_features_available:

        # --- Step 2: Build readable names and mapping ---
        readable_options = [selectbox_box_readable_names(f) for f in raw_features_available]
        mapping = dict(zip(readable_options, raw_features_available))

        # --- Step 3: Restore from logbook (edit mode) ---
        if "inputs" in st.session_state and "variable" in st.session_state.inputs:
            readable_saved = st.session_state.inputs["variable"]
            if readable_saved in mapping:
                st.session_state.selected_feature = mapping[readable_saved]

        # --- Step 4: Ensure a fallback default ---
        if "selected_feature" not in st.session_state or \
        st.session_state.selected_feature not in raw_features_available:
            st.session_state.selected_feature = raw_features_available[0]

        # --- Step 5: Display selectbox ---
        current_readable = selectbox_box_readable_names(st.session_state.selected_feature)
        selected_readable = st.selectbox(
            "Select a raw feature to visualize:",
            readable_options,
            index=readable_options.index(current_readable)
        )

        # --- Step 6: Store the selected raw feature ---
        st.session_state.selected_feature = mapping[selected_readable]

    else:
        st.warning("No raw features available to display.")

    # Now use st.session_state.selected_feature as usual
    feature = st.session_state.selected_feature

    # Non-interaction features
    fig, ax = plt.subplots(figsize=(10, 4))
    display_name = get_readable_name(feature)
    unit = get_unit(feature)

    # --- WeekStart ---
    if feature == "WeekStart":
        df[feature] = pd.to_datetime(df[feature])
        week_numeric = df[feature].map(pd.Timestamp.toordinal)
        ax.hist(week_numeric, bins=20, edgecolor="black")
        bin_edges = np.linspace(week_numeric.min(), week_numeric.max(), 21)
        tick_labels = [pd.Timestamp.fromordinal(int(edge)).strftime("%d %b %Y") for edge in bin_edges[:-1]]
        ax.set_xticks(bin_edges[:-1])
        ax.set_xticklabels(tick_labels, rotation=45, ha="right")
        ax.set_title(f"Distribution of {display_name}")
        ax.set_xlabel(display_name)
        st.caption(get_caption(feature))

    # --- Year ---
    elif feature == "Year":
        years = sorted(df[feature].dropna().astype(int).unique())
        ax.hist(df[feature].dropna().astype(int), bins=len(years), edgecolor="black")
        ax.set_xticks(years)
        ax.set_xticklabels(years, rotation=45)
        ax.set_title(f"Distribution of {display_name}")
        ax.set_xlabel(display_name)
        st.caption(get_caption(feature))

    elif feature == "weekly_CPUE_per_effort":
        # Convert kg/day → tons/day
        cpue_tons = df[feature] / 1000

        ax.hist(cpue_tons, bins=30, edgecolor="black")
        
        # Disable scientific notation
        ax.ticklabel_format(style='plain', axis='x')

        ax.set_xlabel("CPUE per Effort (tons/day)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of CPUE per Effort (tons/day)")
        st.caption(get_caption(feature))

    # --- Month (Jan–Jun) ---
    elif feature == "Month":
        months = df["Month"].dropna().astype(int)
        ax.hist(months, bins=6, edgecolor="black")
        ax.set_xticks(range(1,7))
        ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun"])
        ax.set_title(f"Distribution of {display_name}")
        ax.set_xlabel(display_name)
        st.caption(get_caption(feature))

    # --- Total Weekly Catch (tons) ---
    elif feature == "total_weekly_catch_kg":
        tons = df[feature]/1000
        ax.hist(tons, bins=30, edgecolor="black")
        ax.set_xlabel("Total Weekly Catch (tons)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Total Weekly Catch (tons)")
        st.caption(get_caption(feature))


    # --- Weekly effort ---
    elif feature == "weekly_effort":
        ax.hist(df[feature], bins=7, edgecolor="black")
        ax.set_xlabel("Weekly Effort (days)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Weekly Effort")
        st.caption(get_caption(feature))


    # --- All other numeric / environmental features ---
    else:
        ax.hist(df[feature].dropna(), bins=30, edgecolor="black")
        if unit: 
            ax.set_xlabel(f"{display_name} ({unit})")
            ax.set_title(f"Distribution of {display_name} ({unit})")
        else:
            ax.set_xlabel(display_name)
            ax.set_title(f"Distribution of {display_name}")
        ax.set_ylabel("Frequency")
        st.caption(get_caption(feature))
    
    st.pyplot(fig)




# ========================================
#  TAB 3: FEATURE ENGINEERING
# ========================================

elif page == "Feature Engineering":
    
    from matplotlib.ticker import StrMethodFormatter

    st.title("🛠️ Feature Engineering Exploration")

    df = load_weekly_dataset()

    st.markdown("""
    ### 🔍 What this page shows  
    This page displays the **engineered features** used in the weekly CPUE prediction model.  
    These features are derived from raw observations to capture temporal trends, interactions, and categorical information.

    They include:

    - Rolling windows (2wk, 3wk, 5wk) for smoothing
    - Seasonal cycles (`sin_week`, `cos_week`)
    - Binned environmental categories (Depth_bin, WaterTemp_bin, Chlor_a_bin, SSH_bin)
    - Interaction features (Temp×Depth, Temp×Chlor, Temp×SSH)
    - CPUE level categories

    Use this section to explore distributions and relationships in the **engineered dataset**.
    """)

    # Preview of engineered features
    st.markdown("### Preview of engineered features:")
    st.dataframe(df.head())

    st.subheader("📊 Engineered Feature Distribution Explorer")

  
   
    # Automatic engineered feature detection
    rolling_suffixes = ("_2wk", "_3wk", "_5wk")
    engineered_patterns = ("_x_", "_bin")
    engineered_exact = {"CPUE_level", "sin_week", "cos_week"}

    def is_engineered_feature(name: str) -> bool:
        if name.endswith(rolling_suffixes):
            return True
        if any(p in name for p in engineered_patterns):
            return True
        if name in engineered_exact:
            return True
        return False

    engineered_features_available = [col for col in df.columns if is_engineered_feature(col)]



  # Engineered feature select
    if engineered_features_available:

        readable_options = []
        mapping = {}

        # Binned & special names
        binned_map = {
            "Chlor_a_bin": "Chlorophyll a binned",
            "Depth_bin": "Depth binned",
            "WaterTemp_bin": "Sea Surface Temperature binned",
            "SSH_bin": "Sea Surface Height binned",
            "CPUE_level": "Catch Per Unit Effort Levels",
        }

        for f in engineered_features_available:

            # --- 1️⃣ Interaction features ---
            if "_x_" in f:
                p1, p2 = f.split("_x_")

                # Detect rolling suffix for the FULL interaction name
                rolling_suffix = ""
                for s in ["_2wk", "_3wk", "_5wk"]:
                    if f.endswith(s):
                        rolling_suffix = f" — {s.replace('_',' ')}"
                        break

                # Remove rolling suffix from each side BEFORE mapping names
                def strip_roll(x):
                    for s in ["_2wk", "_3wk", "_5wk"]:
                        if x.endswith(s):
                            return x[:-len(s)]
                    return x

                p1_clean = strip_roll(p1)
                p2_clean = strip_roll(p2)

                # Full names for components
                interaction_fullnames = {
                    "Temp": "Sea Surface Temperature",
                    "Avg_weekly_WaterTemp": "Sea Surface Temperature",

                    "Depth": "Depth",
                    "Avg_weekly_Depth": "Depth",

                    "Chlor": "Chlorophyll a",
                    "Chlor_a": "Chlorophyll a",
                    "Chlor_a_mg_m3": "Chlorophyll a",

                    "SSH": "Sea Surface Height",
                }

                full1 = interaction_fullnames.get(p1_clean, get_readable_name(p1_clean))
                full2 = interaction_fullnames.get(p2_clean, get_readable_name(p2_clean))

                # Final readable name (suffix restored at the END)
                readable_name = f"{full1} × {full2}{rolling_suffix}"

                # store mapping
                readable_options.append(readable_name)
                mapping[readable_name] = f

                continue

            # --- 2️⃣ Binned features ---
            elif f in binned_map:
                readable_name = binned_map[f]

            # --- 3️⃣ Seasonal features ---
            elif f == "sin_week":
                readable_name = "Seasonal Week (sin)"
            elif f == "cos_week":
                readable_name = "Seasonal Week (cos)"

            # --- 4️⃣ Rolling features + normal features ---
            else:
                base_name = get_readable_name(f)

                # Detect rolling window
                rolling_suffix = ""
                for s in ["_2wk", "_3wk", "_5wk"]:
                    if f.endswith(s):
                        # Fix double duplication: NEVER show base again
                        rolling_suffix = " — " + s.replace("_", " ")
                        break

                # Units for non-interaction features
                unit = get_unit(f)

                if unit:
                    readable_name = f"{base_name}({unit})"
                else:
                    readable_name = f"{base_name}{rolling_suffix}"

            # Add to dropdown list
            readable_options.append(readable_name)
            mapping[readable_name] = f


        # Restore saved selection (edit logic safe) 
        saved_feature_raw = None
        if "selected_feature_eng" in st.session_state:
            saved_feature_raw = st.session_state.selected_feature_eng
        elif "note" in locals() and note is not None:
            saved_feature_raw = note.get("feature_raw", None)

        # Ensure stored selection exists
        if saved_feature_raw not in engineered_features_available:
            saved_feature_raw = engineered_features_available[0]

        st.session_state.selected_feature_eng = saved_feature_raw

        # Convert stored raw → readable for selectbox index
        current_readable = mapping_inv = {v: k for k, v in mapping.items()}  # invert mapping
        current_readable = mapping_inv.get(saved_feature_raw, readable_options[0])

        # User selects readable name
        selected_readable = st.selectbox(
            "Select an engineered feature to visualize:",
            readable_options,
            index=readable_options.index(current_readable)
        )

        # Convert readable → raw
        st.session_state.selected_feature_eng = mapping[selected_readable]

    else:
        st.warning("No engineered features available to display.")

    # Save raw + formatted name for logging
    saved_feature_str = selected_readable
    tab_extra_params["feature_raw"] = st.session_state.selected_feature_eng  # raw column for plotting
    tab_extra_params["feature"] = saved_feature_str  # formatted display name


    # PLOTTING — ALWAYS USE THE RAW NAME FROM SESSION STATE ===
    feature = st.session_state.selected_feature_eng

    # PLOTTING
    def get_engineered_readable_name(feature_raw):
        """
        Converts engineered column names into clean readable names.
        Handles rolling windows, binned features, seasonal encodings,
        and interaction features WITHOUT duplicated rolling suffixes.
        """

        # Identify rolling suffix for non-interaction features
        rolling_suffix = ""
        for s in ["_2wk", "_3wk", "_5wk"]:
            if feature_raw.endswith(s):
                rolling_suffix = f" — {s.replace('_', ' ')}"
                break

        # Binned features
        binned_map = {
            "Chlor_a_bin": "Chlorophyll a binned",
            "Depth_bin": "Depth binned",
            "WaterTemp_bin": "Sea Surface Temperature binned",
            "SSH_bin": "Sea Surface Height binned",
            "CPUE_level": "Catch Per Unit Effort Levels",
        }
        if feature_raw in binned_map:
            return binned_map[feature_raw]

        # Seasonal features
        if feature_raw == "sin_week":
            return "Seasonal Week (sin)"
        if feature_raw == "cos_week":
            return "Seasonal Week (cos)"

        # Interaction features
        if "_x_" in feature_raw:

            p1, p2 = feature_raw.split("_x_")

            # strip rolling from each part
            def strip_roll(x):
                for s in ["_2wk", "_3wk", "_5wk"]:
                    if x.endswith(s):
                        return x[:-len(s)]
                return x

            p1_clean = strip_roll(p1)
            p2_clean = strip_roll(p2)

            # Map short names to full environmental readable names
            interaction_fullnames = {
                "Temp": "Sea Surface Temperature",
                "Avg_weekly_WaterTemp": "Sea Surface Temperature",

                "Depth": "Depth",
                "Avg_weekly_Depth": "Depth",

                "Chlor": "Chlorophyll a",
                "Chlor_a": "Chlorophyll a",
                "Chlor_a_mg_m3": "Chlorophyll a",

                "SSH": "Sea Surface Height",
            }

            n1 = interaction_fullnames.get(p1_clean, get_readable_name(p1_clean))
            n2 = interaction_fullnames.get(p2_clean, get_readable_name(p2_clean))

            # IMPORTANT: add rolling suffix once, at the END ONLY
            return f"{n1} × {n2}{rolling_suffix}"

        # Default rolling features
        base = get_readable_name(feature_raw)
        unit = get_unit(feature_raw)

        return f"{base}{rolling_suffix} ({unit})" if unit else f"{base}{rolling_suffix}"


    def interaction_axis_label(col, feature_raw):
        """
        Generate axis label for interaction plots.
        col: the individual column (x or y)
        feature_raw: full interaction feature name (may have rolling suffix)
        """
        # --- Determine rolling suffix from the feature name ---
        rolling_suffix = ""
        for s in ["_2wk","_3wk","_5wk"]:
            if feature_raw.endswith(s):
                rolling_suffix = f" — {s.replace('_',' ')}"
                break

        # --- Map to readable names ---
        clean_col = col
        mapping = {
            "Temp": "Average Weekly Sea Surface Temperature",
            "Depth": "Average Weekly Depth",
            "Chlor": "Chlorophyll a",
            "Chlor_a": "Chlorophyll a",
            "Chlor_a_mg_m3": "Chlorophyll a",
            "SSH": "Sea Surface Height",
            "SSH_": "Sea Surface Height",
        }
        readable = mapping.get(clean_col, get_readable_name(clean_col))
        unit = get_unit(col)

        # --- Append rolling suffix only if it exists ---
        if rolling_suffix:
            label = f"{readable}"
        else:
            label = readable

        return f"{label} ({unit})" if unit else label


    # Interaction features: scatterplots
    if "_x_" in feature:
        interactions_map = {
            "Temp_x_Depth": ["Avg_weekly_WaterTemp","Avg_weekly_Depth"],
            "Temp_x_Depth_2wk": ["Avg_weekly_WaterTemp_2wk","Avg_weekly_Depth_2wk"],
            "Temp_x_Depth_3wk": ["Avg_weekly_WaterTemp_3wk","Avg_weekly_Depth_3wk"],
            "Temp_x_Depth_5wk": ["Avg_weekly_WaterTemp_5wk","Avg_weekly_Depth_5wk"],
            "Temp_x_Chlor": ["Avg_weekly_WaterTemp_3wk","Chlor_a_mg_m3_5wk"],
            "Depth_x_Chlor": ["Avg_weekly_Depth_3wk","Chlor_a_mg_m3_5wk"],
            "Temp_x_SSH": ["Avg_weekly_WaterTemp_3wk","SSH_5wk"],
        }
        feat1, feat2 = interactions_map.get(feature, [feature.split("_x_")[0], feature.split("_x_")[1]])
        
        fig, ax = plt.subplots(figsize=(8,5))
        ax.scatter(df[feat1], df[feat2], alpha=0.5)
        # pass the full interaction feature to know whether rolling suffix exists
        ax.set_xlabel(interaction_axis_label(feat1, feature))
        ax.set_ylabel(interaction_axis_label(feat2, feature))
        ax.set_title(get_engineered_readable_name(feature))
        st.pyplot(fig)
        st.caption(f"⚠️ Interaction feature: combined effect of {get_readable_name(feat1)} and {get_readable_name(feat2)}")

    # Non-interaction engineered features
    else:
        fig, ax = plt.subplots(figsize=(10, 4))
        display_name = get_readable_name(feature)
        unit = get_unit(feature)

        # Binned features or CPUE_level
        if feature.endswith("_bin") or feature == "CPUE_level":
            counts = df[feature].value_counts()
            if feature == "Depth_bin": order = ["shallow","mid","deep","very_deep"]
            elif feature == "WaterTemp_bin": order = ["cold","moderate","warm","very_warm"]
            elif feature == "Chlor_a_bin": order = ["low","moderate","high","very_high"]
            elif feature == "SSH_bin": order = ["very_low","low","neutral","high","very_high"]
            elif feature == "CPUE_level": order = ["Low","Medium","High"]
            else: order = sorted(counts.index)
            counts = counts.reindex(order)
            ax.bar(counts.index.astype(str), counts.values, edgecolor="black")
            read_name = get_engineered_readable_name(feature)
            ax.set_xlabel(read_name)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Distribution of {read_name}")
            st.caption(get_caption(feature))

        # Seasonal encoded features
        elif feature in ["sin_week","cos_week"]:
            ax.hist(df[feature].dropna(), bins=30, edgecolor="black")
            ax.set_xlabel(display_name)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Distribution of {display_name}")
            if feature == "sin_week":
                st.caption("⚠️ sin_week: seasonal encoding 0–1, peaks indicate mid-year weeks.")
            if feature == "cos_week":
                st.caption("⚠️ cos_week: seasonal encoding -1 to 1, peaks indicate mid-year weeks.")

        # Rolling numeric features
        else:
            ax.hist(df[feature].dropna(), bins=30, edgecolor="black")
            if unit:
                ax.set_xlabel(f"{display_name} ({unit})")
                ax.set_title(f"Distribution of {display_name} ({unit})")
            else:
                ax.set_xlabel(display_name)
                ax.set_title(f"Distribution of {display_name}")
            ax.set_ylabel("Frequency")
            st.caption(get_caption(feature))

        st.pyplot(fig)



# ========================================
#  TAB 4: ANOMALY DETECTION
# ========================================
elif page == "Anomaly Detection":
    st.title("🚨 Anomaly Detection (Historical Analysis)")

    st.markdown("""
    ### 🛡️Overview

    This tab helps identify **unusual or unexpected events** in the dataset.  
    Anomalies are detected automatically (`0 = normal`, `1 = anomaly`).  
    Understanding anomalies is valuable because they often point to:

    - sudden environmental shifts  
    - gear malfunctions or data-logging errors  
    - biological events (e.g., unusual migration patterns)  
    - unexpected changes in fishing activity  

    ---

    ## ⚠️ Variables *Not Suitable* for Anomaly Filtering  
    Some variables are **not meaningful** for selecting or interpreting anomalies.  
    We exclude them to keep analysis **real-world, interpretable, and safe**.

    ### 🚫 1. Rolling-window features  
    Examples:  
    - `Temp_2wk`, `SST_3wk`, `Catch_5wk`  

    **Why excluded:**  
    Rolling values smooth the data and distort real conditions.  
    Using them in sliders gives strange min/max ranges and masks true anomalies.

    ---

    ### 🚫 2. Interaction features (`_x_`)  
    Examples:  
    - `Temp_x_Depth`  
    - `Chl_x_Catch`  

    **Why excluded:**  
    These values come from multiplying two variables.  
    They have no physical meaning, huge ranges, and produce confusing sliders.  
    Real-world interpretation becomes impossible.

    ---

    ### 🚫 3. Engineered or categorical features  
    Examples:  
    - `Temp_bin`  
    - `CPUE_level`  
    - `sin_week`, `cos_week`

    **Why excluded:**  
    They are artificial labels or mathematical transformations,  
    not actual environmental measurements.

    ---

    ## ✅ Variables We *Do* Use for Filtering  
    These are **raw environmental or observational variables**, such as:

    - Sea Surface Temperature (SST)/Water Temperature  
    - Sea Surface Height (SSH)  
    - Chlorophyll-a  
    - Total Weekly Catch  
    - Depth  
    - Wind Speed  
    - Year / Month  

    **Why these matter:**  
    They represent real physical or biological conditions,  
    so filtering them lets us answer meaningful questions like:

    - “Do anomalies happen more in warmer waters?”  
    - “Are anomalies higher when catch spikes unexpectedly?”  
    - “Do anomalies cluster at certain times of year?”

    This makes anomaly detection useful and grounded in reality.
                
    ---

    ### 1️⃣ Anomaly Flag Summary
    Shows a quick overview of how many rows are normal vs anomalous using a bar chart.  
    **Real-world use:** Quickly gauge the overall health of our data. For example, if a lot of anomalies appear in catch data, there may be reporting issues, sensor errors, or environmental disruptions.

    ---

    ### 2️⃣ Train vs Test Anomaly Comparison
    Compares anomalies between the first half (Train) and second half (Test) of our dataset using a grouped bar chart.  
    **Real-world use:** Helps evaluate whether anomalies are evenly distributed across the dataset or concentrated in one period. Useful for model training and testing to avoid bias.

    ---

    ### 3️⃣ Anomalies Over Time
    Shows when anomalies occur over time using a 0/1 line chart.  
    **Real-world use:** Track **timing patterns** of unusual events. Even though values are just 0 (normal) and 1 (anomaly), spikes indicate when anomalies happened. This can reveal seasonal patterns, recurring problems, or sudden events that need attention.

    ---

    ### 4️⃣ Filter Anomalies by Environmental Variables
    Allows you to select a numeric variable (e.g., Year, Month, catch amount, temperature) and highlight rows above a threshold. Displays:
    - Total rows above threshold
    - Number of anomalies in that subset
    - Number of normal rows in that subset  

    **Real-world use:** Understand under what conditions anomalies occur. For example, we can see if anomalies happen during high temperature weeks, high catch volumes, or specific years. Helps prioritize investigation and contextualize anomalies.
    """)


    # Load dataset
    try:
        df = load_weekly_dataset()
    except FileNotFoundError:
        st.error("weekly_processed.csv not found. Run anomaly detection in the notebook first.")
        st.stop()


    # After loading df, determine usable raw features
    raw_features = [col for col in df.columns if is_raw_feature(col)]
    readable_options = [selectbox_box_readable_names(f) for f in raw_features]
    mapping = dict(zip(readable_options, raw_features))  # readable -> raw

    # 1️⃣ Restore raw variable from logbook
    saved_raw = st.session_state.get("selected_var")
    if saved_raw in raw_features:
        st.session_state.selected_var = saved_raw
    else:
        st.session_state.selected_var = raw_features[0] if raw_features else None

    # 2️⃣ Convert raw → readable for selectbox
    selected_readable = selectbox_box_readable_names(st.session_state.selected_var)



    # Summary of anomalies
    st.subheader("Anomaly Flag Summary")

    anom_summary = df['anomaly_flag'].value_counts().rename({0:'Normal', 1:'Anomaly'})
    st.bar_chart(anom_summary)

    st.write("Detailed counts:")
    st.dataframe(anom_summary.reset_index().rename(columns={'index':'Flag', 'anomaly_flag':'Count'}))


    # Train vs Test anomaly comparison
    st.subheader("Train vs Test Anomaly Comparison")

    # Ensure 'dataset' column exists
    if 'dataset' not in df.columns:
        st.info("Dataset column automatically generated (Train/Test split).")
        midpoint = len(df) // 2
        df['dataset'] = ['Train']*midpoint + ['Test']*(len(df)-midpoint)

    # Make 'dataset' categorical with Train first, then Test
    df['dataset'] = pd.Categorical(df['dataset'], categories=['Train', 'Test'], ordered=True)

    anom_counts = df.groupby(['dataset', 'anomaly_flag']).size().reset_index(name='Count')
    anom_counts['Flag'] = anom_counts['anomaly_flag'].map({0:'Normal', 1:'Anomaly'})

    fig2 = px.bar(
        anom_counts,
        x='dataset',
        y='Count',
        color='Flag',
        barmode='group',
        title="Anomalies by Dataset (Train vs Test)"
    )
    st.plotly_chart(fig2, width='stretch')


    # Anomalies over time
    st.subheader("Anomalies Over Time")
    # Try to find a date/week column automatically
    date_col = None
    for candidate in ["week", "Week", "date", "Date", "week_start", "WeekStart"]:
        if candidate in df.columns:
            date_col = candidate
            break

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        fig = px.line(
            df,
            x=date_col,
            y='anomaly_flag',
            title="Anomalies Over Time",
            labels={'anomaly_flag': 'Anomaly Flag', date_col: 'Date'},
            markers=True
        )

        st.plotly_chart(fig, width="stretch")
    else:
        st.warning("⚠️ No usable date/week column found — cannot plot anomalies over time.")


# Filter by environmental variable
    # Select only raw numeric variables for filtering
    env_cols = [
        c for c in df.columns
        if (df[c].dtype in ['float64', 'int64']) and is_raw_feature(c)
    ]

    if env_cols:
        st.subheader("Filter Anomalies by Environmental Conditions")

        # ---- Restore previous selection from session_state or default ----
        if "selected_var" not in st.session_state or st.session_state.selected_var not in env_cols:
            st.session_state.selected_var = env_cols[0]

        # Ensure threshold exists
        if "threshold" not in st.session_state or st.session_state.threshold is None:
            st.session_state.threshold = float(df[st.session_state.selected_var].mean())

        # ---- Build readable selectbox ----
        readable_options = [selectbox_box_readable_names(c) for c in env_cols]
        mapping = dict(zip(readable_options, env_cols))

        # Convert stored selection to readable for selectbox index
        current_readable = selectbox_box_readable_names(st.session_state.selected_var)

        selected_readable = st.selectbox(
            "Select a variable",
            readable_options,
            index=readable_options.index(selected_readable) if selected_readable in readable_options else 0,
        )


       # 4️⃣ Update raw variable after selectbox selection
        st.session_state.selected_var = mapping[selected_readable]
        selected_var = st.session_state.selected_var

        # Data for selected variable
        var_data = df[selected_var]

        # ---- Reset threshold ONLY when variable changes AND not in edit mode ----
        last_var = st.session_state.get("last_selected_var")

        if not st.session_state.get("anomaly_edit_mode", False):  
            if selected_var != last_var:
                st.session_state.threshold = float(var_data.mean())

        # Update last selected variable
        st.session_state.last_selected_var = selected_var

        # ---- Slider setup ----
        slider_min = float(var_data.min())
        slider_max = float(var_data.max())
        unit = get_unit(selected_var)

        slider_value = st.session_state.threshold

        # Integer-type slider
        if (
            pd.api.types.is_integer_dtype(var_data)
            or selected_var.lower() in ["year", "month", "day", "weekofyear"]
        ):
            new_threshold = st.slider(
                "Highlight values above",
                int(slider_min),
                int(slider_max),
                value=int(slider_value),
                step=1,
                key=f"slider_threshold_{selected_var}"
            )
        # Float slider
        else:
            new_threshold = st.slider(
                "Highlight values above",
                slider_min,
                slider_max,
                value=float(slider_value),
                step=0.01,
                key=f"slider_threshold_{selected_var}"
            )

        # Update threshold AFTER slider renders
        st.session_state.threshold = new_threshold

        # IMPORTANT: Turn off edit mode once UI is rebuilt
        st.session_state.anomaly_edit_mode = False


        # ---- Filter dataframe ----
        filtered_df = df[df[selected_var] > st.session_state.threshold]
        num_rows = len(filtered_df)
        num_anomalies = filtered_df['anomaly_flag'].sum()
        num_normal = num_rows - num_anomalies

      
        # Format threshold display based on variable type
        threshold = st.session_state.threshold
        if selected_var.lower() in ["year", "month", "day", "weekofyear"]:
            threshold_str = f"{int(threshold)}"
        else:
            threshold_str = f"{threshold:.2f}"


        # ---- Display current threshold ----
       # Only show unit if it's not empty
        threshold = st.session_state.threshold

        if selected_var.lower() in ["year", "day", "weekofyear"]:
            threshold_str = f"{int(threshold)}"
        elif selected_var.lower() == "month":
            month_num = int(threshold)
            # Get month name safely, fallback to empty string if out of range
            month_name = calendar.month_name[month_num] if 1 <= month_num <= 12 else ""
            threshold_str = f"{month_num} ({month_name})"
        else:
            threshold_str = f"{threshold:.2f}"

        st.markdown(
            f"<span style='font-size:0.875rem;'>Current threshold: {threshold_str}</span>",
            unsafe_allow_html=True
        )

        st.info(
            f"""
        ### 📊 Filter Summary  
        **Variable:** `{selected_var}`  
        **Threshold:** `{threshold_str}`  

        - Total rows above threshold: **{num_rows}**  
        - Anomalies: **{num_anomalies}**  
        - Normal rows: **{num_normal}**
        """
        )

    # ---- Safe column detection for display ----
    date_col = None
    for candidate in ["week", "Week", "WeekStart", "week_start", "date"]:
        if candidate in df.columns:
            date_col = candidate
            break

    cols_to_show = [selected_var, "anomaly_flag", "dataset"]
    if date_col:
        cols_to_show.insert(0, date_col)

    st.dataframe(filtered_df[cols_to_show])



# ========================================
#  TAB 5: MODEL EVALUATION
# ========================================
elif page == "Model Evaluation":
    import json
    BASE_DIR = Path(__file__).parent  # App/AutoML

    st.title("📊 Model Evaluation")

    st.markdown("""
    This page displays the performance of our trained  
    **classification** and **regression** models.
    """)

    st.header("🔵 Classification Evaluation")

    # ---- Confusion Matrix ----
    conf_matrix_path = BASE_DIR / "figures" / "classification_confusion_matrix.png"
    st.subheader("Confusion Matrix")
    st.image(conf_matrix_path)

    # Convert text report to a DataFrame
    def report_to_df(report_text):
        """
        Converts sklearn classification_report text to pandas DataFrame safely.
        Works even if labels have spaces.
        """
        lines = report_text.strip().split("\n")
        lines = [line for line in lines if line.strip()]

        rows = []
        headers = ["class", "precision", "recall", "f1-score", "support"]

        for line in lines[1:]:  # skip header
            tokens = line.split()
            if len(tokens) < 2:
                continue

            # Find where numeric metrics start
            for i, tok in enumerate(tokens):
                try:
                    float(tok)
                    start_idx = i
                    break
                except ValueError:
                    continue

            label = " ".join(tokens[:start_idx])
            metrics_tokens = tokens[start_idx:]

            # Convert metrics to float if possible
            metrics = []
            for x in metrics_tokens:
                try:
                    metrics.append(float(x))
                except ValueError:
                    metrics.append(x)

            rows.append([label] + metrics)

        df = pd.DataFrame(rows, columns=headers)
        return df

    # Classification report
    st.subheader("Classification Report")
    report_path = BASE_DIR / "reports" / "classification_report.txt"
    with open(report_path, "r") as f:
        report_text = f.read()


    df_class_report = report_to_df(report_text)
    st.dataframe(df_class_report)

    st.header("🟢 Regression Evaluation")

    # Load regression metrics
    reg_metrics_path = BASE_DIR / "reports" / "regression_metrics.json"
    with open(reg_metrics_path, "r") as f:
        reg_metrics = json.load(f)

    def round_metrics(metrics, decimals=2):
        if isinstance(metrics, dict):
            return {k: round_metrics(v, decimals) for k, v in metrics.items()}
        elif isinstance(metrics, float):
            return round(metrics, decimals)
        else:
            return metrics

    st.subheader("Overall Regression Metrics")
    st.json(round_metrics(reg_metrics))

    # Plot per group
    for grp in ["Low", "Medium", "High"]:

        scatter_path = BASE_DIR / "figures" / f"regression_scatter_{grp}.png"
        residual_path = BASE_DIR / "figures" / f"regression_residuals_{grp}.png"
        
        st.subheader(f"Regression Fit — {grp}")
        st.image(scatter_path)

        st.subheader(f"Residual Plot — {grp}")
        st.image(residual_path)



# ========================================
#  TAB 6: CLASSSIFICATION
# ========================================

elif page == "Classification":

    tab_extra_params = {
        "week_index": st.session_state.get("week_index", 1)
    }

    st.title("🎯 CPUE Level Classification")


    # Load models and data
    models = load_all_models()
    df = load_weekly_dataset()

    st.markdown("Predict whether next week's CPUE is Low, Medium, or High.")


    # Select week to predict
    week_index_user = st.session_state["week_index"]  # user-facing week (1-based)
    week_index = week_index_user - 1                 # 0-based for DataFrame

    st.info(f"Using week {week_index_user} selected from the sidebar.")

    row = build_feature_row(df, week_index)


    # Reset index to ensure proper DataFrame
    if isinstance(row, pd.Series):
        row = row.to_frame().T
    row = row.reset_index(drop=True)

    st.subheader("Input Features (raw)")
    st.dataframe(row)


    # Make predictions
    preds = {}

    for key, label in zip(
        ["clf_top1", "clf_top2", "clf_top3"],
        ["Top 1 Classifier", "Top 2 Classifier", "Top 3 Classifier"]
    ):
        # Get model's expected features, excluding CPUE_level
        required_features = [f for f in models[key].feature_names_in_ if f != "CPUE_level"]

        # Build a safe row containing only required features
        row_model_ordered = pd.DataFrame({f: row[f] if f in row.columns else 0 for f in required_features}, index=[0])

        # Predict
        preds[label] = models[key].predict(row_model_ordered)[0]


    # Display Predicted CPUE Levels
    st.subheader("Predicted CPUE Level")

    # Optionally include a short description for each level
    cpue_text = {
        "Low": "Low CPUE – few catches expected.",
        "Medium": "Medium CPUE – moderate catches expected.",
        "High": "High CPUE – strong catch expected."
    }

    # Display each classifier's prediction with description
    for model_name, prediction in preds.items():
        st.write(f"**{model_name}:** {prediction} – {cpue_text.get(prediction, '')}")



    # Interpretation Section
    week_label = f"Week {week_index_user}"

    if all(p == "High" for p in preds.values()):
        st.subheader(f"{week_label}: High CPUE Predicted")
        st.write(f"""
        All classifiers predict **HIGH CPUE** for {week_label}. 
        This means the week is expected to have a high catch per unit effort.
        
        **Recommended actions for fisheries managers and officials:**
        - **Allocate additional fishing vessels** to areas likely to have dense squid populations.
        - **Ensure sufficient storage and processing capacity** at ports to handle higher catches.
        - **Coordinate with market and distribution channels** to avoid oversupply issues.
        - **Monitor environmental conditions** closely, as high CPUE weeks can be sensitive to weather or currents.

        > Note: The week number corresponds to the actual week being predicted. Models use historical trends and environmental features leading up to this week to forecast CPUE.
        """)

    elif all(p == "Low" for p in preds.values()):
        st.subheader(f"{week_label}: Low CPUE Predicted")
        st.write(f"""
        All classifiers predict **LOW CPUE** for {week_label}. 
        This indicates a lower expected catch per unit effort.

        **Recommended actions for fisheries managers and officials:**
        - **Consider reducing fishing effort** to avoid wasted fuel and labor.
        - **Focus on conservation measures**, such as temporary protected zones or reduced quotas.
        - **Monitor critical habitats and squid populations** to ensure sustainable fishing.
        - **Plan maintenance and training activities** for fishing fleets during low CPUE periods.

        > Note: The week number corresponds to the actual week being predicted. Models use historical trends and environmental features leading up to this week to forecast CPUE.
        """)

    else:
        st.subheader(f"{week_label}: Mixed CPUE Predictions")
        st.write(f"""
        The classifiers have **mixed predictions** for {week_label}. 
        Some models predict high CPUE while others predict low or medium.

        **Recommended actions:**
        - **Prepare for variability:** Deploy a moderate fishing effort.
        - **Monitor CPUE daily** to adjust operations as more information becomes available.
        - **Focus on flexible resource allocation**, such as movable fleets or dynamic port operations.
        - **Document environmental conditions** to improve future predictions.
        
        > Note: The week number corresponds to the actual week being predicted. Models use historical trends and environmental features leading up to this week to forecast CPUE.
        """)



# ========================================
#  TAB 7: REGRESSION
# ========================================
elif page == "Regression":

    tab_extra_params = {
        "week_index": st.session_state.get("week_index", 1)
    }

    st.title("📈 CPUE Regression (Continuous Prediction)")


    # Caution about model accuracy
    st.warning(
        """
        ⚠️ **Important:** Predictions from these models are **not highly accurate**, especially for extreme CPUE weeks. 
        Use them as a **general guide only**, not for precise operational decisions.
        """
    )


    # Load models and data
    models = load_all_models()
    df = load_weekly_dataset()

    st.markdown("""
    Predict **continuous CPUE** using the three bin-specific regression models.
    """)


    # Select week to predict
    week_index_user = st.session_state["week_index"]  # user-facing week (1-based)
    week_index = week_index_user - 1                 # 0-based for DataFrame

    st.info(f"Using week {week_index_user} selected from the sidebar.")

    row = build_feature_row(df, week_index)


    # Ensure row is a DataFrame
    if isinstance(row, pd.Series):
        row = row.to_frame().T
    row = row.reset_index(drop=True)

    st.subheader("Input Features (raw)")
    st.dataframe(row)

  
    # Step 1: Predict Regression Bin
    clf = models["clf_top1"]
    
    # Align features for classifier
    clf_features = [f for f in clf.feature_names_in_ if f != "CPUE_level"]
    row_clf = pd.DataFrame({f: row[f] if f in row.columns else 0 for f in clf_features}, index=[0])

    bin_pred = clf.predict(row_clf)[0]

    # Bin display with abundance description
    bin_text = {
        "Low": "Low CPUE (low abundance)",
        "Medium": "Medium CPUE (moderate abundance)",
        "High": "High CPUE (High abundance)"
    }
    st.subheader(f"Selected Regression Bin: **{bin_text.get(bin_pred, bin_pred)}**")


    # Step 2: Select appropriate regression model
    regressor = {
        "Low": models["reg_low"],
        "Medium": models["reg_med"],
        "High": models["reg_high"],
    }[bin_pred]

    # Align features for regressor, excluding target
    reg_features = [f for f in regressor.feature_names_in_ if f != "CPUE_log1p"]
    row_reg = pd.DataFrame({f: row[f] if f in row.columns else 0 for f in reg_features}, index=[0])

    # Ensure numeric types
    row_reg = row_reg.apply(pd.to_numeric, errors='coerce').fillna(0)

  
    # Step 3: Predict CPUE
    cpue_pred_log = regressor.predict(row_reg)[0]        # PyCaret returns log1p
    cpue_pred_kg = np.expm1(cpue_pred_log)              # inverse of log1p

    # Convert to tons
    cpue_pred_tons = cpue_pred_kg / 1000

    # Color logic: abundance-based
    bin_colors = {
        "Low": "red",      # scarce, caution
        "Medium": "orange",
        "High": "green"    # abundant, good catch
    }

    # Display CPUE with color
    st.subheader("Predicted CPUE")
    st.markdown(
        f"<span style='color:{bin_colors[bin_pred]}; font-size:24px; font-weight:bold;'>"
        f"{cpue_pred_kg:,.0f} kg ({cpue_pred_tons:.1f} tons)"
        f"</span>", 
        unsafe_allow_html=True
    )

  
    # Step 4: Expert Advice / Interpretation
    st.markdown("---")
    st.subheader("💡 Interpretation & Advice")
    st.markdown(f"""
    - These CPUE predictions indicate **estimated catch per unit effort** for the selected week.  
    - Use **CPUE bins** as a rough guide:  
        - **Low CPUE (red)** → Fish abundance is low. Be cautious with fishing effort.  
        - **Medium CPUE (orange)** → Moderate catch expected; plan accordingly.  
        - **High CPUE (green)** → High abundance; potential for good catch, but verify with field observations.  
    - **Caution:** Predictions are **not highly reliable**, especially for extreme weeks (very high or very low CPUE). Models tend to underperform in these scenarios.  
    - **Practical use:** If predictions were accurate, experts would need to:
        - Adjust fishing effort or quotas.  
        - Plan supply chain/logistics based on expected catch.  
        - Monitor trends over multiple weeks to detect anomalies.  
    - Always **cross-check with field surveys** and historical trends before making operational decisions.
    """)



# ========================================
#  TAB 8: PREDICT SCENARIOS
# ========================================
elif page == "Predict Scenarios":

        # Initialize session state
    if "params" not in st.session_state:
        st.session_state["params"] = {}
    params = st.session_state["params"]


    # 1. Use the globally selected week
   # Ensure week exists
    week_index_user = st.session_state.get("week_index", 1)  # 1-based
    params["week_index"] = week_index_user
    week_index = week_index_user - 1  # 0-based for DataFrame

    st.info(f"Using week {week_index_user} selected from the sidebar.")


    st.title("🧪 Scenario Simulation")
    st.markdown("""
    Adjust environmental variables to see how CPUE would change.
    The baseline CPUE and regime are determined **automatically** from the selected week.
    """)

    # Load models & data
    df = load_weekly_dataset()
    models = load_all_models()

    row = build_feature_row(df, week_index)

    if isinstance(row, pd.Series):
        row = row.to_frame().T
    row = row.reset_index(drop=True)


    # 2. Predict baseline classification
    clf = models["clf_top1"]
    clf_features = [f for f in clf.feature_names_in_ if f != "CPUE_level"]
    row_clf = pd.DataFrame({f: row[f] if f in row.columns else 0 for f in clf_features}, index=[0])
    baseline_bin = clf.predict(row_clf)[0]

    st.subheader("Baseline CPUE Regime")
    st.write(f"**{baseline_bin} CPUE** predicted for week {week_index_user}.")

  
    # 3. Predict baseline CPUE (continuous)
    regressor = {
        "Low": models["reg_low"],
        "Medium": models["reg_med"],
        "High": models["reg_high"],
    }[baseline_bin]

    reg_features = [f for f in regressor.feature_names_in_ if f != "CPUE_log1p"]
    row_reg = pd.DataFrame({f: row[f] if f in row.columns else 0 for f in reg_features}, index=[0])
    
    cpue_log_base = regressor.predict(row_reg)[0]
    cpue_base_kg = np.expm1(cpue_log_base)
    cpue_base_tons = cpue_base_kg / 1000

    st.metric("Baseline CPUE", f"{cpue_base_kg:,.0f} kg ({cpue_base_tons:.1f} tons)")


    #  Building Clean Dictionary For Saving
    environmental_vars = {
        "Temperature (°C)": float(params.get("delta_T") or 0.0),
        "Chlorophyll a (mg/m³)": float(params.get("delta_Chlor_a") or 0.0),
        "Depth (m)": float(params.get("depth") or 0.0),  # Always include
    }

    # Include SSH only if Medium CPUE and nonzero
    if params.get("medium_cpue", False):
        ssh_val = float(params.get("delta_SSH") or 0.0)
        environmental_vars["Sea Surface Height (m)"] = ssh_val

    # 4. User-adjustable environmental sliders
    st.subheader("Adjust Environmental Variables")

    params = st.session_state.params
    # --- FIXED SLIDER INITIALIZATION ---
    params = st.session_state.params

    temp_init  = float(params.get("delta_T", 0.0))
    chlor_init = float(params.get("delta_Chlor_a", 0.0))

    # Prevent None from ever reaching Streamlit sliders
    depth_init = float(params.get("depth") or 0.0)
    ssh_init   = float(params.get("delta_SSH") or 0.0)

    # Save baseline & modified values in params
    params["Baseline_Regime"] = baseline_bin
    params["Baseline_CPUE"] = float(cpue_base_kg)
    params["medium_cpue"] = (baseline_bin == "Medium")



    # Build sliders with correct initial values
    deltas = {}
    deltas["temp"] = st.slider("Δ Sea Surface Temperature (SST) (°C)", -3.0, 3.0, float(temp_init), help="Change in sea surface temperature for the selected week (Originally refered to as Water Temperature in dataset)")
    deltas["depth"] = st.slider("Δ Depth (m)", -50.0, 50.0, float(depth_init), help="Change in water column depth for the selected week")
    deltas["chlor"] = st.slider("Δ Chlorophyll-a (mg/m³)", -1.0, 1.0, float(chlor_init), help="Change in chlorophyll-a concentration for the selected week")

    if baseline_bin == "Medium":
        deltas["ssh"] = st.slider("Δ Sea Surface Height (SSH) (m)", -0.05, 0.05, ssh_init, help="Change in sea surface height for the selected week")

    # Always save updated values back to params
    params["delta_T"] = deltas["temp"]
    params["depth"] = deltas["depth"]
    params["delta_Chlor_a"] = deltas["chlor"]
    if "ssh" in deltas:
        params["delta_SSH"] = deltas["ssh"]


    # IMPORTANT: Turn off edit mode once UI is rebuilt
    st.session_state.pred_scen_edit_mode = False
   
    # 5. Apply modifications using helper function
    row_mod = apply_modifications(row.iloc[0], deltas, baseline_bin)

    # Prepare row for regression model
    row_mod_reg = prepare_row_for_model(row_mod, reg_features)

    # Predict modified CPUE
    cpue_log_mod = regressor.predict(row_mod_reg)[0]
    cpue_mod_kg = np.expm1(cpue_log_mod)
    cpue_mod_tons = cpue_mod_kg / 1000

    params["Modified_CPUE"] = float(cpue_mod_kg)


    # --- Prepare save dictionary AFTER computing modified CPUE ---
    tab_extra_params = {
        "Week": params.get("week_index", "N/A"),

        # NEW correctly-added values
        "Baseline_Regime": baseline_bin,
        "Baseline_CPUE": float(cpue_base_kg),
        "Modified_CPUE": float(cpue_mod_kg),

        # Existing (correct)
        "Environmental": environmental_vars,
        "Environmental_Display": ",  ".join(
            f"{k}: {v}" for k, v in environmental_vars.items()
        ),

        # Internal environmental parameters for edit mode
        "Environmental_Internal": {
            "delta_T": params.get("delta_T", 0.0),
            "delta_Chlor_a": params.get("delta_Chlor_a", 0.0),
            "depth": params.get("depth", 0.0),
            "delta_SSH": params.get("delta_SSH", 0.0),
            "medium_cpue": (baseline_bin == "Medium")
        }
    }


    # 6. Display comparison
    st.subheader("Scenario Result")

    delta_kg = cpue_mod_kg - cpue_base_kg
    # Determine delta display
    if delta_kg > 0:
        delta_str = f"+{delta_kg:,.0f} kg"
        delta_color = "normal"
    elif delta_kg < 0:
        delta_str = f"{delta_kg:,.0f} kg"
        delta_color = "normal"
    else:
        delta_str = None
        delta_color = "off"

    st.metric(
        label="Modified CPUE",
        value=f"{cpue_mod_kg:,.0f} kg ({cpue_mod_tons:.1f} tons)",
        delta=delta_str,
        delta_color=delta_color
    )

    if delta_str is None:
        st.markdown("**No change in CPUE**")


    # 7. Dynamic Insights / Interpretation
    st.subheader("💡 Scenario Insights")

    # Map internal variable names to full names + units
    var_labels_units = {
        "temp": ("Sea Surface Temperature (SST)", "°C"),
        "depth": ("Depth", "m"),
        "chlor": ("Chlorophyll-a", "mg/m³"),
        "ssh": ("Sea Surface Height (SSH)", "m")
    }

    # Build a list of readable environmental changes
    env_changes = []


    for var, change in deltas.items():
        if abs(change) > 1e-9:    # avoid floating tiny noise
            direction = "increases" if change > 0 else "decreases"
            name, unit = var_labels_units[var]
            env_changes.append(f"- **{name}**: {direction} by {abs(change):.2f} {unit}")

    if not env_changes:
        env_changes_text = "_No environmental changes applied._"
    else:
        env_changes_text = "\n".join(env_changes)


    # Determine CPUE trend
    if delta_kg > 0:
        trend = "increase"
    elif delta_kg < 0:
        trend = "decrease"
    else:
        trend = "no change"

    # Display dynamic interpretation
    if trend == "no change":
        cpue_impact_text = (
            f"CPUE remains unchanged at {cpue_base_kg:,.0f} kg "
            f"({cpue_base_tons:.1f} tons)."
        )
    else:
        cpue_impact_text = (
            f"**Given our current environmental variables, if:**  \n"
            f"{env_changes_text}  \n\n"
            f"A projected **{trend}** in CPUE of {abs(delta_kg):,.0f} kg,  \n"
            f"from our baseline of {cpue_base_kg:,.0f} kg ({cpue_base_tons:.1f} tons)  \n"
            f"is expected, resulting in a modified CPUE of  \n"
            f"**{cpue_mod_kg:,.0f} kg ({cpue_mod_tons:.1f} tons).**"
        )

    # Display
    st.markdown(cpue_impact_text)

# ---------------- Toast Reminder for Notes ----------------
if page != "Logbook":
    toast_key = f"toast_shown_{page}"

    # Initialize the flag if it doesn't exist yet
    if toast_key not in st.session_state:
        st.session_state[toast_key] = False

    # Show toast if it hasn't been shown yet for this tab click
    if not st.session_state[toast_key]:
        st.toast(
            "💡Take a moment to capture your observations or interpretations in the sidebar notes panel!🙂 " 
            " When you're done, Click Save to store them in the Log Book tab",
            duration=7  # 7 seconds
        )
        st.session_state[toast_key] = True  # mark as shown for this visit


# ---------------- Standard Library ----------------
import base64
import io
import json
import time
from datetime import datetime

# ---------------- Third-Party Libraries ----------------
import gspread
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.oauth2.service_account import Credentials
from PIL import Image
from pathlib import Path

# ---------------- Local/Project Imports ----------------
from utils.data_utils import (
    load_model_data,
    get_model_colors,
    load_prediction_data,
    load_residual_data,
    load_monthly_cpue,
    load_observed_vs_standardized
)

@st.cache_resource
def get_monthly_cpue_plot(df):
    fig = px.line(
        df,
        x="Month",
        y="CPUE_vday_tons",
        color="Year",
        title="Fleet-Aggregated CPUE per Vessel-Day"
    )
    fig.update_layout(width=900, height=600)
    return fig

# ---------------------- Page Configuration ----------------------
st.set_page_config(page_title="Course Correction", layout="wide")


# ---------------------- Custom CSS ----------------------
st.markdown("""
<style>

/* ---------------------- Sidebar ---------------------- */
[data-testid="stSidebar"] > div:first-child {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: inherit;
    overflow-y: auto;        /* allows scrolling */
    min-height: 100vh;
    padding-top: 1rem !important;
    color: #E1EAF2;
    
    /* Combine background image + overlay so it scrolls with content */
    background:
        linear-gradient(rgba(0, 31, 63, 0.6), rgba(0, 31, 63, 0.6)),
        url("https://thumbs.dreamstime.com/b/underwater-seascape-ocean-coral-reef-deep-sea-bottom-swimming-under-water-marine-corals-background-vector-seaweed-algae-354608779.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

/* Ensure sidebar content is above overlay */
[data-testid="stSidebar"] > div:first-child > * {
    position: relative;
    z-index: 1;
}
lor: rgba(0, 31, 63, 0.6);
    z-index: 0;
}

/* Sidebar titles and headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #39FF14 !important;
    margin-top: 4px !important;
}

/* Sidebar 'Tabs' section header */
[data-testid="stSidebar"] [data-testid="stRadioGroupLabel"] p {
    font-size: 25px !important;
    font-weight: 800 !important;
    color: #FFD700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-align: center !important;
    margin-bottom: 10px !important;
}

/* Each sidebar radio button (tab option) */
[data-testid="stSidebar"] [data-baseweb="radio"] label div p {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #E1EAF2 !important;
    line-height: 1.6 !important;
}

/* Each radio option (“Overview”, etc.) */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #E1EAF2 !important;
}

/* Sidebar links */
[data-testid="stSidebar"] a {
    font-size: 20px !important;
    color: #39FF14 !important;
}

/* Sidebar footer */
.sidebar-footer {
    position: absolute;
    bottom: 10px;
    width: 100%;
    padding: 10px;
}
            
/* Make the sidebar background extend the full height */
section[data-testid="stSidebar"] {
    min-height: 100vh !important;
}

/* Optional: adjust padding for expanders inside sidebar */
section[data-testid="stSidebar"] .st-expander {
    margin-bottom: 1rem;
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

.block-container {
    overflow-y: auto !important;
    height: 100vh !important;
    padding-top: 4rem !important;
    padding-bottom: 2rem !important;

    /* Slightly more space on left and right */
    padding-left: 5rem !important;  /* increased from 2rem */
    padding-right: 2rem !important;

    margin-top: 0 !important;
    margin-bottom: 0 !important;
    max-width: 100% !important;
}

/* ---------------------- Sidebar + Main Layout Fix ---------------------- */

/* Sidebar width */
[data-testid="stSidebar"] > div:first-child {
    width: 370px !important;
    min-width: 370px !important;
}

/* Remove default spacing from Streamlit wrappers */
div[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    padding: 0 !important;
    margin: 0 !important;
}

/* Force main content to start exactly at sidebar edge */
div[data-testid="stAppViewContainer"] > div:nth-child(2) {
    margin-left: 370px !important; /* match sidebar width */
    padding-left: 0 !important;
    margin-top: 0 !important;
    transition: margin-left 0.3s ease-in-out;
}

/* Ensure Streamlit’s block container doesn’t add spacing */
.block-container {
    margin: 0 !important;
    padding: 2rem 3rem !important;
    max-width: 100% !important;
    overflow-y: auto !important;
    height: 100vh !important;
}

/* Collapsed sidebar behavior */
@media (max-width: 992px) {
    div[data-testid="stAppViewContainer"] > div:nth-child(2) {
        margin-left: 0 !important;
    }
}

/* Optional thin divider for visual clarity */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(57, 255, 20, 0.3);
}


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

/* ---------------------- Top bar ---------------------- */
header, .css-nahz7x {
    background-color: #001f3f !important;
}
            
/* ---------------------- 🧭 Fix Top Bar Alignment (Streamlit 1.51+) ---------------------- */

/* Keep the top bar visible and consistent */
header[data-testid="stHeader"] {
    background-color: #001f3f !important;
    height: 3.5rem !important;
    z-index: 1000 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
}

/* Sidebar should start just below the fixed top bar */
[data-testid="stSidebar"] {
    position: fixed !important;
    top: 3.5rem !important;      /* push it down below header */
    height: calc(100vh - 3.5rem) !important;
    margin: 0 !important;
}

/* Sidebar inner div scrolls normally */
[data-testid="stSidebar"] > div:first-child {
    height: 100% !important;
    overflow-y: auto !important;
}

/* Main app container shifts down equally */
div[data-testid="stAppViewContainer"] {
    margin-top: 3.5rem !important;   /* align with sidebar */
    padding-top: 0 !important;
}

/* The block container keeps its scroll and padding */
.block-container {
    height: calc(100vh - 3.5rem) !important;
    overflow-y: auto !important;
}

/* ---------------------- Buttons ---------------------- */
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
</style>
""", unsafe_allow_html=True)


# ---------------------- Sidebar Navigation ----------------------
st.sidebar.title(" 🧭 Course Correction")

tabs = [
    "Overview",
    "Model Comparison",
    "Evaluation Metrics",
    "Residual Analysis",
    "Predictions",
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


# ---------------- Initialize Session State ----------------

if "page" not in st.session_state:
    st.session_state.page = tabs[0]  # default to first tab

if "notes" not in st.session_state:
    st.session_state.notes = {tab: [] for tab in tabs if tab != "Logbook"}

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

# ---------------- Toast Message Handler ----------------
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
    "Select page",
    available_tabs,
    index=selected_index,
    key="page",
    disabled=disabled_radio
)

# Optional warning
if st.session_state.edit_mode["active"]:
    st.warning("⚠️ You are editing a reloaded note. You must save before switching tabs.")


# Keep notes panel expander open if typing or editing
st.session_state.notes_expanded = bool(st.session_state.note_input.strip()) or st.session_state.edit_mode["active"]


# 🔹 Keep expander open if user is editing or typing
st.session_state.notes_expanded = (
    bool(st.session_state.note_input.strip())
    or st.session_state.edit_mode["active"]
    or st.session_state.auto_expand_notes
)

# ---------------- Helper Functions ----------------
def format_note_display(note, tab_name):
    # Format inputs nicely
    inputs = note.get("inputs", {})
    input_text = ", ".join(f"{k}: {v}" for k, v in inputs.items() if v is not None) or "N/A"
    
    timestamp = note.get("timestamp")
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown time"
    
    content = note.get("notes", "")
    
    formatted = (
        f"🕒 {timestamp_str} 📍 Source: {tab_name} 🔧 Snapshot Inputs: {input_text}\n"
        f"🗒️ Notes: {content}\n\n"
        f"{'-'*50}\n\n"
    )
    return formatted

# New structure for each note
new_entry = {
    "timestamp": datetime.now(),
    "inputs": {
        "some_input_1": st.session_state.get("some_input_1"),
        "some_input_2": st.session_state.get("some_input_2"),
        # Add any other controls from that tab here
    },
    "notes": st.session_state.note_input.strip()
}


# ---------------- Notes Panel ----------------
if page != "Logbook":
    with st.sidebar:
        # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("### 🗒️ Notes Panel")
        with st.expander(
            f"💬 Notes for {page}",
            expanded=st.session_state.notes_expanded
        ):
            st.session_state.auto_expand_notes = False
            note_text = st.text_area(
                "Write your note here:",
                key="note_input",
                height=150,
                placeholder="Type your note..."
            )

            # 💾 Save Button
            if st.button("💾 Save Note", key=f"save_{page}"):
                content = st.session_state.note_input.strip()
                if content:
                    # If editing an existing note
                    if st.session_state.edit_mode["active"] and st.session_state.edit_mode["tab"] == page:
                        idx = st.session_state.edit_mode["index"]
                        st.session_state.notes[page][idx]["notes"] = content #st.session_state.note_input.strip()
                        st.session_state.notes[page][idx]["inputs"] = {
                            "some_input_1": st.session_state.get("some_input_1"),
                            "some_input_2": st.session_state.get("some_input_2"),
                        }
                        st.session_state.toast_message = f"✏️ Note updated in {page}!"
                        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
                    else:
                        new_entry = {
                            "timestamp": datetime.now(),
                            "inputs": {
                                "some_input_1": st.session_state.get("some_input_1"),
                                "some_input_2": st.session_state.get("some_input_2"),
                            },
                            "notes": content
                        }
                        st.session_state.notes[page].append(new_entry)
                        st.session_state.toast_message = f"✅ 📸 Note saved to Logbook!"
                    # Force UI update after save
                    st.rerun()
                else:
                    st.session_state.toast_message = "⚠️ Nothing to save (note is empty)."

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

            with st.expander(f"🗂 {tab_name} ({len(notes)} notes)", expanded=False):
                for i, note in enumerate(notes):
                    col1, col2, col3 = st.columns([6, 1, 1])

                    with col1:
                        st.markdown(format_note_display(note, tab_name))


                    with col2:
                        # ✏️ Edit button
                            #edit_note_button(tab_name, i, note)
                        if st.button("✏️", key=f"edit_{tab_name}_{i}"):
                            entry = st.session_state.notes[tab_name][i]

                            #Restore note text
                            st.session_state.note_input = entry["notes"]

                            # Restore tab inputs from snapshot
                            for k, v in entry["inputs"].items():
                                st.session_state[k] = v

                            st.session_state.edit_mode = {
                                "active": True,
                                "tab": tab_name,
                                "index": i,
                            }
                            st.session_state.toast_message = f"📸 Snapshot reloaded for {tab_name}. You can now edit your note."
                            st.session_state.auto_expand_notes = True
                            st.rerun()  # <- this triggers immediate rerun with updated session_state

                    with col3:
                        # 🗑 Delete button
                        delete_key = f"{tab_name}_{i}"
                        if not st.session_state.delete_confirm.get(delete_key, False):
                            if st.button("🗑", key=f"delete_{tab_name}_{i}"):
                                st.session_state.delete_confirm[delete_key] = True
                                st.rerun()  # immediately show confirm buttons
                        else:
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("✅", key=f"confirm_del_{tab_name}_{i}"):
                                    del st.session_state.notes[tab_name][i]
                                    st.session_state.delete_confirm.pop(delete_key, None)
                                    st.session_state.toast_message = f"🗑 Deleted note {i+1} from {tab_name}"
                                    st.rerun()  # immediately delete      
                            with c2:
                                if st.button("❌", key=f"cancel_del_{tab_name}_{i}"):
                                    st.session_state.delete_confirm[delete_key] = False
                                    st.rerun()  # immediately decline


    

    # 🧾 Final Observation Section
    st.subheader("🧾 Final Observation")
    if "final_observation" not in st.session_state:
        st.session_state.final_observation = ""

    st.session_state.final_observation = st.text_area(
        "Write your final observation here:",
        value=st.session_state.final_observation,
        height=150,
        placeholder="Summarize your findings or conclusions..."
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
            # Use the same formatting as for Google Sheets
                    all_notes_text += format_note_display(note, tab)
                all_notes_text += "\n"

        st.session_state.all_notes_text = all_notes_text
        st.success("✅ Logbook is ready to download!")

    # --- Step 2: Show download button only if content exists ---
    if "all_notes_text" in st.session_state and st.session_state.all_notes_text:
        buffer = io.BytesIO(st.session_state.all_notes_text.encode("utf-8"))

         # Current datetime string
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"logbook_{timestamp}.txt"

        st.download_button(
            label="📥 Download Logbook (.txt)",
            data=buffer,
            file_name=file_name,
            mime="text/plain",
            key="logbook_download"
        )

    # 📤 Send to Host Section (appears after download)
    
    # --- Define the function ---
    def send_notes_to_host(all_notes_text, tab_name="course_correction"):
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
                    success = send_notes_to_host(all_notes_text)

            if success:
                st.success("✅ Upload to Google Sheets successful! Your notes were sent anonymously. Thank you!")
            else:
                st.error("❌ Failed to send notes. Please try again later.")

# 🔹 Link to next app: Ocean Dynamics (Biomass Estimation)
   OCEAN_DYNAMICS_URL = "https://squidstock-course-correction.streamlit.app"

st.markdown(
    """
    <div style="
        background-color: rgba(10, 47, 68, 0.7);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        color: #FFD700;
        margin-top: 2rem;
    ">
        <div style="font-size:16px; font-weight:600; margin-bottom:0.4rem;">
            🐙 Next Stage:
        </div>
        <div style="font-size:18px; font-weight:500;">
            Ocean Dynamics – Let's extend this analysis into physical ocean drivers and climate signals.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
# 🔹 Centered "Coming Soon" button (functional version)
    st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)

    if st.button("🌊 Visit Ocean Dynamics"):
    st.markdown(
        f"""
        <meta http-equiv="refresh" content="0; url={OCEAN_DYNAMICS_URL}">
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

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

# ---------------------- Data Loaders ----------------------
model_summary, cv_results, eval_results = load_model_data()


if page == "Overview":
    # -------------------- Cached video loader --------------------
    @st.cache_resource
    def load_video(path: str):
        """Read and encode video once per session."""
        with open(path, "rb") as f:
            video_bytes = f.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        return video_b64
    
    # -------------------- Determine path relative to this script --------------------
    BASE_DIR = Path(__file__).parent
    video_path = BASE_DIR / "assets" / "animated_catch.mp4"
    
    # -------------------- Display video --------------------
    video_b64 = load_video(video_path)
    video_html = f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 0;
        margin-bottom: 10px;
        width: 100%;
    ">
        <video 
            autoplay 
            loop 
            muted 
            playsinline 
            style="
                width: 100%;
                max-width: 1600px;
                height: auto;
                border-radius: 12px;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
            "
        >
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """
    
    st.markdown(video_html, unsafe_allow_html=True)
  
    st.title("🎣 CPUE Standardization & Forecasting – Overview")

    st.markdown("""
    ### 🧭 Problem Framing & Decision Context
    
    Raw CPUE is widely used as a proxy for relative abundance, yet it is highly sensitive
    to changes in fishing effort, fleet behavior, spatial targeting, and environmental
    conditions. Without formal standardization, CPUE trends can misrepresent true stock
    dynamics—masking declines, exaggerating recovery, or confounding environmental effects
    with operational noise.
    
    This module addresses that risk by applying **distribution-aware statistical models**
    to disentangle ecological signal from sampling bias, producing **standardized CPUE
    indices suitable for interannual comparison, monitoring, and short-term forecasting**
    in squid fisheries.
    """)

    st.markdown("""
    This interactive module is part of the **SquidStock Expedition**, focused on understanding how **environmental and spatiotemporal variability** shape the productivity of the *Argentine shortfin squid* (*Illex argentinus*) fishery between **2000–2020**.  

    At the core of this analysis is the **Catch Per Unit Effort (CPUE)** — a key indicator of relative abundance, where *effort* is defined as **vessel-days** aggregated to a **monthly scale** to produce a fleet-averaged CPUE.  
    This aggregation smooths operational noise while preserving biologically meaningful variation, providing a clear lens on how environmental changes influence catchability and stock availability.
    """)

    st.markdown(
    """
    <div style='color:red; font-weight:bold; font-size:20px; text-align:center; margin-top:10px;'>
    💡 Note: The animated map above displays <b>catch (Jan-Jun) in kilograms (kg)</b> for finer spatial resolution,<br>
    while all model evaluation results in later tabs are expressed in <b>tons (t)</b> for clarity and comparability.
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("🎯 Objective")
    st.markdown("""
   Standardize and model CPUE for *Illex argentinus* (2000–2020, Jan–Jun) to:
    - Remove biases due to fishing effort, spatiotemporal variability, and environmental drivers  
    - Produce indices suitable for operational fisheries management
    - Reveal ecological trends and multi-year variability 

    > Analyses focus on **January–June**, the period with consistent fishing coverage, ensuring balanced interannual comparisons.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("🧮 Modeling Framework")
    st.markdown("""
    The CPUE standardization applies a suite of nonlinear and machine-learning models to disentangle true abundance signals:

    | Model | Rationale | Strength |
    |--------|------------|-----------|
    | **Linear GAM** | Inspired by Lu et al. (2013); interpretable and ecologically grounded. | Captures nonlinear CPUE–environment relationships. |
    | **Gamma-GAM** | Fits right-skewed, positive-only CPUE data. | Avoids log-transform bias, maintains smooth responses. |
    | **Tweedie Regressor (ML)** | Handles zero-inflated and sparse CPUE records. | Flexible, robust, and computationally efficient. |

    These models collectively address the **nonlinear environmental sensitivity** typical of squid, while maintaining **interpretability** crucial for fisheries management.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("🌍 Real-World Relevance")
    st.markdown("""
    Accurate CPUE standardization allows for:
    - Improved **stock assessment** and catch limit setting,
    - Early detection of **climate-driven distribution shifts**, and
    - Supports **evidence-based management and ecosystem monitoring** 

    By connecting statistical modeling and marine ecology, this app helps bridge the gap between **data science and decision-making** in sustainable fisheries.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("💡 Conceptual Summary")
    st.markdown("""
    This model builds upon the work of **Lu et al. (2013)**:
    > *Standardizing CPUE of Argentine shortfin squid (*Illex argentinus*) from the Taiwanese jigger fishery in the southwest Atlantic Ocean.*  
    > *Fisheries Research, 147*, 145–154.  
    > [https://doi.org/10.1016/j.fishres.2013.06.008](https://doi.org/10.1016/j.fishres.2013.06.008)

    By leveraging **Generalized Additive Models (GAMs)** and **Tweedie regressors**, this study captures complex relationships between environment, fishing activity, and abundance — essential for predicting how squid respond to changing ocean conditions.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("⚠️ Limitations & Caveats")
    st.markdown("""
    While this module provides valuable insights, several important caveats apply:

    **1. Temporal Coverage**  
    Only data from **January–June** were used due to incomplete effort records in other months.  
    This ensures data consistency but omits potential peaks or migrations later in the year.

    **2. Temporal Resolution Mismatch**  
    - **SST** is measured **per vessel-day**, while  
    - **Chlorophyll-a** comes from **monthly remote sensing data**.  
    These differing resolutions can introduce temporal mismatch noise.

    **3. Model Simplifications and Setbacks**  
    - Assumes catchability and effort–CPUE relationships remain stable over time.  
    - Spatial autocorrelation and fleet behavior changes are not explicitly modeled.  
    - Environmental effects are assumed additive and smooth.
    - Doesn't account for recruitment, predator-prey interactions, or fine-scale fleet behavior
    

    **4. Forecasting Scope**  
    Forecasts are **short-term scenario-based** — not long-term predictions — and depend on historical trends rather than mechanistic dynamics.

    **5. Biological Context**  
    The model parameters are tuned for *Illex argentinus* in the Southwest Atlantic and may not apply directly to other cephalopods or regions.

    **6. Ecological Complexity**  
    The model does not include recruitment, prey availability, or predator effects, which are important for complete ecosystem understanding.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    # ⚓ Centered title for navigation
    st.markdown(
        "<h3 style='text-align: center; color: #E1EAF2;'>⚓ Continue Your Journey</h3>",
        unsafe_allow_html=True
    )

    html_links = """
    <div style="text-align: center; color: #E1EAF2; font-size: 20px; line-height: 1.6;">
    If you'd like to dive deeper into the full methods and datasets:<br>
    👉 <a href="https://github.com/Euchie23/SquidStock/tree/main/notebooks/CPUE_Standardization_%26_Prediction" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration: underline;">Explore the CPUE Standardization Notebook</a><br><br>
    Or continue through the broader <b>SquidStock Expedition</b> to see how environmental dynamics link to biomass and warming effects:<br>
    🌊 <a href="https://github.com/Euchie23/SquidStock" target="_blank" style="color:#FFD700; font-weight:bold; text-decoration: underline;">Visit the SquidStock Repository</a>
    </div>
    """
    st.markdown(html_links, unsafe_allow_html=True)




elif page == "Model Comparison":
    st.header("🔍 Model Comparison Table")
    
    # 📘 Description
    st.markdown("""
    This table summarizes the **four modeling frameworks** tested for CPUE standardization.  
    Each approach handles the skewed and zero-inflated nature of catch data differently, allowing comparison of model stability and interpretability.  
    
    > **LinearGAMs** use log-transformed CPUE to stabilize variance, while **Gamma** and **Tweedie models** directly model raw CPUE using distributions suited for positive, skewed, or zero-heavy data.
    """)
    
    if not model_summary.empty:
        st.dataframe(model_summary, hide_index=True)
    else:
        st.warning("Model summary data not found.")

elif page == "Evaluation Metrics":
    st.header("📊 Evaluation Metrics Tables")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Cross-Validation Results")
        
        # 📊 Description
        st.markdown("""
        Cross-validation metrics assess **model robustness** and **predictive stability**.  
        Lower **RMSE** (Root Mean Square Error) values indicate better performance.  
        
        > **Tweedie Regressor** achieved the lowest cross-validation RMSE, followed by **GammaGAM**, confirming their ability to capture ecological variability in CPUE.
        """)
        
        if not cv_results.empty:
            st.dataframe(cv_results, hide_index=True)
        else:
            st.warning("Cross-validation data not found.")

    with col2:
        st.subheader("🧾 Test Set Evaluation")
        
        # 🧮 Description
        st.markdown("""
        These metrics evaluate **out-of-sample predictive accuracy** on unseen data.  
        Both **RMSE** and **MAE** (Mean Absolute Error) were used to assess fit quality.  
        
        > **Tweedie Regressor** again produced the lowest errors, while **GammaGAM** provided consistent, interpretable results — making both ideal for ecological modeling.
        """)
        
        if not eval_results.empty:
            st.dataframe(eval_results, hide_index=True)
        else:
            st.warning("Eval results data not found.")

elif page == "Residual Analysis":
    st.header("📉 Residual Plots")

    # 🧠 Description / Executive Summary
    st.markdown("""
    Residual diagnostics help verify whether each model captures the main structure in the CPUE data.  
    A well-performing model should leave **random, pattern-free residuals**, indicating that most of the remaining variation is stochastic rather than systematic.

    We examine:
    - **Residual vs Fitted plots:** to check for heteroskedasticity or nonlinear patterns  
    - **Distribution of residuals:** to confirm approximate normality (for Gaussian models)  
    - **Temporal patterns:** to ensure no residual autocorrelation across years  
    """)

    residual_dict = load_residual_data()

    if not residual_dict:
        st.warning("⚠️ No residual data available.")
    else:
        for model, data in residual_dict.items():
            with st.expander(f"Residuals for {model}"):
                if isinstance(data, (list, tuple)) and len(data) == 2:
                    x, y = data
                elif isinstance(data, dict) and 'x' in data and 'y' in data:
                    x, y = data['x'], data['y']
                else:
                    st.warning(f"⚠️ Residuals for '{model}' not in expected (x, y) format.")
                    continue

                try:
                    x = list(x)
                    y = list(y)
                except Exception as e:
                    st.warning(f"⚠️ Could not convert residuals for '{model}' to list: {e}")
                    continue

                if isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)):
                    fig_res = go.Figure()
                    fig_res.add_trace(go.Scatter(
                        x=x, y=y,
                        mode='markers',
                        marker=dict(color='steelblue'),
                        name='Residuals'
                    ))
                    fig_res.add_hline(y=0, line=dict(color='red', dash='dash'))
                    fig_res.update_layout(
                        title=f"Residuals: {model}",
                        xaxis_title="Predicted",
                        yaxis_title="Residuals",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig_res, use_container_width=True)

    # 🔍 Interpretation
    st.markdown("""
    ### 🔍 Key Insights
    1. **GammaGAM** provides the most **stable and interpretable residuals**, showing balanced dispersion around zero.  
       → This makes it an excellent choice for capturing ecological structure while remaining interpretable.  
    2. **TweedieRegressor** achieves the **best predictive balance**, with residuals evenly spread and fewer high-end deviations.  
       → This confirms its robustness for zero-inflated, overdispersed CPUE datasets.  
    3. Both models outperform log-transformed GAMs, which display residual widening at high CPUE values.  
       → This suggests that transformation alone cannot fully normalize the data.  
    """)


elif page == "Predictions":
    st.header("📊 Predictions & Standardization")

    # 📘 Overview
    st.markdown("""
    This section compares **model predictions**, **standardized indices**, and **observed CPUE patterns**  
    to evaluate model performance and interpret ecological trends.
    """)

    st.subheader("Standardized Fleet-Aggregated Monthly CPUE per Vessel-Day (Interactive)")

    st.caption("""
    This represents the **average squid catch per vessel-day**, aggregated across the fleet and
    statistically standardized to remove the influence of fishing effort, seasonality, and environmental variability.
    It highlights genuine biological and ecological trends in squid abundance through time.
    """)

    monthly_cpue = load_monthly_cpue()
    fig_monthly = px.line(
        monthly_cpue,
        x="Month",
        y="CPUE_vday_tons",
        color="Year",
        markers=True,
        title="Standardized Fleet-Aggregated Monthly CPUE per Vessel-Day",
        labels={"CPUE_vday_tons": "CPUE (tons/vessel days)", "Month": "Month"}
    )
    fig_monthly.update_layout(
        legend_title="Year",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        hovermode='x unified',
        width=900,
        height=600
    )
    st.plotly_chart(fig_monthly, use_container_width=True)


    st.subheader("Observed vs Standardized CPUE (Interactive)")

    st.caption("""
    This comparison shows the **observed (raw) monthly CPUE** plotted against the **standardized CPUE values**
    produced by each model (Linear GAMs, GammaGAM, Tweedie Regressor).
    Standardization removes the influence of fishing effort, seasonality, and environmental variability,
    revealing how closely each model reproduces the true temporal trend in catch rates.
    """)

    merged, colors = load_observed_vs_standardized()
    fig_obs_std = go.Figure()
    for name in colors:
        if name in merged.columns:
            fig_obs_std.add_trace(
                go.Scatter(x=merged["Year"], y=merged[name],
                           mode="lines+markers", name=name,
                           line=dict(color=colors[name]))
            )
    fig_obs_std.update_layout(
        title="Observed vs Standardized CPUE per Year",
        xaxis_title="Year",
        yaxis_title="CPUE",
        hovermode="x unified",
        width=1000,
        height=600
    )
    st.plotly_chart(fig_obs_std, use_container_width=True)

    st.subheader("Actual vs Predicted CPUE")

    st.caption("""
    This interactive plot compares **actual (observed)** versus **model-predicted** CPUE across months and years.
    Each model (Linear GAMs, GammaGAM, Tweedie Regressor) generates its own predicted series,
    allowing assessment of how well it generalizes beyond the training data.
    A closer match between predicted and actual lines indicates stronger predictive performance
    and better ecological realism.
    """)

    pred_dict, color_dict = load_prediction_data()
    fig_obs_pred = go.Figure()
    for label, (x, y) in pred_dict.items():
        if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
            fig_obs_pred.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name=label,
                    line=dict(color=color_dict.get(label, None))
                )
            )

    fig_obs_pred.update_layout(
        title="Actual vs Predicted CPUE per Year",
        xaxis_title="Year",
        yaxis_title="CPUE",
        hovermode="x unified",
        width=1000,
        height=900
    )
    st.plotly_chart(fig_obs_pred, use_container_width=True)

    # 📊 Interpretive Summary
    st.markdown("""
    ## 📈 Model Performance Summary

    These plots reveal how each model generalizes to unseen data and how effectively they standardize the CPUE signal.

    - **LinearGAMs (`log(CPUE + c/+1)`)** stabilize variance but underpredict high CPUE values.  
    - **GammaGAM** shows consistent, smooth fits across years, making it ideal for ecological interpretation.  
    - **TweedieRegressor** yields the **lowest RMSE and MAE** and the most uniform residuals,  
      confirming its superior handling of overdispersion and zero-inflation in fisheries data.
                
    In summary:
    - **For CPUE standardization**, the GammaGAM emerges as the most balanced and interpretable model.
    - **For predictive accuracy and generalization**, the TweedieRegressor performs best.
    - **The LinearGAM** offers a simple baseline that improves variance stability but lacks flexibility at the extremes.

    Together, these methods deliver a **transparent, distribution-aware framework**  
    for monitoring *Illex argentinus* stock productivity under environmental change.
    """)

    st.markdown("</div>", unsafe_allow_html=True)

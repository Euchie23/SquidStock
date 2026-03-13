# =========================================================
# 📦 CORE LIBRARIES
# =========================================================
import numpy as np
import pandas as pd
import io
import os
import time
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================================
# 🎨 VISUALIZATION & INTERACTIVITY
# =========================================================
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# 🌊 STREAMLIT FRAMEWORK & SESSION MANAGEMENT
# =========================================================
import streamlit as st

# =========================================================
# ⚙️ SYSTEM, UTILITIES & WARNINGS
# =========================================================
import warnings
warnings.filterwarnings("ignore")


# =========================================================
# ⚙️ CSS
# =========================================================
st.markdown("""
<style>

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

# .block-container {
#     overflow-y: auto !important;
#     height: 100vh !important;
#     padding-top: 4rem !important;
#     padding-bottom: 2rem !important;

#     /* Slightly more space on left and right */
#     padding-left: 5rem !important;  /* increased from 2rem */
#     padding-right: 2rem !important;

#     margin-top: 0 !important;
#     margin-bottom: 0 !important;
#     max-width: 100% !important;
# }

# section[data-testid="stSidebar"] + div {
#     margin-left: 18rem; /* sidebar width */
# }

/* -------------------------------------------------- */
/* REMOVE STREAMLIT UI ELEMENTS */
/* -------------------------------------------------- */


/* Hide top header and toolbar */
header[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display: none !important;
}

/* ---------------------- Sidebar ---------------------- */
[data-testid="stSidebar"] > div:first-child {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 370px;
    overflow-y: auto;        /* allows scrolling */
    height: 100vh;
    z-index: 1000;
    # padding-top: 1rem !important;
    
    
    /* Combine background image + overlay so it scrolls with content */
    background:
        linear-gradient(rgba(0, 31, 63, 0.6), rgba(0, 31, 63, 0.6)),
        url("https://thumbs.dreamstime.com/b/underwater-seascape-ocean-coral-reef-deep-sea-bottom-swimming-under-water-marine-corals-background-vector-seaweed-algae-354608779.jpg");
    # background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    color: #E1EAF2;
    border-right: 2px solid rgba(255,255,255,0.15);
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

[data-testid="stSidebar"] [data-baseweb="radio"] label {
    margin-bottom: 12px !important;
}

            
/* ---------------------- Sidebar + Main Layout Fix ---------------------- */

/* Sidebar width */
# [data-testid="stSidebar"] > div:first-child {
#     width: 370px !important;
#     min-width: 370px !important;
# }

# /* Remove default spacing from Streamlit wrappers */
# div[data-testid="stSidebar"],
# section[data-testid="stSidebar"] {
#     padding: 0 !important;
#     margin: 0 !important;
# }

# /* Force main content to start exactly at sidebar edge */
# div[data-testid="stAppViewContainer"] > div:nth-child(2) {
#     margin-left: 370px !important; /* match sidebar width */
#     padding-left: 0 !important;
#     margin-top: 0 !important;
#     transition: margin-left 0.3s ease-in-out;
# }

# /* Ensure Streamlit’s block container doesn’t add spacing */
# .block-container {
#     margin: 0 !important;
#     padding: 2rem 3rem !important;
#     max-width: 100% !important;
#     overflow-y: auto !important;
#     height: 100vh !important;
# }

/* Collapsed sidebar behavior */
@media (max-width: 992px) {

    [data-testid="stSidebar"] {
        position: relative !important;
        width: 100% !important;
        height: auto !important;
    }

    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
    }

}

/* Optional thin divider for visual clarity */
# [data-testid="stSidebar"] {
#     border-right: 1px solid rgba(57, 255, 20, 0.3);
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
# header, .css-nahz7x {
#     background-color: #001f3f !important;
# }
            
/* ---------------------- 🧭 Fix Top Bar Alignment (Streamlit 1.51+) ---------------------- */

# /* Keep the top bar visible and consistent */
# header[data-testid="stHeader"] {
#     background-color: #001f3f !important;
#     height: 3.5rem !important;
#     z-index: 1000 !important;
#     position: fixed !important;
#     top: 0 !important;
#     left: 0 !important;
#     right: 0 !important;
# }

# /* Sidebar should start just below the fixed top bar */
# [data-testid="stSidebar"] {
#     position: fixed !important;
#     top: 3.5rem !important;      /* push it down below header */
#     height: calc(100vh - 3.5rem) !important;
#     margin: 0 !important;
# }

# /* Sidebar inner div scrolls normally */
# [data-testid="stSidebar"] > div:first-child {
#     height: 100% !important;
#     overflow-y: auto !important;
# }

# /* Main app container shifts down equally */
# div[data-testid="stAppViewContainer"] {
#     margin-top: 3.5rem !important;   /* align with sidebar */
#     padding-top: 0 !important;
# }

# /* The block container keeps its scroll and padding */
# .block-container {
#     height: calc(100vh - 3.5rem) !important;
#     overflow-y: auto !important;
# }

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

/* ---------------------- Link Buttons (st.link_button) ---------------------- */
a[data-testid="stLinkButton"] {
    background-color: #39FF14 !important;  /* bright green */
    color: #001f3f !important;             /* dark text */
    font-size: 18px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    text-align: center !important;
    text-decoration: none !important;
    display: inline-block !important;
    width: 100% !important;                /* full width in the column */
    border: none !important;
}

a[data-testid="stLinkButton"]:hover {
    background-color: #32CD32 !important;  /* darker green on hover */
    color: #FFD700 !important;             /* golden text on hover */
    text-decoration: none !important;
}

/* ---------------------- Main Panel Alignment Fix ---------------------- */

.block-container {
    max-width: none !important;
    margin-left: 0 !important;              /* start at left 0 */
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    box-sizing: border-box !important;

    /* occupy full width minus sidebar width */
    width: calc(100vw - 300px) !important;
}

/* ---------------------- Adjust when sidebar collapses ---------------------- */

[data-testid="stSidebar"][aria-expanded="false"] ~ div .block-container {
    width: calc(100vw - 80px) !important;
}

/* ---------------------- Inner content wrapper fix ---------------------- */

.block-container > div {
    max-width: 100% !important;
    width: 100% !important;      /* prevents centering / wrapping */
}

/* ---------------------- Prevent Horizontal Scroll ---------------------- */

html, body, .stApp {
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ============================
# 3️⃣ SIDEBAR NAVIGATION
# ============================
st.sidebar.title("🦑 Biomass Simulator")

tabs = [
    "Overview",
    "Baseline Simulation",
    "Warming Scenario",
    "Sensitivity & CPUE",
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

if "clear_note_input" not in st.session_state:
    st.session_state.clear_note_input = False  # ✅ added for safe clearing

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
        if st.button("❌ Cancel Edit"):
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

# Helper function to save notes
def save_note(tab):
    note = st.session_state.get("current_note", "").strip()
    if note:
        st.session_state.notes[tab].append(
            {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "note": note}
        )
        st.session_state.current_note = ""
        st.success("📝 Note saved to Logbook!")


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

# ---------------- Notes Panels ----------------
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

        # --- Contextual parameters ---
        if page == "Baseline Simulation":
            st.sidebar.markdown("<h3 style='color:#FFD700;'>⚙️ Simulation Controls</h3>", unsafe_allow_html=True)
            st.sidebar.markdown("""
            <p style='font-size:14px; color:#ccc;'>
            Defaults reflect ecosystem-scale literature values.  
            Use sliders to scale parameters for the January–June fishery segment or to test alternative scenarios.
            </p>
            """, unsafe_allow_html=True)
            with st.sidebar.expander("🔧 Expand to adjust EDPSM parameters", expanded=False):
                params["K"] = st.slider("Carrying Capacity (tons)",  2_000_000, 8_000_000, params.get("K", 5_000_000), 100_000, help = "Upper biomass limit (K) — maximum total squid biomass the ecosystem can support.")
                params["N0"] = st.slider("Initial Biomass (tons)",  500_000, 3_000_000, params.get("N0", 1_500_000), 50_000, help="Starting biomass at the beginning of the season (N₀). Should generally be ≤ 30% of K.")
                params["r0"] = st.slider("Max Growth Rate (r₀)", 0.05, 0.3, params.get("r0", 0.15), 0.01, help="Intrinsic daily population growth rate (typical for fast-growing squid).")
                params["T_opt"] = st.slider("Optimal Temperature (°C)", 10.0, 14.0, params.get("T_opt", 12.0), 0.1,  help="Temperature where growth rate and biomass production peak.")
                params["sigma_T"] = st.slider("Temperature Tolerance (σₜ)", 1.0, 4.0, params.get("sigma_T", 3.0), 0.1, help="Thermal tolerance — how far above or below optimal temperature squid can still grow efficiently.")
                params["q"] = st.slider("Catchability (q)", 1e-6, 1e-3, params.get("q", 5e-5), step=1e-6, format="%.6f", help="Fishing efficiency — how easily squid are caught per unit effort. Higher q means stronger harvest pressure.")
        elif page == "Warming Scenario":
            st.sidebar.markdown("<h3 style='color:#FFD700;'>🌡️ Warming Controls</h3>", unsafe_allow_html=True)
            with st.sidebar.expander("🌍 Expand to adjust scenario parameters", expanded=False):
                params["delta_T"] = st.slider("Temperature Increase (°C)", 0.0, 4.0, params.get("delta_T", 2.0), 0.1)
                params["duration"] = st.slider("Warming Period (months)", 1, 60, params.get("duration", 24), 1)
                params["show_baseline"] = st.checkbox("Show Baseline for Comparison", params.get("show_baseline", True))

        #st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14;'>", unsafe_allow_html=True)
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
            TABS_WITH_PARAMS = ["Baseline Simulation", "Warming Scenario"]

            # --- Save Button ---
            if st.button("💾 Save Note", key=f"save_{page}"):
                content = note_text.strip()
                if content:
                    new_entry = {
                        "timestamp": datetime.now(),
                        "notes": content,
                        "inputs": params.copy() if page in TABS_WITH_PARAMS else {}
                    }

                    if st.session_state.edit_mode["active"] and st.session_state.edit_mode["tab"] == page:
                        idx = st.session_state.edit_mode["index"]
                        st.session_state.notes[page][idx] = new_entry
                        st.session_state.toast_message = f"✏️ Note updated in {page}!"
                        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
                    else:
                        st.session_state.notes[page].append(new_entry)
                        st.session_state.toast_message = f"✅ Note saved to {page}!"

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

            with st.expander(f"🗂 {tab_name} ({len(notes)} notes)", expanded=False):
                for i, note in enumerate(notes):
                    col1, col2, col3 = st.columns([6, 1, 1])
                    with col1:
                        st.markdown(format_note_display(note, tab_name))
                    with col2:
                        if st.button("✏️", key=f"edit_{tab_name}_{i}"):
                            #entry = note
                            entry = st.session_state.notes[tab_name][i]

                            #Restore note text
                            st.session_state.note_input = entry["notes"]

                            # Restore tab inputs from snapshot
                            for k, v in entry["inputs"].items():
                                st.session_state.params[k] = v
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
                                st.rerun()
                        else:
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("✅", key=f"confirm_del_{tab_name}_{i}"):
                                    del st.session_state.notes[tab_name][i]
                                    st.session_state.delete_confirm.pop(delete_key, None)
                                    st.session_state.toast_message = f"🗑 Deleted note {i+1} from {tab_name}"
                                    st.rerun()
                            with c2:
                                if st.button("❌", key=f"cancel_del_{tab_name}_{i}"):
                                    st.session_state.delete_confirm[delete_key] = False
                                    st.rerun()

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
    
    # --- Define the function ---
    def send_notes_to_host(all_notes_text, tab_name="ocean_dynamics"):
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

# 🔹 Link to next app: Ocean Dynamics (Biomass Estimation)
    THE_ENGINE_ROOM_URL = "https://squidstock-the-engine-room.streamlit.app"

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
                🐙 Next Stop:
            </div>
            <div style="font-size:18px; font-weight:500;">
                The Engine Room – Let's now try to forecast weekly CPUE with precision using advanced ML and regime analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # 🔹 Centered "Coming Soon" button (functional version)
    st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
         st.link_button("⚙️ Visit The Engine Room", THE_ENGINE_ROOM_URL, use_container_width=True)


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

APP_PATH = os.path.dirname(__file__)  # folder where app.py is
DATA_PATH = os.path.join(APP_PATH, "data/Final_dataset_imputed.csv")

@st.cache_data
def load_data():
    # Load dataset and filter for consistent months (Jan–Jun only)
    df = pd.read_csv(DATA_PATH)
    df = df[df["Month"].between(1, 6)]

    # Convert catch to tons for easier interpretation
    df["SqCatch_tons"] = df["SqCatch_Kg"] / 1000

    # Create a unique trip ID per vessel and day
    df["VesselDay"] = df["CTNO"].astype(str) + "_" + df["Year"].astype(str) + "_" + df["Month"].astype(str) + "_" + df["Day"].astype(str)

    # --- Aggregate catches by trip and then by month ---
    trip_cpue = (
        df.groupby(["Year", "Month", "CTNO", "VesselDay"], as_index=False)
        .agg(DayCatch_tons=("SqCatch_tons", "sum"))
    )

    # Monthly totals and fishing effort
    monthly_summary = (
        trip_cpue.groupby(["Year", "Month"], as_index=False)
        .agg(
            TotalCatch_tons=("DayCatch_tons", "sum"),
            VesselDays=("VesselDay", "count")
        )
    )

    # Calculate Catch per Unit Effort (CPUE)
    monthly_summary["CPUE_tons"] = monthly_summary["TotalCatch_tons"] / monthly_summary["VesselDays"]

    # --- Environmental variables per month ---
    env_features = (
        df.groupby(["Year", "Month"], as_index=False)
        .agg(SST=("WaterTemp", "mean"), ChlA=("Chlor_a_mg_m3", "mean"))
    )

    # Combine summaries
    df_monthly = monthly_summary.merge(env_features, on=["Year", "Month"]).sort_values(["Year", "Month"])

    # ✅ NEW: Normalize CPUE within each year so it can be compared fairly
    df_monthly["CPUE_index"] = df_monthly.groupby("Year")["CPUE_tons"].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )

    # ✅ Optional: Save mean vessel-days for weighting later
    df_monthly["Effort_weight"] = df_monthly["VesselDays"] / df_monthly["VesselDays"].max()

    return df_monthly

df_monthly = load_data()


# ========================================
#  TAB 1: OVERVIEW
# ========================================
if page == "Overview":


    # --- remove top padding of Streamlit main panel ---
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;  /* small top padding, you can adjust */
    }
    </style>
    """, unsafe_allow_html=True)


    
    # Centered Dashboard Tour banner
    st.markdown("""
    <div style="
        display: flex;
        justify-content: center;          /* center horizontally */
        margin-top: 5px;                 /* distance from top of panel */
        margin-bottom: 25px;              /* space below banner */
    ">
        <div style="
            background-color: rgba(255, 215, 0, 0.1);   /* subtle gold background */
            color: #FFD700;
            padding: 8px 20px;
            border-left: 4px solid #FFD700;            /* small gold accent */
            border-radius: 5px;
            font-weight: 600;
            font-size: 16px;
            max-width: 600px;                           /* keeps it neat */
            text-align: center;
            box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
        ">
            🎬 <a href="https://euchie23.github.io/GeoTentacles/Scripts/python/video_under_construction.html"
               target="_blank" style="color:#FFD700; text-decoration:underline;">
               Watch Dashboard Tour
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    
    st.title("🐙 Ocean Dynamics: Biomass Response Simulator")

    st.markdown("""
    ### 🧭 Problem Framing & Decision Context

    Catch-per-unit-effort (CPUE) is widely used as a proxy for stock abundance, but for short-lived,
    highly mobile species like squid, CPUE can decouple from true biomass—especially under changing
    environmental conditions.
    
    This app allows users to test how **environmental variability and warming scenarios**
    affect squid biomass dynamics, and to evaluate when CPUE may become a misleading indicator for
    seasonal management and climate-adaptation decisions.
    """)

    
    st.markdown("""
    This interactive app explores how **squid biomass** (*Illex argentinus*) responds to changing ocean conditions using the **nonlinear Environmentally Dependent Surplus Production Model (EDSPM)**.  
    Adjust model parameters, simulate temperature effects, and record your ecological insights.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")
    
    st.subheader("About the Model")
    st.markdown("""
    The EDSPM links environmental variability to surplus production, capturing how populations grow under optimal conditions and slow near ecological limits.  
    The model combines:
    - **Biomass (tons)** – estimated total population
    - **Growth rate (r_t)** – temperature-dependent growth rate at each time step
    - **Environmental index (E(t))** – weighted combination of normalized SST (60%) and chlorophyll-a (40%)
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")
    
    st.subheader("🌡️ Temperature-Dependent Growth")

    st.markdown("""
    The **growth rate (rₜ)** varies with sea surface temperature (**SST**) following a Gaussian (bell-shaped) thermal response:
    """)

    st.latex(r"""
    r_t = r_0 \times \exp\left(-\frac{(SST - T_{opt})^2}{2\sigma_T^2}\right)
    """)

    st.markdown("""
    **Where:**
    - **r₀** — Maximum intrinsic growth rate (under optimal temperature conditions)  
    - **Tₒₚₜ** — Optimal temperature where the species grows best  
    - **σₜ** — Temperature tolerance; smaller σₜ → more temperature-sensitive species  
    - **SST** — Current sea surface temperature  

    ✅ **Interpretation:**  
    - Growth peaks when SST ≈ Tₒₚₜ (so rₜ ≈ r₀)  
    - Growth declines as SST moves away from Tₒₚₜ  
    - This relationship directly influences biomass: higher rₜ → population increase; lower rₜ → decline.
    """)


    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("Baseline Ecological Settings")

    st.markdown("""
    These settings define the starting ecological conditions for your simulations.  
    You can adjust these interactively in the *Baseline Simulation* and *Warming Scenario* tabs to explore alternative environmental or fishing conditions.
    """)

    st.markdown("""
    To make the simulator realistic, default values were chosen from peer-reviewed studies of **Argentine short-fin squid (*Illex argentinus*)** in the **Southwest Atlantic Ocean**.  
    These provide a credible ecological starting point before you adjust sliders in the *Baseline* or *Warming Scenario* tabs.

    | **Parameter** | **Proposed Default Value** | **Typical Range** | **What It Represents** | **Sources** |
    |----------------|------------------|------------------|------------------------|-------------|
    | **Carrying Capacity (K)** | **5 million tons** | 4–6 million t | Estimated upper limit of total squid biomass the ecosystem can support. | ICES (2004) |
    | **Initial Biomass (N₀)** | **3 million tons** | 2–4 million t | Approximate starting biomass at the season’s onset. | ICES (2004); Haimovici et al., NERC (2014) |
    | **Max Growth Rate (r₀)** | **0.02 day⁻¹** | 0.015–0.03 day⁻¹ | Average daily population growth (about 1.5–3% per day). | ShHyd Marine Research (2018); Haimovici et al. (2014) |
    | **Optimal Temperature (Tₒpt)** | **12 °C** | 10–14 °C | Temperature range where growth and abundance peak. | Xiang et al., *Fishes (2024)*; PMC (2024) |
    | **Temperature Tolerance (σₜ)** | **±3 °C** | ±2–4 °C | How far above or below optimum the squid can still grow well. | Xiang et al. (2024); PMC (2024) |

    These numbers act as **realistic ecological defaults**, but users are encouraged to adjust them to explore “what-if” scenarios such as ocean warming or productivity shifts.
    """)

    st.subheader("Calibration and Data Notes")
    st.markdown("""
    The model was recalibrated using observed data (**2000–2020**, *January–June*), representing the most consistent part of the fishing season.  

    **Key updates and assumptions:**
    - Only **Jan–Jun** data are used to avoid missing-month biases.  
    - Observed catches ranged from **10,000 to 260,000 tons per season**.  
    - Fishing effort varied between **100–180 vessel-days**.  
    - The model assumes a sustainable **25–30% exploitation rate**. 
    - **Catchability (q)** represents how efficiently fishing effort converts biomass into catch — higher values reflect more effective fleets or technologies.
 

    To maintain realistic stock–catch balance, parameters were adjusted to ensure the starting biomass (**N₀**) is always well above the largest recorded catch.  
    For instance, a 260,000-ton catch at a 30% exploitation rate implies:
    """)

    # ✅ Correct LaTeX rendering (inline)
    st.markdown(
        r"The minimum biomass should satisfy \( N₀ \ge \frac{260{,}000}{0.30} \approx 867{,}000\ \text{tons} \)."
    )

    st.markdown("""
    **Calibrated defaults (ecologically realistic):**
    - Carrying capacity (**K**) = **5,000,000 tons**  
    - Initial biomass (**N₀**) = **1,500,000 tons**  
    - Growth rate (**r₀**) = **0.15 day⁻¹**  
    - Optimal temperature (**Tₒpt**) = **12 °C**  
    - Temperature tolerance (**σₜ**) = **3 °C**  

    These settings keep exploitation within realistic ecological limits while still allowing users to explore *“what-if”* scenarios such as warming or changes in productivity.
    """)

    st.markdown("""
    💡 *Why it matters:*  
    Understanding how biomass reacts to small environmental changes helps reveal how short-lived, fast-growing species like **Illex argentinus** might respond to future ocean warming.  
    Try tuning the parameters—small changes in temperature or growth rate can reshape population trajectories dramatically.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("Handling Uncertainty: Monte Carlo Simulation & Normalization")
    st.markdown("""
    To better represent uncertainty in biomass and CPUE estimates, we incorporate **Monte Carlo simulations**:

    1. **Monte Carlo Runs**  
    - Multiple simulations are run using slightly varying environmental inputs and model parameters.  
    - This produces distributions for biomass and CPUE over time rather than a single deterministic line.

    2. **Mean and Confidence Intervals**  
    - Plots show the **mean trajectory** (average across all runs) as the main line.  
    - Shaded areas represent **95% confidence intervals**, capturing the range of plausible outcomes.  
    - This allows users to see **both expected trends and uncertainty** in population predictions.

    3. **Normalization for Comparison**  
    - Both biomass and CPUE are scaled to **0–1** to allow direct comparison on the same graph.  
    - This makes it easier to visually assess correlations and trends without being influenced by different units or magnitudes.

    4. **Correlation Interpretation**  
    - Correlations between CPUE and biomass are computed using Monte Carlo mean values.  
    - Strong correlations indicate that CPUE reflects actual biomass well, while weak or negative correlations highlight potential mismatches or shifts in fishing efficiency.

    💡 *Why it matters:* Monte Carlo-based visualization lets users distinguish between **true ecological trends** and **random variation**, making the simulator more robust and informative.
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    
    st.subheader("Threshold for Meaningful Change")
    st.markdown("""
    - A **±5% change in biomass** is considered biologically significant and changes within ±5% are considered **stable**, while above or below may indicate increasing or declining populations. This threshold is a heuristic for interpretation and not drawn from a universal fisheries management standard.   
    - Users can use this threshold to interpret simulation results in subsequent tabs
    """)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")
    
    st.subheader("Environmental Data Notes")
    st.markdown("""
    - **SST (Sea Surface Temperature):** measured per vessel-day; can vary across trips  
    - **Chlorophyll-a (ChlA):** obtained from monthly remote sensing; smoother temporal resolution  
    - Only **January to June** is used (6 months) to maintain consistency across the 21-year dataset
    """)
    
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("----")

    st.subheader("Limitations & Caveats")
    st.markdown("""
    - EDSPM is **non-linear**, so extreme environmental conditions may yield unrealistic biomass estimates  
    - Using only 6 months may not capture full seasonal dynamics  
    - SST and ChlA have different temporal and spatial resolutions, which may affect the environmental index  
    - Biomass trends are **qualitative** indicators and should be interpreted cautiously
    """)
    
    st.markdown("""
    💡 **Tip:** In the interactive plots, hover over points to see how **environmental conditions (SST, ChlA)** affect **growth rate (r_t)** and **biomass**. This illustrates the pathway: environment → growth → population.
    """)

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
    If you'd like to learn more about the methods, models, and datasets used in this stage of the voyage:<br>
    👉 <a href="https://github.com/Euchie23/SquidStock/tree/main/notebooks/Biomass_Forecasting" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration: underline;">Explore the Biomass Estimation Notebook</a><br><br>
    Or, explore the entire <b>SquidStock Expedition</b> — see how this stage connects to the full storyline:<br>
    🌊 <a href="https://github.com/Euchie23/SquidStock" target="_blank" style="color:#FFD700; font-weight:bold; text-decoration: underline;">Visit the SquidStock Repository</a>
    </div>
    """

    st.markdown(html_links, unsafe_allow_html=True)


# ========================================
#  TAB 2: BASELINE SIMULATION
# ========================================
elif page == "Baseline Simulation":
    st.header("⚙️ Baseline Biomass Simulation")
    params = st.session_state.get("params", {})
    K = params.get("K", 5_000_000)
    N0 = params.get("N0", 1_500_000)
    r0 = params.get("r0", 0.15)
    T_opt = params.get("T_opt", 12.0)
    sigma_T = params.get("sigma_T", 3.0)
    q = params.get("q", 5e-5)

    num_sim = 500  # reduced for performance

    # --- STEP 1: Lightweight preprocessing cache
    @st.cache_data(show_spinner=False)
    def preprocess_env(df):
        df = df.copy()
        sst_min, sst_max = df["SST"].min(), df["SST"].max()
        chla_min, chla_max = df["ChlA"].min(), df["ChlA"].max()
        df["E_env"] = ((df["SST"] - sst_min) / (sst_max - sst_min)) * 0.6 + \
                      ((df["ChlA"] - chla_min) / (chla_max - chla_min)) * 0.4
        return df

    df_monthly = preprocess_env(df_monthly)

    # --- STEP 2: Vectorized simulation core (heavy compute, fully cached)
    @st.cache_data(show_spinner=True, ttl=3600, max_entries=3)
    def run_baseline_simulation(df, K, N0, r0, T_opt, sigma_T, q, num_sim):
        df = df.copy()
        T = len(df)

        # temperature-dependent growth
        r_t = r0 * np.exp(-((df["SST"] - T_opt) ** 2) / (2 * sigma_T**2))
        E_env = df["E_env"].values
        E_eff = df["VesselDays"].values

        # initialize matrix for biomass simulations
        biomass = np.zeros((num_sim, T))
        biomass[:, 0] = N0

        # Vectorized Monte Carlo simulation
        for t in range(1, T):
            N_prev = biomass[:, t - 1]
            growth = r_t.iloc[t] * E_env[t] * N_prev * (1 - N_prev / K)
            catch_loss = q * E_eff[t] * N_prev
            biomass[:, t] = np.maximum(N_prev + growth - catch_loss, 0)

        df["Biomass_mean"] = biomass.mean(axis=0)
        df["Biomass_CI_lower"] = np.percentile(biomass, 2.5, axis=0)
        df["Biomass_CI_upper"] = np.percentile(biomass, 97.5, axis=0)
        df["r_t"] = r_t

        # cap biomass
        df["Biomass_mean"] = np.minimum(df["Biomass_mean"], 1.2 * K)
        df["Biomass_CI_upper"] = np.minimum(df["Biomass_CI_upper"], 1.2 * K)
        return df

    # --- STEP 3: Cache persistent baseline result (memory-safe)
    @st.cache_resource(show_spinner=False)
    def get_baseline_result(df, K, N0, r0, T_opt, sigma_T, q, num_sim):
        return run_baseline_simulation(df, K, N0, r0, T_opt, sigma_T, q, num_sim)

    with st.spinner("Running baseline simulation..."):
        df_monthly = get_baseline_result(df_monthly, K, N0, r0, T_opt, sigma_T, q, num_sim)

    # --- Exploitation rate
    mean_catch = df_monthly["TotalCatch_tons"].mean()
    mean_biomass = df_monthly["Biomass_mean"].mean()
    exploitation_rate = mean_catch / mean_biomass if mean_biomass > 0 else np.nan
    # --- Color-coded exploitation indicator
    if exploitation_rate < 0.01:
        color, verdict = "#FF4C4C", "⚠️ Extremely low exploitation — biomass likely overestimated or catches too small."
    elif exploitation_rate < 0.10:
        color, verdict = "#FFD700", "🟡 Low exploitation — fishery lightly utilized, check biomass initialization."
    elif exploitation_rate <= 0.35:
        color, verdict = "#00FF88", "✅ Plausible exploitation range (biologically realistic)."
    else:
        color, verdict = "#FF6EC7", "🚨 High exploitation — potential overfishing or small biomass stock."

    # --- Styled info block
    st.markdown(
        f"""
        <div style="
            background-color: rgba(20, 20, 20, 0.6);
            padding: 18px 22px;
            border-left: 5px solid {color};
            border-radius: 10px;
            color: #E1EAF2;
            font-size: 18px;
            line-height: 1.5;
        ">
        <b>⚖️ Average exploitation rate:</b> {exploitation_rate:.2%}<br>
        {verdict}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Add the mathematical context using LaTeX
    st.markdown("---")
    with st.expander("📘 Learn More: Understanding Exploitation Rate and Biomass Calibration"):

        st.markdown("### ⚖️ Exploitation Rate")

        st.markdown(
            """
            The **exploitation rate (E)** tells us what portion of the total stock is caught each season.
            In simple terms, it shows how much fishing pressure the population is under.
            """
        )
        st.latex(r"E = \frac{\text{Mean Catch (tons)}}{\text{Mean Simulated Biomass (tons)}}")

        st.markdown(
            """
            👉 For example, if 20% of the total population is caught, then **E = 0.20 (20%)**.  
            For squid and other fast-growing species, a sustainable range is usually **10–30%**.
            """
        )

        st.markdown("### 🧭 Setting a Safe Starting Biomass")

        st.markdown(
            """
            To avoid starting the model with an **overfished stock**,  
            the initial biomass (**N₀**) should be large enough to support the biggest observed catch  
            without exceeding the target exploitation rate:
            """
        )
        st.latex(r"N₀ \ge \frac{\text{max catch}}{E_{target}}")

        # --- Example Calculation
        max_catch = df_monthly["TotalCatch_tons"].max()
        st.caption(
            f"For example, if the maximum observed catch is {max_catch:,.0f} tons "
            f"and you aim for a 30% exploitation rate, the starting biomass "
            f"should be at least ≈ {max_catch / 0.30:,.0f} tons. If it's lower the model might imply overfishing."
        )
    
    # --- Save to session for downstream tabs
    st.session_state["baseline_df"] = df_monthly  # or df_latest if that’s your main df
    st.session_state["latest_df"] = df_monthly.copy()  # or df_monthly.copy() in baseline

    # --- Interactive Plotly chart
    fig = go.Figure()

    # Mean biomass
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_monthly)),
        y=df_monthly["Biomass_mean"],
        mode="lines+markers",
        name="Biomass (mean)",
        line=dict(color="teal"),
        hovertemplate="Month %{x}<br>Biomass: %{y:.1f} tons<br>SST: %{customdata[0]:.2f}°C<br>ChlA: %{customdata[1]:.2f} mg/m³<extra></extra>",
        customdata=np.stack((df_monthly["SST"], df_monthly["ChlA"]), axis=-1)
    ))

    # CI ribbon
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_monthly)),
        y=df_monthly["Biomass_CI_upper"],
        fill=None,
        mode='lines',
        line=dict(color='lightgray'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_monthly)),
        y=df_monthly["Biomass_CI_lower"],
        fill='tonexty',
        mode='lines',
        line=dict(color='lightgray'),
        name="95% CI",
        showlegend=True
    ))

    # r_t trace on secondary y-axis
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_monthly)),
        y=df_monthly["r_t"],
        mode="lines+markers",
        name="Growth rate r_t",
        line=dict(color="orange", dash="dot"),
        yaxis="y2",
        hovertemplate="Month %{x}<br>r_t: %{y:.2f}<br>SST: %{customdata[0]:.2f}°C<extra></extra>",
        customdata=np.stack((df_monthly["SST"],), axis=-1)
    ))

    # Layout with secondary y-axis
    fig.update_layout(
        title="Baseline Biomass Simulation + Temperature-dependent Growth Rate",
        xaxis_title="Time (Months)",
        yaxis=dict(title="Biomass (tons, MC mean)", side="left"),
        yaxis2=dict(title="r_t", overlaying="y", side="right"),
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(fig, width='stretch')

       # --- Add some spacing above
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Observation text with r_t interpretation
    avg_change = (df_monthly["Biomass_mean"].iloc[-1] - df_monthly["Biomass_mean"].iloc[0]) / df_monthly["Biomass_mean"].iloc[0]
    avg_r_t = df_monthly["r_t"].mean()

    if avg_change > 0.05:
        obs_text = (
            "Biomass is generally increasing under these baseline conditions 📈. "
            f"On average, the growth rate (r_t) is {avg_r_t:.2f}, indicating favorable temperature conditions for population growth."
        )
    elif avg_change < -0.05:
        obs_text = (
            "Biomass is decreasing under baseline conditions 📉. "
            f"The growth rate (r_t) is relatively low ({avg_r_t:.2f}), suggesting temperatures may be suboptimal for growth."
        )
    else:
        obs_text = (
            "Biomass is relatively stable ⚖️. "
            f"Average growth rate (r_t) is {avg_r_t:.2f}, indicating that temperature conditions are generally adequate but not strongly promoting growth."
        )

    # --- Dark panel with larger font
    st.markdown(
        f"""
        <div style="
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px 25px;
            border-radius: 10px;
            margin-top: 15px;
            color: #E1EAF2;
            font-size: 20px;
            line-height: 1.6;
        ">
        {obs_text}
        </div>
        """,
        unsafe_allow_html=True
    )



# ========================================
#  TAB 3: WARMING SCENARIO
# ========================================
elif page == "Warming Scenario":
    st.header("🔥 Climate Warming Scenarios")
# --- Load parameters (ensure you included params['q'] in sidebar)
    params = st.session_state.get("params", {})
    delta_T = params.get("delta_T", 2.0)
    r0 = params.get("r0", 0.15)
    T_opt = params.get("T_opt", 12.0)
    sigma_T = params.get("sigma_T", 3.0)
    N0 = params.get("N0", 1_500_000)
    K = params.get("K", 5_000_000)            # or 1_000_000 depending on defaults
    duration = int(params.get("duration", 24))
    show_baseline = params.get("show_baseline", True)
    q = params.get("q", 5e-5)                 # catchability (default if not set)

    # --- Ensure baseline Monte Carlo exists
    df_monthly = st.session_state.get("baseline_df", None)
    if df_monthly is None:
        st.warning("Baseline simulation not found. Run baseline first.")
        st.stop()
    if "Biomass_mean" not in df_monthly.columns:
        st.warning("Baseline simulation is missing Biomass_mean column. Run baseline first.")
        st.stop()

    # Warn if N0 > K (simple check)
    if N0 > K:
        st.warning(f"Note: Initial biomass N0 ({N0:,}) exceeds K ({K:,}). This may produce odd dynamics.")

    # --- Prepare warming dataframe (truncate to duration)
    df_warm = df_monthly.copy().iloc[:duration].reset_index(drop=True)
    # apply warming trend (linear increment across duration)
    df_warm["SST"] = df_warm["SST"] + np.linspace(0, delta_T, len(df_warm))
    # temperature-dependent instantaneous growth modifier
    df_warm["r_t"] = r0 * np.exp(-((df_warm["SST"] - T_opt) ** 2) / (2 * sigma_T**2))

    # --- Clarify environment vs effort
    df_warm["EnvIndex"] = df_warm["E_env"]               # environmental favourability (0-1)
    df_monthly["EnvIndex"] = df_monthly["E_env"]

    # Effort (vessel-days) kept as separate column
    df_warm["Effort"] = df_warm["VesselDays"]
    df_monthly["Effort"] = df_monthly["VesselDays"]

    # --- Quick q diagnostic (optional)
    mean_catch = df_monthly["TotalCatch_tons"].mean()
    mean_effort = df_monthly["Effort"].mean()
    mean_biomass_for_q = max(N0, df_monthly["Biomass_mean"].mean())
    q_init = mean_catch / (mean_effort * (mean_biomass_for_q + 1e-12))
    # show suggested q in UI (non-intrusive)
    st.caption(f"Suggested q (rough) based on historical means: {q_init:.6e}")

    # --- Monte Carlo warming simulation using growth - harvest
    n_sim = 1000
    biomass_sim = np.zeros((n_sim, len(df_warm)))

    for i in range(n_sim):
        N = float(df_monthly["Biomass_mean"].iloc[0])  # start from baseline mean at t=0 (you can change to N0)
        for t in range(len(df_warm)):
            r_t = float(df_warm["r_t"].iloc[t])
            E_env = float(df_warm["EnvIndex"].iloc[t])
            Eff = float(df_warm["Effort"].iloc[t])

            # small multiplicative noise so sims differ
            noise = np.random.normal(1.0, 0.05)

            # natural growth -- environment modifies growth (positive)
            growth = r_t * N * (1 - N / K) * E_env * noise

            # fishing harvest (removal) using catchability q
            harvest = q * Eff * N

            # update population
            N = max(N + growth - harvest, 0.0)
            biomass_sim[i, t] = N

    # --- Compute mean and 95% CI (aligned with time index)
    df_warm["Biomass_mean"] = biomass_sim.mean(axis=0)
    df_warm["Biomass_CI_lower"] = np.percentile(biomass_sim, 2.5, axis=0)
    df_warm["Biomass_CI_upper"] = np.percentile(biomass_sim, 97.5, axis=0)

    # --- Percentage change relative to baseline mean (percent)
    baseline_slice = df_monthly["Biomass_mean"].iloc[:duration].values
    # protect divide-by-zero
    with np.errstate(divide='ignore', invalid='ignore'):
        biomass_change_pct = 100.0 * (df_warm["Biomass_mean"].values - baseline_slice) / (baseline_slice + 1e-12)
    df_warm["Biomass_change_pct"] = biomass_change_pct

    # --- Save warming results in session
    st.session_state["df_warm"] = df_warm.copy()

    # --- Plotting (same multi-panel layout)
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
        subplot_titles=("Simulated Biomass", "% Change in Biomass", "Environmental Index (EnvIndex) and Effort")
    )

    # Baseline trace (top)
    if show_baseline:
        fig.add_trace(go.Scatter(
            x=np.arange(len(df_warm)),
            y=df_monthly["Biomass_mean"].iloc[:duration].values,
            name="Baseline (mean)",
            line=dict(color="blue")
        ), row=1, col=1)

    # Warming mean + CI (top)
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_warm)),
        y=df_warm["Biomass_mean"],
        mode="lines+markers",
        name="Warming (mean)",
        line=dict(color="orange")
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_warm)),
        y=df_warm["Biomass_CI_upper"],
        line=dict(color="orange", dash="dot"),
        showlegend=False
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_warm)),
        y=df_warm["Biomass_CI_lower"],
        fill='tonexty',
        fillcolor='rgba(255,165,0,0.2)',
        line=dict(color="orange", dash="dot"),
        showlegend=False
    ), row=1, col=1)

    # % Change panel (middle)
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_warm)),
        y=df_warm["Biomass_change_pct"],
        name="% Change",
        line=dict(color="red")
    ), row=2, col=1)

    # Environment index and Effort (bottom) - show both (EnvIndex left, Effort right)
    fig.add_trace(go.Scatter(
        x=np.arange(len(df_warm)),
        y=df_warm["EnvIndex"],
        name="EnvIndex (baseline/warm adjusted)",
        line=dict(color="green")
    ), row=3, col=1)
    fig.add_trace(go.Bar(
        x=np.arange(len(df_warm)),
        y=df_warm["Effort"],
        name="Effort (vessel-days)",
        marker=dict(color='rgba(0,0,255,0.3)'),
        yaxis='y2'
    ), row=3, col=1)

    # layout: add second y axis for effort on bottom panel
    fig.update_layout(
        height=900,
        showlegend=True,
        title=f"🔥 Warming Scenario (+{delta_T:.1f}°C) — catchability q={q:.2e}",
        template="plotly_dark"
    )
    fig.update_yaxes(title_text="Biomass (tons)", row=1, col=1)
    fig.update_yaxes(title_text="% Change", row=2, col=1)
    fig.update_yaxes(title_text="EnvIndex (unitless)", row=3, col=1)
    fig.update_xaxes(title_text = "Time (Months)", row=3)

    st.plotly_chart(fig, width='stretch')

    # --- Summary statistics (cleaner)
    avg_pct_change = df_warm["Biomass_change_pct"].mean()
    final_change = df_warm["Biomass_change_pct"].iloc[-1]
    baseline_env_mean = df_monthly["EnvIndex"].iloc[:duration].mean()
    avg_E_change = 100.0 * (df_warm["EnvIndex"].mean() - baseline_env_mean) / (baseline_env_mean + 1e-12)

    # --- Interpretation text
    if avg_pct_change > 5:
        biomass_meaning = (
            "📈 Fish stocks seem to do better in warmer waters — the population grows and stays healthy on average."
        )
    elif avg_pct_change < -5:
        biomass_meaning = (
            "📉 The stock declines under warmer conditions — likely because the water gets too warm for comfort."
        )
    else:
        biomass_meaning = (
            "⚖️ Small temperature changes don’t make much difference — the stock stays relatively stable overall."
        )

    if avg_E_change > 3:
        env_meaning = f"🌡️ Ocean conditions become slightly more favorable — about {avg_E_change:.1f}%  — a small boost in growth potential."
    elif avg_E_change < -3:
        env_meaning = f"🌡️ Ocean conditions become less favorable — around {abs(avg_E_change):.1f}% — warmer water makes things a bit tougher."
    else:
        env_meaning = "🌡️ Ocean conditions stay about the same — no big change from the baseline."


    obs_text = f"""
    <div style="background-color: rgba(0,0,0,0.5); padding: 20px; border-radius:10px; color:#E1EAF2;">
    <h3 style="color:#FFD700">🌍 Warming Scenario Summary (+{delta_T:.1f}°C)</h3>
    <p><b>1️⃣ Squid Population:</b> {biomass_meaning}</p>
    <p><b>2️⃣ Overall Change:</b> On average, biomass changed by {avg_pct_change:.1f}%,
    ending at {final_change:.1f}% compared to the starting levels.  
    In other words, the stock under warming was about 
    <strong>{'higher' if avg_pct_change > 0 else 'lower'}</strong> than the baseline by roughly 
    <strong>{abs(avg_pct_change):.1f}%</strong>.</p>
    <p><b>3️⃣ Ocean Conditions:</b> {env_meaning}</p>
    <p><b>Baseline starting biomass:</b> {N0:,.0f} tons — catchability (q): {q:.2e}</p>
    </div>
    """
    st.markdown(obs_text, unsafe_allow_html=True)

    # --- LaTeX rendering: use st.latex for guaranteed math rendering in Streamlit
    st.markdown("### Calibration check (mass-balance)")
    st.latex(r"N_0 \ge \frac{260000}{0.30} \approx 867000 \ \text{tons}")
    st.markdown("Or in general:")
    st.latex(r"N_0 \ge \frac{\mathrm{max\_catch}}{E_{\mathrm{target}}}")




# ========================================
#  TAB 4: SENSITIVITY & CPUE
# ========================================
elif page == "Sensitivity & CPUE":
    st.header("🎯 Sensitivity & CPUE Relationship")

    df_latest = st.session_state.get("latest_df", None)

    #print(df_latest.columns)

    # --- Check if the raw simulation data is available ---
    if df_latest is None or "CPUE_tons" not in df_latest.columns or "Biomass_mean" not in df_latest.columns:
        st.warning("Please run a biomass simulation first (Baseline or Warming Scenario).")
        st.stop()  # stop the rest of the code from running

    # --- Ensure there’s a proper Date column for time-based plotting ---
    if "Date" not in df_latest.columns and "Year" in df_latest.columns and "Month" in df_latest.columns:
        df_latest["Date"] = pd.to_datetime(df_latest["Year"].astype(str) + "-" + df_latest["Month"].astype(str))

    # --- Compute Biomass mean & CI if missingxs ---
    if "Biomass_mean" not in df_latest.columns:
        df_latest["Biomass_mean"] = df_latest["Biomass"]
        df_latest["Biomass_CI_upper"] = df_latest["Biomass"]
        df_latest["Biomass_CI_lower"] = df_latest["Biomass"]

    # --- Monte Carlo simulation for CPUE (mean + CI) ---
    n_sim = 500
    cpue_sim = np.zeros((len(df_latest), n_sim))
    noise_pct = 0.1  # 10% observation noise
    for i in range(n_sim):
        cpue_sim[:, i] = df_latest["CPUE_tons"] * (1 + np.random.normal(0, noise_pct, size=len(df_latest)))

    df_latest["CPUE_mean"] = cpue_sim.mean(axis=1)
    df_latest["CPUE_CI_upper"] = np.percentile(cpue_sim, 97.5, axis=1)
    df_latest["CPUE_CI_lower"] = np.percentile(cpue_sim, 2.5, axis=1)

    # --- Normalize all indices for plotting ---
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    df_latest["Biomass_mean_index"] = normalize(df_latest["Biomass_mean"])
    df_latest["Biomass_CI_upper_index"] = normalize(df_latest["Biomass_CI_upper"])
    df_latest["Biomass_CI_lower_index"] = normalize(df_latest["Biomass_CI_lower"])

    df_latest["CPUE_mean_index"] = normalize(df_latest["CPUE_mean"])
    df_latest["CPUE_CI_upper_index"] = normalize(df_latest["CPUE_CI_upper"])
    df_latest["CPUE_CI_lower_index"] = normalize(df_latest["CPUE_CI_lower"])

    # --- Compute correlation between CPUE and Biomass ---
    correlation = df_latest["CPUE_mean_index"].corr(df_latest["Biomass_mean_index"])

    # --- Strength interpretation ---
    if abs(correlation) >= 0.7:
        strength = "strong"
    elif abs(correlation) >= 0.4:
        strength = "moderate"
    else:
        strength = "weak"

    # --- Main Time-Series Plot ---
    fig = go.Figure()

    # CPUE mean + CI
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["CPUE_mean_index"],
        mode="lines+markers",
        name="CPUE (mean)",
        line=dict(color="#00BFFF", width=2),
        hovertemplate="Date: %{x}<br>CPUE (mean): %{y:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["CPUE_CI_upper_index"],
        line=dict(color="#00BFFF", dash="dot"),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["CPUE_CI_lower_index"],
        fill='tonexty',
        fillcolor='rgba(0,191,255,0.2)',
        line=dict(color="#00BFFF", dash="dot"),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Biomass mean + CI
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["Biomass_mean_index"],
        mode="lines+markers",
        name="Biomass (mean)",
        line=dict(color="#9932CC", dash="dash", width=2),
        hovertemplate="Date: %{x}<br>Biomass (mean): %{y:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["Biomass_CI_upper_index"],
        line=dict(color="#9932CC", dash="dot"),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=df_latest["Date"],
        y=df_latest["Biomass_CI_lower_index"],
        fill='tonexty',
        fillcolor='rgba(153,50,204,0.2)',
        line=dict(color="#9932CC", dash="dot"),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        title=f"CPUE vs Biomass Index (Correlation = {correlation:.2f}, {strength} relationship)",
        xaxis_title="Time (Years)", yaxis_title="Normalized Index (0–1)",
        height=500,
        template="plotly_dark",
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center")
    )

    st.plotly_chart(fig, width='stretch')

    # --- Optional: Scatter Plot ---
    st.markdown("<br>", unsafe_allow_html=True)
    show_scatter = st.checkbox("Show CPUE vs Biomass scatter relationship", value=False)

    if show_scatter:
        scatter_fig = go.Figure()
        scatter_fig.add_trace(go.Scatter(
            x=df_latest["Biomass_mean_index"],
            y=df_latest["CPUE_mean_index"],
            mode="markers",
            marker=dict(size=8, color="#39FF14", opacity=0.7),
            name="CPUE vs Biomass",
            hovertemplate="Biomass Index: %{x:.2f}<br>CPUE Index: %{y:.2f}<extra></extra>"
        ))

        # Regression line
        m, b = np.polyfit(df_latest["Biomass_mean_index"], df_latest["CPUE_mean_index"], 1)
        scatter_fig.add_trace(go.Scatter(
            x=df_latest["Biomass_mean_index"],
            y=m * df_latest["Biomass_mean_index"] + b,
            mode="lines",
            line=dict(color="#FFD700", dash="dot"),
            name="Trend line"
        ))

        scatter_fig.update_layout(
            title="Scatter Relationship between CPUE and Biomass",
            xaxis_title="Biomass Index (0–1)",
            yaxis_title="CPUE Index (0–1)",
            template="plotly_dark",
            height=400,
        )

        st.plotly_chart(scatter_fig, width='stretch')

    # --- Observations & Caption ---
    st.markdown("<br>", unsafe_allow_html=True)

    if correlation > 0.5:
        obs = "CPUE and biomass move together 📈 — higher catches tend to coincide with higher stock levels."
    elif correlation < -0.5:
        obs = "CPUE and biomass diverge ⚠️ — catch rates may not reflect actual stock abundance."
    else:
        obs = "CPUE and biomass show a weak relationship ⚖️ — other factors might influence catch rates."
    
    with st.expander("📊 Understanding CPUE and Biomass Correlation", expanded=False):
        st.markdown(
            """
            <div style='color: #39FF14; font-size:16px; background-color:rgba(0,0,0,0.5);
                        padding:15px; border-radius:10px;'>
            🎣 <b>Catch Per Unit Effort (CPUE)</b> shows how much squid is caught for each day a vessel spends fishing.  
            It’s a simple way to see how easy (or hard) it is to find and catch squid over time.

            <br><br>
            🔼 When CPUE and biomass move in the <b>same direction</b> (both rise or both fall),  
            it means the fishing data reflects what’s really happening in the ocean.  
            In other words, when there are more squid, boats catch more — and when there are fewer, they catch less.

            <br><br>
            ⚖️ When CPUE and biomass don’t move together (a <b>weak link</b>),  
            it may mean fishers are adapting — for example, finding new hotspots or using better gear —  
            so their catches stay steady even if the overall squid population changes.

            <br><br>
            🔻 If CPUE goes up while biomass goes down,  
            it might mean boats are concentrating in the last dense areas of squid,  
            giving the <i>illusion</i> that the stock is healthy when it’s actually declining.  
            This can happen when squid gather tightly or when fishing becomes more efficient.

            <br><br>
            🌊 <b>In short:</b>  
            • A <b>strong positive link</b> → catches truly reflect abundance.  
            • A <b>weak or negative link</b> → fishing strategies or technology may be masking real changes in the stock.
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        f"""
        <div style="
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px 25px;
            border-radius: 10px;
            margin-top: 15px;
            color: #E1EAF2;
            font-size: 20px;
            line-height: 1.6;
        ">
        {obs}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Store updated dataframe back to session_state ---
    st.session_state["latest_df"] = df_latest

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


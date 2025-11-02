# ---------------- Standard Library ----------------
import base64
import io
import json
import time
import os
import sys
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

# ---------------- Local/Project Imports ----------------

# Ensure Python can find the 'utils' folder
current_dir = os.path.dirname(os.path.abspath(__file__))      # folder containing app.py
utils_dir = os.path.join(current_dir, "utils")                # path to utils/
sys.path.insert(0, utils_dir)                                 # add utils/ to import search path

from utils.data_utils import (
    load_model_data,
    get_model_colors,
    load_prediction_data,
    load_residual_data,
    load_monthly_cpue,
    load_observed_vs_standardized
)
# Define assets folder
assets_dir = os.path.join(current_dir, "assets")

#from utils.plots_utils import plot_predictions  # wherever you put it

# ---------------------- Page Configuration ----------------------
st.set_page_config(page_title="CPUE Model Evaluation Dashboard", layout="wide")



# ---------------------- Custom CSS ----------------------
st.markdown("""
<style>

/* ---------------------- Sidebar ---------------------- */
/* Sidebar background image + navy overlay */
[data-testid="stSidebar"] > div:first-child {
    position: fixed; /* 🧭 Keeps sidebar fixed in place */
    top: 0;
    left: 0;
    bottom: 0;
    overflow-y: auto; /* 🧭 Sidebar scrolls independently */
    background-image: url("https://thumbs.dreamstime.com/b/underwater-seascape-ocean-coral-reef-deep-sea-bottom-swimming-under-water-marine-corals-background-vector-seaweed-algae-354608779.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    width: inherit;
    min-height: 100vh;
    color: #E1EAF2;
    padding-top: 1rem !important;
}
[data-testid="stSidebar"] > div:first-child::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 31, 63, 0.6);
    z-index: 0;
}
[data-testid="stSidebar"] > div:first-child > * {
    position: relative;
    z-index: 1;
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

/* ---------------------- Main panel ---------------------- */
/* Background image + overlay */
.stApp {
    position: relative;
    background-image: url("https://images.unsplash.com/photo-1530951980629-fbeef86f69a1q=80&w=2768&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
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

/* 🧭 Make main content scrollable while sidebar stays fixed */
.block-container {
    overflow-y: auto !important;
    height: 100vh !important;
    padding-top: 4rem !important;
    padding-bottom: 2rem !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* 🧭 Ensure main panel starts beside sidebar */
section[data-testid="stSidebar"] + div {
    margin-left: 18rem; /* Adjust to your sidebar width */
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


# ---------------------- Sidebar ----------------------
# ---------------- Page Selection ----------------
page = st.sidebar.radio("Select page", tabs, label_visibility="collapsed")
st.session_state.page = page


# ---------------- Initialize Session State ----------------
if "notes" not in st.session_state:
    st.session_state.notes = {tab: [] for tab in tabs if tab != "Logbook"}

if "note_input" not in st.session_state:
    st.session_state.note_input = ""

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {"active": False, "tab": None, "index": None}

if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = {}

if "notes_expanded" not in st.session_state:
    st.session_state.notes_expanded = False  # collapsed by default

# if "all_notes_text" not in st.session_state:
#     st.session_state["all_notes_text"] = ""


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
            note_text = st.text_area(
                "Write your note here:",
                value=st.session_state.note_input,
                key="note_input",
                height=150,
                placeholder="Type your note..."
            )

            # 💾 Save Button
            if st.button("💾 Save Note", key=f"save_{page}"):
                content = st.session_state.note_input.strip()
                if content:
                    # If editing an existing note
                    if (
                        st.session_state.edit_mode["active"]
                        and st.session_state.edit_mode["tab"] == page
                    ):
                        idx = st.session_state.edit_mode["index"]
                        st.session_state.notes[page][idx] = content
                        st.toast(f"✏️ Note updated in {page}!", icon="✏️")
                        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
                    else:
                        st.session_state.notes[page].append(content)
                        st.toast(f"✅ Note saved to {page}!")
                else:
                    st.toast("⚠️ Nothing to save (note is empty).")

    # 🔹 Keep expander open if user is editing or typing
    st.session_state.notes_expanded = (
        bool(st.session_state.note_input.strip())
        or st.session_state.edit_mode["active"]
    )


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
                        st.markdown(f"- {note}")

                    with col2:
                        # ✏️ Edit button
                        if st.button("✏️", key=f"edit_{tab_name}_{i}"):
                            st.session_state.note_input = note
                            st.session_state.edit_mode = {
                                "active": True,
                                "tab": tab_name,
                                "index": i,
                            }
                            st.toast(f"✏️ Go back to **{tab_name}** tab to edit this note.")

                    with col3:
                        # 🗑 Delete button
                        delete_key = f"{tab_name}_{i}"
                        if not st.session_state.delete_confirm.get(delete_key, False):
                            if st.button("🗑", key=f"delete_{tab_name}_{i}"):
                                st.session_state.delete_confirm[delete_key] = True
                        else:
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("✅", key=f"confirm_del_{tab_name}_{i}"):
                                    del st.session_state.notes[tab_name][i]
                                    st.session_state.delete_confirm.pop(delete_key, None)
                                    st.toast(f"🗑 Deleted note {i+1} from {tab_name}")
                                    st.rerun()
                            with c2:
                                if st.button("❌", key=f"cancel_del_{tab_name}_{i}"):
                                    st.session_state.delete_confirm[delete_key] = False


    

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
                all_notes_text += "\n".join(f"- {n}" for n in notes) + "\n\n"

        st.session_state.all_notes_text = all_notes_text
        st.success("✅ Logbook is ready to download!")

    # --- Step 2: Show download button only if content exists ---
    if "all_notes_text" in st.session_state and st.session_state.all_notes_text:
        buffer = io.BytesIO(st.session_state.all_notes_text.encode("utf-8"))
        st.download_button(
            label="📥 Download Logbook (.txt)",
            data=buffer,
            file_name="logbook.txt",
            mime="text/plain",
            key="logbook_download"
        )

    # 📤 Send to Host Section (appears after download)
    
    # --- Define the function ---
    def send_notes_to_host(all_notes_text):
        try:
            # Authenticate with Google Sheets
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],  scopes=["https://www.googleapis.com/auth/spreadsheets"])
            client = gspread.authorize(creds)

            # Open the target sheet by ID (no need for an extra ["google_sheets"] key)
            sheet = client.open_by_key("1mLnW5UHnRU8Cs5tD1NKtvr-ODlFPdFOoZi0lqXTEj10").sheet1

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
                    all_notes_text += "\n".join(f"- {note}" for note in notes) + "\n"
            
            # Send to Google Sheets
            success = send_notes_to_host(all_notes_text)

            if success:
                st.success("✅ Your notes (including final observation) were sent successfully and remain anonymous. Thank you for contributing!")
            else:
                st.error("❌ Failed to send notes. Please try again later.")

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

# ---------------------- Page Content ----------------------
if page == "Overview":
    #st.image("assets/animated_catch.gif", use_column_width=True)
    #st.video('assets/animated_catch.mp4', use_column_width=True, format='video/mp4', start_time=0, loop=True)
#     video_file = open('assets/animated_catch.mp4', 'rb').read()
#     video_html = f"""
#     <div style="height:800px; overflow:hidden; position:relative;">
#       <video autoplay loop muted playsinline style="width:100%; height:auto; position:absolute; top:-40px;">
#         <source src="data:video/mp4;base64,{base64.b64encode(video_file).decode()}" type="video/mp4">
#       </video>
#     </div>
# """
#     st.markdown(video_html, unsafe_allow_html=True)

    @st.cache_resource
    def load_video(path: str):
        """Read and encode video once per session."""
        with open(path, "rb") as f:
            video_bytes = f.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        return video_b64

    video_path = os.path.join(assets_dir, "animated_catch.mp4")


    # with open(video_path, 'rb') as f:
    #     video_file = f.read()
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
  
  

    # 🔻 Inserted CPUE color key markdown
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; color: #000;">
    <strong>Catch Classification Per Location (based on 2000–2020 data):</strong><br>
    <em>Catch levels are grouped automatically into low, medium, and high categories based on the overall data distribution from 2000–2020.</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("🎣 CPUE Standardization – Model Summary")
    st.markdown("""
    **Objective:**
    Standardize Monthly CPUE using environmental and spatiotemporal covariates to remove external influences, enabling fair comparison across years for trend analysis and stock assessment.

    **Approaches Explored:**
    - Log-transformed Generalized Additive Models (GAMs)
    - Raw CPUE using Gamma and Tweedie distributions
    - Cross-validation and residual diagnostics
""")
    
    st.markdown("---")
    
    st.markdown(
    """
    <div style='color:red; font-weight:bold; font-size:20px; text-align:Justify; margin-top:10px;'>
    💡 Note: The animated map above displays <b>catch in kilograms (kg)</b> for finer spatial resolution,<br>
    while all model evaluation results in later tabs are expressed in <b>tons (t)</b> for clarity and comparability.
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("---")

    # ⚓ Centered title
    st.markdown(
        "<h3 style='text-align: center; color: #E1EAF2;'>⚓ Continue Your Journey</h3>",
        unsafe_allow_html=True
    )

    # 💬 Justified body with both working links
    html_links = """
    <div style="text-align: center; color: #E1EAF2; font-size: 20px; line-height: 1.6;">
    If you'd like to learn more about the methods, models, and datasets used in this stage of the voyage:<br>
    👉 <a href="https://github.com/Euchie23/SquidStock/tree/main/notebooks/CPUE_Standardization_%26_Prediction" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration: underline;">View the CPUE Standardization Project README</a><br><br>
    Or, explore the entire <b>SquidStock Expedition</b> — see how this stage connects to the full storyline:<br>
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


    # Initialize session state for the "coming soon" click
    if "show_warning" not in st.session_state:
        st.session_state.show_warning = False
    
    # Panel with description
    st.markdown("""
    <div style="
        background-color: rgba(10, 47, 68, 0.7);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: #FFD700;
        font-size: 18px;
        margin-top: 2rem;
    ">
        🐙 <b>Next Stage:</b> Ocean Dynamics – Surplus Production & Biomass Estimation<br>
        Simulate squid biomass under climate warming scenarios using SST, SSH, and Chl-a drivers.
    </div>
    """, unsafe_allow_html=True)
    
    # Spacer
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Show warning if link clicked
    if st.session_state.show_warning:
        st.warning("⚠️ This app is under construction. Check back soon!")
    
    # Create the clickable link as a button
    if st.button("🌊 Visit Ocean Dynamics (Coming Soon)"):
        st.session_state.show_warning = True
        st.experimental_rerun()  # re-run to show the warning above the button

    
        
    st.markdown("</div>", unsafe_allow_html=True)


    


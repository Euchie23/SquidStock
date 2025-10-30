import os
import sys
import streamlit as st
import numpy as np
import pandas as pd
import base64
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
# Ensure Python can find the 'utils' folder
current_dir = os.path.dirname(os.path.abspath(__file__))      # folder containing app.py
utils_dir = os.path.join(current_dir, "utils")                # path to utils/
sys.path.insert(0, utils_dir)                                 # add utils/ to import search path

from data_utils import (
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
    /* --- Sidebar background with coral image + navy transparent overlay --- */
    [data-testid="stSidebar"] > div:first-child {
        position: relative;
        background-image: url("https://thumbs.dreamstime.com/b/underwater-seascape-ocean-coral-reef-deep-sea-bottom-swimming-under-water-marine-corals-background-vector-seaweed-algae-354608779.jpg");
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;
        min-height: 100vh;
        color: #E1EAF2;
    }
    [data-testid="stSidebar"] > div:first-child::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba(0, 31, 63, 0.6); /* navy transparent */
        z-index: 0;
    }
    [data-testid="stSidebar"] > div:first-child > * {
        position: relative;
        z-index: 1;
    }

    /* --- Main app background with deep sea image + navy transparent overlay --- */
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
        background-color: rgba(10, 47, 68, 0.7); /* navy transparent */
        z-index: 0;
    }
    .stApp > * {
        position: relative;
        z-index: 1;
    }

    /* --- Top bar background color navy --- */
    header, .css-nahz7x {
        background-color: #001f3f !important;
    }
.sidebar-footer {
        position: absolute;
        bottom: 10px;
        width: 100%;
        padding: 10px;
    }
/* --- Custom font sizes and UI tweaks --- */
/* General text, captions, and markdown (main page + sidebar) */
.stMarkdown, .stMarkdown p, .stCaption, .stSidebar p, .stSidebar ul, .stSidebar li {
        font-size: 18px !important;
        color: #E1EAF2 !important;
        line-height: 1.6 !important;
    }

/* Sidebar titles and headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #39FF14 !important;
    }

/* Main page titles */
h1, .stTitle {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #39FF14 !important;
    }

/* Tabs */
.stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        color: #E1EAF2 !important;
    }

.stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #FFD700 !important;
        border-bottom: 3px solid #FFD700 !important;
    }

/* Sidebar radio buttons (for “Sections”) */
[data-testid="stSidebar"] label {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #E1EAF2 !important;
    }

/* Links in sidebar contact block */
[data-testid="stSidebar"] a {
        font-size: 18px !important;
        color: #39FF14 !important;
    }
/* --- Sidebar spacing + font sizes --- */
[data-testid="stSidebar"] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
            
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    margin-top: 4px !important;  /* smaller than default */
}
            
/* --- Main page padding fix --- */
.block-container {
    padding-top: 4rem !important;    /* pushes content lower */
    padding-bottom: 2rem !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}
            
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-size: 26px !important;
        font-weight: 800 !important;
        color: #39FF14 !important;
        margin-top: 0 !important;
    }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] a, [data-testid="stSidebar"] li {
        font-size: 18px !important;
        line-height: 1.6 !important;
    }

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem !important; /* small top space */
}

/* --- Make st.dataframe() more readable without breaking layout --- */
[data-testid="stDataFrame"] {
    width: 100% !important;
    margin-bottom: 1.5rem !important;
}

[data-testid="stDataFrame"] table {
    font-size: 17px !important;
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
    </style>
""", unsafe_allow_html=True)

# ---------------------- Sidebar Navigation ----------------------
st.sidebar.title(" 🧭 Course Correction")
page = st.sidebar.radio("Sections", [
    "Overview",
    "Model Comparison",
    "Evaluation Metrics",
    "Residual Analysis",
    "Predictions"
])

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

  

    video_path = os.path.join(assets_dir, "animated_catch.mp4")


    with open(video_path, 'rb') as f:
        video_file = f.read()
    
    video_html = f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 0;       /* remove extra top space */
        margin-bottom: 10px; /* keep small gap below */
        width: 100%;
    ">
        <video 
            autoplay 
            loop 
            muted 
            playsinline 
            style="
                width: 100%;          /* expand almost full container */
                max-width: 1600px;   /* allow bigger video */
                height: auto;
                border-radius: 12px;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
            "
        >
            <source src="data:video/mp4;base64,{base64.b64encode(video_file).decode()}" type="video/mp4">
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
    
    st.markdown(
    """
    <div style='color:red; font-weight:bold; text-align:center; margin-top:10px;'>
    💡 Note: The animated map above displays <b>catch in kilograms (kg)</b> for finer spatial resolution,<br>
    while all model evaluation results in later tabs are expressed in <b>tons (t)</b> for clarity and comparability.
    </div>
    """,
    unsafe_allow_html=True
)

    # 🌐 Additional links section (justified text with clickable links)
    st.markdown("""
    <hr style="border: 1px solid rgba(255,255,255,0.2); margin-top: 2rem; margin-bottom: 1rem;">
    
    <div style="
        background-color: rgba(0, 31, 63, 0.6);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: justify;
        color: #E1EAF2;
        font-size: 18px;
        line-height: 1.6;
    ">
        <p>⚓ <b>Continue Your Journey</b></p>
    
        <p>If you'd like to learn more about the methods, models, and datasets used in this stage of the voyage:</p>
        <p>👉 <a href="https://github.com/Euchie23/SquidStock/tree/main/App/CPUE_Standardization_%26_Prediction" 
           target="_blank" style="color:#39FF14; font-weight:bold; text-decoration: underline;">
           View the CPUE Standardization Project README
        </a></p>
    
        <p>Or, explore the entire <b>SquidStock Expedition</b> — see how this stage connects to the full storyline:</p>
        <p>🌊 <a href="https://github.com/Euchie23/SquidStock" 
           target="_blank" style="color:#FFD700; font-weight:bold; text-decoration: underline;">
           Visit the Main Repository
        </a></p>
    </div>
    """, unsafe_allow_html=True)




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


    # 🔹 Link to next app: Ocean Dynamics (Biomass Estimation)
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
        🐙 Next Stage: <b>Ocean Dynamics – Surplus Production & Biomass Estimation</b><br>
        Simulate squid biomass under climate warming scenarios using SST, SSH, and Chl‑a drivers.<br><br>
    """, unsafe_allow_html=True)
    
    # Streamlit button for “Coming Soon”
    if st.button("Visit this app (Coming Soon)"):
        st.warning("⚠️ This app is under construction. Check back soon!")
    
    st.markdown("</div>", unsafe_allow_html=True)

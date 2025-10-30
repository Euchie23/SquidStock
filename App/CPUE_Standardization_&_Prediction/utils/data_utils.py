import os
import pandas as pd
import numpy as np
import streamlit as st

# --- Define paths ---
current_dir = os.path.dirname(__file__)              # folder containing this script
assets_dir = os.path.join(current_dir, "..", "assets")  # go up one folder, then into assets

# --- Load model summaries ---
def load_model_data():
    try:
        model_summary = pd.read_csv(os.path.join(assets_dir, "model_summary.csv"))
        cv_results = pd.read_csv(os.path.join(assets_dir, "cv_results.csv"))
        test_results = pd.read_csv(os.path.join(assets_dir, "eval_results.csv"))
    except FileNotFoundError:
        model_summary = pd.DataFrame()
        cv_results = pd.DataFrame()
        test_results = pd.DataFrame()
    return model_summary, cv_results, test_results


# --- Model color palette ---
def get_model_colors():
    return {
        "Actual": "#1f77b4",
        "Predicted (LinearGAM_log_CPUE_plus_c)": "#ff7f0e",
        "Predicted (LinearGAM_log_CPUE_plus_1)": "#2ca02c",
        "Predicted (GammaGAM_CPUE)": "#d62728",
        "Predicted (TweedieRegressor_CPUE)": "#9467bd",
    }


# --- Monthly CPUE loader ---
def load_monthly_cpue():
    try:
        df = pd.read_csv(os.path.join(assets_dir, "Monthly_CPUE_summary.csv"))

        # Convert numeric month to month name (1 → January)
        if "Month" in df.columns:
            df["Month"] = pd.to_datetime(df["Month"], format="%m").dt.strftime("%B")

        return df

    except FileNotFoundError:
        return pd.DataFrame(columns=["Month", "Year", "CPUE_vday_tons"])


# --- Observed vs standardized data ---
def load_observed_vs_standardized():
    try:
        merged = pd.read_csv(os.path.join(assets_dir, "observed_vs_standardized.csv"))
        colors = {
            "Observed": "#1f77b4",
            "Standardized_log_cpueC": "#ff7f0e",
            "Standardized_log_cpue1": "#2ca02c",
            "Standardized_CPUE_GammaGAM": "#d62728",
            "Standardized_CPUE_tweedieRegressor": "#9467bd",
        }
        return merged, colors
    except FileNotFoundError:
        return pd.DataFrame(), {}


# --- Residuals data loader ---
def load_residual_data():
    try:
        data_path = os.path.join(assets_dir, "residuals_data_clean.npz")
        data = np.load(data_path, allow_pickle=True)
        return data["residual_dict"].item()
    except Exception as e:
        print("Error loading cleaned residuals_data:", e)
        return {}


# --- Prediction data loader ---
def load_prediction_data():
    try:
        data_path = os.path.join(assets_dir, "prediction_data_clean.npz")
        data = np.load(data_path, allow_pickle=True)
        return data["pred_dict"].item(), data["color_dict"].item()
    except Exception as e:
        print("Error loading cleaned prediction_data:", e)
        return {}, {}

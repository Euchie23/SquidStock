import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)  # points to App/AutoML
DATA_PATH = os.path.join(BASE_DIR, "data", "weekly_processed.csv")

def load_weekly_dataset():
"""Loads your cleaned dataset."""
     return pd.read_csv(DATA_PATH)

# FINAL_FEATURES = [
# "Year", "WeekOfYear",
# "Avg_weekly_Lat", "Avg_weekly_Lon",
# "Avg_weekly_WaterTemp_2wk", "Avg_weekly_WaterTemp_3wk",
# "Avg_weekly_Depth_2wk", "Avg_weekly_Depth_3wk",
# "Chlor_a_mg_m3_5wk", "SSH_5wk",
# "sin_week", "cos_week",
# "Temp_x_Depth", "Temp_x_Chlor",
# "Depth_x_Chlor", "Temp_x_SSH"
# ]

def build_feature_row(df_weekly, week_index, overrides=None):
    """Takes a row + applies environmental slider overrides + recomputes interactions."""
    row = df_weekly.iloc[week_index].copy()

    if overrides:
        for k, v in overrides.items():
            if k in row:
                row[k] = v

    # Recompute interactions
    row["Temp_x_Depth"] = row["Avg_weekly_WaterTemp_3wk"] * row["Avg_weekly_Depth_3wk"]
    row["Temp_x_Chlor"] = row["Avg_weekly_WaterTemp_3wk"] * row["Chlor_a_mg_m3_5wk"]
    row["Depth_x_Chlor"] = row["Avg_weekly_Depth_3wk"] * row["Chlor_a_mg_m3_5wk"]
    row["Temp_x_SSH"]   = row["Avg_weekly_WaterTemp_3wk"] * row["SSH_5wk"]

    return row[FINAL_FEATURES].to_frame().T

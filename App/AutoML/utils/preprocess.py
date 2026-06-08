# preprocess.py
from pathlib import Path
import pandas as pd

def load_weekly_dataset():
    # __file__ is preprocess.py
    root = Path(__file__).resolve().parents[1]  # goes up 2 levels: utils -> AutoML
    data_path = root / "data" / "weekly_processed.csv"
    return pd.read_csv(data_path)


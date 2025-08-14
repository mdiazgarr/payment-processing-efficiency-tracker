import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .config import RAW_FILE

def load_raw_transactions() -> pd.DataFrame:
    # Load the raw CSV from Kaggle (PaySim)
    df = pd.read_csv(RAW_FILE)

    # Simulate datetime columns from 'step' (hours since simulation start)
    base_date = datetime(2023, 1, 1)
    df["transaction_started_at"] = df["step"].apply(
        lambda x: base_date + timedelta(hours=int(x))
    )

    # Random processing delay 1–120 seconds
    df["transaction_completed_at"] = df["transaction_started_at"] + pd.to_timedelta(
        np.random.randint(1, 120, size=len(df)), unit="s"
    )

    # Simulate status: failed if fraud, success otherwise
    df["status"] = np.where(df["isFraud"] == 1, "failed", "success")

    return df

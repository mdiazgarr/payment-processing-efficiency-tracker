import pandas as pd
from typing import Tuple, Optional
from .config import (
    CLEAN_FILE, PROC_DIR,
    CANDIDATE_START_COLS, CANDIDATE_END_COLS, CANDIDATE_STATUS_COLS
)

def _first_present(df: pd.DataFrame, candidates) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None

def infer_core_columns(df: pd.DataFrame) -> Tuple[str, str, str]:
    start_col = _first_present(df, CANDIDATE_START_COLS)
    end_col   = _first_present(df, CANDIDATE_END_COLS)
    status_col= _first_present(df, CANDIDATE_STATUS_COLS)
    if not all([start_col, end_col, status_col]):
        raise ValueError(f"Could not infer core columns. Found start={start_col}, end={end_col}, status={status_col}.")
    return start_col, end_col, status_col

def compute_processing_time(df: pd.DataFrame, start_col: str, end_col: str) -> pd.DataFrame:
    df = df.copy()
    df[start_col] = pd.to_datetime(df[start_col], errors="coerce", utc=True)
    df[end_col]   = pd.to_datetime(df[end_col], errors="coerce", utc=True)
    df["processing_time_secs"] = (df[end_col] - df[start_col]).dt.total_seconds()
    return df

def create_status_flags(df: pd.DataFrame, status_col: str,
                        success_values=("success","approved","completed","ok","paid"),
                        fail_values=("failed","declined","error","timeout","canceled","cancelled","chargeback")) -> pd.DataFrame:
    df = df.copy()
    status_norm = df[status_col].astype(str).str.lower().str.strip()
    df["is_failed"]  = status_norm.isin(set(fail_values)).astype(int)
    df["is_success"] = status_norm.isin(set(success_values)).astype(int)
    return df

def create_delay_flag(df: pd.DataFrame, pt_col: str = "processing_time_secs",
                      success_flag_col: str = "is_success", quantile: float = 0.90) -> pd.DataFrame:
    df = df.copy()
    q = df.loc[df[success_flag_col] == 1, pt_col].quantile(quantile)
    df["is_delayed"] = ((df[pt_col] > q) & (df[success_flag_col] == 1)).astype(int)
    df.attrs["delay_threshold_secs"] = float(q) if pd.notnull(q) else None
    return df

def basic_sanity_filters(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # keep between 0s and 24h
    df = df[df["processing_time_secs"].between(0, 24*3600, inclusive="both")]
    return df

def save_clean(df: pd.DataFrame, path=CLEAN_FILE):
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

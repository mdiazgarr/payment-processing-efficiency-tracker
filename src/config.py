from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"

RAW_FILE = RAW_DIR / "transactions.csv"           # your Kaggle CSV (renamed)
CLEAN_FILE = PROC_DIR / "transactions_clean.parquet"

# we simulate these columns in data_loader.py
CANDIDATE_START_COLS = ["transaction_started_at"]
CANDIDATE_END_COLS   = ["transaction_completed_at"]
CANDIDATE_STATUS_COLS= ["status"]
CANDIDATE_AMOUNT_COLS= ["amount"]

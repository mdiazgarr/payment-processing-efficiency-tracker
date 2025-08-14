#!/usr/bin/env python
from src.data_loader import load_raw_transactions
from src.preprocess import (
    infer_core_columns, compute_processing_time,
    create_status_flags, create_delay_flag,
    basic_sanity_filters, save_clean
)
from src.config import CLEAN_FILE

def main():
    df = load_raw_transactions()

    # quick EDA prints
    print("Columns:", list(df.columns)[:20])
    print(df.dtypes.head(15))
    print("NA ratio (top 15):")
    print(df.isna().mean().sort_values(ascending=False).head(15))

    start_col, end_col, status_col = infer_core_columns(df)
    print(f"Inferred -> start: {start_col} | end: {end_col} | status: {status_col}")

    df = compute_processing_time(df, start_col, end_col)
    df = create_status_flags(df, status_col)
    df = create_delay_flag(df, pt_col="processing_time_secs", success_flag_col="is_success", quantile=0.90)
    df = basic_sanity_filters(df)

    print(df[["processing_time_secs","is_success","is_failed","is_delayed"]].head())
    save_clean(df, CLEAN_FILE)
    print(f"✅ Clean data saved to {CLEAN_FILE} | shape={df.shape}")

if __name__ == "__main__":
    main()

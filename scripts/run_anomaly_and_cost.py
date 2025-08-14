def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", default="1H")
    parser.add_argument("--contamination", type=float, default=0.02)
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()

    # --- Robust column-projected read ---
    wanted = ["transaction_started_at", "is_failed", "is_delayed", "amount"]
    try:
        # Get all columns once (cheap metadata read with pyarrow; falls back if needed)
        all_cols_df = pd.read_parquet(CLEAN_FILE, engine="pyarrow")
        all_cols = list(all_cols_df.columns)
        use_cols = [c for c in wanted if c in all_cols]
        if args.fast and use_cols:
            df = pd.read_parquet(CLEAN_FILE, columns=use_cols, engine="pyarrow")
        else:
            df = all_cols_df  # already loaded
    except Exception:
        # Fallback: just read whole file
        df = pd.read_parquet(CLEAN_FILE)

    # --- Hourly aggregate → anomalies → costs ---
    hourly = hourly_aggregate(df, ts_col="transaction_started_at", bucket=args.bucket)
    scored = score_anomalies(hourly, contamination=args.contamination)
    out_path = REPORTS / "anomaly_scores.csv"
    scored.to_csv(out_path, index=False)

    if "amount" in df.columns:
        lost_rev = df.loc[df["is_failed"] == 1, "amount"].sum() * (1 - ASSUMED_RECOVERY_RATE)
    else:
        lost_rev = None
    delay_cost = float(df["is_delayed"].sum()) * ASSUMED_DELAY_COST_PER_TXN

    print(f"✅ Saved anomalies: {out_path}")
    print(f"💸 Estimated lost revenue (failed): {lost_rev if lost_rev is not None else 'N/A'}")
    print(f"⏱️ Estimated delay cost: {delay_cost:.2f}")

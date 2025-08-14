#!/usr/bin/env python
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import pandas as pd
from src.config import CLEAN_FILE
from src.analysis import by_segment_rates, time_of_day_rate
from src.viz import plot_rate_by_hour, bar_top_segments

REPORTS = ROOT / "reports"
FIGS = REPORTS / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

def maybe_sample(df: pd.DataFrame, frac=0.05, seed=42):
    # sample for faster plotting (5% default)
    return df.sample(frac=frac, random_state=seed) if len(df) > 1_000_000 else df

def main():
    df = pd.read_parquet(CLEAN_FILE)

    # optional: downsample for speed when plotting
    df_small = maybe_sample(df, frac=0.03)  # ~3%

    # by type (in PaySim, 'type' is transfer/cash_out/etc.)
    if "type" in df_small.columns:
        seg = by_segment_rates(df_small, "type")
        seg.to_csv(REPORTS / "kpi_by_type.csv", index=False)
        bar_top_segments(seg, segment="type", top_n=10, metric="failure_rate",
                         save_path=FIGS / "top_type_by_failure_rate.png")
        bar_top_segments(seg, segment="type", top_n=10, metric="delay_rate",
                         save_path=FIGS / "top_type_by_delay_rate.png")

    # hour-of-day
    hourly = time_of_day_rate(df_small, start_col="transaction_started_at")
    hourly.to_csv(REPORTS / "kpi_by_hour.csv", index=False)
    plot_rate_by_hour(hourly, rate_col="failure_rate", save_path=FIGS / "failure_rate_by_hour.png")
    plot_rate_by_hour(hourly, rate_col="delay_rate", save_path=FIGS / "delay_rate_by_hour.png")

    print("✅ KPIs saved to reports/, charts saved to reports/figures/")

if __name__ == "__main__":
    main()

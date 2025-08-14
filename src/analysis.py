import pandas as pd

def by_segment_rates(df: pd.DataFrame, segment: str) -> pd.DataFrame:
    if segment not in df.columns:
        raise KeyError(f"Segment '{segment}' not in dataframe.")
    g = df.groupby(segment).agg(
        n=("is_failed", "size"),
        failure_rate=("is_failed", "mean"),
        delay_rate=("is_delayed", "mean"),
        avg_processing_secs=("processing_time_secs", "mean"),
    ).reset_index()
    return g.sort_values(["failure_rate", "delay_rate"], ascending=False)

def time_of_day_rate(df: pd.DataFrame, start_col="transaction_started_at") -> pd.DataFrame:
    tmp = df.copy()
    tmp[start_col] = pd.to_datetime(tmp[start_col], errors="coerce")
    tmp["hour"] = tmp[start_col].dt.hour
    g = tmp.groupby("hour").agg(
        n=("is_failed", "size"),
        failure_rate=("is_failed", "mean"),
        delay_rate=("is_delayed", "mean"),
        avg_processing_secs=("processing_time_secs", "mean"),
    ).reset_index().sort_values("hour")
    return g

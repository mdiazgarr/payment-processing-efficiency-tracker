import pandas as pd
from sklearn.ensemble import IsolationForest

def bucket_and_score(
    df: pd.DataFrame,
    dt_col: str = "transaction_started_at",
    bucket: str = "1H",
    contamination: float = 0.03
) -> pd.DataFrame:
    tmp = df.copy()
    tmp[dt_col] = pd.to_datetime(tmp[dt_col], errors="coerce", utc=True)
    ts = tmp.set_index(dt_col).sort_index()
    agg = ts.resample(bucket).agg(
        n=("is_failed", "size"),
        failure_rate=("is_failed", "mean"),
        delay_rate=("is_delayed", "mean")
    ).dropna()

    features = agg[["failure_rate", "delay_rate"]].fillna(0)
    model = IsolationForest(random_state=42, contamination=contamination)
    agg["anomaly"] = (model.fit_predict(features) == -1).astype(int)
    return agg.reset_index()


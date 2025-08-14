import pandas as pd
import matplotlib.pyplot as plt

def plot_rate_by_hour(hour_df: pd.DataFrame, rate_col: str = "failure_rate", save_path=None):
    plt.figure()
    plt.plot(hour_df["hour"], hour_df[rate_col], marker="o")
    plt.title(f"{rate_col} by hour")
    plt.xlabel("Hour of day")
    plt.ylabel(rate_col)
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.show()

def bar_top_segments(df: pd.DataFrame, segment: str, top_n=10, metric="failure_rate", save_path=None):
    top = df.nlargest(top_n, metric)
    plt.figure()
    plt.bar(top[segment].astype(str), top[metric])
    plt.title(f"Top {top_n} {segment} by {metric}")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(metric)
    plt.grid(True, axis="y")
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.show()

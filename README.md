# Payment Processing Efficiency Tracker

Detecting failed and delayed transactions in payment systems, estimating their cost, and surfacing insights through anomaly detection and visual analytics.

---

## Why it matters
Failed or delayed payments directly impact user trust, increase support costs, and reduce transaction volume.  
By systematically detecting and analyzing inefficiencies, businesses can:
- Reduce operational costs  
- Improve customer experience  
- Prioritize infrastructure and fraud-prevention investments  

---

## Project Overview

This project follows a complete data science workflow:

1. **EDA** – Explore transaction patterns, check missing values, and detect anomalies in processing times.  
2. **Feature Engineering** – Parse timestamps, compute processing times, flag failed vs delayed transactions.  
3. **Modeling & Anomaly Detection** – Use statistical thresholds and ML (Isolation Forest) to detect unusual spikes in failures/delays.  
4. **Evaluation & Cost Estimation** – Quantify potential revenue impact from inefficiencies.  
5. **Visualization** – Generate charts for KPIs, delay/failure trends, and anomaly periods.

---

## Tech Stack

- **Python**: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `pyarrow`  
- **Jupyter Notebooks** for exploration  
- **Git/GitHub** for version control and collaboration  

---

## Repo Structure

```
.
├── data/
│   ├── raw/               # raw CSV datasets
│   └── processed/         # cleaned parquet files (ignored in git)
├── notebooks/             # exploratory analysis
├── reports/
│   ├── figures/           # charts & plots
│   ├── anomaly_scores.csv # anomaly detection results
│   ├── kpi_by_hour.csv
│   └── kpi_by_type.csv
├── scripts/
│   ├── run_pipeline.py            # load + clean + process transactions
│   ├── compute_kpis_and_charts.py # generate KPIs and charts
│   └── run_anomaly_and_cost.py    # anomaly detection & cost estimation
├── src/
│   ├── data_loader.py
│   ├── preprocess.py
│   ├── analysis.py
│   ├── viz.py
│   ├── modeling.py
│   └── config.py
├── requirements.txt
└── README.md
```

---

## Setup (Quickstart)

### Prerequisites
- Python ≥ 3.10  
- Git  
- (Optional) Conda or `venv` for isolated environments  

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/payment-processing-efficiency-tracker.git
cd payment-processing-efficiency-tracker
```

### 2. Create & activate a virtual environment

**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Features & Flags

The pipeline produces a **clean transactions dataset** with these key engineered columns:

- `processing_time_secs` – completion minus start timestamp  
- `is_failed` – transaction marked as failed  
- `is_success` – transaction succeeded  
- `is_delayed` – success but processing time above 90th percentile  

---

## Key Visuals

- **Failure rate by hour** (`reports/figures/failure_rate_by_hour.png`)  
- **Delay rate by hour** (`reports/figures/delay_rate_by_hour.png`)  
- **Top transaction types by failure/delay** (`reports/figures/top_type_by_*.png`)  

Example KPI table (`reports/kpi_by_type.csv`):

| type        | n     | failure_rate | delay_rate |
|-------------|-------|--------------|------------|
| TRANSFER    | 1.2M  | 0.018        | 0.085      |
| CASH_OUT    | 0.9M  | 0.011        | 0.073      |
| PAYMENT     | 0.7M  | 0.009        | 0.068      |

---

## Models & Metrics

- **Isolation Forest** for anomaly detection on hourly aggregates  
- **Cost Estimation** by multiplying failure/delay rates with average transaction amounts  

Output: `reports/anomaly_scores.csv` with anomaly labels by time bucket.

---

## License & Attribution

- MIT License  
- Dataset: [Synthetic Credit Card Transactions / Online Payment Fraud](https://www.kaggle.com)  

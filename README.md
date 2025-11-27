# Customer Cohort & Retention Analysis

This project implements a small analytics pipeline for:
- Cohort analysis based on customers' first order date
- Retention rate estimation
- Simple prediction of next-month orders from a new cohort
- KPI table per month (orders, average basket, discounts, etc.)
- Heatmap visualization of the cohort table

## Project Structure

```text
customer-cohort-retention-analysis/
├─ src/
│  ├─ __init__.py
│  ├─ data_loader.py          # CSV loading & basic preprocessing
│  ├─ cohort_analysis.py      # cohort table, retention, prediction
│  ├─ kpi.py                  # monthly KPI computations
│  └─ plots.py                # heatmap plotting logic
├─ outputs/
│  └─ (generated CSVs / PNGs / reports)
├─ requirements.txt
└─ run_cohort_analysis.py     # main entry script
```

## Expected Input Data

Place your dataset in the `data/` folder, for example:


The script expects at least the following columns:

- `user_id`          – unique customer identifier
- `order_id`         – unique order identifier
- `created_at`       – order date, format like `%m/%d/%Y` (e.g. `07/15/2022`)
- `basket`           – order basket value (numeric)
- `discount_cost`    – discount amount used in that order (0 if none)

You can change the filename or column names in `src/data_loader.py` if your schema is different.

## How to Run Locally

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:

   ```bash
   python run_cohort_analysis.py          --input-path data/data_analyst_task.csv          --date-format "%m/%d/%Y"
   ```

   You can omit `--date-format` if your dates are already parseable by pandas.

## Outputs

By default, the script writes to the `outputs/` directory:

- `cohort_table.csv`         – cohort counts by `cohort_month` × `year_month`
- `cohort_heatmap.png`       – heatmap figure of the cohort table
- `prediction_report.txt`    – average retention and August 2022 prediction (if July data exists)
- `kpi_data.csv`             – monthly KPIs (orders, basket value, discount usage)

You can change the output directory using the `--output-dir` argument.


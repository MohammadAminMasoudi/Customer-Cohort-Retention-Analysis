import pandas as pd
import numpy as np


def build_cohort_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a cohort table: counts of orders by (cohort_month, year_month).
    Returns a DataFrame indexed by cohort_month, with year_month as columns.
    """
    cohort_pivot = (
        df.groupby(["cohort_month", "year_month"])["order_id"]
        .count()
        .reset_index()
    )
    cohort_table = (
        cohort_pivot
        .pivot(index="cohort_month", columns="year_month", values="order_id")
        .fillna(0)
        .astype(int)
    )
    return cohort_table


def build_retention_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a retention table where each row is a cohort and each column
    (0, 1, 2, ...) is the period number (month offset from cohort month)
    with counts of orders.
    """
    cohort_pivot = (
        df.groupby(["cohort_month", "year_month"])["order_id"]
        .count()
        .reset_index()
    )
    cohort_pivot["period_number"] = (
        cohort_pivot["year_month"] - cohort_pivot["cohort_month"]
    ).apply(lambda x: x.n)

    cohort_retention = (
        cohort_pivot
        .pivot(index="cohort_month", columns="period_number", values="order_id")
        .fillna(0)
    )
    return cohort_retention


def average_first_to_second_month_retention(cohort_retention: pd.DataFrame) -> float:
    """
    Compute average retention rate from first month (period 0) to second month (period 1):

        retention_rate_1 = orders_period_1 / orders_period_0

    Returns the mean over cohorts that have both periods.
    """
    if 0 not in cohort_retention.columns or 1 not in cohort_retention.columns:
        return 0.0

    cohort_retention = cohort_retention.copy()
    cohort_retention["retention_rate_1"] = (
        cohort_retention[1] / cohort_retention[0]
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    return float(cohort_retention["retention_rate_1"].mean())


def predict_august_from_july(cohort_table: pd.DataFrame, avg_retention_1: float) -> int | None:
    """
    Reproduce the logic from the original notebook:
    - Take July 2022 new users (cohort_month == '2022-07', year_month == '2022-07')
    - Predict August orders for that cohort as July_orders * avg_retention_1

    Returns an integer or None if July 2022 is missing.
    """
    idx = pd.Period("2022-07")
    if (idx in cohort_table.index) and (idx in cohort_table.columns):
        july_orders = cohort_table.loc[idx, idx]
        return int(july_orders * avg_retention_1)
    return None

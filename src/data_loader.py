import pandas as pd


def load_orders_csv(path: str, date_format: str | None = "%m/%d/%Y") -> pd.DataFrame:
    """
    Load orders data from CSV and apply basic preprocessing:

    - Parse 'created_at' to datetime
    - Sort by user + date
    - Derive:
      * year_month
      * first_order_date
      * cohort_month
      * is_first_order
      * discount_used_first_order
      * order_rank
      * days_since_prev_order
    """
    df = pd.read_csv(path)

    if date_format:
        df["created_at"] = pd.to_datetime(df["created_at"], format=date_format)
    else:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Sort & derived fields
    df = df.sort_values(by=["user_id", "created_at"])
    df["year_month"] = df["created_at"].dt.to_period("M")

    df["first_order_date"] = df.groupby("user_id")["created_at"].transform("min")
    df["cohort_month"] = df["first_order_date"].dt.to_period("M")

    df["is_first_order"] = df["created_at"] == df["first_order_date"]
    df["discount_used_first_order"] = (
        df.groupby("user_id")["discount_cost"].transform("first") > 0
    )

    df["order_rank"] = df.groupby("user_id").cumcount() + 1

    df["previous_order_date"] = df.groupby("user_id")["created_at"].shift(1)
    df["days_since_prev_order"] = (df["created_at"] - df["previous_order_date"]).dt.days

    return df

import pandas as pd


def compute_monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly KPIs:
    - Total Orders
    - Average Basket Value
    - Total Discount Given
    - Discounted Orders Ratio (share of orders with discount > 0)
    """
    orders_per_month = df.groupby("year_month")["order_id"].count()
    avg_basket_value = df.groupby("year_month")["basket"].mean()
    total_discount = df.groupby("year_month")["discount_cost"].sum()

    orders_without_discount = (
        df[df["discount_cost"] == 0]
        .groupby("year_month")["order_id"]
        .count()
    )

    discounted_orders_ratio = 1 - (orders_without_discount / orders_per_month)

    kpi_data = pd.DataFrame({
        "Total Orders": orders_per_month,
        "Average Basket Value": avg_basket_value,
        "Total Discount Given": total_discount,
        "Discounted Orders Ratio": discounted_orders_ratio,
    })

    return kpi_data

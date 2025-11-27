import argparse
from pathlib import Path

from src.data_loader import load_orders_csv
from src.cohort_analysis import (
    build_cohort_table,
    build_retention_table,
    average_first_to_second_month_retention,
    predict_august_from_july,
)
from src.kpi import compute_monthly_kpis
from src.plots import plot_cohort_heatmap


def main():
    parser = argparse.ArgumentParser(description="Customer cohort & retention analysis pipeline.")
    parser.add_argument(
        "--input-path",
        type=str,
        default="data/data_analyst_task.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory for generated outputs.",
    )
    parser.add_argument(
        "--date-format",
        type=str,
        default="%m/%d/%Y",
        help="Date format for 'created_at' column (pandas strftime style). "
             "Use empty string to let pandas infer.",
    )
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    date_format = args.date_format or None

    print(f"Loading data from: {input_path}")
    df = load_orders_csv(str(input_path), date_format=date_format)

    # Cohort table
    cohort_table = build_cohort_table(df)
    cohort_csv = output_dir / "cohort_table.csv"
    cohort_table.to_csv(cohort_csv)
    print(f"Saved cohort table to: {cohort_csv}")

    # Cohort heatmap
    heatmap_path = output_dir / "cohort_heatmap.png"
    plot_cohort_heatmap(cohort_table, str(heatmap_path))
    print(f"Saved cohort heatmap to: {heatmap_path}")

    # Retention analysis
    cohort_retention = build_retention_table(df)
    avg_retention_1 = average_first_to_second_month_retention(cohort_retention)
    print(f"Average retention rate from first to second month: {avg_retention_1:.2%}")

    # Prediction for August 2022 from July 2022 cohort
    august_pred = predict_august_from_july(cohort_table, avg_retention_1)

    # KPI data
    kpi_data = compute_monthly_kpis(df)
    kpi_csv = output_dir / "kpi_data.csv"
    kpi_data.to_csv(kpi_csv)
    print(f"Saved KPI data to: {kpi_csv}")

    # Text report
    report_path = output_dir / "prediction_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Average retention rate (month 2 vs month 1): {avg_retention_1:.2%}\n")
        if august_pred is not None:
            f.write(
                f"Predicted orders for Aug 2022 (July 2022 cohort): "
                f"{august_pred} orders\n"
            )
        else:
            f.write("July 2022 cohort data not available for prediction.\n")

    print(f"Saved prediction report to: {report_path}")


if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_cohort_heatmap(cohort_table: pd.DataFrame, output_path: str) -> None:
    """
    Plot and save a heatmap of the cohort table.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(cohort_table, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Cohort Analysis - Number of Orders per Month")
    plt.ylabel("Cohort Month (First Order Month)")
    plt.xlabel("Order Month")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

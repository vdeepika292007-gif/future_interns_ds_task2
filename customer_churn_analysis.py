
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Select your Kaggle CSV file
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

file_path = filedialog.askopenfilename(
    title="Select Telco Customer Churn Dataset",
    filetypes=[("CSV files", "*.csv")]
)

root.destroy()

if not file_path:
    raise SystemExit("No dataset selected. Run the script again.")

csv_path = Path(file_path)
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Validate the dataset
required = {
    "customerID", "tenure", "MonthlyCharges",
    "TotalCharges", "Churn"
}

missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing dataset columns: {missing}")

# ---------------- DATA CLEANING ----------------

rows_before = len(df)
duplicate_rows = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
df["MonthlyCharges"] = pd.to_numeric(
    df["MonthlyCharges"], errors="coerce"
)
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].astype(str).str.strip()
      .replace({"": np.nan, "nan": np.nan}),
    errors="coerce"
)

df["tenure"] = df["tenure"].fillna(
    df["tenure"].median()
).astype(int)

df["MonthlyCharges"] = df["MonthlyCharges"].fillna(
    df["MonthlyCharges"].median()
)

# Handle blank historical charges
df.loc[
    df["TotalCharges"].isna() & (df["tenure"] == 0),
    "TotalCharges"
] = 0

df["TotalCharges"] = df["TotalCharges"].fillna(
    df["MonthlyCharges"] * df["tenure"]
)

df["Churn"] = df["Churn"].astype(str).str.strip().str.title()
df = df[df["Churn"].isin(["Yes", "No"])].copy()
df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 36, 48, 60, 100],
    labels=[
        "0-12 months", "13-24 months",
        "25-36 months", "37-48 months",
        "49-60 months", "61+ months"
    ],
    ordered=True
)

# ---------------- KEY METRICS ----------------

total = df["customerID"].nunique()
churned = df.loc[df["Churn"] == "Yes", "customerID"].nunique()
retained = total - churned

churn_rate = churned / total if total else 0
retention_rate = retained / total if total else 0

avg_tenure = df["tenure"].mean()
avg_monthly = df["MonthlyCharges"].mean()
avg_historical_charges = df["TotalCharges"].mean()

# Create output folder beside the CSV
out = csv_path.parent / "Customer_Churn_Analysis_Output"
out.mkdir(exist_ok=True)

# Save cleaned data
df.to_csv(out / "cleaned_customer_churn_data.csv", index=False)

# Save KPI summary
summary = pd.DataFrame({
    "Metric": [
        "Total Customers",
        "Churned Customers",
        "Retained Customers",
        "Churn Rate",
        "Retention Rate",
        "Average Tenure (Months)",
        "Average Monthly Charges",
        "Average Historical Charges",
        "Rows Before Cleaning",
        "Duplicate Rows Found"
    ],
    "Value": [
        total, churned, retained, churn_rate,
        retention_rate, avg_tenure, avg_monthly,
        avg_historical_charges, rows_before, duplicate_rows
    ]
})

summary.to_csv(out / "retention_summary_metrics.csv", index=False)

# ---------------- PROFESSIONAL DASHBOARD ----------------

BG = "#181024"
PANEL = "#2B1B3A"
PURPLE = "#A66BE8"
BLUE = "#45A3F5"
ORANGE = "#F28C52"
TEAL = "#35C7B0"
PINK = "#E66BB3"
WHITE = "#F7F2FC"
MUTED = "#C8BED4"

sns.set_theme(style="whitegrid")

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.labelcolor": MUTED,
    "axes.titlecolor": WHITE,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": WHITE,
    "grid.color": "#594767",
    "grid.alpha": 0.3,
    "savefig.facecolor": BG
})

fig = plt.figure(figsize=(16, 10), facecolor=BG)

fig.text(
    0.04, 0.96,
    "CUSTOMER RETENTION & CHURN ANALYTICS",
    fontsize=22, fontweight="bold", color=WHITE
)

fig.text(
    0.04, 0.92,
    "FUTURE INTERNS | TASK 2 | CUSTOMER BEHAVIOUR ANALYSIS",
    fontsize=10, color=MUTED
)

kpis = [
    ("TOTAL CUSTOMERS", f"{total:,}", BLUE),
    ("CHURNED CUSTOMERS", f"{churned:,}", ORANGE),
    ("RETAINED CUSTOMERS", f"{retained:,}", TEAL),
    ("CHURN RATE", f"{churn_rate:.2%}", PINK),
    ("RETENTION RATE", f"{retention_rate:.2%}", PURPLE),
    ("AVG. TENURE", f"{avg_tenure:.2f} mo", BLUE)
]

for i, (label, value, color) in enumerate(kpis):
    x = 0.04 + i * 0.158

    card = plt.matplotlib.patches.FancyBboxPatch(
        (x, 0.80), 0.145, 0.095,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        transform=fig.transFigure,
        facecolor=PANEL, edgecolor=color, linewidth=1.5
    )

    fig.patches.append(card)

    fig.text(
        x + 0.01, 0.855, label,
        fontsize=7.5, fontweight="bold", color=MUTED
    )

    fig.text(
        x + 0.01, 0.815, value,
        fontsize=17, fontweight="bold", color=WHITE
    )

def churn_table(field):
    result = df.groupby(
        field, observed=False, dropna=False
    ).agg(
        Customers=("customerID", "nunique"),
        Churned=("ChurnFlag", "sum")
    ).reset_index()

    result["ChurnRate"] = (
        result["Churned"] / result["Customers"].replace(0, np.nan)
    )

    return result

fields = [
    c for c in [
        "Contract", "InternetService",
        "PaymentMethod", "TenureGroup"
    ] if c in df.columns
]

colors = [ORANGE, BLUE, PINK, TEAL]

grid = fig.add_gridspec(
    2, 2, left=0.07, right=0.96,
    bottom=0.10, top=0.73,
    hspace=0.38, wspace=0.28
)

segment_results = []

for i, field in enumerate(fields):
    table = churn_table(field)

    temp = table.copy()
    temp.insert(0, "Segment", field)
    temp.rename(columns={field: "SegmentValue"}, inplace=True)
    segment_results.append(temp)

    table = table.sort_values("ChurnRate", ascending=True)

    ax = fig.add_subplot(grid[i // 2, i % 2])

    sns.barplot(
        data=table,
        x="ChurnRate",
        y=field,
        color=colors[i],
        ax=ax
    )

    ax.axvline(
        churn_rate,
        color=TEAL,
        linestyle="--",
        linewidth=1.5
    )

    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:.0%}")
    )

    ax.set_title(
        f"Churn Rate by {field}",
        loc="left", fontweight="bold", pad=8
    )

    ax.set_xlabel("Churn rate")
    ax.set_ylabel("")
    ax.grid(axis="y", visible=False)

    for bar, value in zip(ax.patches, table["ChurnRate"]):
        ax.text(
            value + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1%}",
            va="center", fontsize=8, color=WHITE
        )

    ax.set_xlim(
        0, max(float(table["ChurnRate"].max()) * 1.25, 0.05)
    )

if segment_results:
    pd.concat(
        segment_results, ignore_index=True
    ).to_csv(out / "segment_churn_analysis.csv", index=False)

fig.text(
    0.04, 0.035,
    "Segment churn rates are shown for comparison. "
    "No signup dates or explicit cancellation reasons are available.",
    fontsize=8, color=MUTED
)

fig.savefig(
    out / "customer_retention_dashboard.png",
    dpi=200, bbox_inches="tight"
)

plt.close(fig)

# ---------------- INSIGHTS & RECOMMENDATIONS ----------------

report = [
    "CUSTOMER RETENTION & CHURN ANALYSIS",
    "=" * 42,
    f"Total customers: {total:,}",
    f"Churned customers: {churned:,} ({churn_rate:.2%})",
    f"Retained customers: {retained:,} ({retention_rate:.2%})",
    f"Average tenure: {avg_tenure:.2f} months",
    f"Average monthly charges: {avg_monthly:.2f}",
    "",
    "HIGHEST CHURN-RATE SEGMENTS"
]

for field in fields:
    table = churn_table(field).dropna(subset=["ChurnRate"])
    table = table.sort_values("ChurnRate", ascending=False)

    if not table.empty:
        row = table.iloc[0]
        report.append(
            f"{field}: {row[field]} — {row['ChurnRate']:.2%} "
            f"({int(row['Churned'])}/{int(row['Customers'])} customers)"
        )

report += [
    "",
    "RECOMMENDATIONS TO TEST",
    "1. Prioritize outreach to segments with above-average churn.",
    "2. Test onboarding and early support for newer customers.",
    "3. Review support and online-security experiences.",
    "4. Test suitable plan offers for month-to-month customers.",
    "",
    "LIMITATIONS",
    "The dataset does not record explicit cancellation reasons or signup dates.",
    "Segment patterns do not prove causation.",
    "TotalCharges represents historical billing, not verified future lifetime value."
]

(out / "insights_and_recommendations.txt").write_text(
    "\n".join(report), encoding="utf-8"
)

print("\nANALYSIS COMPLETE!")
print(f"Total customers: {total:,}")
print(f"Churn rate: {churn_rate:.2%}")
print(f"Retention rate: {retention_rate:.2%}")
print(f"Average tenure: {avg_tenure:.2f} months")
print(f"\nResults saved to:\n{out}")
print("\nOpen customer_retention_dashboard.png first.")

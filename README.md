# Customer Retention & Churn Analysis

**Future Interns — Data Science & Analytics Internship | Task 2**

## Project overview

This project analyses customer churn in a subscription-based telecommunications dataset. It explores the overall churn rate, retention, customer tenure, and differences between customer segments. The goal is to turn customer data into practical retention actions.

## Tools used

- Python
- Pandas and NumPy for data preparation and analysis
- Matplotlib and Seaborn for visualisation
- Power BI for a complementary dashboard

## Dataset

The analysis uses the Telco Customer Churn dataset (`WA_Fn-UseC_-Telco-Customer-Churn.csv`). The dataset includes customer, service, contract, payment, tenure, charge, and churn fields.

## Key results

| Metric | Result |
|---|---:|
| Total customers | 7,043 |
| Churned customers | 1,869 |
| Retained customers | 5,174 |
| Overall churn rate | 26.54% |
| Overall retention rate | 73.46% |
| Average tenure | 32.37 months |
| Average monthly charges | 64.76 (currency not specified in the dataset documentation used for this report) |

## Highest-churn segments observed

| Segment | Churn rate | Churned / customers in segment |
|---|---:|---:|
| Tenure: 0–12 months | 47.44% | 1,037 / 2,186 |
| Payment method: Electronic check | 45.29% | 1,071 / 2,365 |
| Contract: Month-to-month | 42.71% | 1,655 / 3,875 |
| Internet service: Fiber optic | 41.89% | 1,297 / 3,096 |

These figures identify groups for further investigation. They do not, on their own, establish why an individual customer churned or prove that a segment attribute causes churn.

## Recommendations to test

1. **Improve early customer experience:** test onboarding messages, setup guidance, and proactive support for customers in their first 12 months.
2. **Review month-to-month retention:** test clear, optional annual-plan incentives and compare retention outcomes against a control group.
3. **Investigate electronic-check churn:** review customer feedback and payment experience for this segment before selecting a targeted intervention.
4. **Review fiber-optic service experience:** examine complaint, outage, speed, and support data, if available, before attributing churn to service quality.
5. **Measure results:** track churn and retention by segment over time to assess whether interventions improve outcomes.

## Methodology

1. Load the CSV dataset and check required columns.
2. Remove duplicate rows and trim whitespace from text fields.
3. Convert tenure and charge columns to numeric values and handle missing charge values.
4. Calculate customer counts, churn and retention rates, and average tenure and monthly charges.
5. Group customers by contract, internet service, payment method, and tenure range to compare churn rates.
6. Generate a dashboard image, analysis CSV files, and a text report.

## Files generated

The `Customer_Churn_Analysis_Output` folder contains the generated dashboard image, cleaned data, KPI summary, segment analysis, and insights report. A Power BI `.pbix` file may also be included as a complementary visual deliverable.

## Limitations

- The dataset does not include explicit cancellation reasons, so churn reasons cannot be directly confirmed from these fields.
- Signup dates are not available, so signup-month cohort retention cannot be reliably calculated.
- Segment relationships are descriptive and do not prove causation.
- `TotalCharges` reflects historical recorded charges; it is not a verified prediction of future customer lifetime value.
- Missing charge values are handled for analysis; results should be interpreted in light of the cleaning assumptions.

## How to run

1. Install the required packages:

   ```bash
   python -m pip install pandas numpy matplotlib seaborn
   ```

2. Run the analysis script:

   ```bash
   python customer_churn_analysis.py
   ```

3. When prompted, select `WA_Fn-UseC_-Telco-Customer-Churn.csv`.
4. Open `customer_retention_dashboard.png` and the generated CSV/text files in `Customer_Churn_Analysis_Output`.

## Conclusion

The analysis indicates an overall churn rate of 26.54%. Newer customers, electronic-check users, month-to-month customers, and fiber-optic customers have comparatively high observed churn rates in this dataset. These segments are useful priorities for further investigation and carefully measured retention experiments.

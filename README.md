# Banking Intelligence Platform — Power BI Dashboard

End-to-end banking analytics pipeline built on synthetic data generated with Python/Faker, covering credit risk scoring, portfolio performance and fraud detection across 41,188 clients and 10 European banks.

**Stack:** PostgreSQL · Python (Faker) · dbt · Power BI Desktop · DAX

---

## Download the Dashboard

The Power BI file is available directly in this repository.

**File:** [bank_project_version.pbix](./bank_project_version.pbix)

To open it, download the file and open it with Power BI Desktop. All data, relationships, DAX measures and visuals are included. No additional setup required.

---

## Dashboard Screenshots

### Page 1 — Risk Overview

![Risk Overview](./Risk%20Overview.png)

This page provides a comprehensive view of the credit risk profile across the entire client portfolio (41,188 clients). It answers a core banking question: how are clients distributed across risk categories, and which client segments carry the most default risk?

**Visual breakdown:**

**Donut chart — Client distribution by ML risk segment (top left)**
The donut shows that 94.13% of clients (38,770) fall into the `very_low_risk` category, while only 1.37K clients (3.33%) are classified as `medium_risk` or above. This distribution reflects a healthy synthetic portfolio deliberately skewed toward low-risk clients. The four segments are color-coded: purple for very_low_risk, dark blue for low_risk, orange for medium_risk, and a distinct color for high_risk.

**Bar chart — Average default rate by risk segment (top right)**
This horizontal bar chart ranks risk segments by their average default rate. The `high_risk` segment shows a default rate close to 100%, `medium_risk` around 90%, `low_risk` around 50%, and `very_low_risk` near 0%. This confirms that the ML scoring model correctly separates clients by default probability — clients labeled high_risk genuinely default more often. This is a key validation chart for the model's reliability.

**Bar chart — Average ML risk score by job (bottom left)**
This chart breaks down the average ML risk score across all professional categories (admin, entrepreneur, management, technician, self-employed, retired, services, blue-collar, housemaid, unemployed, student). All job types show scores clustered between 40 and 100, which indicates that profession alone does not strongly predict risk — a realistic finding, as risk is multi-factorial. This chart is useful for identifying whether any profession is systematically over- or under-scored.

**KPI Cards (right side)**
- **41,188** — Total number of clients in the scoring dataset
- **0.04%** — Percentage of clients classified as high_risk (very low, confirming a low-risk portfolio)
- **2,418** — Number of clients flagged as "requires review" by the dbt business rules engine
- **100.00%** — Agreement rate between the ML model and the dbt rule-based scoring system (both models assign the same risk segment to every client)

---

### Page 2 — Portfolio Performance

![Portfolio Performance](./Portfolio%20Performance.png)

This page focuses on the stock market performance of 10 major European and American banks over a multi-year period. It answers investment-level questions: which banks delivered the best returns, which offered the best risk-adjusted performance, and how does return relate to volatility?

**Visual breakdown:**

**Scatter chart — Annualized return vs. volatility by bank (top left)**
Each dot on this chart represents one bank. The X-axis shows the average annualized return (%), the Y-axis shows the average volatility (%). The ideal bank is positioned toward the bottom-right: high return, low volatility. Banks clustered in the top-left deliver poor returns with high risk — the worst possible combination. This chart is a standard tool in portfolio management to assess the risk/return tradeoff at a glance.

**Line chart — Average annualized return by bank (top right)**
This descending line chart ranks all 10 banks by their annualized return. Commerzbank leads at approximately 50%, while Bank of America trails near 15%. The downward slope makes it immediately clear how large the performance gap is between the best and worst performers across the portfolio.

**Bar chart — Average Sharpe ratio by bank (bottom left)**
The Sharpe ratio measures how much return a bank generated per unit of risk taken. A higher Sharpe ratio is always better. HSBC Holdings leads with a ratio of approximately 1.6, meaning it delivered the best risk-adjusted performance. Bank of America sits at the bottom with a ratio around 0.5. This ranking is different from the pure return ranking — a bank can have high returns but also high volatility, which penalizes its Sharpe ratio.

**Column chart — Average cumulative return by bank (bottom right)**
This vertical bar chart shows total cumulative return over the full observation period. Commerzbank reaches approximately 230%, while Bank of America sits near 50%. This chart is complementary to the annualized return: it shows the absolute wealth creation over time, not just the annual rate.

**KPI Cards (right side)**
- **230.74%** — Best cumulative return achieved across all banks (Commerzbank)
- **1.6135** — Best Sharpe ratio achieved across all banks (HSBC Holdings)
- **Commerzbank** — Top performing bank by total cumulative return
- **HSBC Holdings** — Top performing bank by risk-adjusted return (Sharpe ratio)

---

## Glossary — English Terms Explained

This section explains every technical term used in the dashboard so that any reader can correctly interpret the charts and measures.

### Risk & Scoring Terms

| Term | Explanation |
|------|-------------|
| **ml_risk_segment** | The risk category assigned to a client by the Machine Learning model. Four possible values: `very_low_risk`, `low_risk`, `medium_risk`, `high_risk`. The higher the segment, the more likely the client is to default on a loan. |
| **dbt_risk_segment** | The risk category assigned by a set of business rules written in dbt (data build tool). This is a rule-based scoring system, as opposed to the ML model which learns from data patterns. |
| **ml_risk_score** | A numerical score between 0 and 100 assigned by the ML model. The higher the score, the higher the estimated risk. This score is then converted into a segment (very_low / low / medium / high). |
| **dbt_risk_score** | A numerical score between 0 and 100 assigned by the dbt rule engine, based on predefined business logic (e.g. number of loans, default history, DTI ratio). |
| **segments_agree** | A boolean (TRUE/FALSE) column that indicates whether the ML model and the dbt rule engine assigned the same risk segment to a client. A value of TRUE means both methods agree. |
| **% Model Agreement** | The percentage of clients for which both the ML model and the dbt rules assigned the same risk segment. 100% agreement means the two methods are perfectly aligned. |
| **requires_review** | A flag (TRUE/FALSE) set by the dbt engine. Clients flagged TRUE have characteristics that require manual review by a credit analyst before any loan decision. |
| **has_credit_default** | Indicates whether a client has a history of credit default (failure to repay a loan). 1 = yes, 0 = no. |
| **default_rate_pct** | The percentage of a client's loans that ended in default. A rate of 100% means all their past loans were not repaid. |
| **avg_dti** | Average Debt-to-Income ratio. It measures what percentage of a client's income is absorbed by debt repayments. A high DTI (e.g. 80%) means the client is heavily indebted relative to their income and represents a higher risk. |
| **credit_score_component** | The portion of the dbt risk score that comes from credit history (defaults, loan repayment behavior). One of three sub-components of the total risk score. |
| **transaction_score_component** | The portion of the dbt risk score derived from transaction behavior (frequency, amounts, anomalies). |
| **profile_score_component** | The portion of the dbt risk score derived from client profile characteristics (age, job, education, marital status). |
| **proba_very_low_risk / proba_low_risk / proba_medium_risk / proba_high_risk** | Probability outputs from the ML classification model. For each client, the model outputs four probabilities (e.g. 0.85 for very_low_risk, 0.10 for low_risk, etc.) that sum to 1. The segment is assigned based on the highest probability. |
| **ml_segment_ordinal** | A numeric code (1, 2, 3, 4) that represents the ml_risk_segment in ordered form, used to sort segments correctly in charts. |

### Portfolio & Finance Terms

| Term | Explanation |
|------|-------------|
| **bank_name** | The name of one of the 10 banks in the portfolio: Commerzbank, Santander, Deutsche Bank, HSBC Holdings, Intesa Sanpaolo, Goldman Sachs, JPMorgan Chase, Credit Agricole, BNP Paribas, Bank of America. |
| **cumulative_return_pct** | The total percentage gain of a bank's stock over the entire observation period. For example, 230% means that an investment of $100 would have grown to $330. |
| **annualized_return_pct** | The average yearly percentage return, normalized so that performances over different periods can be compared fairly. Also called CAGR (Compound Annual Growth Rate). |
| **annualized_volatility_pct** | The standard deviation of daily returns, scaled to a yearly figure. It measures how much the stock price fluctuates. High volatility = high risk. |
| **sharpe_ratio** | A risk-adjusted performance metric. It is calculated as (return - risk-free rate) / volatility. A Sharpe ratio above 1.0 is considered good. The higher the ratio, the more return is earned per unit of risk taken. A risk-free rate of 3% was used as the baseline. |
| **model_accuracy** | The overall accuracy of the ML classification model — the percentage of clients whose risk segment was correctly predicted. |
| **model_f1_macro** | The F1-macro score of the ML model. It measures the balance between precision and recall across all four risk segments equally, regardless of how many clients are in each segment. A score near 1.0 is ideal. |
| **model_auc** | Area Under the ROC Curve. A standard metric for classification models. A score of 1.0 means perfect classification; 0.5 means random guessing. |

### Fraud Detection Terms

| Term | Explanation |
|------|-------------|
| **total_fraud_count** | The total number of fraudulent transactions detected for a client. |
| **fraud_rate_pct** | The percentage of a client's transactions that were flagged as fraudulent. |
| **fraud_suspicion_score** | A composite score (0–100) reflecting how suspicious a client's transaction behavior is. It combines fraud frequency, transaction anomalies and risk profile. |
| **nb_fraud_transactions** | The raw count of transactions classified as fraudulent for a client. |

### General Terms

| Term | Explanation |
|------|-------------|
| **avg_inflation_pct** | The average inflation rate in the client's country during the observation period. Used as a macroeconomic feature in the ML model. |
| **eur_usd_rate** | The EUR/USD exchange rate at the time of scoring. Used as a macroeconomic context variable. |
| **scored_at** | The timestamp when the ML model generated the risk score for a client. |
| **job** | The professional category of a client: admin, entrepreneur, management, technician, self-employed, retired, services, blue-collar, housemaid, unemployed, student, unknown. |
| **education_level** | The highest level of education completed by the client: primary, secondary, tertiary, unknown. |
| **marital_status** | The civil status of the client: single, married, divorced. |
| **has_housing_loan** | Indicates whether the client currently has a mortgage or housing loan (TRUE/FALSE). |
| **has_personal_loan** | Indicates whether the client currently has a personal loan (TRUE/FALSE). |
| **subscribed_term_deposit** | Indicates whether the client has subscribed to a term deposit product at the bank (TRUE/FALSE). |
| **nb_loans** | Total number of loans a client has had (past and current). |
| **total_loan_amount** | The total cumulative loan amount for a client across all their loans. |
| **nb_transactions** | Total number of banking transactions recorded for a client. |

---

## Architecture Overview

```
Python / Faker
     |
     v
BRONZE      Raw synthetic data — clients, loans, transactions, market prices
     |
     v
SILVER      Cleaned and typed data — standardized formats, NULL handling
     |
     v
GOLD        Business-ready tables — credit scoring, risk scoring, portfolio perf, fraud
     |
     v
POWER BI    Semantic layer — DAX measures, 3-page dashboard, 3 RLS roles
```

---

## Repository Structure

```
powerbi-banking-dashboard/
├── dax/
│   ├── risk_overview_measures.dax       # DAX measures for Page 1
│   ├── portfolio_measures.dax           # DAX measures for Page 2
│   ├── fraud_detection_measures.dax     # DAX measures for Page 3
│   └── rls_definitions.dax              # Row-Level Security role filters
├── rls/
│   └── roles.md                         # RLS role descriptions
├── Risk Overview.png                    # Dashboard Page 1 screenshot
├── Portfolio Performance.png            # Dashboard Page 2 screenshot
├── bank_project_version.pbix            # Power BI dashboard — 3 pages, 16 measures, 3 RLS roles
├── generate_data.py                     # Synthetic data generation (Python / Faker)
└── README.md
```

---

## Data Model

### Tables

| Table | Rows | Description |
|-------|------|-------------|
| `credit_scoring_results` | 41,188 | ML scoring output — risk scores, segments, probabilities, client features |
| `mart_risk_scoring` | 41,188 | dbt rule-based scoring — business logic risk scores and flags |
| `mart_portfolio_perf` | 10 | Stock performance metrics for 10 major banks |
| `mart_fraud_indicators` | 41,188 | Fraud transaction counts, rates and suspicion scores per client |

### Active Relationships

| From | To | Type |
|------|----|------|
| `credit_scoring_results[client_id]` | `mart_risk_scoring[client_id]` | 1:1 |
| `credit_scoring_results[client_id]` | `mart_fraud_indicators[client_id]` | 1:1 |

### DAX Measures (16 total)

| Measure | Description | Table |
|---------|-------------|-------|
| `Total Clients` | Total number of scored clients | credit_scoring_results |
| `Avg ML Risk Score` | Average ML risk score (0–100) | credit_scoring_results |
| `Avg DBT Risk Score` | Average dbt rule-based score | credit_scoring_results |
| `Score Delta ML vs DBT` | Gap between ML and dbt average scores | credit_scoring_results |
| `% Model Agreement` | % of clients where ML and dbt segments match | credit_scoring_results |
| `Very Low Risk Count` | Count of very_low_risk clients | credit_scoring_results |
| `Low Risk Count` | Count of low_risk clients | credit_scoring_results |
| `Medium Risk Count` | Count of medium_risk clients | credit_scoring_results |
| `High Risk Count` | Count of high_risk clients | credit_scoring_results |
| `% High Risk` | Percentage of high_risk clients on total | credit_scoring_results |
| `% Requires Review` | % of clients flagged for manual review | mart_risk_scoring |
| `Clients Requires Review` | Count of clients requiring review | mart_risk_scoring |
| `Avg Credit Score Component` | Average credit sub-score | mart_risk_scoring |
| `Avg DTI` | Average Debt-to-Income ratio | mart_risk_scoring |
| `Avg Default Rate` | Average default rate across portfolio | mart_risk_scoring |
| `Avg Cumulative Return %` | Average cumulative stock return | mart_portfolio_perf |
| `Avg Annualized Return %` | Average CAGR across banks | mart_portfolio_perf |
| `Avg Volatility %` | Average annualized volatility | mart_portfolio_perf |
| `Avg Sharpe Ratio` | Average Sharpe ratio (risk-free 3%) | mart_portfolio_perf |
| `Best Sharpe Ratio` | Maximum Sharpe ratio in portfolio | mart_portfolio_perf |
| `Best Return %` | Maximum cumulative return in portfolio | mart_portfolio_perf |
| `Top Bank by Return` | Name of the bank with highest cumulative return | mart_portfolio_perf |
| `Top Bank by Sharpe` | Name of the bank with best Sharpe ratio | mart_portfolio_perf |

---

## Row-Level Security (RLS)

Three roles restrict data access based on the user's function:

| Role | Access |
|------|--------|
| `Risk_Manager` | Full access to credit_scoring_results and mart_risk_scoring |
| `Fraud_Analyst` | Access restricted to mart_fraud_indicators data |
| `Portfolio_Manager` | Access restricted to mart_portfolio_perf data |

---

## Key Findings

| Insight | Value |
|---------|-------|
| Total clients scored | 41,188 |
| Clients classified as very_low_risk | 94.13% |
| Clients flagged for manual review | 2,418 |
| ML / dbt model agreement | 100% |
| Best performing bank (return) | Commerzbank — 230.74% cumulative |
| Best performing bank (risk-adjusted) | HSBC Holdings — Sharpe ratio 1.6135 |
| Worst performing bank | Bank of America — ~50% cumulative return |

---

## How to Reproduce

```bash
# 1. Generate synthetic data
python generate_data.py

# 2. Load to PostgreSQL
psql -d postgres -f load_bronze.sql

# 3. Run dbt transformations
dbt run

# 4. Open Power BI Desktop
#    File > Open > bank_project_version.pbix
#    Home > Refresh
```

Alternatively, download [bank_project_version.pbix](./bank_project_version.pbix) directly — all data is already embedded.

---

## License

MIT — Synthetic data generated with Python Faker. No real client data used.

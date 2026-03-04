# Banking Intelligence Platform – Power BI Dashboard

A Power BI dashboard for banking risk analysis, fraud detection, and portfolio performance monitoring. Built on a Medallion architecture (Bronze, Silver, Gold) with synthetic data generated via Python and dbt transformations.

**Stack:** Python · Faker · dbt · Power BI Desktop · DAX · RLS

---

## Download the Dashboard

**File:** [bank_project.pbix](./bank_project.pbix)

Download the file and open it with Power BI Desktop. All data, relationships, DAX measures, visuals, and RLS roles are included. No additional setup required.

---

## Dashboard Preview

![Risk Overview](./Capture%20d'%C3%A9cran%202026-03-03%20151859.png)

The Risk Overview page shows 4 KPI cards (Total Clients, Clients High Risk, Avg ML Risk Score, DBT ML Agreement %) and a donut chart showing the distribution of clients by ML risk segment.

---

## Project Context

This project builds a banking risk intelligence dashboard in Power BI for strategic decision-making in the financial sector. It covers four analytical dimensions:

- Client segmentation by ML risk level (low_risk, medium_risk, high_risk)
- Fraud detection with transaction-level indicators and alert scoring
- Portfolio performance analysis by banking institution (Sharpe Ratio, annualized return, volatility)
- Macro-economic layer with geolocation data (inflation, unemployment, lending rates by country)

All data is fully synthetic, generated with Python and the Faker library. No real or personal data was used. The project applies Privacy by Design principles in line with GDPR requirements.

---

## Data Pipeline – Medallion Architecture

```
Python / Faker
      |
      v
Bronze Layer   Raw generated data (CSV flat files) - no transformation
      |
      v
Silver Layer   Cleaning and transformation via dbt
               Deduplication, type normalization, ML score computation
      |
      v
Gold Layer     Analytical marts ready for Power BI
               Aggregated tables, business columns, dbt validation tests
      |
      v
Power BI       Interactive dashboard – 16 DAX measures, 3 pages, 3 RLS roles
```

---

## Tables Used

| Table | Layer | Role in Power BI |
|---|---|---|
| `credit_scoring_results` | Bronze + Silver + Gold | Client risk segmentation |
| `mart_risk_scoring` | Silver + Gold | ML vs business rule comparison |
| `mart_fraud_indicators` | Silver + Gold | Fraud indicators per client |
| `mart_portfolio_perf` | Silver + Gold | Bank performance (Sharpe, Return) |
| `macro_geo_latest` | Bronze + Silver + Gold | Macro-economic context by country |

---

## Data Model – Relationships

Two valid relationships in the Power BI model:

| Source | Column | Target | Column | Cardinality |
|---|---|---|---|---|
| `credit_scoring_results` | `client_id` | `mart_risk_scoring` | `client_id` | 1:1 |
| `credit_scoring_results` | `client_id` | `mart_fraud_indicators` | `client_id` | 1:1 |

`mart_portfolio_perf` and `macro_geo_latest` are intentionally independent (no common key).
Relations on `bank_id` and `country_code` were identified as invalid and excluded.

---

## DAX Measures (16 total across 4 tables)

See the full measures in the [dax/](./dax/) folder:

- `credit_scoring.dax` – 6 measures: Risk Segment Count, Risk Segment %, Total Clients, Avg ML Risk Score, Clients High Risk, DBT ML Agreement %
- `portfolio_perf.dax` – 5 measures: Sharpe Ratio, Avg Sharpe Ratio, Best Sharpe Bank, Avg Volatility %, Avg Annualized Return %
- `fraud_indicators.dax` – 4 measures: Fraud Rate Pct, Fraud High Alert Count, Fraud Amount % of Total, Priority Investigation Count
- `macro_geo.dax` – 1 measure: Macro Risk Index

---

## Report Pages (3 pages – 20 visuals)

**Page 1 – Risk Overview:** 4 KPI cards, donut chart (risk segments), histogram (score distribution), horizontal bar (risk by job), filled map (macro by country), slicer (risk segment)

**Page 2 – Portfolio Performance:** 4 KPI cards, clustered bar (returns by bank), scatter plot (volatility vs return), line chart (Sharpe ratio), table with conditional formatting

**Page 3 – Fraud Detection:** 4 KPI cards, scatter plot (anomalous transactions), TOP 10 client table, matrix heatmap (job x alert level), histogram (suspicion scores), slicer (alert level)

---

## Row-Level Security (3 roles)

See full definition in [rls/roles_definition.md](./rls/roles_definition.md)

| Role | Fraud access | Portfolio access | Client/Risk access |
|---|---|---|---|
| Risk_Manager | LOW + MEDIUM only | Full | Full |
| Fraud_Analyst | HIGH + MEDIUM + anomalies | None | Partial (score > 20) |
| Portfolio_Manager | None | Full | None (GDPR) |

---

## Repository Structure

```
powerbi-banking-dashboard/
├── README.md
├── bank_project.pbix
├── Capture d'écran 2026-03-03 151859.png
├── dax/
│   ├── credit_scoring.dax
│   ├── portfolio_perf.dax
│   ├── fraud_indicators.dax
│   └── macro_geo.dax
└── rls/
    └── roles_definition.md
```

---

## What This Project Demonstrates

- End-to-end data pipeline from synthetic generation to analytical dashboard
- Medallion architecture applied to a financial use case
- DAX modeling with 16 measures across 4 tables
- Row-level security with 3 distinct business roles (GDPR-compliant)
- Data quality validation via dbt test layer

---

*Built with Power BI Desktop, Python, Faker, dbt – Medallion Architecture, DAX, RLS*

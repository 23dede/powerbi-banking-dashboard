"""
generate_data.py
Generates synthetic banking data for the Banking Intelligence Platform.
Tables: credit_scoring_results, mart_risk_scoring, mart_fraud_indicators,
        mart_portfolio_perf, macro_geo_latest
Output: CSV files in the data/ folder.

Usage:
    pip install faker
    python generate_data.py
"""

import random
import csv
import os
from faker import Faker

fake = Faker()
random.seed(42)

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_CLIENTS = 1000

BANK_NAMES = [
    "Atlas Bank", "Meridian Finance", "Crestview Bank", "Horizon Trust",
    "Northgate Capital", "Silverstone Bank", "Apex Financial", "Unity Bank",
    "Pinnacle Credit", "Redwood Savings"
]

COUNTRIES = [
    ("France", "FR"), ("Germany", "DE"), ("Spain", "ES"), ("Italy", "IT"),
    ("Portugal", "PT"), ("Netherlands", "NL"), ("Belgium", "BE"), ("Poland", "PL"),
    ("Sweden", "SE"), ("Norway", "NO"), ("Denmark", "DK"), ("Finland", "FI"),
    ("Austria", "AT"), ("Switzerland", "CH"), ("Czech Republic", "CZ"),
    ("Hungary", "HU"), ("Romania", "RO"), ("Greece", "GR"), ("Ireland", "IE"),
    ("Luxembourg", "LU")
]

JOBS = [
    "engineer", "teacher", "doctor", "lawyer", "accountant",
    "nurse", "manager", "analyst", "consultant", "entrepreneur",
    "developer", "architect", "researcher", "sales_representative", "technician"
]

RISK_SEGMENTS = ["low_risk", "medium_risk", "high_risk"]


def write_csv(filename, rows):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filepath}  ({len(rows)} rows)")


def generate_credit_scoring_results():
    rows = []
    for client_id in range(1, NUM_CLIENTS + 1):
        ml_score = round(random.uniform(0, 100), 2)
        if ml_score < 35:
            ml_seg = "low_risk"
        elif ml_score < 65:
            ml_seg = "medium_risk"
        else:
            ml_seg = "high_risk"

        biz_seg = ml_seg
        if random.random() < 0.15:
            biz_seg = random.choice([s for s in RISK_SEGMENTS if s != ml_seg])

        rows.append({
            "client_id": client_id,
            "job": random.choice(JOBS),
            "country_code": random.choice(COUNTRIES)[1],
            "ml_risk_score": ml_score,
            "ml_risk_segment": ml_seg,
            "business_segment": biz_seg,
            "segments_agree": ml_seg == biz_seg,
            "fraud_suspicion_score": round(random.uniform(0, 100), 2),
            "total_fraud_count": random.randint(0, 5),
            "credit_score": random.randint(300, 850),
            "loan_amount": round(random.uniform(1000, 100000), 2),
            "annual_income": round(random.uniform(20000, 200000), 2),
        })
    return rows


def generate_mart_risk_scoring(credit_scoring):
    rows = []
    for row in credit_scoring:
        rows.append({
            "client_id": row["client_id"],
            "ml_risk_score": row["ml_risk_score"],
            "ml_risk_segment": row["ml_risk_segment"],
            "business_risk_segment": row["business_segment"],
            "segments_agree": row["segments_agree"],
            "risk_score_delta": round(abs(row["ml_risk_score"] - random.uniform(0, 100)), 2),
            "last_updated": fake.date_between(start_date="-1y", end_date="today"),
        })
    return rows


def generate_mart_fraud_indicators(credit_scoring):
    rows = []
    for row in credit_scoring:
        total_tx = random.randint(10, 500)
        fraud_count = row["total_fraud_count"]
        total_amount = round(random.uniform(500, 50000), 2)
        nb_anomalous = random.randint(0, 10)
        suspicion = row["fraud_suspicion_score"]

        if suspicion > 70 or nb_anomalous > 5:
            alert_level = "HIGH"
        elif suspicion > 40:
            alert_level = "MEDIUM"
        else:
            alert_level = "LOW"

        rows.append({
            "client_id": row["client_id"],
            "total_transactions": total_tx,
            "total_fraud_count": fraud_count,
            "total_amount": total_amount,
            "total_fraud_amount": round(fraud_count * random.uniform(50, 500), 2),
            "fraud_rate_pct": round(fraud_count / total_tx * 100, 4),
            "avg_tx_amount": round(total_amount / total_tx, 2),
            "nb_anomalous_tx": nb_anomalous,
            "fraud_suspicion_score": suspicion,
            "fraud_alert_level": alert_level,
            "priority_investigation": 1 if alert_level == "HIGH" else 0,
        })
    return rows


def generate_mart_portfolio_perf():
    rows = []
    for i, bank_name in enumerate(BANK_NAMES):
        ret = round(random.uniform(2, 18), 2)
        vol = round(random.uniform(5, 30), 2)
        sharpe = round((ret - 3) / vol, 4)

        if sharpe > 1.5:
            perf_seg = "top_performer"
        elif sharpe > 0.8:
            perf_seg = "average_performer"
        else:
            perf_seg = "underperformer"

        rows.append({
            "bank_id": i + 1,
            "bank_name": bank_name,
            "ticker": bank_name[:3].upper(),
            "annualized_return_pct": ret,
            "annualized_volatility_pct": vol,
            "sharpe_ratio": sharpe,
            "cumulative_return_pct": round(ret * random.uniform(2, 5), 2),
            "avg_daily_volume": round(random.uniform(100000, 10000000), 2),
            "performance_segment": perf_seg,
        })
    return rows


def generate_macro_geo_latest():
    rows = []
    for country_name, country_code in COUNTRIES:
        rows.append({
            "country_code": country_code,
            "country_name": country_name,
            "inflation_pct": round(random.uniform(0.5, 12.0), 2),
            "unemployment_pct": round(random.uniform(2.0, 20.0), 2),
            "lending_rate_pct": round(random.uniform(1.0, 15.0), 2),
            "gdp_trillion_usd": round(random.uniform(0.1, 5.0), 3),
            "last_updated": fake.date_between(start_date="-6m", end_date="today"),
        })
    return rows


if __name__ == "__main__":
    print("Generating synthetic banking data...\n")
    credit = generate_credit_scoring_results()
    write_csv("credit_scoring_results.csv", credit)
    write_csv("mart_risk_scoring.csv", generate_mart_risk_scoring(credit))
    write_csv("mart_fraud_indicators.csv", generate_mart_fraud_indicators(credit))
    write_csv("mart_portfolio_perf.csv", generate_mart_portfolio_perf())
    write_csv("macro_geo_latest.csv", generate_macro_geo_latest())
    print("\nDone. All CSV files saved in data/")
    print("Load into Power BI: Home > Get Data > Text/CSV")

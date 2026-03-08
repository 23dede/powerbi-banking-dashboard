# Definition des roles RLS — Projet Bancaire Power BI

## Vue d'ensemble

| Role | Acces Fraude | Acces Portfolio | Acces Clients/Risk |
|------|-------------|-----------------|-------------------|
| `Risk_Manager` | LOW + MEDIUM | Complet | Complet |
| `Fraud_Analyst` | HIGH + MEDIUM + anomalies | Aucun | Partiel (score > 20) |
| `Portfolio_Manager` | Aucun | Complet | Aucun (RGPD) |

---

## Risk_Manager

```dax
-- mart_fraud_indicators
[fraud_alert_level] IN { "LOW", "MEDIUM" }

-- Toutes les autres tables : pas de filtre (acces complet)
```

**Acces :** Voit les alertes fraude faibles et moyennes. Acces complet au risque client, scoring ML et donnees macro.

---

## Fraud_Analyst

```dax
-- mart_fraud_indicators
[fraud_alert_level] IN { "HIGH", "MEDIUM" }
    || [nb_anomalous_tx] > 0
    || [priority_investigation] = 1

-- credit_scoring_results
[fraud_suspicion_score] > 20
    || [total_fraud_count] > 0

-- mart_portfolio_perf (aucun acces)
[ticker] = "__NO_ACCESS__"
```

**Acces :** Specialise fraude haute et moyenne criticite. Aucun acces aux donnees portfolio (cloisonnement metier).

---

## Portfolio_Manager

```dax
-- mart_portfolio_perf : pas de filtre (acces complet)
-- macro_geo_latest : pas de filtre (acces complet)

-- credit_scoring_results (aucun acces - RGPD)
[client_id] = -1

-- mart_risk_scoring (aucun acces)
[client_id] = -1

-- mart_fraud_indicators (aucun acces)
[client_id] = -1
```

**Acces :** Vision complete du portfolio et des donnees macro-economiques. Aucun acces aux donnees personnelles clients (conformite RGPD stricte).

---

*Configuration a appliquer dans Power BI Desktop > Modelisation > Gerer les roles*

# 🔐 Définition des rôles RLS — Projet Bancaire Power BI

## Vue d'ensemble

| Rôle | Accès Fraude | Accès Portfolio | Accès Clients/Risk |
|------|-------------|-----------------|-------------------|
| `Risk_Manager` | LOW + MEDIUM | ✅ Complet | ✅ Complet |
| `Fraud_Analyst` | HIGH + MEDIUM + anomalies | ❌ Aucun | ⚠️ Partiel (score > 20) |
| `Portfolio_Manager` | ❌ Aucun | ✅ Complet | ❌ Aucun (RGPD) |

---

## 🏦 Risk_Manager

```dax
-- mart_fraud_indicators
[fraud_alert_level] IN { "LOW", "MEDIUM" }

-- Toutes les autres tables : pas de filtre (accès complet)
```

**Accès :** Voit les alertes fraude faibles et moyennes. Accès complet au risque client, scoring ML et données macro.

---

## 🔍 Fraud_Analyst

```dax
-- mart_fraud_indicators
[fraud_alert_level] IN { "HIGH", "MEDIUM" }
    || [nb_anomalous_tx] > 0
    || [priority_investigation] = 1

-- credit_scoring_results
[fraud_suspicion_score] > 20
    || [total_fraud_count] > 0

-- mart_portfolio_perf (aucun accès)
[ticker] = "__NO_ACCESS__"
```

**Accès :** Spécialisé fraude haute et moyenne criticité. Aucun accès aux données portfolio (cloisonnement métier).

---

## 📈 Portfolio_Manager

```dax
-- mart_portfolio_perf : pas de filtre (accès complet)
-- macro_geo_latest : pas de filtre (accès complet)

-- credit_scoring_results (aucun accès — RGPD)
[client_id] = -1

-- mart_risk_scoring (aucun accès)
[client_id] = -1

-- mart_fraud_indicators (aucun accès)
[client_id] = -1
```

**Accès :** Vision complète du portfolio et des données macro-économiques. Aucun accès aux données personnelles clients (conformité RGPD stricte).

---

*Configuration à appliquer dans Power BI Desktop → Modélisation → Gérer les rôles*

# 📊 Projet Bancaire – Power BI Dashboard

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![Architecture](https://img.shields.io/badge/Architecture-Médaillon%20Bronze%2FSilver%2FGold-blue)
![Status](https://img.shields.io/badge/Status-Publié-brightgreen)

---

## 🎯 Contexte

Ce projet a pour objectif de construire un **dashboard d'analyse de risque bancaire** sous Power BI, destiné à la prise de décision stratégique dans le secteur financier.

Il intègre :
- Une **segmentation ML** des clients par niveau de risque (`low_risk`, `medium_risk`, `high_risk`)
- Des **indicateurs clés de fraude** pour identifier les transactions suspectes
- Une analyse de la **performance du portfolio** bancaire par établissement
- Une vue **macro-économique** géolocalisée (inflation, chômage, taux de prêt)

Le projet s'inscrit dans une **architecture moderne de données en médaillon (Bronze → Silver → Gold)**, garantissant qualité, traçabilité et fiabilité des données à chaque étape du pipeline :

| Couche | Rôle |
|--------|------|
| 🥉 **Bronze** | Données brutes ingérées depuis les sources (banques, transactions, scores ML) |
| 🥈 **Silver** | Données nettoyées, normalisées et dédupliquées |
| 🥇 **Gold** | Marts analytiques prêts à consommer dans Power BI |

---

## 📋 Récapitulatif complet

### 🔗 Relations entre les tables

Deux relations valides ont été créées dans le modèle Power BI :

| Table source | Colonne | Table cible | Colonne | Cardinalité |
|---|---|---|---|---|
| `credit_scoring_results` | `client_id` | `mart_risk_scoring` | `client_id` | **1:1** |
| `credit_scoring_results` | `client_id` | `mart_fraud_indicators` | `client_id` | **1:1** |

> `mart_portfolio_perf` et `macro_geo_latest` sont des tables **indépendantes** (pas de clé commune — comportement normal et voulu).

**Corrections effectuées :** Relations sur `bank_id` et `country_code` identifiées comme invalides → non créées.

---

### 📐 Mesures DAX créées (16 au total)

#### Table `credit_scoring_results` — 6 mesures

```dax
Risk Segment Count =
CALCULATE(
    COUNTROWS( credit_scoring_results ),
    ALLSELECTED( credit_scoring_results[ml_risk_segment] )
)

Risk Segment % =
DIVIDE(
    COUNTROWS( credit_scoring_results ),
    CALCULATE( COUNTROWS( credit_scoring_results ), ALL( credit_scoring_results ) ),
    0
)

Total Clients =
COUNTROWS( credit_scoring_results )

Avg ML Risk Score =
AVERAGE( credit_scoring_results[ml_risk_score] )

Clients High Risk =
CALCULATE(
    COUNTROWS( credit_scoring_results ),
    credit_scoring_results[ml_risk_segment] = "high_risk"
)

DBT ML Agreement % =
DIVIDE(
    CALCULATE(
        COUNTROWS( credit_scoring_results ),
        credit_scoring_results[segments_agree] = TRUE()
    ),
    COUNTROWS( credit_scoring_results ),
    0
) * 100
```

#### Table `mart_portfolio_perf` — 5 mesures

```dax
Sharpe Ratio =
DIVIDE(
    mart_portfolio_perf[annualized_return_pct] - 3,
    mart_portfolio_perf[annualized_volatility_pct],
    0
)

Avg Sharpe Ratio =
AVERAGE( mart_portfolio_perf[sharpe_ratio] )

Best Sharpe Bank =
CALCULATE(
    SELECTEDVALUE( mart_portfolio_perf[bank_name] ),
    mart_portfolio_perf[sharpe_ratio] = MAX( mart_portfolio_perf[sharpe_ratio] )
)

Avg Volatility % =
AVERAGE( mart_portfolio_perf[annualized_volatility_pct] )

Avg Annualized Return % =
AVERAGE( mart_portfolio_perf[annualized_return_pct] )
```

#### Table `mart_fraud_indicators` — 4 mesures

```dax
Fraud Rate Pct =
DIVIDE(
    SUM( mart_fraud_indicators[total_fraud_count] ),
    SUM( mart_fraud_indicators[total_transactions] ),
    0
) * 100

Fraud High Alert Count =
CALCULATE(
    COUNTROWS( mart_fraud_indicators ),
    mart_fraud_indicators[fraud_alert_level] = "HIGH"
)

Fraud Amount % of Total =
DIVIDE(
    SUM( mart_fraud_indicators[total_fraud_amount] ),
    SUM( mart_fraud_indicators[total_amount] ),
    0
) * 100

Priority Investigation Count =
CALCULATE(
    COUNTROWS( mart_fraud_indicators ),
    mart_fraud_indicators[priority_investigation] = 1
)
```

#### Table `macro_geo_latest` — 1 mesure

```dax
Macro Risk Index =
VAR inflation_norm = DIVIDE( macro_geo_latest[inflation_pct], 10, 0 ) * 40
VAR unemp_norm     = DIVIDE( macro_geo_latest[unemployment_pct], 20, 0 ) * 30
VAR lending_norm   = DIVIDE( COALESCE( macro_geo_latest[lending_rate_pct], 5 ), 50, 0 ) * 30
RETURN ROUND( inflation_norm + unemp_norm + lending_norm, 1 )
```

---

### 📄 Pages et visuels construits (3 pages – 20 visuels)

#### Page 1 — Risk Overview (6 visuels)

| # | Visuel | Champs |
|---|---|---|
| 1 | 4 Cartes KPI | Total Clients / Clients High Risk / Avg ML Risk Score / DBT ML Agreement % |
| 2 | Graphique en anneau | Valeurs = Risk Segment Count · Légende = ml_risk_segment |
| 3 | Histogramme | Axe X = ml_risk_score (tranches 10) · Axe Y = Count |
| 4 | Barres horizontales | Axe Y = job · Axe X = Avg ML Risk Score · trié ASC |
| 5 | Filled Map | Emplacement = country_name · Saturation = inflation_pct · Tooltip = gdp, lending_rate, Macro Risk Index |
| 6 | Slicer | ml_risk_segment (boutons, sélection multiple) |

#### Page 2 — Portfolio Performance (5 visuels)

| # | Visuel | Champs |
|---|---|---|
| 1 | 4 Cartes KPI | Avg Annualized Return % / Avg Sharpe Ratio / Best Sharpe Bank / Avg Volatility % |
| 2 | Barres groupées | Axe X = bank_name · Axe Y = cumulative_return_pct + annualized_return_pct · trié DESC |
| 3 | Nuage de points | Axe X = annualized_volatility_pct · Axe Y = annualized_return_pct · Taille = avg_daily_volume · Légende = bank_name |
| 4 | Graphique en courbes | Axe X = bank_name · Axe Y = sharpe_ratio · Ligne référence Y=1.0 |
| 5 | Table | bank_name / cumulative_return_pct / sharpe_ratio / annualized_volatility_pct / performance_segment — icônes conditionnelles |

#### Page 3 — Fraud Detection (6 visuels)

| # | Visuel | Champs |
|---|---|---|
| 1 | 4 Cartes KPI | Fraud High Alert Count / Fraud Amount % of Total / Priority Investigation Count / Fraud Rate Pct |
| 2 | Nuage de points | Axe X = avg_tx_amount · Axe Y = fraud_suspicion_score · Taille = nb_anomalous_tx · Couleur = fraud_alert_level |
| 3 | Table TOP 10 | client_id / fraud_suspicion_score / fraud_alert_level / nb_anomalous_tx / fraud_rate_pct — Top N = 10 |
| 4 | Matrice heatmap | Lignes = job · Colonnes = fraud_alert_level · Valeurs = Count · Mise en forme cond. blanc→rouge |
| 5 | Histogramme | Axe X = fraud_suspicion_score (tranches 10) · Ligne référence X=60 |
| 6 | Slicer | fraud_alert_level (boutons ALL / LOW / MEDIUM / HIGH) |

---

### 🔐 Rôles RLS définis (3 rôles)

#### 🏦 Risk_Manager
```dax
-- mart_fraud_indicators
[fraud_alert_level] IN { "LOW", "MEDIUM" }
-- Toutes les autres tables : accès complet
```

#### 🔍 Fraud_Analyst
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

#### 📈 Portfolio_Manager
```dax
-- mart_portfolio_perf : accès complet
-- macro_geo_latest : accès complet

-- credit_scoring_results (aucun accès — RGPD)
[client_id] = -1

-- mart_risk_scoring (aucun accès)
[client_id] = -1

-- mart_fraud_indicators (aucun accès)
[client_id] = -1
```

---

## 📷 Capture d'écran — Risk Overview

> 📌 *Capture d'écran à insérer ici* — Page **Risk Overview**

Cette page illustre les **5 visuels principaux** retenus :
- 🔢 **4 cartes KPI** : Total Clients, Clients High Risk, Avg ML Risk Score, DBT ML Agreement %
- 🍩 **Donut chart** : répartition des clients par segment de risque ML

```
screenshots/Risk_Overview.png
```

_Pour ajouter la capture : glissez votre fichier `Risk_Overview.png` dans le dossier `screenshots/` du dépôt._

---

## 🚀 Valeur ajoutée

| Apport | Détail |
|---|---|
| 🔍 **Vue d'ensemble des risques** | Segmentation ML claire (low / medium / high risk) avec scores et distribution |
| 📈 **Indicateurs clés décisionnels** | 16 mesures DAX couvrant risque, fraude, portfolio et macro-économie |
| 🛡️ **Sécurité des données via RLS** | 3 rôles distincts avec filtres DAX précis — conformité RGPD garantie |
| 🏦 **Performance portfolio** | Sharpe Ratio, volatilité, rendement annualisé par banque |
| 🌍 **Contexte macro-géographique** | Carte interactive avec inflation, chômage et taux de prêt par pays |

La structuration **Bronze / Silver / Gold** apporte une **gouvernance robuste** :
- Chaque couche est versionnée et traçable
- Les données Gold consommées par Power BI sont **validées et certifiées**
- Le pipeline garantit la **cohérence** entre les marts analytiques

---

## 🔮 Améliorations futures

- [ ] **Page "Client Profiling"** : analyse démographique (âge, revenu, montant de crédit, historique)
- [ ] **Filtres interactifs avancés** : période temporelle, région géographique, segment de banque
- [ ] **Publication du fichier `.pbix`** : mise à disposition du fichier Power BI complet
- [ ] **Alertes dynamiques** : notifications automatiques pour les cas `HIGH` fraud alert
- [ ] **Intégration CI/CD** : validation automatique des mesures DAX via pipeline dbt
- [ ] **Connexion live** : passage de l'import mode au DirectQuery sur la couche Gold

---

## 📁 Structure du dépôt

```
powerbi-banking-dashboard/
├── README.md                    ← Documentation complète du projet
├── dax/
│   ├── credit_scoring.dax       ← Mesures table credit_scoring_results
│   ├── portfolio_perf.dax       ← Mesures table mart_portfolio_perf
│   ├── fraud_indicators.dax     ← Mesures table mart_fraud_indicators
│   └── macro_geo.dax            ← Mesure Macro Risk Index
├── rls/
│   └── roles_definition.md      ← Définition complète des 3 rôles RLS
└── screenshots/
    └── Risk_Overview.png        ← Capture d'écran page Risk Overview (à ajouter)
```

---

*Projet réalisé avec Power BI Desktop · Architecture Médaillon · DAX · RLS*

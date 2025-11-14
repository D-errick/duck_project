# 🦆 Duck Analytics — Bidco Retail ETL & Visualization

![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)
![Postgres](https://img.shields.io/badge/Postgres-14+-blue?logo=postgresql)
![Superset](https://img.shields.io/badge/Apache%20Superset-Dashboarding-orange?logo=apache)
![Status](https://img.shields.io/badge/Status-Active-success)

> **End-to-end analytics pipeline for Bidco retail data — from Excel ingestion → Postgres ETL → Superset dashboards.**

---

## 🧭 Project Overview

This project demonstrates a **modern data analytics pipeline** built with:
- 🧩 **PostgreSQL** — centralized data warehouse  
- 🧹 **Python ETL (pandas + SQLAlchemy)** — data cleaning, health scoring, and KPI computation  
- 📊 **Apache Superset** — dashboarding and insight visualization  
- 🐳 **Docker Compose** — unified orchestration of all components  

---

## 🧱 Architecture

```

Excel Source (.xlsx)
│
▼
🐍 etl_bidco.py
(pandas + SQLAlchemy)
│
▼
PostgreSQL (Docker)
│
▼
Apache Superset
(visual dashboards)

````

---

## ⚙️ Setup Instructions

### 🐳 1️⃣ Build and Start the Containers

```bash
docker-compose build --no-cache superset
docker-compose up -d
````

---

### 🧪 2️⃣ Verify Python-Postgres Connector

```bash
docker exec -it superset_app python -c "import psycopg2; print('psycopg2 OK')"
```

✅ Expected output:

```
psycopg2 OK
```

---

### 🧹 3️⃣ Run the ETL Script

```bash
python3 etl_bidco.py
```

Example output:

```
📥 Loading Excel file...
🧹 Cleaning data...
💰 Computing KPIs...
🚀 Loading tables into Postgres...
✅ ETL Complete! Tables loaded:
- cleaned_sales
- data_health
- kpi_promotions
- kpi_pricing_index
```

---

### ⚙️ 4️⃣ Connect Superset to Postgres

In your browser → **[http://localhost:8088](http://localhost:8088)**
Login (default): `admin / admin`

Go to
**Settings → Data → Databases → + Database → Connect SQLAlchemy URI**

Paste this connection string:

```
postgresql://duckuser:duckpass@postgres:5432/duckdb
```

✅ **Test Connection → Save**

---

## 📊 Visualization & Insights

### 🧹 1️⃣ Data Health — Table: `data_health`

**Purpose:** Track data quality across stores.

| Column          | Description             |
| --------------- | ----------------------- |
| `store_name`    | Store identifier        |
| `missing_pct`   | % of missing values     |
| `duplicate_pct` | % of duplicate entries  |
| `outlier_pct`   | % of anomalies detected |
| `health_score`  | Overall quality score   |
| `remarks`       | Data quality notes      |

**Recommended Visuals:**

* **Horizontal Bar Chart:** `store_name` vs `health_score`
* **Heatmap:** `missing_pct` & `duplicate_pct`
* **KPI Card:** “% of stores below 70% health”

> 🧠 *Insight:* Quickly detect which stores or regions need data quality improvement.

---

### 💸 2️⃣ Promotions Performance — Table: `kpi_promotions`

**Purpose:** Evaluate effectiveness of promotions across SKUs.

| Column                           | Description                   |
| -------------------------------- | ----------------------------- |
| `supplier`                       | Product supplier              |
| `description`                    | SKU name                      |
| `baseline_units` / `promo_units` | Sales before/during promotion |
| `promo_uplift_%`                 | % increase in units sold      |
| `promo_price_impact_%`           | % change in price             |
| `coverage_%`                     | Share of SKUs promoted        |

**Recommended Visuals:**

* **Bar Chart:** `supplier` vs `promo_uplift_%`
* **Scatter Plot:** `promo_price_impact_%` vs `coverage_%`
* **KPI Card:** “Average promo uplift”

> 🧠 *Insight:* Identify which products deliver the highest promo ROI.

---

### 💰 3️⃣ Pricing Index — Table: `kpi_pricing_index`

**Purpose:** Compare Bidco’s price positioning against competitors.

| Column                      | Description                           |
| --------------------------- | ------------------------------------- |
| `store_name`                | Store or region                       |
| `sub-department`            | Product grouping                      |
| `avg_unit_price_bidco`      | Average Bidco price                   |
| `avg_unit_price_competitor` | Competitor average                    |
| `price_index`               | (Bidco / Competitor) × 100            |
| `positioning`               | “Below Market” / “At Par” / “Premium” |

**Recommended Visuals:**

* **Grouped Bar Chart:** Compare Bidco vs competitors by `sub-department`
* **Box Plot:** Price index distribution by `section`
* **KPI Card:** “% of Bidco products priced below market”

> 🧠 *Insight:* Reveals Bidco’s competitiveness and pricing opportunities.

---

## 🧩 Suggested Dashboard Layout

**Dashboard Name:** `Bidco Retail Insights`

| Section        | Visualization         | Purpose                     |
| -------------- | --------------------- | --------------------------- |
| 🧹 Data Health | Bar chart + KPI cards | Store-level data quality    |
| 💸 Promotions  | Bar + Scatter         | Uplift and coverage impact  |
| 💰 Pricing     | Grouped bar + KPI     | Market positioning analysis |

---

## 🔮 Future Enhancements

* 🕒 Automate ETL with **Apache Airflow** or **Prefect**
* ☁️ Deploy stack on **AWS ECS** or **Azure Container Apps**
* 🧠 Add **forecasting (Prophet)** or anomaly detection to Superset
* 🧾 Build **management dashboards** with cross-filters

---

## 🧑‍💻 Author

---

## 🪶 License

MIT License © 2025 Thonnet Wange
Free for educational and personal use.
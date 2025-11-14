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

-------------------
Dashboard snapshot:
--------------------
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/c15f68f8-39da-4607-9f37-13d6f1a55eb5" />





## 🔮 Future Enhancements

* 🕒 Automate ETL with **Apache Airflow** or **Prefect**
* ☁️ Deploy stack on **AWS ECS** or **Azure Container Apps**
* 🧠 Add **forecasting (Prophet)** or anomaly detection to Superset
* 🧾 Build **management dashboards** with cross-filters

---

## 🧑‍💻 Author
Derrick Simiyu. 
---

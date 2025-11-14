# etl_bidco.py
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# =============================
# 1. CONFIG
# =============================
POSTGRES_USER = "duckuser"
POSTGRES_PASSWORD = "duckpass"
POSTGRES_DB = "duckdb"
POSTGRES_HOST = "localhost"  # use 'postgres' if running from inside another container

EXCEL_PATH = "Test_Data.xlsx"

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}")

# =============================
# 2. LOAD RAW DATA
# =============================
print("📥 Loading Excel file...")
df = pd.read_excel(EXCEL_PATH)

# standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# =============================
# 3. CLEANING AND ENRICHMENT
# =============================
print("🧹 Cleaning data...")

# Remove duplicates
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Handle missing numeric fields
df["quantity"] = df["quantity"].fillna(0)
df["total_sales"] = df["total_sales"].fillna(0)
df["rrp"] = df["rrp"].fillna(df["rrp"].median())

# Derived metrics
df["unit_price"] = df["total_sales"] / df["quantity"].replace(0, np.nan)
df["discount_pct"] = 1 - (df["unit_price"] / df["rrp"])
df["on_promo"] = df["discount_pct"] > 0.10

# Flag outliers
df["is_outlier"] = (df["quantity"] < 0) | (df["unit_price"] < 0) | (df["unit_price"] > df["rrp"] * 3)

# =============================
# 4. DATA HEALTH SCORE
# =============================
print("🩺 Computing data health...")

health_df = (
    df.groupby("store_name")
    .agg(
        missing_pct=("quantity", lambda x: x.isna().mean() * 100),
        duplicate_pct=("item_code", lambda x: duplicates / len(df) * 100),
        outlier_pct=("is_outlier", lambda x: x.mean() * 100),
    )
    .reset_index()
)
health_df["health_score"] = 100 - (
    health_df["missing_pct"] * 0.4 + health_df["duplicate_pct"] * 0.3 + health_df["outlier_pct"] * 0.3
)
health_df["remarks"] = np.where(health_df["health_score"] >= 90, "Clean",
                                np.where(health_df["health_score"] >= 80, "Fair", "Unreliable"))

# =============================
# 5. PROMOTION KPIs
# =============================
print("📊 Computing promotion KPIs...")

promo_df = (
    df.groupby(["supplier", "description"])
    .agg(
        baseline_units=("quantity", lambda x: x[~df.loc[x.index, "on_promo"]].sum()),
        promo_units=("quantity", lambda x: x[df.loc[x.index, "on_promo"]].sum()),
        avg_rrp=("rrp", "mean"),
        promo_price=("unit_price", lambda x: x[df.loc[x.index, "on_promo"]].mean()),
        baseline_price=("unit_price", lambda x: x[~df.loc[x.index, "on_promo"]].mean()),
    )
    .reset_index()
)

promo_df["promo_uplift_%"] = (
    (promo_df["promo_units"] - promo_df["baseline_units"]) / promo_df["baseline_units"].replace(0, np.nan)
) * 100
promo_df["promo_price_impact_%"] = (
    (1 - promo_df["promo_price"] / promo_df["avg_rrp"]) * 100
)
# compute store coverage properly using aligned indices
promo_coverage = (
    df[df["on_promo"]]
    .groupby(["supplier", "description"])["store_name"]
    .nunique()
    .rename("promo_stores")
    .reset_index()
)

total_coverage = (
    df.groupby(["supplier", "description"])["store_name"]
    .nunique()
    .rename("total_stores")
    .reset_index()
)

coverage_df = pd.merge(promo_coverage, total_coverage, on=["supplier", "description"], how="right")
coverage_df["coverage_%"] = (coverage_df["promo_stores"] / coverage_df["total_stores"]) * 100
coverage_df["coverage_%"] = coverage_df["coverage_%"].fillna(0)

# merge back into promo_df
promo_df = pd.merge(promo_df, coverage_df[["supplier", "description", "coverage_%"]],
                    on=["supplier", "description"], how="left")

# =============================
# 6. PRICING INDEX
# =============================
print("💰 Computing price index...")

# Average price per sub-department, section, supplier
pricing_df = (
    df.groupby(["store_name", "sub-department", "section", "supplier"])
    .agg(avg_unit_price=("unit_price", "mean"))
    .reset_index()
)

# Identify Bidco and competitors
bidco_prices = pricing_df[pricing_df["supplier"].str.contains("bidco", case=False)]
competitor_prices = pricing_df[~pricing_df["supplier"].str.contains("bidco", case=False)]

price_index = bidco_prices.merge(
    competitor_prices,
    on=["store_name", "sub-department", "section"],
    suffixes=("_bidco", "_competitor"),
    how="left",
)
price_index["price_index"] = (price_index["avg_unit_price_bidco"] / price_index["avg_unit_price_competitor"]) * 100
price_index["positioning"] = np.select(
    [price_index["price_index"] > 105, price_index["price_index"] < 95],
    ["Premium", "Discount"],
    default="Near-Market",
)

# =============================
# 7. LOAD TO POSTGRES
# =============================
print("🚀 Loading tables into Postgres...")

df.to_sql("cleaned_sales", engine, if_exists="replace", index=False)
health_df.to_sql("data_health", engine, if_exists="replace", index=False)
promo_df.to_sql("kpi_promotions", engine, if_exists="replace", index=False)
price_index.to_sql("kpi_pricing_index", engine, if_exists="replace", index=False)

print("✅ ETL Complete! Tables loaded:")
print("- cleaned_sales")
print("- data_health")
print("- kpi_promotions")
print("- kpi_pricing_index")

# ======================================================
# AMAZON DATA PREPROCESSING (PRODUCTION ETL PIPELINE)
# Raw CSV → Clean → Feature Engineering → SQLite
# + CATEGORY NORMALIZATION (Business Ready)
# ======================================================

import pandas as pd
import sqlite3
import re
import os

print("🚀 Starting preprocessing...")


# ======================================================
# 1. FILE PATHS (WINDOWS ABSOLUTE PATHS)
# ======================================================

csv_path = r"C:\Users\acer\Downloads\amazon.csv"
db_path  = r"C:\Users\acer\Downloads\amazon_sales.db"

print("📂 CSV Path :", csv_path)
print("📂 DB Path  :", db_path)


# ======================================================
# 2. LOAD DATA
# ======================================================

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ CSV not found: {csv_path}")

df = pd.read_csv(csv_path)

print(f"✅ Loaded {len(df):,} rows")


# ======================================================
# 3. CLEANING HELPERS
# ======================================================

def clean_price(x):
    if pd.isna(x):
        return 0.0
    return float(re.sub(r"[^\d.]", "", str(x)) or 0)


def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip().lower()


# ======================================================
# 4. CORE CLEANING
# ======================================================

print("🧹 Cleaning prices...")

df["discounted_price"] = df["discounted_price"].apply(clean_price)
df["actual_price"] = df["actual_price"].apply(clean_price)

print("🧹 Cleaning ratings...")

df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=True)
)

df["rating_count"] = (
    pd.to_numeric(df["rating_count"], errors="coerce")
    .fillna(0)
    .astype(int)
)

print("🧹 Cleaning text columns...")

df["product_name"] = df["product_name"].apply(clean_text)
df["category"] = df["category"].apply(clean_text)


# ======================================================
# ⭐ 5. CATEGORY NORMALIZATION (REAL DATA-DRIVEN)
# ======================================================
# electronics|mobiles|smartphones → electronics
# home&kitchen|cookware → home&kitchen

print("🏷 Normalizing categories...")

df["main_category_raw"] = df["category"].str.split("|").str[0]

category_map = {
    "electronics": "Electronics",
    "computers&accessories": "Computers",
    "home&kitchen": "Home & Kitchen",
    "health&personalcare": "Personal Care",
    "officeproducts": "Stationery",
    "homeimprovement": "Home Improvement",
    "toys&games": "Toys & Games",
    "musicalinstruments": "Musical Instruments",
    "car&motorbike": "Automotive"
}

df["main_category"] = df["main_category_raw"].map(category_map).fillna("Other")


# ======================================================
# 6. FEATURE ENGINEERING
# ======================================================

print("⚙️ Creating features...")

df["discount_percent"] = (
    (df["actual_price"] - df["discounted_price"]) /
    df["actual_price"].replace(0, 1)
) * 100

df["discount_percent"] = df["discount_percent"].round(2)

df["price_savings"] = df["actual_price"] - df["discounted_price"]

df["popularity_score"] = df["rating"] * df["rating_count"]

df["price_bucket"] = pd.cut(
    df["discounted_price"],
    bins=[0, 500, 1000, 2000, 5000, 10000, 999999],
    labels=["budget", "low", "mid", "upper-mid", "premium", "luxury"]
)


# ======================================================
# 7. REMOVE BAD DATA
# ======================================================

before = len(df)

df = df[df["actual_price"] > 0]
df = df[df["discounted_price"] >= 0]

df.drop_duplicates(subset=["product_name", "discounted_price"], inplace=True)

after = len(df)

print(f"🗑 Removed {before-after:,} bad/duplicate rows")


# ======================================================
# 8. FINAL STRUCTURED DATASET
# ======================================================

final_df = df[[
    "product_name",
    "category",          # raw breadcrumb
    "main_category",     # ⭐ clean business category
    "discounted_price",
    "actual_price",
    "price_savings",
    "discount_percent",
    "rating",
    "rating_count",
    "popularity_score",
    "price_bucket"
]].copy()

print("✅ Final dataset ready")
print(final_df.head())


# ======================================================
# 9. SAVE TO SQLITE DATABASE
# ======================================================

print("💾 Writing to SQLite...")

conn = sqlite3.connect(db_path)

final_df.to_sql("sales", conn, if_exists="replace", index=False)

# Indexes for faster dashboard
conn.execute("CREATE INDEX IF NOT EXISTS idx_main_category ON sales(main_category)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_rating ON sales(rating)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_price ON sales(discounted_price)")

conn.commit()
conn.close()


# ======================================================
# 10. DONE
# ======================================================

print(f"""
🎉 ETL Complete!

Database  : {db_path}
Rows      : {len(final_df):,}
Columns   : {len(final_df.columns)}

Main Categories Created:
Electronics | Computers | Home & Kitchen | Personal Care |
Stationery | Home Improvement | Toys & Games |
Musical Instruments | Automotive
""")

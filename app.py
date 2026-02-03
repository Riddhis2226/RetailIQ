# =====================================================
# AMAZON SALES BI DASHBOARD (Streamlit + SQLite + Plotly)
# Colorful • Full Width • Professional BI Layout
# =====================================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio

# -----------------------------------------------------
# GLOBAL STYLE (makes everything colorful + modern)
# -----------------------------------------------------

pio.templates.default = "plotly_dark"   # dark professional theme
COLORS = px.colors.qualitative.Set2     # nice dashboard palette


st.set_page_config(page_title="Amazon Sales BI", layout="wide")

st.title("📊 Amazon Sales Intelligence Dashboard")


# =====================================================
# DATABASE CONNECTION
# =====================================================

DB_PATH = r"C:\Users\acer\Downloads\amazon_sales.db"


@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


conn = get_conn()


# =====================================================
# FILTER OPTIONS
# =====================================================

categories = pd.read_sql(
    "SELECT DISTINCT main_category FROM sales ORDER BY main_category",
    conn
)

buckets = pd.read_sql(
    "SELECT DISTINCT price_bucket FROM sales ORDER BY price_bucket",
    conn
)


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Filters")

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories["main_category"].tolist()
)

selected_bucket = st.sidebar.selectbox(
    "Price Bucket",
    ["All"] + buckets["price_bucket"].astype(str).tolist()
)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)


# =====================================================
# SAFE WHERE CLAUSE
# =====================================================

conditions = ["1=1"]
params = {"rating": min_rating}

if selected_category != "All":
    conditions.append("main_category = :cat")
    params["cat"] = selected_category

if selected_bucket != "All":
    conditions.append("price_bucket = :bucket")
    params["bucket"] = selected_bucket

conditions.append("rating >= :rating")

where_clause = " AND ".join(conditions)


# =====================================================
# KPI CARDS
# =====================================================

kpis = pd.read_sql(f"""
SELECT
    COUNT(*) as products,
    ROUND(AVG(rating),2) as rating,
    ROUND(AVG(discount_percent),2) as discount,
    ROUND(SUM(discounted_price),2) as revenue
FROM sales
WHERE {where_clause}
""", conn, params=params)

products = int(kpis.products[0])
rating = kpis.rating[0]
discount = kpis.discount[0]
revenue = int(kpis.revenue[0])

c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Products", f"{products:,}")
c2.metric("⭐ Avg Rating", rating)
c3.metric("💸 Avg Discount", f"{discount}%")
c4.metric("💰 Revenue", f"₹ {revenue:,}")

st.divider()


# =====================================================
# HELPER → truncate long product names
# =====================================================

def shorten(text, n=45):
    return text[:n] + "..." if len(text) > n else text


# =====================================================
# FULL WIDTH COLORFUL CHARTS
# =====================================================


# -----------------------------------------------------
# 🔥 Most Popular (green gradient)
# -----------------------------------------------------

popular = pd.read_sql(f"""
SELECT product_name, popularity_score
FROM sales
WHERE {where_clause}
ORDER BY popularity_score DESC
LIMIT 10
""", conn, params=params)

popular["short_name"] = popular["product_name"].apply(shorten)

fig1 = px.bar(
    popular,
    x="popularity_score",
    y="short_name",
    orientation="h",
    text="popularity_score",
    color="popularity_score",
    color_continuous_scale="viridis",
    hover_data=["product_name"],
    title="🔥 Most Popular Products"
)

fig1.update_layout(height=520, yaxis=dict(autorange="reversed"))

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------------------------------
# 💸 Discounts (red gradient)
# -----------------------------------------------------

discounts = pd.read_sql(f"""
SELECT product_name, discount_percent
FROM sales
WHERE {where_clause}
ORDER BY discount_percent DESC
LIMIT 10
""", conn, params=params)

discounts["short_name"] = discounts["product_name"].apply(shorten)

fig2 = px.bar(
    discounts,
    x="discount_percent",
    y="short_name",
    orientation="h",
    text="discount_percent",
    color="discount_percent",
    color_continuous_scale="reds",
    hover_data=["product_name"],
    title="💸 Top Discounted Products"
)

fig2.update_layout(height=520, yaxis=dict(autorange="reversed"))

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------------------------------
# 📦 Category Share (multi-color donut)
# -----------------------------------------------------

cat_df = pd.read_sql("""
SELECT main_category, COUNT(*) as count
FROM sales
GROUP BY main_category
ORDER BY count DESC
""", conn)

fig3 = px.pie(
    cat_df,
    names="main_category",
    values="count",
    hole=0.5,
    color_discrete_sequence=COLORS,
    title="📦 Product Share by Category"
)

st.plotly_chart(fig3, use_container_width=True)


# -----------------------------------------------------
# 💰 Revenue by Category (colorful bars)
# -----------------------------------------------------

rev_df = pd.read_sql("""
SELECT main_category,
       ROUND(SUM(discounted_price),2) as revenue
FROM sales
GROUP BY main_category
ORDER BY revenue DESC
""", conn)

fig4 = px.bar(
    rev_df,
    x="main_category",
    y="revenue",
    color="main_category",
    color_discrete_sequence=COLORS,
    text="revenue",
    title="💰 Revenue by Category"
)

st.plotly_chart(fig4, use_container_width=True)


# -----------------------------------------------------
# ⭐ Avg Rating by Price Segment (colorful bars)
# -----------------------------------------------------

rating_avg_df = pd.read_sql(f"""
SELECT price_bucket,
       ROUND(AVG(rating), 2) as avg_rating
FROM sales
WHERE {where_clause}
GROUP BY price_bucket
""", conn, params=params)

fig5 = px.bar(
    rating_avg_df,
    x="price_bucket",
    y="avg_rating",
    text="avg_rating",
    color="price_bucket",
    color_discrete_sequence=COLORS,
    title="⭐ Average Rating by Price Segment"
)

fig5.update_layout(height=450, yaxis=dict(range=[0, 5]))

st.plotly_chart(fig5, use_container_width=True)


# -----------------------------------------------------
# 💲 Price Bucket Distribution (colorful bars)
# -----------------------------------------------------

bucket_df = pd.read_sql("""
SELECT price_bucket, COUNT(*) as count
FROM sales
GROUP BY price_bucket
""", conn)

fig6 = px.bar(
    bucket_df,
    x="price_bucket",
    y="count",
    color="price_bucket",
    color_discrete_sequence=COLORS,
    text="count",
    title="💲 Product Distribution by Price Bucket"
)

st.plotly_chart(fig6, use_container_width=True)


# =====================================================
# FOOTER
# =====================================================

st.caption("Built with Streamlit • SQLite • Plotly | Colorful Professional BI Dashboard")

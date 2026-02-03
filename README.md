# 🛒 RetailIQ – Sales Intelligence Dashboard

A full-stack **Data Engineering + Business Intelligence (BI)** project that transforms raw e-commerce sales data into an interactive analytics dashboard using **Python, SQLite, and Streamlit**.

RetailIQ provides clean insights into product performance, pricing strategy, discounts, and customer ratings through a professional BI-style dashboard.

---

## 🚀 Features

### 📊 Dashboard Insights
- 🔥 Most popular products
- 💸 Top discounted products
- 📦 Category-wise distribution
- 💰 Revenue by category
- ⭐ Average rating by price segment
- 💲 Price bucket segmentation
- Interactive filters (category, price, rating)

### ⚙️ Data Engineering
- ETL pipeline
- Data cleaning & normalization
- Category standardization
- Feature engineering
- SQLite data warehouse
- Indexed queries for fast analytics

### 🎨 UI/UX
- Full-width charts
- Colorful visualizations
- Professional BI layout
- Streamlit-based interactive dashboard

---

## 🏗️ Project Architecture

```

amazon.csv (raw data)
↓
preprocessing.py (ETL + cleaning + features)
↓
amazon_sales.db (SQLite warehouse)
↓
analysis.ipynb (EDA & SQL analytics)
↓
app.py (Streamlit BI dashboard)

```

---

## 📂 Project Structure

```

RetailIQ/
│
├── preprocessing.py     # ETL pipeline
├── amazon.csv           # raw dataset
├── amazon_sales.db      # cleaned database
├── analysis.ipynb       # analytics notebook
├── app.py               # Streamlit dashboard
├── README.md

````

---

## ⚙️ Tech Stack

- Python
- Pandas
- SQLite
- Plotly
- Streamlit
- SQL

---

## 🧹 ETL Pipeline

`preprocessing.py` performs:

- Price cleaning (₹ removal, numeric conversion)
- Rating normalization
- Duplicate removal
- Feature engineering:
  - discount %
  - price savings
  - popularity score
  - price bucket
- Category normalization:
  - Electronics
  - Home & Kitchen
  - Computers
  - Personal Care
  - etc.
- Saves clean data to SQLite

Run:

```bash
python preprocessing.py
````

---

## 📊 Run Dashboard

Start the BI dashboard:

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 📸 Sample Insights

* Which products are most popular?
* Which categories generate highest revenue?
* Do premium products have better ratings?
* Where are the biggest discounts?
* Which price segment performs best?

---

## 🎯 Use Cases

* Sales performance monitoring
* Pricing strategy analysis
* Discount optimization
* Category trend analysis
* BI dashboard portfolio project
* Data engineering practice

---

## 🚀 Future Improvements

* Search functionality
* Export CSV/Excel
* ML price prediction
* Recommendation system
* Deployment to cloud (Streamlit Cloud / Render)
* Live auto-refresh

---

## 👩‍💻 Author

**Riddhima Singh**
Data Science & Analytics Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork & enhance!

```

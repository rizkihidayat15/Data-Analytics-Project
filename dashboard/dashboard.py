import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

sns.set(style="whitegrid")

st.set_page_config(page_title="Olist E-Commerce Dashboard", page_icon="🛒", layout="wide")

# ----------------------------------------------------------------
# Load data
# ----------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    date_cols = [
        "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df

all_df = load_data()

# ----------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------
st.sidebar.title("🛒 Olist E-Commerce")
st.sidebar.markdown("Filter data berdasarkan rentang tanggal pembelian dan negara bagian pelanggan.")

min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Tanggal Pembelian",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

state_options = sorted(all_df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    label="Negara Bagian Pelanggan",
    options=state_options,
    default=state_options,
)

mask = (
    (all_df["order_purchase_timestamp"].dt.date >= start_date)
    & (all_df["order_purchase_timestamp"].dt.date <= end_date)
    & (all_df["customer_state"].isin(selected_states))
)
main_df = all_df.loc[mask]

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard ini dibuat sebagai bagian dari submission Proyek Analisis Data Dicoding menggunakan dataset E-Commerce Public Dataset (Olist Brazilian E-Commerce).")

# ----------------------------------------------------------------
# Header
# ----------------------------------------------------------------
st.title("🛒 E-Commerce Public Dataset Dashboard")
st.markdown("Dashboard interaktif untuk eksplorasi performa penjualan, pengiriman, dan pelanggan pada **E-Commerce Public Dataset (Olist Brazilian E-Commerce)**.")

# ----------------------------------------------------------------
# Key Metrics
# ----------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_orders = main_df["order_id"].nunique()
total_revenue = main_df["total_price"].sum()
avg_review = main_df["review_score"].mean()
total_customers = main_df["customer_id"].nunique()

with col1:
    st.metric("Total Orders", f"{total_orders:,}")
with col2:
    st.metric("Total Revenue (BRL)", f"R$ {total_revenue:,.2f}")
with col3:
    st.metric("Rata-rata Review Score", f"{avg_review:.2f} / 5.0")
with col4:
    st.metric("Total Pelanggan", f"{total_customers:,}")

st.markdown("---")

# ----------------------------------------------------------------
# Pertanyaan 1: Tren order & revenue, kategori produk terbaik
# ----------------------------------------------------------------
st.header("📈 Tren Penjualan Bulanan & Kategori Produk Terbaik")

monthly_summary = (
    main_df.groupby("order_purchase_month")
    .agg(total_orders=("order_id", "nunique"), total_revenue=("total_price", "sum"))
    .reset_index()
    .sort_values("order_purchase_month")
)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly_summary["order_purchase_month"], monthly_summary["total_orders"], marker="o", color="#1f77b4")
    ax.set_title("Tren Jumlah Order per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Order")
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly_summary["order_purchase_month"], monthly_summary["total_revenue"], marker="o", color="#ff7f0e")
    ax.set_title("Tren Total Revenue per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Revenue (BRL)")
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)

st.subheader("Top 10 Kategori Produk Berdasarkan Revenue")

category_summary = (
    main_df.groupby("product_category_name_english")
    .agg(total_revenue=("total_price", "sum"), total_orders=("order_id", "nunique"))
    .reset_index()
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#d62728" if i == 0 else "#1f77b4" for i in range(len(category_summary))]
sns.barplot(data=category_summary, x="total_revenue", y="product_category_name_english", palette=colors, ax=ax)
ax.set_title("Top 10 Kategori Produk Berdasarkan Total Revenue")
ax.set_xlabel("Total Revenue (BRL)")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

st.markdown("---")

# ----------------------------------------------------------------
# Pertanyaan 2: Performa pengiriman vs review score
# ----------------------------------------------------------------
st.header("🚚 Performa Pengiriman & Kepuasan Pelanggan")

delivered_df = main_df[main_df["order_status"] == "delivered"].dropna(subset=["delivery_delay_days", "review_score"])
delivered_df["is_late"] = delivered_df["delivery_delay_days"] > 0

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(delivered_df["delivery_delay_days"], bins=30, kde=True, color="#2ca02c", ax=ax)
    ax.axvline(0, color="red", linestyle="--", label="Tepat waktu (0 hari)")
    ax.set_title("Distribusi Selisih Waktu Pengiriman Aktual vs Estimasi")
    ax.set_xlabel("Delivery Delay (hari)")
    ax.set_ylabel("Jumlah Order")
    ax.legend()
    st.pyplot(fig)

with col2:
    review_by_delay = delivered_df.groupby("is_late")["review_score"].mean().reset_index()
    review_by_delay["is_late"] = review_by_delay["is_late"].map({False: "Tepat Waktu / Lebih Cepat", True: "Terlambat"})

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=review_by_delay, x="is_late", y="review_score", palette=["#2ca02c", "#d62728"], ax=ax)
    ax.set_title("Rata-rata Review Score: Tepat Waktu vs Terlambat")
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata Review Score")
    ax.set_ylim(0, 5)
    st.pyplot(fig)

st.markdown("---")

# ----------------------------------------------------------------
# Analisis Lanjutan: RFM
# ----------------------------------------------------------------
st.header("🎯 Analisis Lanjutan: Segmentasi Pelanggan (RFM)")

rfm_base = main_df[main_df["order_status"] == "delivered"].copy()

if len(rfm_base) > 0:
    snapshot_date = rfm_base["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm_df = (
        rfm_base.groupby("customer_id")
        .agg(
            last_order_date=("order_purchase_timestamp", "max"),
            frequency=("order_id", "nunique"),
            monetary=("total_price", "sum"),
        )
        .reset_index()
    )
    rfm_df["recency"] = (snapshot_date - rfm_df["last_order_date"]).dt.days

    try:
        rfm_df["r_score"] = pd.qcut(rfm_df["recency"], 4, labels=[4, 3, 2, 1], duplicates="drop").astype(int)
        rfm_df["f_score"] = pd.qcut(rfm_df["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4], duplicates="drop").astype(int)
        rfm_df["m_score"] = pd.qcut(rfm_df["monetary"], 4, labels=[1, 2, 3, 4], duplicates="drop").astype(int)
        rfm_df["rfm_score"] = rfm_df["r_score"] + rfm_df["f_score"] + rfm_df["m_score"]

        def segment_customer(score):
            if score >= 10:
                return "Best Customer"
            elif score >= 7:
                return "Loyal Customer"
            elif score >= 5:
                return "Potential Customer"
            else:
                return "Churn Risk"

        rfm_df["segment"] = rfm_df["rfm_score"].apply(segment_customer)

        col1, col2 = st.columns([1, 1])

        with col1:
            segment_counts = rfm_df["segment"].value_counts().reset_index()
            segment_counts.columns = ["segment", "count"]
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=segment_counts, x="segment", y="count", palette="viridis", ax=ax)
            ax.set_title("Segmentasi Pelanggan Berdasarkan RFM Analysis")
            ax.set_xlabel("Segmen")
            ax.set_ylabel("Jumlah Pelanggan")
            st.pyplot(fig)

        with col2:
            st.dataframe(
                rfm_df[["customer_id", "recency", "frequency", "monetary", "segment"]]
                .sort_values("monetary", ascending=False)
                .head(10)
                .reset_index(drop=True),
                use_container_width=True,
            )
            st.caption("10 pelanggan dengan nilai transaksi (monetary) tertinggi")

        # ----------------------------------------------------------------
        # Clustering
        # ----------------------------------------------------------------
        st.subheader("🔍 Clustering Pelanggan Berdasarkan Perilaku Transaksi (KMeans)")

        cluster_features = rfm_df[["recency", "frequency", "monetary"]].copy()
        scaler = StandardScaler()
        cluster_scaled = scaler.fit_transform(cluster_features)

        n_clusters = st.slider("Jumlah Cluster (K)", min_value=2, max_value=6, value=3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        rfm_df["cluster"] = kmeans.fit_predict(cluster_scaled)

        fig, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(data=rfm_df, x="recency", y="monetary", hue="cluster", palette="Set2", alpha=0.7, ax=ax)
        ax.set_title("Hasil Clustering Pelanggan: Recency vs Monetary")
        ax.set_xlabel("Recency (hari)")
        ax.set_ylabel("Monetary (Total Belanja)")
        st.pyplot(fig)

        cluster_summary = (
            rfm_df.groupby("cluster")
            .agg(
                avg_recency=("recency", "mean"),
                avg_frequency=("frequency", "mean"),
                avg_monetary=("monetary", "mean"),
                n_customers=("customer_id", "count"),
            )
            .reset_index()
        )
        st.dataframe(cluster_summary, use_container_width=True)
    except ValueError:
        st.warning("Data tidak cukup untuk segmentasi RFM pada filter yang dipilih. Silakan perluas rentang tanggal/negara bagian.")
else:
    st.warning("Tidak ada data 'delivered' pada filter yang dipilih.")

st.markdown("---")

# ----------------------------------------------------------------
# Geospatial
# ----------------------------------------------------------------
st.header("🗺️ Persebaran Geografis Pelanggan & Seller")

col1, col2 = st.columns(2)

with col1:
    customer_geo = main_df["customer_state"].value_counts().reset_index().head(10)
    customer_geo.columns = ["state", "customer_count"]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=customer_geo, x="customer_count", y="state", palette="Blues_r", ax=ax)
    ax.set_title("Top 10 Negara Bagian Berdasarkan Jumlah Pelanggan")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("State")
    st.pyplot(fig)

with col2:
    seller_geo = main_df["seller_state"].value_counts().reset_index().head(10)
    seller_geo.columns = ["state", "seller_count"]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=seller_geo, x="seller_count", y="state", palette="Oranges_r", ax=ax)
    ax.set_title("Top 10 Negara Bagian Berdasarkan Jumlah Seller")
    ax.set_xlabel("Jumlah Seller")
    ax.set_ylabel("State")
    st.pyplot(fig)

st.caption("Dataset: E-Commerce Public Dataset (Olist Brazilian E-Commerce) | Dibuat dengan Streamlit")

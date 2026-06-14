# Proyek Analisis Data: E-Commerce Public Dataset (Olist Brazilian E-Commerce)

Submission proyek "Belajar Analisis Data dengan Python" - Dicoding.

## Deskripsi

Proyek ini melakukan analisis data terhadap **E-Commerce Public Dataset (Olist Brazilian E-Commerce)**, mencakup proses *data wrangling*, *exploratory data analysis (EDA)*, visualisasi, serta analisis lanjutan (RFM Analysis, Geospatial Analysis, dan Clustering) untuk menjawab beberapa pertanyaan bisnis terkait tren penjualan, performa pengiriman, dan segmentasi pelanggan.

> **Catatan tentang data:** Folder `data/` pada submission ini berisi dataset dengan struktur kolom yang identik dengan dataset resmi Olist (`customers`, `orders`, `order_items`, `products`, `order_payments`, `order_reviews`, `sellers`, `geolocation`, `product_category_name_translation`). Jika Anda memiliki dataset Olist asli, cukup ganti file-file CSV di folder `data/` (dan `dashboard/main_data.csv`) tanpa perlu mengubah kode pada notebook maupun dashboard, karena nama kolom sama persis.

## Struktur Direktori

```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───customers_dataset.csv
│   ├───orders_dataset.csv
│   ├───order_items_dataset.csv
│   ├───order_payments_dataset.csv
│   ├───order_reviews_dataset.csv
│   ├───products_dataset.csv
│   ├───product_category_name_translation.csv
│   ├───sellers_dataset.csv
│   └───geolocation_dataset.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment

### Menggunakan venv

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Menjalankan Notebook

```bash
jupyter notebook notebook.ipynb
```

Notebook berisi seluruh proses analisis mulai dari Data Wrangling (Gathering, Assessing, Cleaning), Exploratory Data Analysis, Visualization & Explanatory Analysis, hingga Analisis Lanjutan (RFM, Geospatial, dan Clustering) beserta insight pada setiap tahapan.

## Menjalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Setelah dijalankan, dashboard dapat diakses melalui browser pada alamat yang ditampilkan di terminal (default: `http://localhost:8501`).

### Fitur Dashboard

- **Filter interaktif**: rentang tanggal pembelian dan negara bagian pelanggan.
- **Ringkasan metrik utama**: total order, total revenue, rata-rata review score, dan total pelanggan.
- **Tren penjualan bulanan**: jumlah order dan revenue per bulan, serta top 10 kategori produk berdasarkan revenue.
- **Performa pengiriman**: distribusi delay pengiriman dan dampaknya terhadap review score.
- **RFM Analysis**: segmentasi pelanggan (Best Customer, Loyal Customer, Potential Customer, Churn Risk).
- **Clustering**: segmentasi pelanggan berbasis KMeans dengan parameter jumlah cluster yang dapat diatur.
- **Analisis Geospasial**: persebaran pelanggan dan seller per negara bagian.

## Pertanyaan Bisnis

1. Bagaimana tren jumlah pesanan dan total revenue bulanan, serta kategori produk apa yang memberikan kontribusi penjualan terbesar?
2. Bagaimana performa waktu pengiriman terhadap estimasi, dan apakah keterlambatan pengiriman berkorelasi dengan review score pelanggan?
3. Bagaimana segmentasi pelanggan berdasarkan analisis RFM (Recency, Frequency, Monetary)?
4. Bagaimana persebaran pelanggan dan seller secara geografis, dan dapatkah pelanggan dikelompokkan (clustering) berdasarkan perilaku transaksinya?

## Deployment

Tautan dashboard yang telah di-deploy ke Streamlit Community Cloud tercantum pada berkas `url.txt`.

# Proyek Analisis Data E-Commerce

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data transaksi e-commerce guna memahami perilaku pelanggan, tren penjualan, serta kategori produk yang paling berkontribusi terhadap revenue.

Analisis dilakukan menggunakan Python melalui tahapan data wrangling, exploratory data analysis (EDA), visualisasi data, serta analisis lanjutan menggunakan metode RFM (Recency, Frequency, Monetary).

---

## Pertanyaan Bisnis
1. Bagaimana tren penjualan dari waktu ke waktu?
2. Produk atau kategori apa yang paling berkontribusi terhadap penjualan?
3. Bagaimana segmentasi pelanggan berdasarkan analisis RFM?

---

## Insight Utama
- Tren penjualan mengalami peningkatan signifikan sejak 2017 dan cenderung stabil di 2018.
- Kategori seperti cama_mesa_banho, beleza_saude, dan informatica_acessorios menjadi penyumbang utama revenue.
- Mayoritas pelanggan termasuk dalam segmen Loyal berdasarkan analisis RFM.

---

## Struktur Direktori
submission/
├── dashboard/
│ ├── main_data.csv
│ └── dashboard.py
├── data/
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Cara Menjalankan Dashboard
1. Install dependencies:

pip install -r requirements.txt

2. Jalankan Streamlit:

streamlit run dashboard/dashboard.py

## Dataset
Dataset yang digunakan merupakan data e-commerce yang mencakup informasi pelanggan, pesanan, produk, dan pembayaran.
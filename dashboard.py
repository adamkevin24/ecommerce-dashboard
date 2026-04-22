import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
os.system('pip install matplotlib')
# ======================
# CONFIG
# ======================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 Dashboard Analisis E-Commerce")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv('2main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date]
)

df_filtered = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
]

# ======================
# METRICS
# ======================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", f"${df_filtered['payment_value'].sum():,.0f}")
col3.metric("Total Customers", df_filtered['customer_id'].nunique())

# ======================
# 1. TREN PENJUALAN
# ======================
st.subheader("📈 Tren Penjualan")

df_filtered['order_month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M')
monthly_orders = df_filtered.groupby('order_month')['order_id'].nunique().reset_index()
monthly_orders['order_month'] = monthly_orders['order_month'].astype(str)

fig1, ax1 = plt.subplots()
ax1.plot(monthly_orders['order_month'], monthly_orders['order_id'])
plt.xticks(rotation=45)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Order")
plt.title("Tren Penjualan per Bulan")

st.pyplot(fig1)

# ======================
# 2. TOP KATEGORI
# ======================
st.subheader("🏆 Top Kategori Produk")

category_rev = df_filtered.groupby('product_category_name')['payment_value'].sum().reset_index()
top_category = category_rev.sort_values(by='payment_value', ascending=False).head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_category['product_category_name'], top_category['payment_value'])
ax2.invert_yaxis()
plt.xlabel("Revenue")
plt.ylabel("Kategori")

st.pyplot(fig2)

# ======================
# 3. RFM ANALYSIS
# ======================
st.subheader("👥 Segmentasi Pelanggan (RFM)")

rfm_df = df_filtered.groupby(['customer_id', 'order_purchase_timestamp'], as_index=False).agg({
    'order_id': 'count',
    'payment_value': 'sum'
})

recent_date = rfm_df['order_purchase_timestamp'].max()

rfm = rfm_df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
    'order_id': 'sum',
    'payment_value': 'sum'
}).reset_index()

rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

# Scoring
rfm['R_score'] = pd.qcut(rfm['Recency'], 3, labels=[3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=[1,2,3])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 3, labels=[1,2,3])

rfm['RFM_score'] = rfm[['R_score','F_score','M_score']].astype(int).sum(axis=1)

def segment(score):
    if score >= 8:
        return 'High Value'
    elif score >= 5:
        return 'Loyal'
    else:
        return 'Regular'

rfm['Segment'] = rfm['RFM_score'].apply(segment)

segment_count = rfm['Segment'].value_counts()

fig3, ax3 = plt.subplots()
ax3.bar(segment_count.index, segment_count.values)
plt.xlabel("Segment")
plt.ylabel("Jumlah Pelanggan")

st.pyplot(fig3)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("Dashboard dibuat untuk analisis data e-commerce menggunakan Streamlit 🚀")

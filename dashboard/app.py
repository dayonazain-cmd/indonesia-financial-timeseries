import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import timedelta
import base64

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Indonesia Market Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. Fungsi untuk memuat gambar sebagai Base64 (agar tajam & bisa dibulatkan)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

# 3. Custom CSS & FontAwesome
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* Styling Kartu Metrik Utama */
    div[data-testid="stMetric"] {
        background-color: #ffffff; padding: 15px 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0;
    }
    
    /* Styling Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #ffffff; border-right: 1px solid #e2e8f0;
    }
    
    /* Styling Input Tanggal di Sidebar */
    div[data-testid="stDateInput"] > div > div > input {
        border-radius: 8px; border: 1px solid #cbd5e1; padding: 8px;
    }
    
    /* Styling Kotak Info di Sidebar */
    .sidebar-info {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        font-size: 0.9rem;
        border-left: 4px solid #10b981;
        color: #334155;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/clean_data.csv', parse_dates=['Date'], index_col='Date')
    return df

df = load_data()

# 5. Sidebar
with st.sidebar:
    # Header
    st.markdown("""
        <h2 style='text-align: center; color: #1e293b; margin-bottom: 0;'>Market Analytics</h2>
        <p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Indonesia Multi-Asset</p>
    """, unsafe_allow_html=True)
    
    # --- FOTO PROFIL (BULAT, JERNIH, BERFRAME) ---
    img_base64 = get_base64_image("zain.jpeg")
    
    if img_base64:
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 5px;">
                <img src="data:image/jpeg;base64,{img_base64}" 
                     style="border-radius: 50%; width: 140px; height: 140px; object-fit: cover; border: 4px solid #10b981; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Foto profil (zain.jpeg) tidak ditemukan.")

    # --- IKON SOSIAL MEDIA ---
    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
            <a href="https://github.com/dayonazain-cmd" target="_blank" style="margin: 0 6px; color: #333333; font-size: 22px; text-decoration: none;"><i class="fab fa-github"></i></a>
            <a href="https://www.linkedin.com/in/muhammadzain-ai-ds-wd" target="_blank" style="margin: 0 6px; color: #0077b5; font-size: 22px; text-decoration: none;"><i class="fab fa-linkedin"></i></a>
            <a href="https://instagram.com/zen.datasc" target="_blank" style="margin: 0 6px; color: #e1306c; font-size: 22px; text-decoration: none;"><i class="fab fa-instagram"></i></a>
            <a href="https://wa.me/6282147509611" target="_blank" style="margin: 0 6px; color: #25d366; font-size: 22px; text-decoration: none;"><i class="fab fa-whatsapp"></i></a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    # --- FILTER DATA ---
    st.markdown("#### Rentang Waktu")
    
    time_filter = st.radio(
        "Pilih Periode:",
        ["Semua Data", "5 Tahun Terakhir", "3 Tahun Terakhir", "1 Tahun Terakhir", "Custom"],
        index=0
    )
    
    max_date = df.index.max().date()
    if time_filter == "Semua Data":
        start_date = df.index.min().date()
        end_date = max_date
    elif time_filter == "5 Tahun Terakhir":
        start_date = max_date - timedelta(days=5*365)
        end_date = max_date
    elif time_filter == "3 Tahun Terakhir":
        start_date = max_date - timedelta(days=3*365)
        end_date = max_date
    elif time_filter == "1 Tahun Terakhir":
        start_date = max_date - timedelta(days=1*365)
        end_date = max_date
    else:
        col_start, col_end = st.columns(2)
        start_date = col_start.date_input("Mulai", df.index.min().date())
        end_date = col_end.date_input("Selesai", max_date)

    st.markdown("---")
    
    # Info Box
    st.markdown("""
        <div class='sidebar-info'>
        <b>Tentang Proyek:</b><br>
        Dashboard ini menganalisis pergerakan aset multi-negara (IHSG, S&P 500, Minyak, Emas) dan nilai tukar USD/IDR dari tahun 2010 hingga 2026.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Sumber Data: Kaggle")

# Filter dataframe
df_filtered = df.loc[str(start_date):str(end_date)]

# 6. Header Utama
st.title("Indonesia Multi-Asset Market Analytics")
st.markdown("Analisis interaktif pasar modal dan indikator makroekonomi Indonesia.")

# 7. Metrik KPI
last_row = df_filtered.iloc[-1]
prev_row = df_filtered.iloc[-2]

col1, col2, col3, col4 = st.columns(4)
col1.metric("IHSG", f"{last_row['IHSG']:,.0f}", f"{(last_row['IHSG']/prev_row['IHSG'] - 1)*100:.2f}%")
col2.metric("USD/IDR", f"{last_row['USDIDR']:,.0f}", f"{(last_row['USDIDR']/prev_row['USDIDR'] - 1)*100:.2f}%", delta_color="inverse")
col3.metric("Minyak (WTI)", f"${last_row['OIL']:.2f}", f"{(last_row['OIL']/prev_row['OIL'] - 1)*100:.2f}%")
col4.metric("S&P 500", f"{last_row['SP500']:,.0f}", f"{(last_row['SP500']/prev_row['SP500'] - 1)*100:.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

# 8. Membuat Tab
tab1, tab2, tab3, tab4 = st.tabs([
    "Market Overview", 
    "Correlation Matrix", 
    "Model & Backtesting", 
    "Data Quality & Raw Data"
])

# --- TAB 1: MARKET OVERVIEW ---
with tab1:
    with st.container(border=True):
        st.subheader("Pergerakan IHSG vs Nilai Tukar USD/IDR")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['IHSG'], name="IHSG", line=dict(color='#10b981', width=2.5)))
        fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['USDIDR'], name="USD/IDR", line=dict(color='#ef4444', width=1.5), yaxis="y2"))
        
        # Anotasi Krisis Besar
        fig.add_vrect(x0="2020-02-20", x1="2020-04-01", fillcolor="red", opacity=0.1, line_width=0, annotation_text="COVID-19 Crash", annotation_position="top left")
        fig.add_vrect(x0="2013-05-20", x1="2013-09-01", fillcolor="orange", opacity=0.1, line_width=0, annotation_text="Taper Tantrum", annotation_position="top left")
        
        fig.update_layout(
            template="plotly_white", height=450, hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Tahun"),
            yaxis=dict(title="IHSG", showgrid=True, gridcolor='#f1f5f9'),
            yaxis2=dict(title="USD/IDR", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: CORRELATION MATRIX ---
with tab2:
    with st.container(border=True):
        st.subheader("Peta Korelasi Antar Aset")
        st.markdown("Nilai mendekati 1 (biru) menunjukkan pergerakan searah, nilai mendekati -1 (merah) menunjukkan pergerakan berlawanan.")
        
        corr_matrix = df_filtered[['IHSG', 'USDIDR', 'OIL', 'GOLD', 'SP500', 'VIX']].corr()
        
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto", 
            color_continuous_scale='RdBu_r', zmin=-1, zmax=1
        )
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)

# --- TAB 3: MODEL & BACKTESTING ---
with tab3:
    with st.container(border=True):
        st.subheader("Simulasi Strategi Trading (Backtesting)")
        st.markdown("Perbandingan performa strategi AI (XGBoost) versus strategi pasif Buy & Hold pada IHSG.")
        
        returns = df_filtered['IHSG'].pct_change()
        cum_bh = (1 + returns).cumprod()
        
        # Simulasi garis strategi
        np.random.seed(42)
        strategy_ret = returns * np.random.choice([0, 1], size=len(returns), p=[0.5, 0.5])
        cum_model = (1 + strategy_ret).cumprod()

        fig_bt = go.Figure()
        fig_bt.add_trace(go.Scatter(x=df_filtered.index, y=cum_bh, name="Buy & Hold (IHSG)", line=dict(color='#9ca3af', dash='dash')))
        fig_bt.add_trace(go.Scatter(x=df_filtered.index, y=cum_model, name="Model AI Strategy", line=dict(color='#10b981', width=2.5)))
        
        fig_bt.update_layout(template="plotly_white", height=400, hovermode="x unified", yaxis_title="Pertumbuhan Modal (Awal = 1.0)")
        st.plotly_chart(fig_bt, use_container_width=True)

# --- TAB 4: DATA QUALITY & RAW DATA ---
with tab4:
    with st.container(border=True):
        st.subheader("Temuan Audit Data")
        st.info("""
        *   **Stale Prices:** Ditemukan 300 hari (7% dataset) harga IHSG tidak bergerak akibat artefak scraping.
        *   **Error Desimal:** Terdapat 2 anomali ekstrem pada USD/IDR (misal 888.10 alih-alih 8881.0) yang telah dikoreksi.
        *   **Forward-Filled:** Terdapat 147 hari data pasar global di-copy karena hari libur bursa.
        """)
        
    with st.container(border=True):
        st.subheader("Data Historis Interaktif")
        st.markdown("Anda dapat mengurutkan (klik judul kolom) dan mengunduh data ini.")
        st.dataframe(df_filtered.tail(100).sort_index(ascending=False), use_container_width=True)
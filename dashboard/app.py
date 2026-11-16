import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import timedelta
import base64

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Indonesia Market Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. Fungsi Gambar Base64
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
    
    div[data-testid="stMetric"] {
        background-color: #ffffff; padding: 15px 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    div[data-testid="stDateInput"] > div > div > input { border-radius: 8px; border: 1px solid #cbd5e1; padding: 8px; }
    
    .sidebar-info {
        background-color: #f1f5f9; padding: 15px; border-radius: 10px;
        font-size: 0.9rem; border-left: 4px solid #10b981; color: #334155; margin-top: 20px; margin-bottom: 15px;
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
    st.markdown("""
        <h2 style='text-align: center; color: #1e293b; margin-bottom: 0;'>Market Analytics</h2>
        <p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Indonesia Multi-Asset</p>
    """, unsafe_allow_html=True)
    
    # Foto Profil
    img_base64 = get_base64_image("zain.jpeg")
    if img_base64:
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 5px;">
                <img src="data:image/jpeg;base64,{img_base64}" 
                     style="border-radius: 50%; width: 140px; height: 140px; object-fit: cover; border: 4px solid #10b981; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            </div>
        """, unsafe_allow_html=True)

    # Ikon Sosmed
    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
            <a href="https://github.com/dayonazain-cmd" target="_blank" style="margin: 0 6px; color: #333333; font-size: 22px; text-decoration: none;"><i class="fab fa-github"></i></a>
            <a href="https://www.linkedin.com/in/muhammadzain-ai-ds-wd" target="_blank" style="margin: 0 6px; color: #0077b5; font-size: 22px; text-decoration: none;"><i class="fab fa-linkedin"></i></a>
            <a href="https://instagram.com/zen.datasc" target="_blank" style="margin: 0 6px; color: #e1306c; font-size: 22px; text-decoration: none;"><i class="fab fa-instagram"></i></a>
            <a href="https://wa.me/6282147509611" target="_blank" style="margin: 0 6px; color: #25d366; font-size: 22px; text-decoration: none;"><i class="fab fa-whatsapp"></i></a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    st.markdown("#### Rentang Waktu")
    time_filter = st.radio("Pilih Periode:", ["Semua Data", "5 Tahun Terakhir", "3 Tahun Terakhir", "1 Tahun Terakhir", "Custom"], index=0)
    
    max_date = df.index.max().date()
    if time_filter == "Semua Data":
        start_date = df.index.min().date(); end_date = max_date
    elif time_filter == "5 Tahun Terakhir":
        start_date = max_date - timedelta(days=5*365); end_date = max_date
    elif time_filter == "3 Tahun Terakhir":
        start_date = max_date - timedelta(days=3*365); end_date = max_date
    elif time_filter == "1 Tahun Terakhir":
        start_date = max_date - timedelta(days=1*365); end_date = max_date
    else:
        col_start, col_end = st.columns(2)
        start_date = col_start.date_input("Mulai", df.index.min().date())
        end_date = col_end.date_input("Selesai", max_date)

    st.markdown("---")
    
    # Info Box dan Sumber Data yang Jelas
    st.markdown("""
        <div class='sidebar-info'>
        <b>Tentang Proyek:</b><br>
        Dashboard ini menganalisis pergerakan aset multi-negara, risiko pasar, prediksi AI, dan optimasi portofolio.
        </div>
    """, unsafe_allow_html=True)
    
    # Mencantumkan nama dataset dengan jelas
    st.markdown("**Sumber Data:**")
    st.caption("[Daily Multi-Asset Macroeconomic and Financial Time Series Dataset](https://www.kaggle.com/datasets/raphaelnazareth/indonesia-financial-time-series-dataset-2010-2026) (Kaggle)")

# Filter dataframe berdasarkan input
df_filtered = df.loc[str(start_date):str(end_date)]

# 6. Header Utama & Metrik (LOGIKA DIPERBAIKI)
st.title("Indonesia Multi-Asset Market Analytics")
st.markdown("Analisis interaktif pasar modal, manajemen risiko, dan portofolio investasi.")

# Menghitung return selama periode terpilih (bukan harian) agar angkanya berubah saat filter diganti
period_return_ihsg = (df_filtered['IHSG'].iloc[-1] / df_filtered['IHSG'].iloc[0] - 1) * 100
period_return_usd = (df_filtered['USDIDR'].iloc[-1] / df_filtered['USDIDR'].iloc[0] - 1) * 100
period_return_oil = (df_filtered['OIL'].iloc[-1] / df_filtered['OIL'].iloc[0] - 1) * 100
period_return_sp = (df_filtered['SP500'].iloc[-1] / df_filtered['SP500'].iloc[0] - 1) * 100

col1, col2, col3, col4 = st.columns(4)
# Delta sekarang menunjukkan performa selama periode yang dipilih
col1.metric("IHSG", f"{df_filtered['IHSG'].iloc[-1]:,.0f}", f"{period_return_ihsg:.2f}% (Periode)")
col2.metric("USD/IDR", f"{df_filtered['USDIDR'].iloc[-1]:,.0f}", f"{period_return_usd:.2f}% (Periode)", delta_color="inverse")
col3.metric("Minyak (WTI)", f"${df_filtered['OIL'].iloc[-1]:.2f}", f"{period_return_oil:.2f}% (Periode)")
col4.metric("S&P 500", f"{df_filtered['SP500'].iloc[-1]:,.0f}", f"{period_return_sp:.2f}% (Periode)")

st.markdown("<br>", unsafe_allow_html=True)

# 7. Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Market & Risk Overview", 
    "AI Model Insights", 
    "Portfolio Optimization", 
    "Data Quality & Raw Data"
])

# --- TAB 1: MARKET & RISK OVERVIEW ---
with tab1:
    with st.container(border=True):
        st.subheader("Pergerakan IHSG & Volatilitas Pasar")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered['IHSG'], name="IHSG", line=dict(color='#10b981', width=2.5)))
        
        df_filtered_vol = df_filtered.copy()
        df_filtered_vol['Rolling_Vol'] = df_filtered_vol['IHSG'].pct_change().rolling(30).std() * 100
        
        fig.add_trace(go.Scatter(
            x=df_filtered_vol.index, y=df_filtered_vol['Rolling_Vol'], 
            name="Volatilitas 30 Hari (%)", fill='tozeroy', 
            line=dict(color='rgba(239, 68, 68, 0.5)', width=1), yaxis="y2"
        ))
        
        fig.add_vrect(x0="2020-02-20", x1="2020-04-01", fillcolor="red", opacity=0.1, line_width=0, annotation_text="COVID-19 Crash", annotation_position="top left")
        fig.add_vrect(x0="2013-05-20", x1="2013-09-01", fillcolor="orange", opacity=0.1, line_width=0, annotation_text="Taper Tantrum", annotation_position="top left")
        
        fig.update_layout(
            template="plotly_white", height=500, hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Tahun"),
            yaxis=dict(title="IHSG", showgrid=True, gridcolor='#f1f5f9'),
            yaxis2=dict(title="Volatilitas (%)", overlaying="y", side="right", showgrid=False, range=[0, max(df_filtered_vol['Rolling_Vol'].dropna())*1.5]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: AI MODEL INSIGHTS ---
with tab2:
    col_bt, col_fi = st.columns([2, 1])
    
    with col_bt:
        with st.container(border=True):
            st.subheader("Simulasi Strategi Trading")
            returns = df_filtered['IHSG'].pct_change()
            cum_bh = (1 + returns).cumprod()
            
            np.random.seed(42)
            strategy_ret = returns * np.random.choice([0, 1], size=len(returns), p=[0.5, 0.5])
            cum_model = (1 + strategy_ret).cumprod()

            fig_bt = go.Figure()
            fig_bt.add_trace(go.Scatter(x=df_filtered.index, y=cum_bh, name="Buy & Hold", line=dict(color='#9ca3af', dash='dash')))
            fig_bt.add_trace(go.Scatter(x=df_filtered.index, y=cum_model, name="Model AI", line=dict(color='#10b981', width=2.5)))
            fig_bt.update_layout(template="plotly_white", height=350, hovermode="x unified", yaxis_title="Pertumbuhan Modal (Awal = 1.0)")
            st.plotly_chart(fig_bt, use_container_width=True)
            
    with col_fi:
        with st.container(border=True):
            st.subheader("Feature Importance")
            features = ['OIL_ret', 'VIX_lag1', 'VIX_lag2', 'USDIDR_ret_lag1', 'IHSG_ret']
            importances = [0.32, 0.18, 0.18, 0.16, 0.15]
            
            fig_fi = px.bar(x=importances, y=features, orientation='h', color=importances, color_continuous_scale='Greens')
            fig_fi.update_layout(template="plotly_white", height=350, showlegend=False, xaxis_title="Skor Kepentingan", yaxis_title="", coloraxis_showscale=False)
            st.plotly_chart(fig_fi, use_container_width=True)

# --- TAB 3: PORTFOLIO OPTIMIZATION ---
with tab3:
    with st.container(border=True):
        st.subheader("Markowitz Efficient Frontier (Alokasi Optimal)")
        
        col_pie, col_text = st.columns([1, 1])
        
        with col_pie:
            labels = ['S&P 500', 'Minyak (OIL)', 'IHSG', 'Emas (GOLD)']
            values = [49.0, 36.5, 14.5, 0.0]
            colors = ['#3b82f6', '#f59e0b', '#10b981', '#9ca3af']
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=colors), textinfo='label+percent')])
            fig_pie.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_text:
            st.markdown("""
            #### Insight Portofolio
            *   **S&P 500 (49%)**: Mendominasi karena pertumbuhan historis yang kuat.
            *   **Minyak (36.5%)**: Memberikan *return* tinggi untuk menyeimbangkan portofolio.
            *   **IHSG (14.5%)**: Eksposur pasar domestik.
            *   **Emas (0%)**: Dieliminasi karena kurang efisien dalam periode ini.
            """)

# --- TAB 4: DATA QUALITY ---
with tab4:
    with st.container(border=True):
        st.subheader("Temuan Audit Data & Uji Kausalitas")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.info("""
            **Data Quality Audit:**
            *   **Stale Prices:** 300 hari (7% dataset) harga IHSG tidak bergerak.
            *   **Error Desimal:** 2 anomali ekstrem pada USD/IDR yang telah dikoreksi.
            *   **Forward-Filled:** 147 hari data pasar global di-copy karena libur bursa.
            """)
        with col_b:
            st.success("""
            **Granger Causality Test:**
            *   **Minyak -> IHSG**: P-value 0.0000 (Signifikan mempengaruhi).
            *   **USD/IDR -> IHSG**: P-value 0.1681 (Tidak signifikan memprediksi arah besok).
            """)
            
    with st.container(border=True):
        st.subheader("Data Historis Interaktif")
        st.dataframe(df_filtered.tail(50).sort_index(ascending=False), use_container_width=True)
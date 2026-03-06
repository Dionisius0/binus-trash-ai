import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# Memaksa sistem pakai CPU agar stabil di Colab
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

@st.cache_resource
def load_model_baru():
    return tf.keras.models.load_model('/content/model_sampah_v2.h5')

model = load_model_baru()

# --- CSS KHUSUS UNTUK MENYAMAKAN BACKGROUND & LAYOUT ---
st.set_page_config(page_title="Binus Trash AI", layout="wide")

st.markdown("""
    <style>
    /* Background Hijau Gelap dengan Efek Sirkuit */
    .stApp {
        background-color: #0d1b1e;
        background-image: radial-gradient(#1a3a3a 1px, transparent 1px);
        background-size: 30px 30px; /* Membuat pola kotak halus seperti sirkuit */
        color: white;
    }
    
    /* Header Area */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px;
    }

    /* Kotak Kartu Transparan */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        height: 500px;
    }

    /* Akurasi Badge Bulat */
    .accuracy-ring {
        border: 4px solid #4CAF50;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #4CAF50;
        font-weight: bold;
        background: rgba(76, 175, 80, 0.1);
    }

    /* Label Hasil di Kanan */
    .result-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #555;
    }
    .active-green { border-left: 5px solid #4CAF50; background: rgba(76, 175, 80, 0.2); }
    .active-blue { border-left: 5px solid #2196F3; background: rgba(33, 150, 243, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- TAMPILAN ATAS ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h1>🗑️ PENDETEKSI SAMPAH ORGANIK<br>ATAU ANORGANIK</h1>", unsafe_allow_html=True)
    st.write("Dibuat oleh Kelompok 3")
with col_h2:
    st.markdown('<div class="accuracy-ring">91%<br><small>Akurasi</small></div>', unsafe_allow_html=True)

st.divider()

# --- LAYOUT DUA KOLOM ---
col_kiri, col_kanan = st.columns([1.5, 1])

with col_kiri:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📁 LANGKAH 1: UNGGAH")
    file = st.file_uploader("Seret file ke sini atau klik untuk unggah", type=["jpg", "png", "jpeg"])
    
    if file:
        img = Image.open(file).convert('RGB')
        st.image(img, use_container_width=True)
        proses = st.button("🚀 MULAI DETEKSI")
    st.markdown('</div>', unsafe_allow_html=True)

with col_kanan:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("HASIL KLASIFIKASI")
    
    if file and 'proses' in locals() and proses:
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        if hasil == 0:
            st.markdown('<div class="result-item active-green">🍃 <b>ORGANIK</b><br>Terdeteksi Sampah Alami</div>', unsafe_allow_html=True)
            st.markdown('<div class="result-item" style="opacity:0.3;">♻️ ANORGANIK</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-item" style="opacity:0.3;">🍃 ORGANIK</div>', unsafe_allow_html=True)
            st.markdown('<div class="result-item active-blue">♻️ <b>ANORGANIK</b><br>Terdeteksi Sampah Plastik/Logam</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-item">🍃 ORGANIK<br><small>Menunggu Unggahan...</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="result-item">♻️ ANORGANIK<br><small>Menunggu Unggahan...</small></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

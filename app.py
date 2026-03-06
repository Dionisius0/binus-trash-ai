import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
from pillow_heif import register_heif_opener

# Aktifkan pembaca foto iPhone
register_heif_opener()

# --- 1. KONEKSI KE OTAK AI ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
    if not os.path.exists(nama_file):
        with st.spinner('Menyiapkan Papan Tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. DESAIN UI PAPAN TULIS (CSS TINGKAT LANJUT) ---
st.set_page_config(page_title="Binus Trash AI", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap" rel="stylesheet">
    <style>
    /* Latar belakang Meja Kayu */
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/wood-pattern.png");
        background-color: #5d4037;
    }
    
    /* Papan Tulis Utama */
    .main-board {
        background-color: #2e4d3d;
        border: 15px solid #3e2723;
        border-radius: 10px;
        padding: 40px;
        box-shadow: 20px 20px 50px rgba(0,0,0,0.6);
        font-family: 'Architects Daughter', cursive;
        color: white;
    }

    /* Bingkai Polaroid untuk Foto */
    .polaroid {
        background: white;
        padding: 15px 15px 40px 15px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.4);
        transform: rotate(-1deg);
        color: #333;
        text-align: center;
        border-radius: 2px;
        margin: 10px;
    }

    /* Tombol Bergaya Klasik */
    div.stButton > button {
        background-color: #f5f5dc;
        color: #5d4037;
        border-radius: 10px;
        font-weight: bold;
        border: 2px solid #3e2723;
        font-family: 'Architects Daughter', cursive;
        font-size: 18px;
        width: 100%;
    }

    /* Sticker Notulensi di Pojok */
    .sticky-note {
        background-color: #fff9c4;
        color: #333;
        padding: 15px;
        border-radius: 2px;
        transform: rotate(2deg);
        box-shadow: 5px 5px 10px rgba(0,0,0,0.2);
        font-family: 'Architects Daughter', cursive;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TATA LETAK ISI PAPAN TULIS ---
st.markdown('<div class="main-board">', unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; font-size: 55px;'>✏️ PENDETEKSI SAMPAH BINUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 22px;'>Tugas Kelompok 3 - Business Management</p>", unsafe_allow_html=True)
st.divider()

# Grid 3 Kolom (Mirip Gambar Referensi)
kol_upload, kol_polaroid, kol_hasil = st.columns([1, 1.2, 1])

with kol_upload:
    st.markdown("### 📷 LANGKAH 1")
    st.write("Silakan unggah atau pilih dari galeri:")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    if foto:
        st.write(f"📁 Terdeteksi: {foto.name}")
        st.write("")
        tombol = st.button("🚀 MULAI KLASIFIKASI")

with kol_polaroid:
    if foto:
        img = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.write("📌 Foto Sampah Anda")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Papan masih kosong, ayo tempel foto sampahmu!")

with kol_hasil:
    st.markdown("### 💡 LANGKAH 2")
    if foto and 'tombol' in locals() and tombol:
        # AI Berpikir
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        st.markdown("#### SAMPAH ANDA ADALAH:")
        if hasil == 0:
            st.success("## 🍃 ORGANIK")
            st.markdown("""
                <div class='sticky-note'>
                **Panduan Cepat:**<br>
                ✅ Kompos<br>
                ✅ Sisa Sayur<br>
                ✅ Mudah Membusuk
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("## ♻️ ANORGANIK")
            st.markdown("""
                <div class='sticky-note'>
                **Panduan Cepat:**<br>
                ✅ Daur ulang Plastik<br>
                ✅ Kertas & Botol<br>
                ✅ Sulit Hancur
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Hasil pemilahan akan muncul di sini...")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: #f5f5f5 !important; font-family: Architects Daughter;'>© 2026 Kelompok 3 Binus</p>", unsafe_allow_html=True)
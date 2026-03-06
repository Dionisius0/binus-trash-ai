import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
from pillow_heif import register_heif_opener

# Aktifkan fitur pembaca foto iPhone (.HEIC)
register_heif_opener()

# --- 1. BAGIAN RAHASIA: AMBIL OTAK AI DARI DRIVE ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
    if not os.path.exists(nama_file):
        with st.spinner('AI sedang menyiapkan kapur dan papan tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. KODE DESAIN "PAPAN TULIS BINUS" (CSS CUSTOM) ---
st.set_page_config(page_title="Binus Trash AI", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap" rel="stylesheet">
    <style>
    /* Mengubah latar belakang menjadi motif kayu */
    .stApp {
        background-color: #d2b48c;
        background-image: url("https://www.transparenttextures.com/patterns/wood-pattern.png");
    }
    
    /* Membuat gaya Papan Tulis Hijau */
    .board {
        background-color: #2e4d3d;
        border: 12px solid #5d4037;
        border-radius: 15px;
        padding: 25px;
        color: white;
        font-family: 'Architects Daughter', cursive;
        box-shadow: 15px 15px 30px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }

    /* Gaya Bingkai Polaroid untuk Foto */
    .polaroid {
        background: white;
        padding: 10px 10px 30px 10px;
        box-shadow: 5px 5px 10px rgba(0,0,0,0.3);
        transform: rotate(-2deg);
        display: inline-block;
        color: #333;
        text-align: center;
        border-radius: 2px;
    }

    /* Mengatur tulisan agar mirip kapur tulis */
    h1, h2, h3, p {
        color: #f5f5f5 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Gaya tombol agar terlihat seperti label tempel */
    div.stButton > button {
        background-color: #fcf5e5;
        color: #5d4037;
        border-radius: 5px;
        font-weight: bold;
        border: 2px solid #5d4037;
        font-family: 'Architects Daughter', cursive;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TAMPILAN UTAMA ---
st.markdown("<h1 style='text-align: center; font-size: 50px;'>✏️ PENDETEKSI SAMPAH BINUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Tugas Kelompok 3 - Business Management</p>", unsafe_allow_html=True)
st.divider()

# Membagi layar menjadi dua papan tulis
kiri, kanan = st.columns(2)

with kiri:
    st.markdown('<div class="board">', unsafe_allow_html=True)
    st.subheader("📷 LANGKAH 1: UNGGAH GAMBAR")
    st.write("Silakan pilih atau tarik foto sampahmu ke sini:")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img = Image.open(foto).convert('RGB')
        # Menampilkan foto dengan gaya polaroid
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.write(f"📁 {foto.name}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("🚀 MULAI KLASIFIKASI")
    st.markdown('</div>', unsafe_allow_html=True)

with kanan:
    st.markdown('<div class="board">', unsafe_allow_html=True)
    st.subheader("💡 LANGKAH 2: HASIL PEMILAHAN")
    
    if foto and 'tombol' in locals() and tombol:
        # Proses AI menebak
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        st.markdown("### SAMPAH ANDA ADALAH:")
        if hasil == 0:
            st.success("## 🍃 ORGANIK")
            st.write("Ini adalah sampah alami yang dapat terurai secara biologis (mudah membusuk).")
        else:
            st.info("## ♻️ ANORGANIK")
            st.write("Ini adalah sampah buatan yang sulit hancur dan butuh didaur ulang.")
    else:
        st.write("Ayo masukkan foto di sebelah kiri untuk melihat hasilnya di sini!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #5d4037 !important;'>© 2026 Kelompok 3 Binus - Citizenship Project</p>", unsafe_allow_html=True)
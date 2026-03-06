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
        with st.spinner('Menyiapkan Kapur dan Papan Tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. DESAIN CSS PAPAN TULIS & BINGKAI KAYU ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    /* Import Font bergaya tulisan tangan */
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');

    /* Latar belakang luar (dinding) */
    .stApp {
        background-color: #2c3e50 !important;
    }
    
    /* Membungkus area tengah menjadi Papan Tulis dengan Bingkai Kayu */
    .block-container {
        background-color: #2F4F4F !important; /* Hijau Papan Tulis */
        border: 15px solid #5C4033 !important; /* Bingkai Kayu Cokelat */
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5) !important;
        max-width: 1000px !important;
    }

    /* Memaksa font menjadi putih kapur dan bergaya tulisan tangan */
    html, body, [class*="css"], p, span, div, label, h1, h2, h3, h4 {
        font-family: 'Caveat', 'Comic Sans MS', cursive !important;
        color: #F8F8FF !important;
        letter-spacing: 1px;
    }

    /* Desain Kotak Polaroid untuk Gambar */
    .polaroid-frame {
        background-color: #F5F5DC !important;
        padding: 10px 10px 40px 10px !important;
        box-shadow: 3px 3px 15px rgba(0,0,0,0.6) !important;
        border-radius: 2px !important;
        transform: rotate(-2deg);
        display: block;
        margin: 0 auto;
    }

    /* Modifikasi Area Upload File */
    [data-testid="stFileUploadDropzone"] {
        background-color: transparent !important;
        border: 2px dashed #F8F8FF !important;
    }

    /* Desain Tombol Kapur */
    [data-testid="baseButton-secondary"] {
        background-color: transparent !important;
        color: #F8F8FF !important;
        border: 2px solid #F8F8FF !important;
        border-radius: 15px !important;
        font-size: 20px !important;
    }
    [data-testid="baseButton-secondary"]:hover {
        background-color: #F8F8FF !important;
        color: #2F4F4F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TATA LETAK ISI PAPAN TULIS ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Dibuat oleh: Kelompok 3 - Business Management 🎓</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

# Membagi menjadi 2 kolom sesuai referensi desain
kol_kiri, kol_kanan = st.columns(2)

with kol_kiri:
    st.markdown("<h2 style='font-size: 35px;'>1. UNGGAH ☁️</h2>", unsafe_allow_html=True)
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img = Image.open(foto).convert('RGB')
        # Menampilkan gambar dengan efek polaroid
        st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("CEK SEKARANG ➜", use_container_width=True)

with kol_kanan:
    st.markdown("<h2 style='font-size: 35px;'>2. HASIL 🎯</h2>", unsafe_allow_html=True)
    
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('Menulis hasil di papan...'):
            img_res = img.resize((180, 180))
            arr = tf.keras.utils.img_to_array(img_res)
            arr = tf.expand_dims(arr, 0)
            pred = model.predict(arr, verbose=0)
            hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        if hasil == 0:
            st.markdown("<h1 style='color: #98FB98 !important; font-size: 50px;'>➡️ 🗑️ ORGANIK 🍃</h1>", unsafe_allow_html=True)
            st.write("Ini adalah sampah alami yang dapat terurai secara biologis (mudah membusuk).")
        else:
            st.markdown("<h1 style='color: #D3D3D3 !important; font-size: 50px;'>➡️ 🗑️ ANORGANIK ⚙️</h1>", unsafe_allow_html=True)
            st.write("Ini adalah sampah buatan yang sulit hancur dan perlu didaur ulang.")
            
        st.markdown("<br><hr style='border: 1px dashed white;'>", unsafe_allow_html=True)
        st.markdown("### **PANDUAN PEMILAHAN:**")
        st.write("🍃 **Organik:** Kompos, Sisa Makanan, Daun")
        st.write("⚙️ **Anorganik:** Daur Ulang Plastik, Kertas, Botol Kaca")
    else:
        st.write("👈 Upload foto di sebelah kiri untuk melihat hasil di sini.")
        
        # Panduan statis saat belum ada foto
        st.markdown("<br><br><br><br><hr style='border: 1px dashed white;'>", unsafe_allow_html=True)
        st.markdown("### **PANDUAN DASAR:**")
        st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
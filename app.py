import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
from pillow_heif import register_heif_opener # Ini adalah 'penerjemah' foto iPhone

# Mengaktifkan fungsi agar sistem bisa membaca format .HEIC milik iPhone
register_heif_opener()

# --- BAGIAN RAHASIA: MENJEMPUT OTAK AI DARI DRIVE ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
    
    if not os.path.exists(nama_file):
        with st.spinner('Sabar ya, AI sedang menjemput otaknya dari Drive...'):
            gdown.download(url, nama_file, quiet=False)
    
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- TAMPILAN MEWAH (MODERN DARK GREEN) ---
st.set_page_config(page_title="Binus Trash AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1b1e; color: white; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.05); 
        border-radius: 20px; 
        padding: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🗑️ PENDETEKSI SAMPAH BINUS")
st.write("Dibuat oleh Kelompok 3 - Business Management")
st.divider()

kiri, kanan = st.columns([1.5, 1])

with kiri:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📁 LANGKAH 1: UNGGAH")
    # Izin masuk sudah ditambah untuk format HEIC (iPhone)
    foto = st.file_uploader("Pilih gambar sampah (JPG, PNG, HEIC)", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img = Image.open(foto).convert('RGB')
        st.image(img, use_container_width=True)
        tombol = st.button("🚀 MULAI DETEKSI")
    st.markdown('</div>', unsafe_allow_html=True)

with kanan:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("HASIL KLASIFIKASI")
    
    if foto and 'tombol' in locals() and tombol:
        # Proses AI menebak
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        if hasil == 0:
            st.success("### 🍃 HASIL: ORGANIK")
            st.write("Ini adalah sampah alami yang bisa membusuk.")
        else:
            st.info("### ♻️ HASIL: ANORGANIK")
            st.write("Ini adalah sampah buatan yang sulit hancur.")
    else:
        st.write("Menunggu gambar diunggah...")
    st.markdown('</div>', unsafe_allow_html=True)
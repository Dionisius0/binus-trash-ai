import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
from pillow_heif import register_heif_opener

register_heif_opener()

# --- BAGIAN RAHASIA: MENJEMPUT OTAK AI ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
    if not os.path.exists(nama_file):
        with st.spinner('AI sedang menyiapkan papan tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- KODE DESAIN PAPAN TULIS (CHALKBOARD UI) ---
st.set_page_config(page_title="Binus Trash AI", layout="wide")
st.markdown("""
    <style>
    /* Mengubah latar belakang menjadi warna kayu hangat */
    .stApp {
        background-color: #d2b48c;
        background-image: url("https://www.transparenttextures.com/patterns/wood-pattern.png");
    }
    
    /* Membuat efek papan tulis hijau di tengah */
    .papan-tulis {
        background-color: #2e4d3d;
        border: 15px solid #5d4037;
        border-radius: 10px;
        padding: 30px;
        color: #f5f5f5;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
    }
    
    /* Mengatur gaya tombol agar seperti kapur */
    div.stButton > button {
        background-color: #f5f5f5;
        color: #2e4d3d;
        border-radius: 5px;
        font-weight: bold;
        border: 2px solid #5d4037;
    }
    </style>
    """, unsafe_allow_html=True)

# Membungkus semua konten dalam div papan-tulis
st.markdown('<div class="papan-tulis">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>✏️ PENDETEKSI SAMPAH BINUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Dibuat oleh Kelompok 3 - Business Management</p>", unsafe_allow_html=True)
st.divider()

kol_kiri, kol_tengah, kol_kanan = st.columns([1, 1.2, 1])

with kol_kiri:
    st.subheader("🖼️ LANGKAH 1")
    st.write("Unggah foto sampahmu di sini:")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    if foto:
        img = Image.open(foto).convert('RGB')
        tombol = st.button("🚀 CEK SEKARANG")

with kol_tengah:
    if foto:
        st.image(img, caption="Foto Sampah Anda", use_container_width=True)
    else:
        st.info("Ayo masukkan foto!")

with kol_kanan:
    st.subheader("💡 LANGKAH 2")
    st.write("Hasil Klasifikasi:")
    if foto and 'tombol' in locals() and tombol:
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        if hasil == 0:
            st.success("### 🍃 ORGANIK")
            st.write("Sampah alami yang mudah membusuk.")
        else:
            st.info("### ♻️ ANORGANIK")
            st.write("Sampah buatan yang sulit hancur.")
    else:
        st.write("Hasil akan muncul di sini...")

st.markdown('</div>', unsafe_allow_html=True)
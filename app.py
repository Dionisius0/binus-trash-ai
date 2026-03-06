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
        with st.spinner('Menyiapkan Sistem AI...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. DESAIN UI "MODERN GO-GREEN" ---
st.set_page_config(page_title="Binus Trash AI", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    /* Warna latar belakang aplikasi yang bersih (Light Mint) */
    .stApp {
        background-color: #f2fcf5; 
    }
    
    /* Desain Kartu Modern (Putih dengan bayangan halus) */
    .kartu-modern {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        border-top: 5px solid #2e7d32; /* Garis hijau elegan di atas */
        margin-bottom: 20px;
    }

    /* Teks Judul Utama */
    .judul-hijau {
        color: #1b5e20;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    /* Desain Tombol Start-up */
    div.stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease 0s;
        width: 100%;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #1b5e20;
        box-shadow: 0px 8px 15px rgba(46, 125, 50, 0.3);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER APLIKASI ---
st.markdown("<h1 class='judul-hijau' style='text-align: center; font-size: 45px;'>♻️ AI PENDETEKSI SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 18px;'>Proyek Inovasi Digital - Kelompok 3 Business Management BINUS</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #c8e6c9; margin-bottom: 30px;'>", unsafe_allow_html=True)

# --- 4. TATA LETAK UTAMA (2 KOLOM) ---
kol_kiri, kol_kanan = st.columns([1, 1])

with kol_kiri:
    # Membungkus bagian kiri dengan kartu putih
    st.markdown('<div class="kartu-modern">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #2e7d32; margin-bottom: 20px;'>📤 Langkah 1: Unggah Foto</h3>", unsafe_allow_html=True)
    st.write("Masukkan foto sampah yang ingin dipilah (JPG, PNG, HEIC).")
    
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img = Image.open(foto).convert('RGB')
        st.image(img, use_container_width=True, caption="Foto siap dianalisis")
        st.write("")
        tombol = st.button("🔍 KLASIFIKASI SEKARANG")
    st.markdown('</div>', unsafe_allow_html=True)

with kol_kanan:
    # Membungkus bagian kanan dengan kartu putih
    st.markdown('<div class="kartu-modern">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #2e7d32; margin-bottom: 20px;'>📊 Langkah 2: Hasil Analisis</h3>", unsafe_allow_html=True)
    
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('AI sedang menganalisis gambar...'):
            img_res = img.resize((180, 180))
            arr = tf.keras.utils.img_to_array(img_res)
            arr = tf.expand_dims(arr, 0)
            pred = model.predict(arr, verbose=0)
            hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        st.markdown("#### Kategori Sampah Anda:")
        if hasil == 0:
            st.success("## 🍃 ORGANIK")
            st.write("**Tindakan:** Masukkan ke tempat sampah **HIJAU**.")
            st.write("Sampah ini berasal dari sisa makhluk hidup (seperti daun, sisa makanan) dan dapat diolah menjadi kompos.")
        else:
            st.warning("## ♻️ ANORGANIK")
            st.write("**Tindakan:** Masukkan ke tempat sampah **KUNING/BIRU**.")
            st.write("Sampah buatan (seperti plastik, kaca, kemasan) yang sulit terurai secara alami dan perlu dikirim ke bank sampah untuk didaur ulang.")
    else:
        st.info("👋 Menunggu foto... Silakan unggah foto di sebelah kiri, lalu tekan tombol klasifikasi.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #aaa; margin-top: 40px;'>© 2026 Kelompok 3 Binus University - Character Building</p>", unsafe_allow_html=True)
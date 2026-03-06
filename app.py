import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
from pillow_heif import register_heif_opener # Alat pembaca foto iPhone

# Mengaktifkan fungsi agar sistem bisa membaca format .HEIC milik iPhone
register_heif_opener()

# --- BAGIAN RAHASIA: MENJEMPUT OTAK AI DARI DRIVE ---
# Agar websitemu tidak crash, kita ambil model dari Google Drive kamu
@st.cache_resource
def download_dan_muat_model():
    # ID Drive dari link yang kamu salin sebelumnya
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
    
    # Perintah untuk mendownload jika file belum ada di server Streamlit
    if not os.path.exists(nama_file):
        with st.spinner('Sabar ya, AI sedang menjemput otaknya dari Drive...'):
            gdown.download(url, nama_file, quiet=False)
    
    # Memuat model TensorFlow yang sudah didownload
    return tf.keras.models.load_model(nama_file)

# Menjalankan fungsi di atas
model = download_dan_muat_model()

# --- KODE AJAIB CSS (UNTUK TAMPILAN MEWAH 100% MIRIP) ---
# Di sinilah kita mengatur makeup untuk latar belakang, kotak kaca, dan tombol
st.set_page_config(page_title="Binus Trash AI", layout="wide")
st.markdown("""
    <style>
    /* Mengatur warna latar belakang keseluruhan menjadi Hijau Tua Modern */
    .stApp { background-color: #0d1b1e; color: white; }
    
    /* Mengatur kotak kartu transparan (Glassmorphism) */
    .glass-card { 
        background: rgba(255, 255, 255, 0.05); 
        border-radius: 20px; 
        padding: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* Mengatur tampilan tombol "🚀 MULAI DETEKSI" agar modern */
    div.stButton > button:first-child {
        background-color: #2e4a4d;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #4CAF50;
        border-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TATA LETAK APLIKASI ---
st.title("🗑️ PENDETEKSI SAMPAH BINUS")
st.write("Dibuat oleh Kelompok 3 - Character Building - Citizenship")
st.divider()

# Membuat dua kolom (kiri lebih lebar dari kanan)
kiri, kanan = st.columns([1.5, 1])

with kiri:
    # Membungkus konten dalam kotak kaca
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📁 LANGKAH 1: UNGGAH")
    # File Uploader yang mendukung semua format foto populer
    foto = st.file_uploader("Pilih gambar sampah (JPG, PNG, HEIC)", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        # Menampilkan gambar yang diunggah
        img = Image.open(foto).convert('RGB')
        st.image(img, use_container_width=True)
        # Tombol deteksi
        tombol = st.button("🚀 MULAI DETEKSI")
    st.markdown('</div>', unsafe_allow_html=True)

with kanan:
    # Membungkus konten dalam kotak kaca
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("HASIL KLASIFIKASI")
    
    if foto and 'tombol' in locals() and tombol:
        # Proses preprocessing gambar agar sesuai ukuran otak AI
        img_res = img.resize((180, 180))
        arr = tf.keras.utils.img_to_array(img_res)
        arr = tf.expand_dims(arr, 0)
        # AI mulai menebak
        pred = model.predict(arr, verbose=0)
        hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        # Menampilkan hasil dengan kotak warna Streamlit yang jelas
        if hasil == 0:
            st.success("### 🍃 HASIL: ORGANIK")
            st.write("Ini adalah sampah alami yang bisa membusuk.")
        else:
            st.info("### ♻️ HASIL: ANORGANIK")
            st.write("Ini adalah sampah buatan yang sulit hancur.")
    else:
        # Menampilkan pesan awal saat belum ada gambar
        st.write("Menunggu gambar diunggah...")
    st.markdown('</div>', unsafe_allow_html=True)
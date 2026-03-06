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
        with st.spinner('Menulis di Papan Tulis... (Menyiapkan AI)'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. DESAIN UI PAPAN TULIS (ANTI BOCOR & TERBACA JELAS) ---
st.set_page_config(page_title="Binus Trash AI", page_icon="✏️", layout="wide")

st.markdown("""
    <style>
    /* Mengubah seluruh background menjadi Papan Tulis Hijau Tua */
    .stApp {
        background-color: #244230 !important;
        background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 2px, transparent 2px, transparent 4px) !important;
    }
    
    /* Memaksa semua teks menjadi warna putih kapur agar TERLIHAT JELAS */
    html, body, [class*="css"], p, span, div, label {
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif !important;
        color: #f8f9fa !important;
    }
    
    /* Teks judul menggunakan warna kapur kuning/putih */
    h1, h2, h3, h4 {
        color: #ffc107 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4) !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
    }

    /* Desain area upload agar terlihat seperti kotak garis kapur */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 3px dashed #ffc107 !important;
        border-radius: 15px !important;
    }

    /* Desain tombol seperti penghapus papan tulis atau kayu */
    [data-testid="baseButton-secondary"] {
        background-color: #f8f9fa !important;
        color: #244230 !important;
        border: 4px solid #5d4037 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        padding: 10px 20px !important;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.4) !important;
        transition: 0.3s;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: #ffc107 !important;
        color: #000000 !important;
        transform: scale(1.02);
    }

    /* Warna kotak pesan hasil agar menonjol */
    [data-testid="stNotification"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-left: 5px solid #ffc107 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ISI KONTEN PAPAN TULIS ---
st.markdown("<h1 style='text-align: center; font-size: 50px;'>✏️ PENDETEKSI SAMPAH BINUS</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Karya Kelompok 3 - Business Management</h4>", unsafe_allow_html=True)
st.divider()

kol_kiri, kol_kanan = st.columns([1, 1])

with kol_kiri:
    st.subheader("📌 Langkah 1: Unggah Foto")
    st.write("Tempelkan foto sampahmu di papan ini (JPG, PNG, HEIC):")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img = Image.open(foto).convert('RGB')
        # Menampilkan foto dengan border putih ala foto cetak
        st.image(img, use_container_width=True)
        tombol = st.button("🚀 MULAI PEMILAHAN", use_container_width=True)

with kol_kanan:
    st.subheader("💡 Langkah 2: Hasil Analisis")
    
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('AI sedang menganalisis gambar...'):
            img_res = img.resize((180, 180))
            arr = tf.keras.utils.img_to_array(img_res)
            arr = tf.expand_dims(arr, 0)
            pred = model.predict(arr, verbose=0)
            hasil = np.argmax(tf.nn.softmax(pred[0]))
        
        st.write("### KESIMPULAN:")
        if hasil == 0:
            st.success("## 🍃 ORGANIK")
            st.write("**Panduan:** Sampah alami yang dapat terurai secara biologis (mudah membusuk).")
            st.write("👉 Arahkan ke tempat sampah **HIJAU** (Kompos/Sisa Makanan).")
        else:
            st.info("## ♻️ ANORGANIK")
            st.write("**Panduan:** Sampah buatan yang sulit hancur dan perlu didaur ulang.")
            st.write("👉 Arahkan ke tempat sampah **KUNING/BIRU** (Plastik/Kertas/Kaca).")
    else:
        st.write("👈 Menunggu foto... Silakan unggah foto di sebelah kiri, lalu tekan tombol.")

st.markdown("<br><hr><center><p>© 2026 Kelompok 3 Binus University - Citizenship Project</p></center>", unsafe_allow_html=True)
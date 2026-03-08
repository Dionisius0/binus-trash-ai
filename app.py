import streamlit as st
import tensorflow as tf
from PIL import Image, ImageFilter
import numpy as np
import os
import gdown
import matplotlib.cm as cm
import random 
from pillow_heif import register_heif_opener

register_heif_opener()

# --- 1. KONEKSI KE OTAK AI V4 ---
@st.cache_resource
def download_dan_muat_model():
    # ID Drive Otak V4 milikmu sudah terpasang
    id_drive = '1m0LTjbpmfEI-pqjpOb-cwu_MvZRaqraO' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v4.h5' 
    if not os.path.exists(nama_file):
        with st.spinner('Memasang Otak V4 Super Cerdas...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. MESIN SINAR-X KONTUR ---
def buat_xray_kontur(img_asli):
    img_gray = img_asli.convert("L")
    img_edges = img_gray.filter(ImageFilter.FIND_EDGES)
    arr_edges = np.array(img_edges)
    jet = cm.get_cmap("jet") 
    colored_edges = jet(arr_edges / 255.0)
    colored_edges = np.uint8(colored_edges * 255)
    return Image.fromarray(colored_edges).convert("RGB")

# --- 3. DATABASE IDE BISNIS ---
ide_organik = [
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50.000", "target": "Pecinta Tanaman & Petani Lokal"},
    {"ide": "🐛 Budidaya Maggot BSF", "modal": "Rp 100.000", "target": "Peternak Ikan & Ayam"}
]
ide_anorganik = [
    {"ide": "🧱 Paving Block Eco-Brick", "modal": "Rp 20.000", "target": "Kontraktor & Perumahan"},
    {"ide": "👜 Tas Anyaman Estetik", "modal": "Rp 15.000", "target": "Pasar Fashion & Turis"}
]

# --- 4. DESAIN CSS PAPAN TULIS ANTI-LIGHT MODE (UPGRADE) ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    /* 1. MENGGEMBOK LATAR BELAKANG HP AGAR TETAP GELAP */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #1a252f !important; 
    }
    
    /* 2. PAPAN TULIS UTAMA */
    .block-container {
        background-color: #2F4F4F !important;
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        border: 15px solid #5C4033 !important; 
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: inset 0 0 80px rgba(0,0,0,0.8), 5px 5px 25px rgba(0,0,0,0.5) !important;
    }

    /* 3. MENGGEMBOK SELURUH TEKS AGAR PUTIH */
    html, body, p, h1, h2, h3, h4, h5, h6, li, span, label, div { 
        font-family: 'Caveat', cursive !important; 
        color: #F8F8FF !important; 
    }

    /* 4. MENGGEMBOK KOTAK UPLOAD AGAR ANTI-LIGHT MODE */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1e2a35 !important; /* Paksa latar kotak menjadi gelap */
        border: 2px dashed #F8F8FF !important;
        border-radius: 10px !important;
    }
    
    /* Paksa teks di dalam kotak upload menjadi putih */
    [data-testid="stFileUploadDropzone"] * { 
        color: #F8F8FF !important; 
    }
    
    /* Paksa tombol "Browse files" di dalam kotak upload */
    [data-testid="stFileUploadDropzone"] button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* 5. ELEMEN BISNIS & POLAROID */
    .polaroid { 
        background: white !important; 
        padding: 10px 10px 30px 10px; 
        border-radius: 2px; 
        transform: rotate(-1deg); 
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4); 
    }
    
    .business-note { 
        background: #fff9c4 !important; 
        padding: 15px; 
        border-radius: 2px; 
        border-top: 10px solid #fbc02d !important; 
    }
    
    /* Khusus kotak bisnis, teks harus gelap agar bisa dibaca */
    .business-note * { 
        color: #333 !important; 
        text-shadow: none !important; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH V4</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"])
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("MULAI ANALISIS ➜", use_container_width=True)

with kanan:
    st.markdown("### 2. HASIL ANALISIS 🎯")
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('Otak V4 sedang memikir...'):
            img_res = img_asli.resize((150, 150))
            
            # PENTING 1: Dibagi 255.0 agar AI tidak bingung (Skala 0-1)
            arr = tf.keras.utils.img_to_array(img_res) / 255.0 
            arr = np.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            
            # PENTING 2: LOGIKA FIX BERDASARKAN ALFABET COLAB ('O'=0, 'R'=1)
            if pred[0][0] < 0.5:
                status, warna = "ORGANIK 🍃", "#98FB98"
                ide = random.choice(ide_organik)
                pesan = "Keren! Sampah ini bisa kembali ke alam sebagai pupuk kompos."
            else:
                status, warna = "ANORGANIK / DAUR ULANG ♻️", "#D3D3D3"
                ide = random.choice(ide_anorganik)
                pesan = "Masuk kategori daur ulang pabrik untuk menjaga bumi!"

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 45px;'>➡️ {status}</h1>", unsafe_allow_html=True)
            st.write(f"🌍 {pesan}")
            
            st.markdown(f"""
                <div class="business-note">
                    <h3>💡 Peluang Bisnis:</h3>
                    <p style="font-size:24px; font-weight:bold;">{ide['ide']}</p>
                    <ul>
                        <li>Modal Awal: {ide['modal']}</li>
                        <li>Target Pasar: {ide['target']}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Struktur Material (Sinar-X):")
            st.image(buat_xray_kontur(img_asli), use_container_width=True)
    else:
        st.info("Unggah foto sampah di sebelah kiri untuk menguji keajaiban Otak V4!")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas & Kardus | 🍎 Sisa Makanan")
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

# --- 1. KONEKSI KE OTAK AI (ID DRIVE TER-UPDATE) ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1Trv1Itbr8YeTnkes4FF5CpNB5ApmcpK7' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v3.h5'
    if not os.path.exists(nama_file):
        with st.spinner('Menyiapkan Kapur dan Papan Tulis...'):
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

# --- 3. DATABASE FALLBACK ---
ide_organik = [
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50.000", "target": "Pecinta Tanaman"},
    {"ide": "🐛 Budidaya Maggot", "modal": "Rp 100.000", "target": "Peternak Lokal"}
]
ide_anorganik = [
    {"ide": "🧱 Paving Block Eco", "modal": "Rp 20.000", "target": "Kontraktor"},
    {"ide": "👜 Tas Anyaman Estetik", "modal": "Rp 15.000", "target": "Pasar Fashion"}
]

# --- 4. DESAIN CSS ULTRA (TEXTURE & ANTI-LIGHT MODE) ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    /* FIX: PAKSA BACKGROUND TETAP GELAP (ANTI-LIGHT MODE) */
    .stApp, [data-testid="stAppViewContainer"] { 
        background-color: #1a252f !important; 
    }
    
    /* TEKSTUR PAPAN TULIS: GRID & VIGNETTE */
    .block-container {
        background-color: #2F4F4F !important;
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        border: 12px solid #5C4033 !important; 
        border-radius: 8px !important;
        padding: 30px !important;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.8), 5px 5px 25px rgba(0,0,0,0.5) !important;
    }

    /* FIX: KOTAK UPLOAD HP AGAR TULISAN TERBACA */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(0,0,0,0.4) !important;
        border: 2px dashed #F8F8FF !important;
    }
    [data-testid="stFileUploadDropzone"] * { color: #F8F8FF !important; }

    /* ANIMASI JUDUL MENGAMBANG */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .judul-animasi {
        animation: floating 3s ease-in-out infinite;
        text-align: center; color: #F8F8FF; font-size: 55px;
    }

    /* ANIMASI TOMBOL PULSE */
    @keyframes pulse-green {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    div.stButton > button {
        animation: pulse-green 2s infinite !important;
        background-color: #4CAF50 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 15px !important;
        font-size: 22px !important;
    }

    /* GLOBAL FONT */
    html, body, p, h1, h2, h3, li, span { 
        font-family: 'Caveat', cursive !important; 
        color: #F8F8FF !important; 
    }
    .polaroid { background: #fdfdfd; padding: 10px 10px 30px 10px; border-radius: 2px; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); transform: rotate(-1deg); }
    .business-note { background: #fff9c4; padding: 15px; border-radius: 2px; border-top: 10px solid #fbc02d; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); }
    .business-note * { color: #333 !important; }
    .eco-box { background: rgba(76, 175, 80, 0.15); border-left: 5px solid #4CAF50; padding: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK UTAMA ---
st.markdown("<h1 class='judul-animasi'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    # FIX: MENAMBAHKAN KEMBALI JFIF DAN VARIAN LAINNYA
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"])
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("MULAI ANALISIS ➜")

with kanan:
    st.markdown("### 2. HASIL ANALISIS 🎯")
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('Menganalisis material...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0
            arr = np.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            
            if pred[0][0] > 0.5:
                status, warna = "ORGANIK 🍃", "#98FB98"
                ide = random.choice(ide_organik)
                pesan = "Aman! Sampah ini bisa kembali ke alam."
            else:
                status, warna = "ANORGANIK ⚙️", "#D3D3D3"
                ide = random.choice(ide_anorganik)
                pesan = "Daur ulang segera! Jangan biarkan ia mencemari bumi."

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 50px;'>➡️ {status}</h1>", unsafe_allow_html=True)
            st.markdown(f"<div class='eco-box'><p style='font-size:22px;'>🌍 {pesan}</p></div>", unsafe_allow_html=True)
            
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
        st.info("Unggah foto sampahmu untuk melihat analisis AI!")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
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

# --- 1. KONEKSI KE OTAK AI ---
@st.cache_resource
def download_dan_muat_model():
    # ID Drive milikmu sudah saya pasang di sini
    id_drive = '1Trv1Itbr8YeTnkes4FF5CpNB5ApmcpK7' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v3.h5'
    if not os.path.exists(nama_file):
        with st.spinner('Menghapus coretan di papan tulis...'):
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
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50rb", "target": "Pecinta Tanaman"},
    {"ide": "🐛 Budidaya Maggot", "modal": "Rp 100rb", "target": "Peternak Lokal"}
]
ide_anorganik = [
    {"ide": "🧱 Paving Block Eco", "modal": "Rp 20rb", "target": "Kontraktor"},
    {"ide": "👜 Tas Anyaman Estetik", "modal": "Rp 15rb", "target": "Pasar Fashion"}
]

# --- 4. DESAIN CSS PAPAN TULIS ULTRA (DENGAN ANIMASI FIX) ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    /* 1. PAKSA TEMA GELAP (ANTI-LIGHT MODE) */
    [data-testid="stAppViewContainer"], .stApp { background-color: #1a252f !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    html, body, p, span, h1, h2, h3, h4, li, div, label {
        font-family: 'Caveat', cursive !important;
        color: #F8F8FF !important;
    }
    
    /* 2. TEKSTUR PAPAN TULIS: GRID & DEBU KAPUR */
    .block-container {
        background-color: #2F4F4F !important;
        background-image: 
            linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px) !important;
        background-size: 40px 40px !important;
        border: 15px solid #5C4033 !important; 
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.9), 10px 10px 30px rgba(0,0,0,0.6) !important;
        max-width: 1000px !important;
    }

    /* 3. FIX: KOTAK UPLOAD HP AGAR TETAP GELAP & TERBACA */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(0,0,0,0.5) !important;
        border: 2px dashed #F8F8FF !important;
        border-radius: 15px !important;
    }
    [data-testid="stFileUploadDropzone"] * { color: #F8F8FF !important; }

    /* 4. ANIMASI JUDUL MENGAMBANG (SINKRON) */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    .judul-float {
        animation: floating 3s ease-in-out infinite;
        text-align: center; font-size: 65px; margin-bottom: 0px;
    }

    /* 5. ANIMASI TOMBOL BERDENYUT */
    @keyframes pulse-green {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(76, 175, 80, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    div.stButton > button {
        animation: pulse-green 2s infinite !important;
        background-color: #4CAF50 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 15px !important;
        font-size: 24px !important;
        width: 100% !important;
    }

    /* LAIN-LAIN */
    .polaroid { background: #fdfdfd; padding: 10px 10px 30px 10px; border-radius: 2px; box-shadow: 3px 3px 15px rgba(0,0,0,0.5); transform: rotate(-1deg); }
    .business-note { background: #fff9c4; padding: 15px; border-radius: 2px; border-top: 10px solid #fbc02d; box-shadow: 3px 3px 15px rgba(0,0,0,0.4); margin-top: 15px; }
    .business-note * { color: #333 !important; }
    .eco-box { background: rgba(76, 175, 80, 0.2); border-left: 5px solid #4CAF50; padding: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK UTAMA ---
st.markdown("<h1 class='judul-float'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 22px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kol1, kol2 = st.columns(2)

with kol1:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    # Penambahan format file lebih lengkap
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"])
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("MULAI ANALISIS ➜")

with kol2:
    st.markdown("### 2. HASIL ANALISIS 🎯")
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('AI sedang memindai struktur material...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0
            arr = np.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            
            # FIX LOGIKA: 0=Organik ('O'), 1=Anorganik ('R')
            if pred[0][0] < 0.5:
                status, warna = "ORGANIK 🍃", "#98FB98"
                ide = random.choice(ide_organik)
                pesan = "Hebat! Sampah ini adalah sisa alam yang bisa didaur ulang jadi kompos."
            else:
                status, warna = "ANORGANIK ⚙️", "#D3D3D3"
                ide = random.choice(ide_anorganik)
                pesan = "Penting! Sampah anorganik ini harus dikelola dengan baik agar tidak merusak bumi."

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
        st.info("Silakan unggah foto di sebelah kiri untuk melihat keajaiban AI!")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
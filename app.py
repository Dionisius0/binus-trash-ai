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

# --- 1. KONEKSI KE OTAK AI (STABIL) ---
@st.cache_resource
def download_dan_muat_model():
    # ID Drive milikmu yang sudah terbukti jalan
    id_drive = '1Trv1Itbr8YeTnkes4FF5CpNB5ApmcpK7' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v3.h5'
    if not os.path.exists(nama_file):
        with st.spinner('Menyiapkan Papan Tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. MESIN SINAR-X ---
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
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50.000", "target": "Petani Lokal"},
    {"ide": "🐛 Budidaya Maggot", "modal": "Rp 100.000", "target": "Peternak"}
]
ide_anorganik = [
    {"ide": "🧱 Paving Block Eco", "modal": "Rp 20.000", "target": "Kontraktor"},
    {"ide": "👜 Tas Anyaman Estetik", "modal": "Rp 15.000", "target": "Pasar Fashion"}
]

# --- 4. DESAIN CSS PAPAN TULIS (VERSI STABIL & RAPI) ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    .stApp { background-color: #2c3e50 !important; }
    
    .block-container {
        background-color: #2F4F4F !important; 
        border: 15px solid #5C4033 !important; 
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5) !important;
        max-width: 1000px !important;
    }
    
    html, body, p, span, div, label, h1, h2, h3, h4, li {
        font-family: 'Caveat', cursive !important;
        color: #F8F8FF !important;
    }

    /* FIX UNTUK LIGHT MODE HP */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(0,0,0,0.2) !important;
        border: 2px dashed #F8F8FF !important;
    }

    .polaroid { background: white; padding: 10px 10px 30px 10px; border-radius: 2px; transform: rotate(-1deg); }
    .business-note { background: #fff9c4; padding: 15px; border-radius: 2px; border-top: 10px solid #fbc02d; color: #333 !important; }
    .business-note * { color: #333 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    # Format foto sudah lengkap termasuk JFIF
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"])
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("CEK SEKARANG ➜", use_container_width=True)

with kanan:
    st.markdown("### 2. HASIL ANALISIS 🎯")
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('Menganalisis...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0
            arr = np.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            
            # LOGIKA KEMBALI NORMAL: 0=ANORGANIK (R), 1=ORGANIK (O)
            if pred[0][0] < 0.5:
                status, warna = "ANORGANIK ⚙️", "#D3D3D3"
                ide = random.choice(ide_anorganik)
                pesan = "Aksi daur ulangmu membantu mengurangi jejak karbon!"
            else:
                status, warna = "ORGANIK 🍃", "#98FB98"
                ide = random.choice(ide_organik)
                pesan = "Keren! Sampah ini bisa jadi pupuk alami."

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 50px;'>➡️ {status}</h1>", unsafe_allow_html=True)
            st.write(f"🌍 {pesan}")
            
            st.markdown(f"""
                <div class="business-note">
                    <h3>💡 Peluang Bisnis Daur Ulang:</h3>
                    <p style="font-size:24px; font-weight:bold;">{ide['ide']}</p>
                    <ul>
                        <li>Modal: {ide['modal']}</li>
                        <li>Target: {ide['target']}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Analisis Struktur (Sinar-X):")
            st.image(buat_xray_kontur(img_asli), use_container_width=True)
    else:
        st.info("Silakan unggah foto di sebelah kiri.")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
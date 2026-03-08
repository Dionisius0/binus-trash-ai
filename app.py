import streamlit as st
import tensorflow as tf
from PIL import Image, ImageFilter
import numpy as np
import os
import gdown
import matplotlib.cm as cm
import google.generativeai as genai
from pillow_heif import register_heif_opener

register_heif_opener()

# --- 1. KONEKSI KE OTAK AI & GEMINI ---
# Masukkan API Key Gemini kamu di bawah ini
API_KEY_GEMINI = "MASUKKAN_API_KEY_GEMINI_KAMU_DI_SINI" 
genai.configure(api_key=API_KEY_GEMINI)

@st.cache_resource
def download_dan_muat_model():
    id_drive = '1Trv1Itbr8YeTnkes4FF5CpNB5ApmcpK7' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v3.h5'
    if not os.path.exists(nama_file):
        with st.spinner('Menyiapkan Papan Tulis...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model = download_dan_muat_model()

# --- 2. FITUR DINAMIS GEMINI ---
def ambil_ide_bisnis_dinamis(img, kategori):
    try:
        model_gemini = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Sebagai konsultan bisnis, lihat foto sampah {kategori} ini. Berikan 1 ide bisnis kreatif, estimasi modal awal, dan siapa target konsumennya. Gunakan bahasa yang mudah dimengerti mahasiswa."
        response = model_gemini.generate_content([prompt, img])
        return response.text
    except:
        return "⚠️ Hubungkan API Key Gemini untuk mendapatkan ide bisnis dinamis sesuai foto."

# --- 3. MESIN SINAR-X ---
def buat_xray_kontur(img_asli):
    img_gray = img_asli.convert("L")
    img_edges = img_gray.filter(ImageFilter.FIND_EDGES)
    arr_edges = np.array(img_edges)
    jet = cm.get_cmap("jet") 
    colored_edges = jet(arr_edges / 255.0)
    colored_edges = np.uint8(colored_edges * 255)
    return Image.fromarray(colored_edges).convert("RGB")

# --- 4. DESAIN CSS ULTRA (ANTI-LIGHT MODE & TEKSTUR) ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    /* PAKSA TEMA GELAP */
    .stApp, [data-testid="stAppViewContainer"] { background-color: #1a252f !important; }
    
    /* TEKSTUR PAPAN TULIS */
    .block-container {
        background-color: #2F4F4F !important;
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        border: 12px solid #5C4033 !important; 
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: inset 0 0 80px rgba(0,0,0,0.8), 5px 5px 25px rgba(0,0,0,0.5) !important;
    }

    /* KOTAK UPLOAD ANTI-LIGHT MODE HP */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(0,0,0,0.4) !important;
        border: 2px dashed #F8F8FF !important;
    }
    [data-testid="stFileUploadDropzone"] * { color: #F8F8FF !important; }

    /* ANIMASI JUDUL */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .judul-binus {
        animation: floating 3s ease-in-out infinite;
        text-align: center; color: #F8F8FF !important; font-size: 55px;
    }

    html, body, p, h1, h2, h3, li, span, label { 
        font-family: 'Caveat', cursive !important; 
        color: #F8F8FF !important; 
    }
    .business-note { background: #fff9c4; padding: 20px; border-radius: 2px; border-top: 10px solid #fbc02d; }
    .business-note * { color: #333 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 class='judul-binus'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"])
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.image(img_asli, use_container_width=True)
        st.write("")
        tombol = st.button("MULAI ANALISIS ➜")

with kanan:
    st.markdown("### 2. HASIL ANALISIS 🎯")
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('AI sedang membedah material...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0
            arr = np.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            
            # FIX LOGIKA BERDASARKAN TRAINING: 0=ANORGANIK (R), 1=ORGANIK (O)
            if pred[0][0] < 0.5:
                status, warna = "ANORGANIK ⚙️", "#D3D3D3"
            else:
                status, warna = "ORGANIK 🍃", "#98FB98"

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 50px;'>➡️ {status}</h1>", unsafe_allow_html=True)
            
            st.markdown("<div class='business-note'>", unsafe_allow_html=True)
            st.markdown("### 💡 Ide Bisnis Khusus Untukmu:")
            st.write(ambil_ide_bisnis_dinamis(img_asli, status))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("### 👁️ Struktur Material (Sinar-X):")
            st.image(buat_xray_kontur(img_asli), use_container_width=True)
    else:
        st.info("Unggah foto sampah di sebelah kiri untuk memulai!")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
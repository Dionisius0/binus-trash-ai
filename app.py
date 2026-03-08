import streamlit as st
import tensorflow as tf
from PIL import Image, ImageFilter
import numpy as np
import os
import gdown
import matplotlib.cm as cm
import random 
import google.generativeai as genai
from pillow_heif import register_heif_opener

register_heif_opener()

# --- 1. KONFIGURASI OTAK LOGIKA (GEMINI API) ---
# ⬇️ MASUKKAN API KEY GEMINI KAMU DI DALAM TANDA KUTIP DI BAWAH INI ⬇️
API_KEY_GEMINI = "AIzaSyBb91GinWcUQ_9hPShEEbELUlm0iKx8Tqw"
genai.configure(api_key=API_KEY_GEMINI)

def analisis_mendalam_gemini(img, tebakan_awal):
    try:
        model_gemini = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Kamu adalah konsultan bisnis dan pengolahan limbah. 
        Mata sensor AI kami menebak gambar ini masuk kategori: {tebakan_awal}. 
        Tolong analisa gambar ini seperti manusia:
        1. Konfirmasi: Benda apa sebenarnya yang ada di foto ini? (Koreksi jika tebakan sensor salah).
        2. Ide Bisnis: Berikan 1 ide kreatif untuk mendaur ulang atau memanfaatkan benda tersebut, lengkap dengan perkiraan modal dan target pasarnya.
        Jawab dengan bahasa yang profesional namun santai ala mahasiswa bisnis."""
        
        response = model_gemini.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"⚠️ ERROR TEKNIS GEMINI: {e}"

# --- 2. KONEKSI KE OTAK INSTING V4 (TENSORFLOW) ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1m0LTjbpmfEI-pqjpOb-cwu_MvZRaqraO' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v4.h5' 
    if not os.path.exists(nama_file):
        with st.spinner('Memasang Otak V4 Super Cerdas...'):
            gdown.download(url, nama_file, quiet=False)
    return tf.keras.models.load_model(nama_file)

model_v4 = download_dan_muat_model()

# --- 3. MESIN SINAR-X KONTUR ---
def buat_xray_kontur(img_asli):
    img_gray = img_asli.convert("L")
    img_edges = img_gray.filter(ImageFilter.FIND_EDGES)
    arr_edges = np.array(img_edges)
    jet = cm.get_cmap("jet") 
    colored_edges = jet(arr_edges / 255.0)
    colored_edges = np.uint8(colored_edges * 255)
    return Image.fromarray(colored_edges).convert("RGB")

# --- 4. DATABASE STANDAR (JIKA GEMINI ERROR) ---
ide_organik = [
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50.000", "target": "Pecinta Tanaman & Petani Lokal"}
]
ide_anorganik = [
    {"ide": "🧱 Paving Block Eco-Brick", "modal": "Rp 20.000", "target": "Kontraktor & Perumahan"}
]

# --- 5. DESAIN UI PAPAN TULIS ANTI-LIGHT MODE ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    .stApp, [data-testid="stAppViewContainer"] { background-color: #1a252f !important; }
    
    .block-container {
        background-color: #2F4F4F !important;
        background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        border: 15px solid #5C4033 !important; 
        border-radius: 10px !important;
        padding: 40px !important;
        box-shadow: inset 0 0 80px rgba(0,0,0,0.8), 5px 5px 25px rgba(0,0,0,0.5) !important;
    }

    html, body, p, h1, h2, h3, li, span, label { font-family: 'Caveat', cursive !important; color: #F8F8FF !important; }

    /* WARNA FONT UNIVERSAL UNTUK KOTAK UPLOAD */
    [data-testid="stFileUploadDropzone"] { border: 3px dashed #E67E22 !important; background-color: transparent !important;}
    [data-testid="stFileUploadDropzone"] * { color: #E67E22 !important; font-weight: bold !important; }
    [data-testid="stFileUploadDropzone"] button { background-color: #E67E22 !important; color: white !important; border: 2px solid white !important; border-radius: 8px !important; }

    .polaroid { background: white; padding: 10px 10px 30px 10px; border-radius: 2px; transform: rotate(-1deg); box-shadow: 3px 3px 10px rgba(0,0,0,0.4); }
    .business-note { background: #fff9c4; padding: 25px; border-radius: 5px; border-top: 15px solid #fbc02d; color: #333 !important; margin-top: 20px;}
    .business-note * { color: #333 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 6. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH V5 (HIBRIDA AI)</h1>", unsafe_allow_html=True)
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
        
        # --- A. KERJA OTAK INSTING (TENSORFLOW) ---
        with st.spinner('Mata AI sedang memindai pola tekstur...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0 
            arr = np.expand_dims(arr, 0)
            
            pred = model_v4.predict(arr, verbose=0)
            
            if pred[0][0] < 0.5:
                status, warna = "ORGANIK 🍃", "#98FB98"
            else:
                status, warna = "ANORGANIK / DAUR ULANG ♻️", "#D3D3D3"

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 40px;'>➡️ Prediksi Sensor: {status}</h1>", unsafe_allow_html=True)

        # --- B. KERJA OTAK LOGIKA (GEMINI) ---
        with st.spinner('Otak Logika sedang mengkonfirmasi hasil...'):
            analisis_cerdas = analisis_mendalam_gemini(img_asli, status)
            
            st.markdown(f"""
                <div class="business-note">
                    <h3>🧠 Analisis Bisnis Mendalam (Gemini AI):</h3>
                    <p style="font-size:18px; font-family: sans-serif !important;">{analisis_cerdas}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Struktur Material (Sinar-X):")
            st.image(buat_xray_kontur(img_asli), use_container_width=True)
    else:
        st.info("Unggah foto di sebelah kiri untuk menguji kekuatan Kolaborasi 2 AI!")

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas & Kardus | 🍎 Sisa Makanan")
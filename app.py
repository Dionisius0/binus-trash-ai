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
API_KEY_GEMINI = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY_GEMINI)

def analisis_mendalam_gemini(img, tebakan_awal):
    try:
        model_gemini = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""Anda adalah seorang konsultan bisnis tingkat eksekutif dan pakar manajemen limbah profesional.
        Sistem sensor AI kami memprediksi gambar ini masuk dalam kategori: {tebakan_awal}.
        Tolong berikan analisis teknis dan objektif berdasarkan gambar tersebut:
        
        1. Identifikasi Material: Konfirmasi secara akurat objek apa yang ada di dalam foto. Jika prediksi sistem sensor salah, berikan koreksi yang tepat berdasarkan jenis materialnya (organik/anorganik).
        2. Prospek Daur Ulang & Bisnis: Berikan 1 (satu) rekomendasi ide bisnis atau pemanfaatan limbah tersebut yang bernilai ekonomis. Sertakan estimasi modal awal yang logis dan segmentasi target pasar yang spesifik.
        
        Instruksi Eksekusi: Gunakan Bahasa Indonesia yang sangat formal, akademis, dan profesional. DILARANG KERAS menggunakan kata sapaan santai (seperti 'bro', 'sis', 'halo'), gaya bahasa percakapan, atau basa-basi. Jawab langsung pada poinnya dengan struktur yang rapi."""
        
        response = model_gemini.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"⚠️ Peringatan Sistem: Gagal memuat analisis lanjutan. Error: {e}"

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

# --- 4. DESAIN UI PAPAN TULIS ANTI-LIGHT MODE ---
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
    
    .maps-btn {
        background-color: #4CAF50 !important; color: white !important; padding: 12px 20px !important;
        text-align: center !important; text-decoration: none !important; display: block !important;
        font-size: 22px !important; font-family: 'Caveat', cursive !important; border-radius: 10px !important;
        border: 2px solid white !important; box-shadow: 3px 3px 10px rgba(0,0,0,0.5) !important;
        transition: 0.3s !important; margin-top: 20px; margin-bottom: 25px;
    }
    .maps-btn:hover { background-color: #45a049 !important; transform: scale(1.02); }

    /* REVISI MUTLAK: KOTAK TUNGGU PRESISI 95PX */
    .kotak-tunggu {
        background-color: rgba(33, 150, 243, 0.1) !important;
        border: 2px dashed #2196F3 !important;
        border-radius: 8px !important;
        height: 95px !important; /* Tinggi fix 95 piksel, sama persis dengan tinggi minimal kotak upload */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 15px !important; /* Hilangkan padding atas-bawah */
        font-size: 16px !important; 
        color: #F8F8FF !important;
        margin-bottom: -20px !important; /* MENGHANCURKAN MARGIN GAIB BAWAAN STREAMLIT */
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH V5 (HIBRIDA AI)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    st.markdown("### 1. UNGGAH FOTO ☁️")
    foto = st.file_uploader("Unggah", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"], label_visibility="collapsed")
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

        with st.spinner('Otak Logika sedang menyusun proposal bisnis...'):
            analisis_cerdas = analisis_mendalam_gemini(img_asli, status)
            
            st.markdown(f"""
                <div class="business-note">
                    <h3>🧠 Laporan Analisis & Eksekusi Bisnis (Gemini AI):</h3>
                    <p style="font-size:18px; font-family: sans-serif !important;">{analisis_cerdas}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if status == "ANORGANIK / DAUR ULANG ♻️":
                st.markdown("""
                    <a href="https://www.google.com/maps/search/Bank+Sampah+Terdekat" target="_blank" class="maps-btn">
                        📍 Buka Peta: Cari Bank Sampah Terdekat
                    </a>
                """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Struktur Material (Sinar-X):")
            st.image(buat_xray_kontur(img_asli), use_container_width=True)
    else:
        st.markdown('<div class="kotak-tunggu">Unggah foto di sebelah kiri untuk menguji kekuatan Kolaborasi 2 AI!</div>', unsafe_allow_html=True)

st.write("---")
st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas & Kardus | 🍎 Sisa Makanan")
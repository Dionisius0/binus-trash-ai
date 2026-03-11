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

# --- 4. DESAIN UI GLASSMORPHISM & PAPAN TULIS ---
st.set_page_config(page_title="Detektor Sampah Binus", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');
    
    .stApp, [data-testid="stAppViewContainer"] { background-color: #1a252f !important; }
    
    /* LATAR BELAKANG PAPAN TULIS (TETAP) */
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

    /* EFEK GLOWING PADA JUDUL */
    h1 { text-shadow: 0 0 15px rgba(152, 251, 152, 0.6) !important; }

    /* KEAJAIBAN GLASSMORPHISM UNTUK KOTAK KOLOM */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.05) !important; /* Kaca transparan tipis */
        backdrop-filter: blur(12px) !important; /* Efek blur kaca buram */
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important; /* Garis pinggir kaca berpendar */
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important; /* Bayangan 3D */
    }

    /* DESAIN KOTAK UPLOAD DALAM KACA */
    [data-testid="stFileUploadDropzone"] { 
        background-color: rgba(0, 0, 0, 0.2) !important; 
        border: 2px dashed rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
    }
    [data-testid="stFileUploadDropzone"] * { color: #F8F8FF !important; font-weight: bold !important; }
    [data-testid="stFileUploadDropzone"] button { 
        background-color: rgba(255,255,255,0.1) !important; 
        color: white !important; 
        border: 1px solid white !important; 
        border-radius: 8px !important; 
    }

    /* ANIMASI IKON MELAYANG (CLOUD & TARGET) */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .glowing-icon {
        font-size: 80px;
        text-align: center;
        display: block;
        text-shadow: 0 0 25px rgba(255, 255, 255, 0.7);
        animation: float 3s ease-in-out infinite;
        margin-bottom: 10px;
    }
    .glowing-icon-target { text-shadow: 0 0 25px rgba(255, 99, 71, 0.8); }
    .glowing-icon-cloud { text-shadow: 0 0 25px rgba(135, 206, 250, 0.8); }

    .polaroid { background: white; padding: 10px 10px 30px 10px; border-radius: 2px; transform: rotate(-1deg); box-shadow: 3px 3px 10px rgba(0,0,0,0.4); margin-top: 15px;}
    .business-note { background: rgba(255, 249, 196, 0.9); padding: 25px; border-radius: 10px; border-top: 10px solid #fbc02d; color: #333 !important; margin-top: 20px;}
    .business-note * { color: #333 !important; }
    
    .maps-btn {
        background-color: rgba(76, 175, 80, 0.8) !important; color: white !important; padding: 12px 20px !important;
        text-align: center !important; text-decoration: none !important; display: block !important;
        font-size: 22px !important; font-family: 'Caveat', cursive !important; border-radius: 10px !important;
        border: 1px solid white !important; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4) !important;
        transition: 0.3s !important; margin-top: 20px; margin-bottom: 10px;
    }
    .maps-btn:hover { background-color: #45a049 !important; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH V5 (HIBRIDA AI)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Kelompok 3 - Business Management B29 🎓</p>", unsafe_allow_html=True)
st.write("---")

kiri, kanan = st.columns(2)

with kiri:
    # IKON AWAN MELAYANG
    st.markdown('<span class="glowing-icon glowing-icon-cloud">☁️</span>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>1. UNGGAH FOTO</h3>", unsafe_allow_html=True)
    
    foto = st.file_uploader("Unggah", type=["jpg", "png", "jpeg", "webp", "jfif", "heic", "JPG", "PNG", "JPEG"], label_visibility="collapsed")
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("MULAI ANALISIS ➜", use_container_width=True)

with kanan:
    # IKON TARGET MELAYANG
    st.markdown('<span class="glowing-icon glowing-icon-target">🎯</span>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>2. HASIL ANALISIS</h3>", unsafe_allow_html=True)
    
    if foto and 'tombol' in locals() and tombol:
        
        with st.spinner('Mata AI sedang memindai pola tekstur...'):
            img_res = img_asli.resize((150, 150))
            arr = tf.keras.utils.img_to_array(img_res) / 255.0 
            arr = np.expand_dims(arr, 0)
            
            pred = model_v4.predict(arr, verbose=0)
            
            if pred[0][0] < 0.5:
                status, warna = "ORGANIK 🍃", "#98FB98"
            else:
                status, warna = "ANORGANIK / DAUR ULANG ♻️", "#FFB6C1"

            st.markdown(f"<h1 style='color:{warna} !important; font-size: 40px; text-align: center;'>➡️ Prediksi: {status}</h1>", unsafe_allow_html=True)

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
        # TAMPILAN KOSONG ELEGAN
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 20px;">
                <span style="font-size: 50px; animation: float 2s infinite;">👇</span>
                <p style="color: #D3D3D3; font-family: 'Caveat', cursive; font-size: 22px; text-align: center; margin-top: 15px;">
                    Kamera AI Sudah Siap!<br>Tarik & lepas foto sampahmu ke kotak di sebelah kiri.
                </p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<h4 style='text-align: center; color: #D3D3D3;'>🌱 Kompos &nbsp; | &nbsp; 🚰 Plastik &nbsp; | &nbsp; 📰 Kertas & Kardus &nbsp; | &nbsp; 🍎 Sisa Makanan</h4>", unsafe_allow_html=True)
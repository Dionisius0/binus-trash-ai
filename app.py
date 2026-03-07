import streamlit as st
import tensorflow as tf
from PIL import Image, ImageFilter
import numpy as np
import os
import gdown
import matplotlib.cm as cm
import random # Alat baru untuk mengacak ide bisnis
from pillow_heif import register_heif_opener

register_heif_opener()

# --- 1. KONEKSI KE OTAK AI ---
@st.cache_resource
def download_dan_muat_model():
    id_drive = '1AbjMsB3EZr5wRamQmdLNUjbUGaYpvOEt' 
    url = f'https://drive.google.com/uc?id={id_drive}'
    nama_file = 'model_sampah_v2.h5'
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

# --- 3. DATABASE IDE BISNIS (FITUR BARU) ---
ide_organik = [
    {"ide": "🌱 Pupuk Kompos Cair", "modal": "Rp 50.000 (Beli EM4 & Ember)", "jual": "Rp 25.000 / botol", "target": "Pecinta tanaman hias & petani lokal."},
    {"ide": "🐛 Budidaya Maggot BSF", "modal": "Rp 100.000 (Kandang mini)", "jual": "Rp 50.000 / kg", "target": "Peternak ayam & ikan lele."},
    {"ide": "🔥 Briket Bioarang", "modal": "Rp 150.000 (Alat cetak sederhana)", "jual": "Rp 15.000 / kg", "target": "Warung sate & restoran BBQ."}
]

ide_anorganik = [
    {"ide": "🧱 Paving Block Eco-Brick", "modal": "Rp 20.000 (Semen campuran)", "jual": "Rp 15.000 / blok", "target": "Kontraktor perumahan ramah lingkungan."},
    {"ide": "👜 Tas Anyaman Estetik", "modal": "Rp 15.000 (Gunting & benang)", "jual": "Rp 75.000 / pcs", "target": "Pasar fashion eco-friendly & turis."},
    {"ide": "💡 Lampu Hias Botol Kaca", "modal": "Rp 35.000 (Lampu LED strip)", "jual": "Rp 120.000 / pcs", "target": "Kafe kekinian & dekorasi kamar."}
]

# --- 4. DESAIN CSS PAPAN TULIS & BINGKAI KAYU ---
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
    html, body, [class*="css"], p, span, div, label, h1, h2, h3, h4 {
        font-family: 'Caveat', 'Comic Sans MS', cursive !important;
        color: #F8F8FF !important;
        letter-spacing: 1px;
    }
    .polaroid-frame {
        background-color: #F5F5DC !important;
        padding: 10px 10px 35px 10px !important;
        box-shadow: 3px 3px 15px rgba(0,0,0,0.6) !important;
        border-radius: 2px !important;
        transform: rotate(-2deg);
        display: block; margin: 0 auto;
    }
    .xray-frame {
        background-color: #000000 !important;
        padding: 5px !important;
        border: 2px solid #00FF00 !important;
        box-shadow: 0px 0px 15px #00FF00 !important;
        border-radius: 5px !important;
    }
    /* Desain Sticky Note untuk Proposal Bisnis */
    .business-note {
        background-color: #FFF9C4 !important;
        color: #3E2723 !important;
        padding: 20px !important;
        border-radius: 2px !important;
        transform: rotate(1deg);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.4) !important;
        border-top: 15px solid #FFD54F !important;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .business-note h3, .business-note p, .business-note li {
        color: #3E2723 !important;
        text-shadow: none !important;
        font-family: 'Caveat', cursive !important;
    }
    [data-testid="stFileUploadDropzone"] { background-color: transparent !important; border: 2px dashed #F8F8FF !important; }
    [data-testid="baseButton-secondary"] {
        background-color: transparent !important; color: #F8F8FF !important; border: 2px solid #F8F8FF !important; border-radius: 15px !important; font-size: 20px !important;
    }
    [data-testid="baseButton-secondary"]:hover { background-color: #F8F8FF !important; color: #2F4F4F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TATA LETAK ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>DETEKTOR SAMPAH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Dibuat oleh: Kelompok 3 - Business Management 🎓</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

kol_kiri, kol_kanan = st.columns(2)

with kol_kiri:
    st.markdown("<h2 style='font-size: 35px;'>1. UNGGAH ☁️</h2>", unsafe_allow_html=True)
    foto = st.file_uploader("", type=["jpg", "png", "jpeg", "webp", "jfif", "heic"])
    
    if foto:
        img_asli = Image.open(foto).convert('RGB')
        st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
        st.image(img_asli, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        tombol = st.button("CEK SEKARANG ➜", use_container_width=True)

with kol_kanan:
    st.markdown("<h2 style='font-size: 35px;'>2. HASIL 🎯</h2>", unsafe_allow_html=True)
    
    if foto and 'tombol' in locals() and tombol:
        with st.spinner('Menganalisis pola dan mencari peluang bisnis...'):
            img_res = img_asli.resize((180, 180))
            arr = tf.keras.utils.img_to_array(img_res)
            arr = tf.expand_dims(arr, 0)
            
            pred = model.predict(arr, verbose=0)
            hasil = np.argmax(tf.nn.softmax(pred[0]))
            
            img_xray = buat_xray_kontur(img_asli)
            
            # --- BAGIAN HASIL & PROPOSAL BISNIS ---
            if hasil == 0:
                st.markdown("<h1 style='color: #98FB98 !important; font-size: 50px;'>➡️ 🗑️ ORGANIK 🍃</h1>", unsafe_allow_html=True)
                bisnis = random.choice(ide_organik) # Mengacak ide organik
            else:
                st.markdown("<h1 style='color: #D3D3D3 !important; font-size: 50px;'>➡️ 🗑️ ANORGANIK ⚙️</h1>", unsafe_allow_html=True)
                bisnis = random.choice(ide_anorganik) # Mengacak ide anorganik
            
            # Menampilkan Proposal Bisnis Mini di atas Kertas Kuning (Sticky Note)
            st.markdown(f"""
                <div class="business-note">
                    <h3>💡 Peluang Bisnis Daur Ulang:</h3>
                    <p style="font-size: 24px; font-weight: bold;">{bisnis['ide']}</p>
                    <ul>
                        <li><b>Estimasi Modal:</b> {bisnis['modal']}</li>
                        <li><b>Potensi Harga Jual:</b> {bisnis['jual']}</li>
                        <li><b>Target Pasar:</b> {bisnis['target']}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Analisis Struktur AI:")
            st.markdown('<div class="xray-frame">', unsafe_allow_html=True)
            st.image(img_xray, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
    else:
        st.write("👈 Upload foto di sebelah kiri untuk melihat hasil, ide bisnis, dan Sinar-X di sini.")
        
    # --- PANDUAN DASAR SELALU MUNCUL ---
    st.markdown("<br><hr style='border: 1px dashed white;'>", unsafe_allow_html=True)
    st.markdown("### **PANDUAN DASAR:**")
    st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
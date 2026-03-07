import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import gdown
import matplotlib.cm as cm
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

# --- 2. MESIN SINAR-X (GRAD-CAM) ---
# Ini adalah kode baru yang bertugas membedah isi kepala AI
def buat_xray(img_array, model):
    try:
        # 2a. Mencari 'mata' AI (Layer Konvolusi Terakhir)
        last_conv_layer_name = None
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:
                last_conv_layer_name = layer.name
                break
        
        if not last_conv_layer_name: return None

        # 2b. Merekam proses berpikir AI
        grad_model = tf.keras.models.Model(
            [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
        )
        with tf.GradientTape() as tape:
            last_conv_layer_output, preds = grad_model(img_array)
            pred_index = tf.argmax(preds[0])
            class_channel = preds[:, pred_index]

        # 2c. Menghitung area mana yang paling penting (mewarnainya)
        grads = tape.gradient(class_channel, last_conv_layer_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()
    except:
        return None # Jika AI bingung, matikan Sinar-X agar tidak error

# Fungsi untuk menempelkan warna Sinar-X ke foto asli
def gabungkan_xray(img_asli, heatmap):
    heatmap = np.uint8(255 * heatmap)
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]
    jet_heatmap = tf.keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img_asli.size[0], img_asli.size[1]))
    jet_heatmap = tf.keras.utils.img_to_array(jet_heatmap)
    # Mencampur foto asli dengan warna Sinar-X (40% transparan)
    superimposed_img = jet_heatmap * 0.4 + np.array(img_asli)
    return tf.keras.utils.array_to_img(superimposed_img)


# --- 3. DESAIN CSS PAPAN TULIS & BINGKAI KAYU ---
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
    [data-testid="stFileUploadDropzone"] { background-color: transparent !important; border: 2px dashed #F8F8FF !important; }
    [data-testid="baseButton-secondary"] {
        background-color: transparent !important; color: #F8F8FF !important; border: 2px solid #F8F8FF !important; border-radius: 15px !important; font-size: 20px !important;
    }
    [data-testid="baseButton-secondary"]:hover { background-color: #F8F8FF !important; color: #2F4F4F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TATA LETAK ---
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
        with st.spinner('Menganalisis dan menyalakan mesin Sinar-X...'):
            # Persiapan Gambar untuk AI
            img_res = img_asli.resize((180, 180))
            arr = tf.keras.utils.img_to_array(img_res)
            arr = tf.expand_dims(arr, 0)
            
            # AI Berpikir
            pred = model.predict(arr, verbose=0)
            hasil = np.argmax(tf.nn.softmax(pred[0]))
            
            # Membuat Gambar Sinar-X
            heatmap = buat_xray(arr, model)
            
            # Menampilkan Teks Hasil
            if hasil == 0:
                st.markdown("<h1 style='color: #98FB98 !important; font-size: 50px;'>➡️ 🗑️ ORGANIK 🍃</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='color: #D3D3D3 !important; font-size: 50px;'>➡️ 🗑️ ANORGANIK ⚙️</h1>", unsafe_allow_html=True)
            
            # Menampilkan Gambar Sinar-X jika berhasil dibuat
            if heatmap is not None:
                st.markdown("### 👁️ X-Ray Vision AI:")
                st.write("Area bercahaya terang adalah alasan mengapa AI menebak sampah tersebut.")
                img_xray = gabungkan_xray(img_asli, heatmap)
                st.markdown('<div class="xray-frame">', unsafe_allow_html=True)
                st.image(img_xray, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
    else:
        st.write("👈 Upload foto di sebelah kiri untuk melihat hasil dan Sinar-X di sini.")
        st.markdown("<br><hr style='border: 1px dashed white;'>", unsafe_allow_html=True)
        st.markdown("### **PANDUAN DASAR:**")
        st.write("🍃 Kompos | 🥤 Plastik | 📰 Kertas | 🍎 Sisa Makanan")
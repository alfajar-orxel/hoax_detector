import streamlit as st
from prompts import prompt
from gemini_interface import tanya_gemini
from utils import ekstrak_teks

# Konfigurasi halaman
st.set_page_config(page_title="Detektor Berita Hoax", layout="centered")

# ===== CSS Custom =====
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .main > div {
            padding: 30px 20px;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            max-width: 800px;
            margin: auto;
        }
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .stRadio > div {
            flex-direction: row !important;
            justify-content: center;
        }
        .stButton button {
            background-color: #1f77b4;
            color: white;
            padding: 0.6em 1.2em;
            border-radius: 8px;
            border: none;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #135a96;
        }
        .stTextArea textarea, .stTextInput input {
            border-radius: 10px;
            padding: 12px;
            font-size: 1em;
        }
        .result-box {
            background-color: #e8f0fe;
            border-left: 6px solid #1f77b4;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ===== UI =====
st.title("Detektor Berita Hoax")

input_type = st.radio("Pilih jenis input:", ["Teks", "Link Berita"])
teks_input = ""

if input_type == "Teks":
    teks_input = st.text_area("Masukkan teks berita:")
else:
    url = st.text_input("Masukkan URL berita:")
    if url:
        teks_input = ekstrak_teks(url)
        st.text_area("Isi berita (hasil ekstrak):", teks_input, height=400)

if st.button("Deteksi") and teks_input:
    with st.spinner("Mohon tunggu ya, AI sedang menganalisis beritanya..."):
        prompt_ = prompt(teks_input)
        hasil = tanya_gemini(prompt_)

        lines = hasil.split("\n")
        kategori = ""
        penjelasan = ""
        confidence = ""

        for line in lines:
            if line.lower().startswith("kategori:"):
                kategori = line.split(":", 1)[1].strip()
            elif line.lower().startswith("penjelasan:"):
                penjelasan = line.split(":", 1)[1].strip()
            elif "confidence" in line.lower():
                confidence = line.split(":", 1)[1].strip()

        # Output hasil dalam box bergaya
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"**Kategori**: `{kategori}`")
        st.markdown(f"**Penjelasan**: {penjelasan}")
        st.markdown(f"**Tingkat Keyakinan AI**: {confidence}")
        st.markdown("</div>", unsafe_allow_html=True)

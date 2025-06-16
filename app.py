import streamlit as st
from prompts import prompt
from gemini_interface import tanya_gemini
from utils import ekstrak_teks

st.set_page_config(page_title="Detektor Berita", layout="centered")
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
    with st.spinner("Mohon tunggu ya, AI sedang menganalisis beritanya ^_^"):
        prompt_ = prompt(teks_input)
        hasil = tanya_gemini(prompt_)

        st.success("Hasil Deteksi AI:")

        lines = hasil.split("\n")
        kategori = ""
        penjelasan = ""
        kalimat_dasar = ""
        confidence = ""

        for line in lines:
            if line.lower().startswith("kategori:"):
                kategori = line.split(":", 1)[1].strip()
            elif line.lower().startswith("penjelasan:"):
                penjelasan = line.split(":", 1)[1].strip()
            elif "dasar" in line.lower():
                kalimat_dasar = line.split(":", 1)[1].strip()
            elif "confidence" in line.lower():
                confidence = line.split(":", 1)[1].strip()

        st.markdown(f"**Kategori**: `{kategori}`")
        st.markdown(f"**Penjelasan**: {penjelasan}")
        st.markdown(f"**Kalimat Bermasalah**: _{kalimat_dasar}_")
        st.markdown(f"**Tingkat Keyakinan AI**: {confidence}")

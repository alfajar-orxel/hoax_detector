# Detektor Hoax

Detektor Berita Hoax adalah sebuah website detektor yang dapat menganalisis teks atau link berita dan mengklasifikasikannya secara otomatis ke dalam empat kategori: Hoax, Clickbait, Misleading, atau Valid. Sistem ini dibangun menggunakan teknologi Artificial Intelligence (AI) berupa model AI dari Gemini.

---

## Tujuan Pembuatan

Web ini dibuat sebagai bagian dari projek dengan tujuan:

- Membantu masyarakat memverifikasi kebenaran informasi secara cepat dan mudah.
- Melawan dan mengurangi penyebaran berita hoax pada masyarakat, utamanya kalangan orang tua/ orang lanjut usia yang rentan termakan berita hoax
---

## Cara Kerja Aplikasi

1. Input Teks / Link Beita
   Pengguna dapat memasukkan berita dalam bentuk teks langsung, atau menyalin link berita dari internet.

2. Ekstraksi Teks Otomatis
   Jika input berupa link, aplikasi akan melakukan web scraping menggunakan `newspaper3k` dan fallback ke `BeautifulSoup` jika scraping gagal.

3. Analisis AI
   Teks akan dikirim ke model Gemini 2.5 API yang telah dioptimalkan dengan prompt yang sebelumnya sudah dibuat (ada di file prompts.py). AI akan memberikan:
   - Kategori berita
   - Penjelasan 
   - Tingkat keyakinan AI (Confidence Score)

---

## Teknologi yang Digunakan

| Komponen       | Teknologi / Tools                  |
|----------------|-------------------------------------|
| Bahasa         | Python 3.13                         |
| Framework UI   | Streamlit                           |
| AI Engine      | Gemini 2.5 API (Generative AI by Google) |
| Web Scraping   | Newspaper3k + BeautifulSoup         |
| Deployment     | Streamlit Cloud                     |

---

## Contoh Kasus Penggunaan

1. Seseorang menerima pesan hoax viral di grup WhatsApp.
2. Menyalin berita tersebut dan menempelkannya di aplikasi Detektor Hoax.
3. AI memberikan hasil klasifikasi sebagai Hoax, lengkap dengan alasan dan referensi pendukung.
4. Pengguna menjadi lebih sadar dan tidak ikut menyebarkan berita palsu.


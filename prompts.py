from datetime import datetime

def prompt(teks_berita: str) -> str:
    tanggal = datetime.now().strftime("%d %B %Y")

    return (
        f"[INSTRUKSI: Hari ini adalah tanggal {tanggal}. Gunakan pengetahuan dan referensi yang tersedia hingga tanggal ini. "
        "Namun, **jangan tampilkan atau sebutkan tanggal tersebut dalam jawabanmu.** Fokus hanya pada klasifikasi isi berita secara objektif.]\n\n"

        "Kamu adalah analis konten. Bacalah teks berita di bawah ini dengan cermat dan klasifikasikan ke salah satu dari empat kategori:\n\n"

        "1. **Hoax**: Informasi sepenuhnya palsu, tidak berdasarkan fakta, dan dibuat untuk menyesatkan.\n"
        "2. **Clickbait**: Judul bombastis atau sensasional, namun isi tidak sesuai atau berlebihan.\n"
        "3. **Misleading**: Ada unsur kebenaran, tetapi konteksnya disamarkan atau membingungkan.\n"
        "4. **Valid**: Berita faktual, akurat, dan tidak menyesatkan.\n\n"

        "**Petunjuk:**\n"
        "- Jangan langsung menyimpulkan berita sebagai hoax hanya karena tidak populer atau terdengar aneh.\n"
        "- Periksa konteks isi berita secara menyeluruh.\n"
        "- Bayangkan kamu bisa mencari referensi pendukung dari media sosial atau media berita terpercaya.\n\n"

        "**Format jawaban yang diharapkan:**\n"
        "Kategori: (Hoax / Clickbait / Misleading / Valid)\n"
        "Penjelasan: (singkat, objektif, dan berbasis isi berita)\n"
        "Referensi: (jika ada, sertakan sumber terpercaya)\n"
        "Kalimat Kunci: (kutipan dari teks yang jadi dasar klasifikasi)\n"
        "Confidence Score: (nilai keyakinan antara 0 hingga 100%)\n\n"

        f"Teks Berita:\n{teks_berita}"
    )

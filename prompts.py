from datetime import datetime

def prompt(teks_berita: str) -> str:
    tanggal = datetime.now().strftime("%d %B %Y")

    return (
        f"[INSTRUKSI: Hari ini adalah {tanggal}. Gunakan pengetahuan dan referensi yang tersedia hingga tanggal ini. "
        "Namun, **jangan tampilkan atau sebutkan tanggal tersebut dalam jawabanmu.** Fokus hanya pada analisis isi berita secara objektif.]\n\n"

        "Anda berperan sebagai **analis berita dan fakta** yang mampu mengidentifikasi hoaks, misinformasi, dan konten valid. "
        "Tugas Anda adalah membaca dan mengevaluasi teks berita di bawah ini, lalu mengklasifikasikannya ke dalam salah satu dari empat kategori berikut:\n\n"
        
        "1. **Hoax** – Informasi sepenuhnya salah, tidak berbasis fakta, dan bertujuan menyesatkan.\n"
        "2. **Clickbait** – Judul bersifat sensasional atau provokatif, tetapi isi tidak sesuai atau sangat mengecewakan ekspektasi.\n"
        "3. **Misleading** – Terdapat unsur fakta, tetapi konteksnya disalahgunakan, diputarbalikkan, atau disajikan secara menyesatkan.\n"
        "4. **Valid** – Informasi faktual, akurat, didukung oleh bukti, dan tidak menyesatkan.\n\n"
        
        "**Panduan untuk analisis:**\n"
        "- Periksa fakta dan konteks isi berita secara menyeluruh.\n"
        "- Jangan menyimpulkan 'hoax' hanya karena topiknya tidak populer atau terdengar tidak biasa.\n"
        "- Anda boleh mempertimbangkan referensi atau sumber terpercaya seperti media arus utama, jurnal resmi, atau lembaga pemeriksa fakta.\n"
        "- Fokus pada isi konten, bukan opini atau gaya penulisan semata.\n\n"

        "**Format output yang diharapkan:**\n"
        "Kategori: (Hoax / Clickbait / Misleading / Valid)\n"
        "Penjelasan: (Objektif, ringkas, berdasarkan isi berita dan data faktual)\n"
        "Confidence Score: (Nilai keyakinan dalam persen, antara 0% hingga 100%)\n\n"

        f"Teks Berita:\n{teks_berita}"
    )

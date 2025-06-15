from datetime import datetime

def prompt(teks_berita: str) -> str:
    # tanggal = datetime.now().strftime("%d %B %Y")

    return (
        "Tugas kamu adalah menganalisis isi berita di bawah ini dan mengklasifikasikannya secara akurat ke salah satu dari empat kategori berikut:\n\n"
        "1. **Hoax**: Informasi sepenuhnya palsu, tidak berdasarkan fakta, dan sengaja dibuat untuk menipu atau menyesatkan publik.\n"
        "2. **Clickbait**: Judul dibuat sensasional atau bombastis untuk menarik klik, tapi isi berita tidak sebanding, tidak sesuai dengan judul atau konteks, atau dilebih-lebihkan.\n"
        "3. **Misleading**: Mengandung unsur kebenaran, tetapi disampaikan dengan cara yang membingungkan, mengaburkan konteks, atau membuat pembaca salah paham.\n"
        "4. **Valid**: Berita akurat, faktual, dan tidak mengandung unsur penyesatan atau manipulasi.\n\n"
        "**Catatan penting:** Jangan langsung menyimpulkan berita sebagai hoax hanya karena terdengar aneh, tidak menyertakan sumber, atau belum populer. Bacalah secara kritis dan perhatikan konteks isi berita secara menyeluruh. Jika perlu, cari referensi dari sumber berita lain yang membahas topik serupa untuk memperkuat analisis dan klasifikasi kamu.\n\n"
        "Berikan hasil analisis dengan format seperti ini:\n"
        "Kategori: (Hoax / Clickbait / Misleading / Valid)\n"
        "Penjelasan: (jelaskan alasan secara singkat, objektif, dan faktual)\n"
        "Referensi: (jika memungkinkan, berikan sumber atau tautan terpercaya)\n\n"
        "Kalimat yang Menjadi Dasar Klasifikasi: (kutip kalimat yang menurutmu paling berperan dalam keputusan kamu)\n"
        "Confidence Score: (angka keyakinan antara 0 hingga 100 persen)\n\n"
        f"Teks Berita:\n{teks_berita}"
    )

from prompts import prompt
from gemini_interface import tanya_gemini

uji_data = [
    {
        "label": "Hoax",
        "berita": "Sebuah video yang beredar di YouTube mengklaim bahwa pemerintah diam-diam menyebarkan virus melalui sinyal 5G. Dalam video itu, narator menyebutkan bahwa menara 5G digunakan untuk melemahkan sistem kekebalan tubuh manusia dan menyebarkan penyakit secara masif. Klaim ini sama sekali tidak berdasar dan telah dibantah oleh berbagai lembaga kesehatan dunia, termasuk WHO dan CDC."
    },
    {
        "label": "Misleading",
        "berita": "Sebuah artikel menyatakan bahwa minum air lemon di pagi hari bisa menyembuhkan kanker. Artikel tersebut hanya mengutip satu studi laboratorium terhadap sel kanker tanpa uji klinis pada manusia. Namun, tidak dijelaskan bahwa penelitian itu masih dalam tahap awal dan belum terbukti secara medis. Pembaca bisa salah mengira air lemon adalah pengganti pengobatan medis yang sebenarnya."
    },
    {
        "label": "Valid",
        "berita": "Kementerian Pendidikan dan Kebudayaan secara resmi mengumumkan kebijakan baru terkait Kurikulum Merdeka. Dalam keterangan resminya, kurikulum ini bertujuan memberi fleksibilitas kepada guru dalam menyusun materi ajar sesuai konteks dan kebutuhan murid. Implementasi kurikulum dilakukan bertahap dan telah melalui proses uji coba di beberapa sekolah percontohan."
    },
    {
        "label": "Clickbait",
        "berita": "Anda tidak akan percaya siapa yang memenangkan lomba masak antar RT ini! Ternyata hasilnya benar-benar di luar dugaan semua orang. Artikel tersebut berjudul bombastis, namun isi beritanya hanya mencatat daftar pemenang lomba dan tidak ada kejutan seperti yang dijanjikan pada judul."
    },
    {
        "label": "Hoax",
        "berita": "Sebuah unggahan di Facebook menyebutkan bahwa jika kita menempelkan bawang putih di telinga saat tidur, maka virus flu dan COVID-19 akan hilang dengan sendirinya. Unggahan tersebut menyebar luas tanpa referensi ilmiah, dan metode yang disebutkan tidak memiliki dasar medis apapun."
    },
    {
        "label": "Misleading",
        "berita": "Sebuah media online memberitakan bahwa vaksin flu menyebabkan autisme pada anak-anak. Namun, tidak dijelaskan bahwa studi yang mereka kutip sudah lama dibantah dan ditarik dari jurnal ilmiah. Artikel ini membuat pembaca salah paham dan takut untuk melakukan vaksinasi yang sebenarnya penting."
    },
    {
        "label": "Valid",
        "berita": "Bank Indonesia mengumumkan kenaikan suku bunga acuan sebesar 25 basis poin dalam upaya menahan laju inflasi. Keputusan ini diambil setelah mempertimbangkan kondisi global dan nilai tukar rupiah yang fluktuatif. Informasi disampaikan melalui konferensi pers resmi dan tercantum dalam situs BI."
    },
    {
        "label": "Clickbait",
        "berita": "Pria Ini Mengubah Hidupnya Hanya dengan Satu Kebiasaan Setiap Pagi! Simak Rahasianya di Sini! Setelah diklik, artikel hanya berisi tips umum seperti bangun lebih awal dan minum air putih, yang tidak seheboh klaim judulnya."
    },
    {
        "label": "Hoax",
        "berita": "Beredar informasi di grup WhatsApp bahwa mengonsumsi soda dengan mentimun dapat membunuh sel kanker dalam waktu 24 jam. Pesan itu mengklaim metode ini ditemukan oleh ilmuwan Jepang, tetapi tidak ada bukti ilmiah atau publikasi yang mendukungnya. Ini adalah klaim palsu yang menyesatkan."
    },
    {
        "label": "Valid",
        "berita": "Presiden Joko Widodo meresmikan jalan tol baru yang menghubungkan daerah Kalikuto hingga Batang. Dalam sambutannya, beliau menyatakan bahwa tol ini akan mempersingkat waktu tempuh antar kota dan mendukung distribusi logistik nasional. Acara peresmian diliput langsung oleh media nasional dan dihadiri oleh beberapa menteri terkait."
    }
]


total = len(uji_data)
benar = 0

for i, data in enumerate(uji_data):
    prompt_ = prompt(data['berita'])
    hasil = tanya_gemini(prompt_)
    
    print(f"Uji {i+1}:")
    print("label sebenarnya:", data['label'])
    print("hasil klasifikasi:", hasil)
    
    if data['label'].lower() in hasil.lower():
        benar += 1
        print("Hasil: BENAR")
    else:
        print("Hasil: SALAH")
    print("-" * 50)
    
print(f"Total: {total}, Benar: {benar}, Akurasi: {benar / total * 100:.2f}%")
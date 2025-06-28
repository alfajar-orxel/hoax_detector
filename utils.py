from newspaper import Article
import shutil
from bs4 import BeautifulSoup
import requests
import traceback
import os
import tempfile

def bersihkan_folder_temp_newspaper():
    """
    Bersihkan dan pastikan direktori .newspaper_scraper tersedia.
    """
    temp_dir = tempfile.gettempdir()
    scraper_path = os.path.join(temp_dir, '.newspaper_scraper')
    article_path = os.path.join(scraper_path, 'article_resources')

    if os.path.exists(scraper_path):
        try:
            shutil.rmtree(scraper_path)
        except Exception as e:
            print("Gagal menghapus folder:", e)

    try:
        os.makedirs(article_path, exist_ok=True)
    except Exception as e:
        print("Gagal membuat ulang folder:", e)

def ekstrak_teks(url):
    try:

        bersihkan_folder_temp_newspaper()

        article = Article(url)
        article.download_state = 0
        article.set_html('')
        article.config.request_headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/114.0.0.0 Safari/537.36'
            )
        }
        article.download()
        article.parse()

        if not article.text or len(article.text.strip()) < 100:
            raise ValueError("Isi artikel terlalu pendek, gunakan fallback.")

        return article.title + "\n\n" + article.text.strip()

    except Exception as e:
        try:
  
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/114.0.0.0 Safari/537.36'
                )
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, 'html.parser')
            paragraphs = soup.find_all('p')

            isi = "\n".join([
                p.get_text(strip=True)
                for p in paragraphs
                if len(p.get_text(strip=True)) > 10
            ])

            title = soup.title.string.strip() if soup.title and soup.title.string else "Judul Tidak Ditemukan"

            if not isi:
                raise ValueError("Tidak ditemukan paragraf yang cukup panjang.")

            return title + "\n\n" + isi.strip()

        except Exception as e2:
            print("Gagal ekstrak teks dari URL:", e2)
            traceback.print_exc()
            return "Gagal mengekstrak teks dari URL. Pastikan URL valid dan dapat diakses."

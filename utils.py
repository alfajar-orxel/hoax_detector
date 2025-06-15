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
        return article.title + "\n\n" + article.text
    except Exception as e:
        try:
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/114.0.0.0 Safari/537.36'
                )
            }
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            paragraphs = soup.find_all('p')
            isi = "\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 40])
            
            title = soup.title.string if soup.title else "Berita Tanpa Judul"
            return title + "\n\n" + isi.strip()
        except Exception as e2:
            print("Gagal ekstrak teks dari URL:", e2)
            traceback.print_exc()
            return "Gagal mengekstrak teks dari URL. Pastikan URL valid dan dapat diakses.  {traceback.format_exc()}"
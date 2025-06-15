def cari_Ref_Berita(query: str, jumlah: int = 3) -> list:
    """
    Prioritaskan pencarian dari Kominfo atau Turnbackhoax,
    jika tidak ditemukan, lanjutkan dengan pencarian umum.
    """
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    def google_search(q):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": q,
            "num": jumlah
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            {"title": item["title"], "link": item["link"]}
            for item in data.get("items", [])
        ]
    try:
        query_kominfo = f"{query} site:turnbackhoax.id OR site:kominfo.go.id"
        hasil_prioritas = google_search(query_kominfo)
        if hasil_prioritas:
            return hasil_prioritas
    except Exception as e:
        print("Gagal cari dari Kominfo:", e)

    try:
        return google_search(query)
    except Exception as e:
        return [{"title": "Gagal mencari referensi berita", "link": str(e)}]

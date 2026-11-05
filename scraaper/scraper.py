import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# ====== UBAH SESUAI WEB ======
BASE_URL = "https://otakudesu.blog"
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 15
DEBUG = False   # True = tampilkan langkah penelusuran video (buat cek kalau gagal)
MAX_DEPTH = 4  # maksimal kedalaman iframe


def _get(url, **kwargs):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def cari_anime(judul):
    """Return list of {'judul':..., 'url':...}"""
    soup = _get(f"{BASE_URL}/", params={"s": judul, "post_type": "anime"})
    hasil = []
    # TODO: sesuaikan selector dengan HTML hasil pencarian
    for a in soup.select("ul.chivsrc li h2 a"):
        hasil.append({"judul": a.get_text(strip=True), "url": a["href"]})
    return hasil


def list_episode(url_anime):
    """Return list of {'episode':..., 'url':...}"""
    soup = _get(url_anime)
    hasil = []
    # TODO: sesuaikan selector daftar episode
    for a in soup.select("div.episodelist ul li span a"):
        hasil.append({"episode": a.get_text(strip=True), "url": a["href"]})
    return hasil


# Pola link video akhir (googlevideo / blogger / mp4 langsung)
POLA_VIDEO = [
    r'https?://[^\s"\'<>\\]+googlevideo\.com/videoplayback[^\s"\'<>\\]*',
    r'https?://(?:www\.)?blogger\.com/video-play\.mp4[^\s"\'<>\\]*',
    r'https?://[^\s"\'<>\\]+\.mp4[^\s"\'<>\\]*',
]


def _log(*args):
    if DEBUG:
        print("  [debug]", *args)


def _bersihkan(teks):
    """Di dalam JS, link sering ditulis dengan escape (\\u0026, \\/, &amp;)."""
    return (teks.replace("\\u0026", "&").replace("\\u003d", "=")
                .replace("\\/", "/").replace("&amp;", "&"))


def _cari_video(teks):
    teks = _bersihkan(teks)
    for pola in POLA_VIDEO:
        m = re.search(pola, teks)
        if m:
            return m.group(0)
    return None


def ikuti_redirect(url, referer=None):
    """Ikuti redirect sampai URL akhir. Return (url_akhir, rantai_url)."""
    headers = dict(HEADERS)
    if referer:
        headers["Referer"] = referer
    r = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True, allow_redirects=True)
    rantai = [h.url for h in r.history] + [r.url]
    r.close()  # stream=True: video tidak ikut terunduh
    return r.url, rantai


def _telusuri(url, referer, depth):
    """Buka url, cari link video. Kalau tidak ada, masuk ke iframe di dalamnya."""
    if depth > MAX_DEPTH:
        return None
    _log(f"buka (level {depth}):", url[:100])

    headers = dict(HEADERS)
    if referer:
        headers["Referer"] = referer
    r = requests.get(url, headers=headers, timeout=TIMEOUT)
    r.raise_for_status()

    video = _cari_video(r.text)
    if video:
        _log("ketemu link video:", video[:100])
        return video, url

    soup = BeautifulSoup(r.text, "html.parser")
    for iframe in soup.select("iframe[src]"):
        hasil = _telusuri(urljoin(url, iframe["src"]), url, depth + 1)
        if hasil:
            return hasil
    return None


def ambil_video(url_episode):
    """Membuka browser otomatis untuk melewati proteksi dan mengambil link video akhir."""
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    
    options = Options()
    options.add_argument("--headless")  # Jalankan di latar belakang (ubah jadi non-headless jika ingin lihat)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={UA if 'UA' in globals() else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}")

    driver = webdriver.Chrome(options=options)
    video_url = None
    referer_url = url_episode

    try:
        driver.get(url_episode)
        time.sleep(3)  # Beri waktu iframe/JavaScript termuat sempurna
        
        # Cari elemen video atau iframe yang memuat video
        frames = driver.find_elements("tag name", "iframe")
        for frame in frames:
            src = frame.get_attribute("src")
            if src:
                driver.get(src)
                time.sleep(2)
        
        # Ambil sumber video atau cari pola video dari halaman aktif
        page_source = driver.page_source
        video_url = _cari_video(page_source)
        
    except Exception as e:
        print(f"Gagal mengambil via browser: {e}")
    finally:
        driver.quit()

    return video_url, referer_url
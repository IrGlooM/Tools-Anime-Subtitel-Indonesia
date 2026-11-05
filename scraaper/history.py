import json
import os
from datetime import datetime

FILE_RIWAYAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")


def load():
    if not os.path.exists(FILE_RIWAYAT):
        return []
    try:
        with open(FILE_RIWAYAT, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save(data):
    with open(FILE_RIWAYAT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def tambah(judul, episode, url):
    """Simpan riwayat. Kalau anime+episode sama sudah ada, cukup update waktunya."""
    data = load()
    data = [d for d in data if not (d["judul"] == judul and d["episode"] == episode)]
    data.insert(0, {
        "judul": judul,
        "episode": episode,
        "url": url,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save(data[:100])  # simpan maksimal 100 terakhir


def hapus_semua():
    save([])
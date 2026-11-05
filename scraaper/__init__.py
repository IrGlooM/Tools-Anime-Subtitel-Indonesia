"""Package scraaper: cari anime, pilih episode, riwayat tontonan, dan putar di mpv."""

import os

from .scraper import cari_anime, list_episode, ambil_video
from .history import load as muat_riwayat
from .history import tambah as tambah_riwayat
from .history import hapus_semua as hapus_riwayat
from .player import putar


def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def _pilih(items, label):
    """Tampilkan list bernomor, return item yang dipilih atau None."""
    for i, item in enumerate(items, 1):
        print(f"{i}. {item[label]}")
    print("0. Kembali")
    try:
        n = int(input("\nPilih :"))
    except ValueError:
        return None
    if 1 <= n <= len(items):
        return items[n - 1]
    return None


def _tonton(judul, episode, url):
    """Ambil link video, simpan ke riwayat, lalu putar di mpv."""
    print("\nMengambil link video...")
    video, referer = ambil_video(url)
    if not video:
        print("\nVideo Tidak Ditemukan")
        input("\nEnter...")
        return False

    tambah_riwayat(judul, episode, url)
    putar(video, f"{judul} - {episode}", referer)
    return True


def cari(judul):
    """Alur: cari judul -> pilih anime -> pilih episode -> putar (bisa lanjut episode lain)."""
    judul = judul.strip()
    if not judul:
        return

    try:
        print("\nMencari judul...")
        hasil = cari_anime(judul)
        if not hasil:
            print("\nAnime Tidak Ditemukan")
            input("\nEnter...")
            return

        _clear()
        print(f"Hasil pencarian : {judul}\n")
        anime = _pilih(hasil, "judul")
        if not anime:
            return

        print("\nMengambil daftar episode...")
        episodes = list_episode(anime["url"])
        if not episodes:
            print("\nEpisode Tidak Ditemukan")
            input("\nEnter...")
            return

        # setelah nonton, kembali ke daftar episode (0 = keluar)
        while True:
            _clear()
            print(f"{anime['judul']}\n")
            eps = _pilih(episodes, "episode")
            if not eps:
                return
            _tonton(anime["judul"], eps["episode"], eps["url"])

    except Exception as e:
        print(f"\nTerjadi Error : {e}")
        input("\nEnter...")


def riwayat():
    """Tampilkan riwayat tontonan. Pilih nomor untuk menonton lagi."""
    while True:
        _clear()
        data = muat_riwayat()
        if not data:
            print("Belum ada riwayat tontonan.")
            input("\nEnter...")
            return

        print("=" * 40)
        print("      Riwayat Tontonan")
        print("=" * 40)
        for i, d in enumerate(data, 1):
            print(f"{i}. {d['judul']} - {d['episode']}  ({d['waktu']})")
        print("\nNomor = tonton lagi | h = hapus semua | 0 = kembali")
        pilih = input("\nPilih :").strip().lower()

        if pilih == "0":
            return
        if pilih == "h":
            hapus_riwayat()
            continue
        if pilih.isdigit() and 1 <= int(pilih) <= len(data):
            d = data[int(pilih) - 1]
            try:
                # link video diambil ulang karena cepat kedaluwarsa
                _tonton(d["judul"], d["episode"], d["url"])
            except Exception as e:
                print(f"\nTerjadi Error : {e}")
                input("\nEnter...")


__all__ = [
    "cari",
    "riwayat",
    "cari_anime",
    "list_episode",
    "ambil_video",
    "muat_riwayat",
    "tambah_riwayat",
    "hapus_riwayat",
    "putar",
]
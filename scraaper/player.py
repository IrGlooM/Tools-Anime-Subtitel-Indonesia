import os
import shutil
import subprocess

# Kalau mpv ada di tempat lain, isi alamatnya di sini. Contoh:
# MPV_PATH = r"D:\Tools\mpv\mpv.exe"
MPV_PATH = ""

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

_FOLDER_INI = os.path.dirname(os.path.abspath(__file__))   # folder scraaper
_FOLDER_ROOT = os.path.dirname(_FOLDER_INI)                # folder main.py
LOG = os.path.join(_FOLDER_ROOT, "mpv_log.txt")


def _kandidat():
    """Daftar lokasi mpv yang dicek berurutan."""
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    local = os.environ.get("LOCALAPPDATA", "")
    home = os.path.expanduser("~")

    return [
        MPV_PATH,
        # di luar program (satu folder dengan project)
        os.path.join(_FOLDER_ROOT, "mpv.exe"),
        os.path.join(_FOLDER_ROOT, "mpv", "mpv.exe"),
        os.path.join(_FOLDER_INI, "mpv", "mpv.exe"),
        # Program Files biasa dan x86
        os.path.join(pf, "mpv", "mpv.exe"),
        os.path.join(pf86, "mpv", "mpv.exe"),
        # hasil install winget / scoop / chocolatey
        os.path.join(local, "Microsoft", "WinGet", "Links", "mpv.exe"),
        os.path.join(home, "scoop", "apps", "mpv", "current", "mpv.exe"),
        r"C:\ProgramData\chocolatey\bin\mpv.exe",
        r"C:\mpv\mpv.exe",
    ]


def cari_mpv():
    """Return alamat mpv, atau None kalau tidak ketemu."""
    path = shutil.which("mpv")
    if path:
        return path
    for p in _kandidat():
        if p and os.path.isfile(p):
            return p
    return None


def _uji_link(url, referer):
    """Tes link dari Python dan tampilkan status HTTP-nya (membantu cari penyebab gagal)."""
    try:
        import requests
    except ImportError:
        return

    kombinasi = {"tanpa referer": {}}
    if referer:
        kombinasi["dengan referer"] = {"Referer": referer}

    print("\nUji link dari Python:")
    for nama, h in kombinasi.items():
        try:
            r = requests.get(
                url,
                headers={"User-Agent": UA, "Range": "bytes=0-1023", **h},
                timeout=15, stream=True,
            )
            print(f"  [{nama}] -> status {r.status_code}, tipe {r.headers.get('content-type', '?')}")
            r.close()
        except Exception as e:
            print(f"  [{nama}] -> gagal: {e}")


def _tampilkan_error_log():
    try:
        with open(LOG, encoding="utf-8", errors="ignore") as f:
            baris = [b for b in f if "][e]" in b or "][w]" in b or "][f]" in b]
        print("\nError/peringatan mpv:")
        print("".join(baris[-15:]) or "(tidak ada baris error di log)")
    except OSError:
        pass


def putar(url, judul="", referer=None):
    """Putar video langsung di mpv. Tidak membuka browser."""
    mpv = cari_mpv()
    if not mpv:
        print("\nmpv tidak ditemukan.")
        print("Taruh mpv di salah satu tempat ini:")
        print("  - C:\\Program Files\\mpv\\mpv.exe")
        print("  - C:\\Program Files (x86)\\mpv\\mpv.exe")
        print(f"  - {os.path.join(_FOLDER_ROOT, 'mpv', 'mpv.exe')}  (di folder project)")
        print("atau isi MPV_PATH di scraaper/player.py")
        input("\nEnter...")
        return

    perintah = [
        mpv,
        "--no-config",
        "--idle=no",        # kalau gagal, mpv tutup sendiri
        "--ytdl=no",        # link sudah langsung, tidak lewat yt-dlp
        f"--log-file={LOG}",
        f"--force-media-title={judul}",
        f"--user-agent={UA}",
    ]
    if referer:
        perintah.append(f"--referrer={referer}")
    perintah.append(url)

    print(f"\nMemutar : {judul}")
    print(f"Link    : {url[:90]}{'...' if len(url) > 90 else ''}\n")

    hasil = subprocess.run(perintah)

    if hasil.returncode != 0:
        print(f"\nmpv gagal memutar (kode {hasil.returncode}).")
        _tampilkan_error_log()
        _uji_link(url, referer)
        print("\nLink lengkap:")
        print(url)
        input("\nEnter...")
# Ani-Cli Terminal (Tools Streaming Anime Indo)

Aplikasi berbasis *Command Line Interface* (CLI) ringan menggunakan Python untuk mencari, mengelola riwayat tontonan, dan memutar *streaming* anime secara langsung melalui **mpv player** tanpa terganggu iklan.

---

## Fitur Utama

- **Pencarian Anime**: Mencari judul anime langsung dari sumber *streaming* pilihan.
- **Manajemen Episode**: Memilih daftar episode secara mudah dengan navigasi interaktif.
- **Riwayat Tontonan (`history.json`)**: Menyimpan riwayat episode terakhir yang ditonton lengkap dengan timestamp, serta opsi hapus riwayat.
- **Pemutar Otomatis (`mpv`)**: Integrasi mulus dengan *mpv media player* untuk pemutaran video yang stabil.
- **Ekstraksi Video Headless**: Menggunakan Selenium di latar belakang untuk melewati proteksi iframe dan mengekstrak link video langsung.

---

## Prasyarat (Requirements)

Sebelum menjalankan aplikasi ini, pastikan sistem kamu sudah terinstal:

1. **Python** versi 3.8 atau yang lebih baru.
2. **Git** untuk *cloning* repositori.
3. **Mpv Media Player**:
   - Install **mpv** di sistem kamu.
   - Atau letakkan berkas `mpv.exe` di dalam folder proyek/folder `scraaper/mpv/`.
4. **Google Chrome** (dibutuhkan oleh Selenium untuk mengekstrak iframe video).

---

## Panduan Instalasi & Penggunaan

### 1. Clone Repositori

Buka terminal (Command Prompt, PowerShell, atau Git Bash) dan jalankan perintah berikut:

```bash
git clone https://github.com/IrGlooM/Ani-Cli.git](https://github.com/IrGlooM/Tools-Anime-Subtitel-Indonesia
cd Tools-Anime-Subtitel-Indonesia
```

### 2. Buat dan Aktifkan Virtual Environment (`.venv`) *(Opsional tapi Disarankan)*

Menggunakan *virtual environment* disarankan agar paket/library proyek ini tidak mengotori instalasi Python utama di sistem kamu.

**Membuat environment:**
```bash
python -m venv .venv
```

**Mengaktifkan environment:**
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Linux / macOS / Git Bash:**
  ```bash
  source .venv/bin/activate
  ```

*(Setelah diaktifkan, tanda `(.venv)` akan muncul di baris perintah terminal kamu).*

### 3. Install Dependencies

Install seluruh pustaka yang dibutuhkan menggunakan `pip`:

```bash
pip install requests beautifulsoup4 selenium
```

### 4. Jalankan Aplikasi

Setelah semua dependencies terinstal dan mpv siap, jalankan aplikasi utama:

```bash
python main.py
```

---

## Struktur Proyek

```text
.
├── main.py              # Entry point utama (UI Terminal & Menu)
├── history.json         # File otomatis untuk menyimpan riwayat tontonan
├── README.md            # Dokumentasi proyek
└── scraaper/            # Modul inti aplikasi
    ├── __init__.py      # Pengendali alur logika utama paket scraaper
    ├── scraper.py       # Logika pencarian anime dan web scraping (Selenium & BS4)
    ├── history.py       # Pengelola pembacaan & penyimpanan riwayat tontonan
    └── player.py        # Deteksi lokasi mpv dan eksekusi pemutar video
```

---

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan penggunaan pribadi.

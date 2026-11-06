# Ani-Cli Terminal (Tools Streaming Anime Indo)

Aplikasi berbasis *Command Line Interface* (CLI) ringan menggunakan Python untuk mencari, mengelola riwayat tontonan, dan memutar *streaming* anime secara langsung melalui **mpv player** tanpa terganggu iklan.

---

## Fitur Utama

- **Pencarian Anime**: Mencari judul anime secara interaktif langsung dari sumber *streaming* pilihan.
- **Manajemen Episode**: Memilih daftar episode secara mudah dengan navigasi interaktif.
- **Riwayat Tontonan (`history.json`)**: Menyimpan riwayat episode terakhir yang ditonton lengkap dengan *timestamp*, serta fitur hapus riwayat.
- **Pemutar Otomatis (`mpv`)**: Integrasi mulus dengan *mpv media player* untuk pemutaran video yang stabil.
- **Ekstraksi Video Headless**: Menggunakan Selenium di latar belakang untuk melewati proteksi *iframe* dan mengekstrak link video langsung.

---

## Prasyarat (Requirements)

Sebelum menjalankan aplikasi ini, pastikan sistem kamu sudah memenuhi prasyarat berikut:

1. **Python** (versi 3.8 atau yang lebih baru).
2. **Git** untuk proses *cloning* repositori.
3. **Mpv Media Player**:
   - Pasang **mpv** di sistem kamu.
   - Atau letakkan berkas `mpv.exe` di dalam folder proyek/folder `scraaper/mpv/`.
4. **Google Chrome / Chromium**:
   - **Windows**: Menggunakan Google Chrome standar yang sudah terpasang di Windows (tidak perlu konfigurasi tambahan).
   - **Linux / WSL**: Memerlukan instalasi Google Chrome versi Linux agar Selenium dapat berjalan di latar belakang.

---

## Panduan Instalasi & Penggunaan

### 1. Clone Repositori

Buka terminal (PowerShell di Windows, atau Terminal di Linux/macOS) lalu jalankan perintah berikut:

```bash
git clone https://github.com/IrGlooM/Tools-Anime-Subtitel-Indonesia
cd Tools-Anime-Subtitel-Indonesia
```

---

### 2. Buat dan Aktifkan Virtual Environment (`.venv`)

Sangat disarankan menggunakan *virtual environment* (`.venv`) agar semua *library* Python tersimpan terisolasi di dalam proyek ini dan tidak mengotori instalasi Python utama sistem kamu.

#### A. Membuat Virtual Environment
```bash
python -m venv .venv
```

#### B. Mengaktifkan Virtual Environment

- **Windows (PowerShell - Direkomendasikan):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  *(Jika muncul error terkait execution policy di PowerShell, jalankan sekali: `Set-ExecutionPolicy Unrestricted -Scope Process`)*

- **Windows (Command Prompt / CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS / WSL (Git Bash):**
  ```bash
  source .venv/bin/activate
  ```

*(Setelah diaktifkan, indikator `(.venv)` akan muncul di baris awal terminal kamu).*

---

### 3. Install Dependencies

Setelah `.venv` aktif, install seluruh pustaka yang dibutuhkan menggunakan berkas `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Jalankan Aplikasi

Setelah seluruh *dependencies* terpasang dan `mpv` siap, jalankan aplikasi utama:

```bash
python main.py
```

---

## Catatan Penting & Troubleshooting (Khusus Pengguna WSL / Linux)

Bagi pengguna yang menjalankan aplikasi ini di lingkungan **WSL (Windows Subsystem for Linux)** atau **Linux Native**, harap perhatikan beberapa hal berikut agar program tidak mengalami *hang* atau berhenti tanpa pesan *error*:

### A. Pengguna Windows Native
- **Tidak perlu install Chrome manual lewat terminal.** Selenium akan otomatis mendeteksi instalasi Google Chrome yang ada di sistem Windows kamu.

### B. Pengguna Linux / WSL (Instalasi Chrome Khusus Linux)
Jika dijalankan di WSL/Linux dan muncul masalah *hang* pada pesan **"Mengambil link video..."**, itu menandakan Selenium tidak menemukan biner Google Chrome Linux di dalam lingkungan WSL kamu.

Jalankan perintah ini di terminal WSL untuk mengunduh dan menginstal Google Chrome versi Linux:

```bash
sudo apt update && sudo apt install wget -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

### C. Penanganan Pemutar Video (`mpv`) di WSL
- Pastikan `mpv` sudah terpasang di lingkungan Linux/WSL:
  ```bash
  sudo apt install mpv
  ```
- Pastikan kamu menggunakan WSL2 di Windows 11 / Windows 10 (dengan dukungan WSLg) agar jendela GUI `mpv` dapat tampil di layar.

---

## Struktur Proyek

```text
.
├── main.py              # Entry point utama (UI Terminal & Menu Navigasi)
├── history.json         # Berkas otomatis untuk menyimpan riwayat tontonan
├── requirements.txt     # Daftar dependensi library Python
├── README.md            # Dokumentasi lengkap proyek
└── scraaper/            # Modul inti aplikasi
    ├── __init__.py      # Pengendali alur logika utama paket scraaper
    ├── scraper.py       # Logika pencarian anime dan web scraping (Selenium & BS4)
    ├── history.py       # Pengelola pembacaan & penyimpanan riwayat tontonan
    └── player.py        # Deteksi lokasi mpv dan eksekusi pemutar video
```

---

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan penggunaan pribadi.

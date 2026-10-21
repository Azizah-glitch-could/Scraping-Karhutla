# Project Scraping Data Karhutla via Python API

Repository ini berisi project scraping data media sosial terkait isu Karhutla (Kebakaran Hutan dan Lahan) di Indonesia. Project ini dibuat untuk memenuhi tugas mata kuliah Analisis Media Sosial dengan memanfaatkan API serta pemrosesan data menggunakan Python.

---

## 1. Deskripsi Project
* Topik: Karhutla (Kebakaran Hutan dan Lahan) dan Kabut Asap di Indonesia.
* Tujuan: Mengumpulkan data teks percakapan dan berita publik mengenai Karhutla untuk analisis sentimen dan isu lingkungan.
* Target Data: Minimum 1.000 baris dataset bersih siap analisis.
* Metode: Pengambilan data otomatis menggunakan script Python berbasis API.

---

## 2. Struktur Repository

| Nama File / Folder | Keterangan |
| :--- | :--- |
| data_karhutla_final.csv | Dataset utama hasil scraping (>1.000 baris data Karhutla bersih). |
| apify_scraper.py | Script Python utama untuk menjalankan request API scraping. |
| config.py | File konfigurasi token API dan parameter pencarian. |
| .gitattributes | Konfigurasi Git LFS untuk pengelolaan file dataset berukuran besar. |
| README.md | Dokumentasi lengkap project. |

---

## 3. Ringkasan Dataset
Dataset disimpan dalam format CSV (data_karhutla_final.csv) dengan atribut data sebagai berikut:
* tweet_id / id: Identifikasi unik tiap postingan/tweet.
* text / full_text: Isi pesan atau postingan masyarakat mengenai Karhutla.
* author_handle / author_name: Nama pengguna / pembuat postingan.
* created_at / timestamp: Waktu postingan dibuat.
* metrics: Jumlah interaksi (like, retweet, atau komentar).

---

## 4. Panduan Menjalankan Script (How to Run)

### Prasyarat (Prerequisites)
* Python 3.10+
* Visual Studio Code / Terminal
* Git LFS (Large File Storage)

### Langkah-Langkah:
1. Clone Repository Ini:
   git clone https://github.com/Azizah-glitch-could/Scraping-Karhutla.git
   cd Scraping-Karhutla

2. Aktifkan Virtual Environment & Install Library:
   # Di Windows (PowerShell)
   .\envku\Scripts\Activate.ps1
   
   # Install dependencies
   pip install pandas requests apify-client

3. Jalankan Script Scraper:
   python apify_scraper.py

---

## Kelompok 5
* 1. Nur Asizah.S (240907501032)
* 2. Hilda Selfianti (240907500021)
* 3. Hasrah Tazkia (240907502034)
* Program Studi: Bisnis Digital
* Fakultas: Ekonomi dan Bisnis, Universitas Negeri Makassar
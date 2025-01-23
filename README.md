# 📱 Play Store Scraper 🛠️

**Play Store Scraper** adalah aplikasi GUI berbasis Python yang memungkinkan pengguna untuk melakukan scraping data aplikasi dan review dari Google Play Store. Aplikasi ini menggunakan library `google-play-scraper` untuk mengambil data dan `matplotlib` untuk visualisasi data. Aplikasi ini juga dilengkapi dengan fitur untuk menyimpan data ke dalam file CSV. 🚀

---

## 🌟 Fitur

- **🔍 Pencarian Aplikasi**: Mencari aplikasi berdasarkan judul.
- **📥 Input ID Aplikasi**: Memasukkan ID aplikasi secara manual.
- **📊 Scraping Review**: Mengambil review dari aplikasi yang dipilih.
- **📈 Visualisasi Data**:
  - Distribusi rating.
  - Rata-rata rating berdasarkan waktu.
  - Word cloud dari konten review.
- **💾 Simpan Data**: Menyimpan data review ke dalam file CSV.

---

## 🛠️ Instalasi

1. **Clone Repository**:
   ```bash
   git clone https://github.com/bayusegara27/playstore-scraper.git
   cd playstore-scraper
   ```

2. **Install Dependencies**:
   Pastikan Anda telah menginstal Python 3.x dan pip. Kemudian, jalankan perintah berikut untuk menginstal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**:
   Setelah semua dependensi terinstal, jalankan aplikasi dengan perintah berikut:
   ```bash
   python main.py
   ```

---

## 🎮 Penggunaan

1. **Pilih Mode**:
   - **🔍 Search by Title**: Mencari aplikasi berdasarkan judul.
   - **📥 Input ID**: Memasukkan ID aplikasi secara manual.

2. **Pencarian Aplikasi**:
   - Jika memilih mode "Search by Title", masukkan judul aplikasi dan klik "Search".
   - Pilih aplikasi dari daftar yang muncul.

3. **Input Jumlah Review**:
   - Masukkan jumlah review yang ingin diambil dan klik "Scrape".

4. **Analisis Data**:
   - Setelah data review diambil, Anda dapat melihat visualisasi data seperti distribusi rating, rata-rata rating berdasarkan waktu, dan word cloud.
   - Anda juga dapat menyimpan data ke dalam file CSV dengan mengklik "Simpan Data ke CSV".

---

## 🧩 Struktur Kode

- **📄 main.py**: File utama yang berisi kode untuk menjalankan aplikasi.
- **📄 requirements.txt**: Daftar dependensi yang diperlukan untuk menjalankan aplikasi.

---

## 📦 Dependensi

- `tkinter`: Untuk antarmuka pengguna grafis.
- `google-play-scraper`: Untuk mengambil data dari Google Play Store.
- `matplotlib`: Untuk visualisasi data.
- `pandas`: Untuk manipulasi data.
- `wordcloud`: Untuk membuat word cloud dari konten review.
- `ttkthemes`: Untuk tema tambahan pada antarmuka pengguna.

---

## ❗ Kontribusi

Tidak perlu berkontribusi untuk projek ini, karena projek ini digunakan sebagai Ujian Akhir Semester. 🎓

---

## 👨‍💻 Penulis

- **[bayusegara27](https://github.com/bayusegara27)** 🚀

---

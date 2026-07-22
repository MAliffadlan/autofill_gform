# 🤖 Google Form Auto Fill Script

Script Python otomatisasi pengisian Google Form dengan data acak (nama, jenis kelamin, nomor telepon, asal kampus, dan 16 pertanyaan kuisioner skala Likert 1-5).

Dibuat khusus untuk pengujian otomatisasi respons Google Form multi-halaman/section secara cepat dan efisien.

---

## ✨ Fitur Utama

- **Multi-Section Support**: Mengatasi Google Form 2 halaman (Halaman Identitas & Halaman Kuisioner) menggunakan parameter `pageHistory`.
- **Gender-Matched Name Generator**: Nama otomatis disesuaikan dengan jenis kelamin (nama laki-laki untuk *Laki-Laki*, nama perempuan untuk *Perempuan*).
- **Zero External Dependencies**: Menggunakan modul bawaan Python (`urllib`, `re`, `random`), sehingga **tidak perlu `pip install`**.
- **Dynamic Session Token (`fbzx`)**: Secara otomatis mengambil token `fbzx` terbaru dari Google Form untuk memastikan pengiriman valid.
- **Batch Submission**: Dapat melakukan pengiriman secara berulang sesuai jumlah yang ditentukan pengguna.

---

## 📋 Struktur Form yang Dihitung

1. **Halaman 1 (Identitas)**:
   - Nama Lengkap (Random)
   - Jenis Kelamin (Laki-Laki / Perempuan)
   - Nomor Telepon (Random format `08xx`)
   - Asal Kampus (10 Cabang LP3I)

2. **Halaman 2 (Kuisioner Pernyataan)**:
   - 16 Indikator & Sub-Indikator Keamanan Jaringan Linux (Skala 1 - 5)

---

## 🚀 Cara Penggunaan

### 1. Clone Repository
```bash
git clone https://github.com/MAliffadlan/autofill_gform.git
cd autofill_gform
```

### 2. Jalankan Script
```bash
python3 isi_gform.py
```

### 3. Masukkan Jumlah Pengisian
Saat script dijalankan, Anda akan diminta memasukkan jumlah pengisian yang diinginkan:
```text
Mau kirim berapa kali? (default 1): 5
```

---

## 📝 Lisensi
[MIT License](LICENSE) - Bebas digunakan dan dikembangkan.

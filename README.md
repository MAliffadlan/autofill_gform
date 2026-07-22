# 🤖 Google Form Auto Fill Script

Script Python otomatisasi pengisian Google Form dengan data acak realistis (nama, jenis kelamin, nomor telepon, asal kampus, dan 16 pertanyaan kuisioner skala Likert 1-5).

Dibuat khusus untuk pengujian otomatisasi respons Google Form multi-halaman/section secara cepat, tahan eror, dan teratur.

---

## ✨ Fitur Utama

- 📑 **Multi-Section Support**: Mengatasi Google Form 2 halaman (Halaman Identitas & Halaman Kuisioner) menggunakan parameter `pageHistory: '0,1'`.
- 📊 **Distribusi Likert Realistis**: Jawaban kuisioner (skala 1-5) di-generate dengan bobot realistis (dominan 4 dan 5) agar data hasil survei tampak alami.
- 👤 **Gender-Matched Name Generator**: Nama otomatis disesuaikan secara konsisten dengan jenis kelamin (*Laki-Laki* / *Perempuan*).
- 🔄 **Auto-Retry Mechanism**: Otomatis mencoba ulang (*retry*) hingga 3x jika terjadi gangguan jaringan atau respons lambat dengan *exponential backoff*.
- 🌐 **User-Agent Rotation**: Berganti header perangkat secara acak (Android, iPhone, Windows, Mac, Linux) di tiap pengiriman agar tidak terdeteksi sebagai bot tunggal.
- 📈 **Terminal Progress Bar**: Menampilkan indikator status dan progress bar visual secara *real-time* di Terminal.
- ⏱️ **Random Delay**: Memberikan jeda acak 1.0 - 2.5 detik antar pengiriman untuk mencegah *rate limiting*.
- 📦 **Zero External Dependencies**: Dibuat menggunakan modul bawaan standar Python (`urllib`, `re`, `random`, `time`, `sys`), sehingga **tidak perlu `pip install`**.

---

## 📋 Struktur Form yang Didukung

1. **Halaman 1 (Identitas Responden)**:
   - **Nama Lengkap** (Random kombinasi 50+ nama depan & belakang)
   - **Jenis Kelamin** (Laki-Laki / Perempuan - terintegrasi dengan nama)
   - **Nomor Telepon** (Random format provider Indonesia `08xx`)
   - **Asal Kampus** (10 Cabang LP3I)

2. **Halaman 2 (Kuisioner Pernyataan)**:
   - **16 Indikator & Sub-Indikator** Efektivitas Linux Native (Skala Likert 1 - 5)

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

### 3. Tentukan Jumlah Pengiriman
Saat script dijalankan, Anda akan diminta memasukkan jumlah pengisian yang diinginkan:
```text
Mau kirim berapa kali? (default 1): 10

=== Mengirim 10x Data RANDOM (Auto-Retry Enabled) ke Google Form LP3I ===

#1:  [+] Ahmad Pratama | Laki-Laki | 081298471029 | Lp3i Jakarta Pusat
      Jawaban: 4,5,3,4,5,4,4,5,3,4,4,5,4,3,4,5
Progress: [█████████████████████████] 100% (1/10)
...
=== Selesai! 10/10 berhasil terkirim ===
```

---

## 📝 Lisensi
[MIT License](LICENSE) - Bebas digunakan dan dikembangkan.

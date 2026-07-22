# Google Form Auto Fill Script

Script Python untuk otomatisasi pengisian data pada Google Form multi-halaman/section secara terstruktur dengan generasi data acak yang realistis.

Dibuat untuk keperluan pengujian dan otomatisasi pengisian survei/kuesioner berbasis Google Form.

---

## Fitur Utama

- **Dukungan Multi-Section**: Mengisi data pada Google Form 2 halaman (Identitas dan Kuesioner) menggunakan parameter `pageHistory`.
- **Generasi Identitas Konsisten**: Penyesuaian nama responden otomatis berdasarkan jenis kelamin (Laki-Laki / Perempuan).
- **Distribusi Jawaban Realistis**: Pengisian kuesioner skala Likert (1 - 5) menggunakan distribusi bobot terarah agar data tetap representatif.
- **Mekanisme Auto-Retry**: Mencoba ulang pengiriman hingga 3 kali secara otomatis apabila terjadi kendala jaringan atau kegagalan koneksi.
- **Rotasi User-Agent**: Mengganti header browser/perangkat secara acak pada setiap permintaan untuk mensimulasikan akses dari berbagai perangkat.
- **Indikator Progres**: Menampilkan status pengiriman dan progress bar pada terminal secara real-time.
- **Jeda Waktu Acak (Random Delay)**: Memberikan jeda waktu acak 1.0 hingga 2.5 detik antar pengiriman untuk menghindari *rate-limiting*.
- **Tanpa Dependensi Eksternal**: Menggunakan modul standar Python (`urllib`, `re`, `random`, `time`, `sys`), sehingga dapat dijalankan tanpa instalasi paket tambahan.

---

## Struktur Form yang Didukung

1. **Halaman 1 (Identitas Responden)**:
   - Nama Lengkap (Kombinasi nama depan dan belakang)
   - Jenis Kelamin (Laki-Laki / Perempuan)
   - Nomor Telepon (Format provider Indonesia `08xx`)
   - Asal Kampus (10 Pilihan Kampus LP3I)

2. **Halaman 2 (Kuesioner Pernyataan)**:
   - 16 Pertanyaan Indikator Pembelajaran Keamanan Jaringan Linux (Skala Likert 1 - 5)

---

## Cara Penggunaan

### 1. Kloning Repository
```bash
git clone https://github.com/MAliffadlan/autofill_gform.git
cd autofill_gform
```

### 2. Menjalankan Script
```bash
python3 isi_gform.py
```

### 3. Memasukkan Jumlah Pengisian
Tentukan jumlah data yang ingin dikirimkan saat diminta pada terminal:
```text
Mau kirim berapa kali? (default 1): 10

=== Mengirim 10x Data RANDOM (Auto-Retry Enabled) ke Google Form LP3I ===

#1:  [+] Ahmad Pratama | Laki-Laki | 081298471029 | Lp3i Jakarta Pusat
      Jawaban: 4,5,3,4,5,4,4,5,3,4,4,5,4,3,4,5
Progress: [█████████████████████████] 100% (1/10)

=== Selesai! 10/10 berhasil terkirim ===
```

---

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

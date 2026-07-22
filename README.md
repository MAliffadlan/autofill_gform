# Google Form Auto Fill & Universal Generator Script

Script Python untuk otomatisasi pengisian Google Form secara terstruktur dengan fitur pembuatan script pengisi form otomatis (*Universal Form Generator*).

Dibuat untuk keperluan pengujian dan otomatisasi pengisian survei/kuesioner berbasis Google Form multi-halaman/section.

---

## Modul Proyek

1. **`setup_form.py` (Universal Generator)**:
   - Menganalisis dan mengekstrak pertanyaan, opsi jawaban, ID entry, dan struktur halaman dari URL Google Form manapun secara otomatis.
   - Meng-generate file script `isi_gform.py` yang siap pakai tanpa perlu konfigurasi manual.

2. **`isi_gform.py` (Auto Fill Engine)**:
   - Eksekutor otomatisasi pengisian data ke Google Form yang telah dikonfigurasi.
   - Dilengkapi fitur auto-retry, rotasi User-Agent, indikator progres terminal, dan jeda acak.

---

## Fitur Utama

- **Universal Form Generator**: Cukup masukkan link Google Form baru, script akan otomatis menyesuaikan struktur form tersebut.
- **Dukungan Multi-Section**: Mengisi data pada Google Form multi-halaman menggunakan parameter `pageHistory`.
- **Generasi Identitas Konsisten**: Penyesuaian nama responden otomatis berdasarkan jenis kelamin (Laki-Laki / Perempuan).
- **Distribusi Jawaban Realistis**: Pengisian kuesioner skala Likert (1 - 5) menggunakan distribusi bobot terarah.
- **Mekanisme Auto-Retry**: Mencoba ulang pengiriman hingga 3 kali secara otomatis apabila terjadi kendala jaringan.
- **Rotasi User-Agent**: Mengganti header browser/perangkat secara acak pada setiap permintaan.
- **Indikator Progres**: Menampilkan status pengiriman dan progress bar pada terminal secara real-time.
- **Tanpa Dependensi Eksternal**: Menggunakan modul standar Python (`urllib`, `re`, `random`, `time`, `sys`, `json`).

---

## Cara Penggunaan

### 1. Kloning Repository
```bash
git clone https://github.com/MAliffadlan/autofill_gform.git
cd autofill_gform
```

### 2. Mengkonfigurasi Form Baru (Jika Menggunakan Form Baru)
Jalankan script generator dan masukkan URL Google Form baru Anda:
```bash
python3 setup_form.py https://forms.gle/XXXXXX
```
Script akan menganalisis form dan secara otomatis membuat/memperbarui file `isi_gform.py`.

### 3. Menjalankan Otomatisasi Pengisian
Jalankan script eksekutor `isi_gform.py`:
```bash
python3 isi_gform.py
```

Tentukan jumlah data yang ingin dikirimkan saat diminta pada terminal:
```text
Mau kirim berapa kali? (default 1): 10

=== Mengirim 10x Data ke Google Form ===

Progress: [█████████████████████████] 100% (10/10)

=== Selesai! 10/10 berhasil terkirim ===
```

---

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

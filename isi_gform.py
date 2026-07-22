import urllib.request
import urllib.parse
import re
import random
import string
import time

FORM_VIEW_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc1GdRi9CL90AetRzRjf2UCwIkZS8HQ8q90Un2Mjk02fSkFfA/viewform"
FORM_POST_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc1GdRi9CL90AetRzRjf2UCwIkZS8HQ8q90Un2Mjk02fSkFfA/formResponse"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
]

# ==========================================
# DATA RANDOM (Nama Cowok & Cewek Dipisah)
# ==========================================
NAMA_DEPAN_COWOK = [
    "Ahmad", "Muhammad", "Rizki", "Dimas", "Andi", "Budi", "Fajar", "Gilang",
    "Hendra", "Irfan", "Joko", "Kevin", "Lutfi", "Naufal", "Oka", "Putra",
    "Rafi", "Satria", "Taufik", "Yoga", "Zainal", "Arif", "Bayu", "Cahyo",
    "Deni", "Eko", "Faisal", "Galih", "Hafiz", "Ivan", "Rian", "Surya",
    "Agus", "Wahyu", "Ridwan", "Ilham", "Yusuf", "Rizal", "Farhan", "Aditya",
]

NAMA_DEPAN_CEWEK = [
    "Siti", "Nur", "Dewi", "Ayu", "Putri", "Rina", "Dian", "Fitri",
    "Mega", "Nisa", "Indah", "Lestari", "Wulan", "Ratna", "Sari", "Tika",
    "Yuni", "Zahra", "Anisa", "Bella", "Citra", "Eka", "Fadila", "Gita",
    "Intan", "Kartika", "Laras", "Maya", "Nabila", "Rahma", "Salma", "Vina",
]

NAMA_BELAKANG_COWOK = [
    "Pratama", "Saputra", "Nugraha", "Hidayat", "Ramadhan", "Kurniawan",
    "Setiawan", "Permana", "Firmansyah", "Hakim", "Putra", "Wijaya",
    "Suryadi", "Maulana", "Fadillah", "Santoso", "Wibowo", "Prasetyo",
    "Harianto", "Susanto", "Syahputra", "Dermawan", "Arifin", "Gunawan",
]

NAMA_BELAKANG_CEWEK = [
    "Rahayu", "Lestari", "Wulandari", "Handayani", "Puspitasari",
    "Anggraeni", "Maharani", "Fitriani", "Kusuma", "Utami",
    "Safitri", "Permatasari", "Oktaviani", "Damayanti", "Setiawati",
    "Nurhaliza", "Rahmawati", "Agustina", "Hartini", "Salsabila",
]

KAMPUS_LIST = [
    "Lp3i Ciputat", "Lp3i Pasar Minggu", "Lp3i Cimone", "Lp3i Depok",
    "Lp3i Cikarang", "Lp3i Jakarta Pusat", "Lp3i Bekasi", "Lp3i Pondok Cabe",
    "Lp3i Jakarta Utara", "Lp3i Tanggerang",
]

def random_identitas():
    """Generate nama, jenis kelamin, dan no HP yang konsisten"""
    jk = random.choice(["Laki-Laki", "Perempuan"])
    if jk == "Laki-Laki":
        nama = random.choice(NAMA_DEPAN_COWOK) + " " + random.choice(NAMA_BELAKANG_COWOK)
    else:
        nama = random.choice(NAMA_DEPAN_CEWEK) + " " + random.choice(NAMA_BELAKANG_CEWEK)
    
    prefix = random.choice(["0812", "0813", "0856", "0857", "0878", "0877", "0838", "0852", "0853", "0896", "0895", "0858", "0815", "0816"])
    hp = prefix + ''.join(random.choices(string.digits, k=random.randint(7, 8)))
    kampus = random.choice(KAMPUS_LIST)
    
    return nama, jk, hp, kampus

def get_fbzx(user_agent):
    try:
        req = urllib.request.Request(FORM_VIEW_URL, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'name="fbzx"\s+value="([^"]+)"', html)
            if match:
                return match.group(1)
    except Exception:
        pass
    return ""

def kirim_jawaban(max_retries=3):
    nama, jk, hp, kampus = random_identitas()
    user_agent = random.choice(USER_AGENTS)
    
    # Generate jawaban kuisioner (cenderung positif 3-5 agar realistis)
    jawaban = [str(random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]) for _ in range(16)]

    for attempt in range(1, max_retries + 1):
        fbzx_token = get_fbzx(user_agent)

        form_data = {
            'fvv': '1',
            'pageHistory': '0,1',
            'fbzx': fbzx_token,

            # Halaman 1: Identitas
            'entry.34848792': nama,
            'entry.809906928': jk,
            'entry.90992771': hp,
            'entry.1784634142': kampus,

            # Halaman 2: 16 Pertanyaan Kuisioner (Skala 1-5)
            'entry.1835673699': jawaban[0],
            'entry.636093874': jawaban[1],
            'entry.1378027831': jawaban[2],
            'entry.1701081268': jawaban[3],
            'entry.326256740': jawaban[4],
            'entry.600013373': jawaban[5],
            'entry.637910123': jawaban[6],
            'entry.419144614': jawaban[7],
            'entry.1274611282': jawaban[8],
            'entry.2104695321': jawaban[9],
            'entry.2120481503': jawaban[10],
            'entry.1830729736': jawaban[11],
            'entry.1532633421': jawaban[12],
            'entry.1720710831': jawaban[13],
            'entry.538628680': jawaban[14],
            'entry.69916659': jawaban[15],
        }

        encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
        req = urllib.request.Request(
            FORM_POST_URL, 
            data=encoded_data, 
            headers={'User-Agent': user_agent}
        )

        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    retry_info = f" (Percobaan ke-{attempt})" if attempt > 1 else ""
                    print(f"  [+] {nama} | {jk} | {hp} | {kampus}{retry_info}")
                    print(f"      Jawaban: {','.join(jawaban)}")
                    return True
        except Exception as e:
            print(f"  [!] Percobaan {attempt}/{max_retries} gagal ({e})...", end="\r")
            time.sleep(1.5 * attempt) # Exponential backoff
            
    print(f"  [-] Gagal mengirim data setelah {max_retries}x percobaan.")
    return False

# ==========================================
# JALANKAN
# ==========================================
if __name__ == '__main__':
    jumlah = input("Mau kirim berapa kali? (default 1): ").strip()
    jumlah = int(jumlah) if jumlah.isdigit() else 1

    print(f"\n=== Mengirim {jumlah}x Data RANDOM (Auto-Retry Enabled) ke Google Form LP3I ===\n")
    
    berhasil = 0
    for i in range(jumlah):
        print(f"#{i+1}:", end="")
        if kirim_jawaban():
            berhasil += 1
            # Jeda acak 1 - 2.5 detik antar pengiriman
            if i < jumlah - 1:
                delay = round(random.uniform(1.0, 2.5), 1)
                time.sleep(delay)

    print(f"\n=== Selesai! {berhasil}/{jumlah} berhasil terkirim ===")

import urllib.request
import urllib.parse
import re
import random
import string
import time
import sys

FORM_VIEW_URL = "https://forms.gle/78wuNRTRadEhdiuz8"
FORM_POST_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc1GdRi9CL90AetRzRjf2UCwIkZS8HQ8q90Un2Mjk02fSkFfA/formResponse"
PAGE_HISTORY = "0,1"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
]

NAMA_DEPAN_COWOK = ["Ahmad", "Muhammad", "Rizki", "Dimas", "Andi", "Budi", "Fajar", "Gilang", "Hendra", "Irfan", "Kevin", "Naufal", "Putra", "Rafi", "Satria", "Yoga", "Bayu", "Deni", "Faisal"]
NAMA_DEPAN_CEWEK = ["Siti", "Nur", "Dewi", "Ayu", "Putri", "Rina", "Dian", "Fitri", "Mega", "Nisa", "Indah", "Lestari", "Wulan", "Ratna", "Sari", "Anisa", "Bella", "Citra", "Maya"]
NAMA_BELAKANG_COWOK = ["Pratama", "Saputra", "Nugraha", "Hidayat", "Ramadhan", "Kurniawan", "Setiawan", "Permana", "Firmansyah", "Hakim", "Wijaya", "Maulana", "Santoso", "Wibowo"]
NAMA_BELAKANG_CEWEK = ["Rahayu", "Lestari", "Wulandari", "Handayani", "Puspitasari", "Anggraeni", "Maharani", "Fitriani", "Kusuma", "Utami", "Safitri", "Permatasari", "Damayanti"]

def random_identitas():
    jk = random.choice(["Laki-Laki", "Perempuan"])
    if jk == "Laki-Laki":
        nama = random.choice(NAMA_DEPAN_COWOK) + " " + random.choice(NAMA_BELAKANG_COWOK)
    else:
        nama = random.choice(NAMA_DEPAN_CEWEK) + " " + random.choice(NAMA_BELAKANG_CEWEK)
    prefix = random.choice(["0812", "0813", "0856", "0857", "0878", "0877", "0838", "0852", "0853", "0896", "0895"])
    hp = prefix + ''.join(random.choices(string.digits, k=random.randint(7, 8)))
    return nama, jk, hp

def show_progress_bar(current, total, bar_length=25):
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = '░' * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(round(percent * 100))}% ({current}/{total})")
    sys.stdout.flush()

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

def kirim_jawaban(i=0, max_retries=3):
    nama, jk, hp = random_identitas()
    user_agent = random.choice(USER_AGENTS)
    fbzx_token = get_fbzx(user_agent)

    form_data = {
        'fvv': '1',
        'pageHistory': PAGE_HISTORY,
        'fbzx': fbzx_token,

        # Data Isian Otomatis
        'entry.34848792': nama,  # Nama Lengkap
        'entry.809906928': jk,  # Jenis Kelamin
        'entry.90992771': hp,  # Nomer Telpon
        'entry.1784634142': random.choice(['Lp3i Ciputat', 'Lp3i Pasar Minggu', 'Lp3i Cimone', 'Lp3i Depok', 'Lp3i Cikarang', 'Lp3i Jakarta Pusat', 'Lp3i Bekasi', 'Lp3i Pondok Cabe', 'Lp3i Jakarta Utara', 'Lp3i Tanggerang', 'Non Lp3i']),  # Asal Kampus
        'entry.1835673699': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 1: Stabilitas Psikologis & Fokus (Te
        'entry.636093874': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 1: Stabilitas Psikologis & Fokus (Te
        'entry.1378027831': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Pencapaian Kompetensi Teknis    S
        'entry.1701081268': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Pencapaian Kompetensi Teknis    S
        'entry.326256740': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Pencapaian Kompetensi Teknis    S
        'entry.600013373': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Pencapaian Kompetensi Teknis    P
        'entry.637910123': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 3: Efisiensi Waktu Praktikum    Saya
        'entry.419144614': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 3: Efisiensi Waktu Praktikum    Wakt
        'entry.1274611282': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 1: Akses Perangkat Keras (Hardware L
        'entry.2104695321': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 1: Akses Perangkat Keras (Hardware L
        'entry.2120481503': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Manajemen Sumber Daya (Resource M
        'entry.1830729736': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 2: Manajemen Sumber Daya (Resource M
        'entry.1532633421': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 3: Kompatibilitas Sistem & Dukungan 
        'entry.1720710831': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 3: Kompatibilitas Sistem & Dukungan 
        'entry.538628680': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 4: Responsivitas Antarmuka    Antarm
        'entry.69916659': str(random.choices(['1', '2', '3', '4', '5'], weights=[5, 10, 20, 35, 30][:len(['1', '2', '3', '4', '5'])])[0]),  # Sub-Indikator 4: Responsivitas Antarmuka    Secara
    }

    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
    req = urllib.request.Request(
        FORM_POST_URL, 
        data=encoded_data, 
        headers={'User-Agent': user_agent}
    )

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"  [+] Respon #{i+1} terkirim: {nama} | {jk} | {hp}")
                    return True
        except Exception:
            time.sleep(1.5 * attempt)
            
    print(f"  [-] Gagal mengirim respon #{i+1} setelah {max_retries}x percobaan.")
    return False

if __name__ == '__main__':
    jumlah = input("Mau kirim berapa kali? (default 1): ").strip()
    jumlah = int(jumlah) if jumlah.isdigit() else 1

    print(f"\n=== Mengirim {jumlah}x Data ke Google Form: Analisis Efektivitas Penggunaan OS Linux Native bagi Pembelajaran Keamanan Jaringan Komputer Mahasiswa LP3I Jakarta ===\n")
    
    berhasil = 0
    for i in range(jumlah):
        if kirim_jawaban(i):
            berhasil += 1
            show_progress_bar(i + 1, jumlah)
            print()
            if i < jumlah - 1:
                time.sleep(round(random.uniform(1.0, 2.0), 1))

    print(f"\n=== Selesai! {berhasil}/{jumlah} berhasil terkirim ===")

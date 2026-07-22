import urllib.request
import urllib.parse
import re
import json
import random
import string
import time
import sys

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
]

NAMA_DEPAN_COWOK = ["Ahmad", "Muhammad", "Rizki", "Dimas", "Andi", "Budi", "Fajar", "Gilang", "Hendra", "Irfan", "Kevin", "Naufal", "Putra", "Rafi", "Satria", "Yoga", "Bayu", "Deni", "Faisal", "Galih", "Hafiz", "Ivan", "Rian", "Surya", "Agus", "Wahyu", "Ridwan", "Ilham", "Yusuf", "Rizal", "Farhan", "Aditya"]
NAMA_DEPAN_CEWEK = ["Siti", "Nur", "Dewi", "Ayu", "Putri", "Rina", "Dian", "Fitri", "Mega", "Nisa", "Indah", "Lestari", "Wulan", "Ratna", "Sari", "Anisa", "Bella", "Citra", "Maya", "Intan", "Kartika", "Laras", "Nabila", "Rahma", "Salma", "Vina", "Zahra", "Fadila", "Gita"]
NAMA_BELAKANG_COWOK = ["Pratama", "Saputra", "Nugraha", "Hidayat", "Ramadhan", "Kurniawan", "Setiawan", "Permana", "Firmansyah", "Hakim", "Wijaya", "Maulana", "Santoso", "Wibowo", "Prasetyo", "Gunawan", "Susanto", "Arifin"]
NAMA_BELAKANG_CEWEK = ["Rahayu", "Lestari", "Wulandari", "Handayani", "Puspitasari", "Anggraeni", "Maharani", "Fitriani", "Kusuma", "Utami", "Safitri", "Permatasari", "Damayanti", "Rahmawati", "Salsabila", "Agustina"]

# ==========================================
# ANALISIS FORM
# ==========================================
def parse_gform(url):
    """Menganalisis Google Form dan mengekstrak semua pertanyaan, entry ID, dan opsi jawaban"""
    req = urllib.request.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            final_url = resp.url  # URL setelah redirect (paling reliable)
    except Exception as e:
        print(f"[-] Gagal mengambil halaman Google Form: {e}")
        return None

    # Cari posisi awal data JSON setelah FB_PUBLIC_LOAD_DATA_
    marker = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*', html)
    if not marker:
        print("[-] Gagal mengekstrak data form.")
        return None

    try:
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(html, marker.end())
    except Exception as e:
        print(f"[-] Gagal parse JSON: {e}")
        return None

    form_title = data[1][8] if len(data[1]) > 8 and data[1][8] else "Google Form"

    # Ambil Form ID dari final redirect URL (paling reliable, tidak pernah double /e/)
    form_id_match = re.search(r'/forms/d/e/([^/]+)/', final_url)
    if form_id_match:
        form_id = form_id_match.group(1)
    else:
        # Fallback: ambil dari data[14]
        raw = data[14] if len(data) > 14 else ""
        form_id = raw.replace("e/", "") if raw.startswith("e/") else raw

    post_url = f"https://docs.google.com/forms/d/e/{form_id}/formResponse"
    view_url = f"https://docs.google.com/forms/d/e/{form_id}/viewform"

    # Deteksi fitur 'Wajib Login' di setelan Google Form (meta10[6] == 3)
    meta10 = data[1][10] if len(data[1]) > 10 and data[1][10] else None
    requires_login = (meta10 is not None and len(meta10) > 6 and meta10[6] == 3)

    if requires_login:
        print(f"[!] PERINGATAN: Form ini mengaktifkan opsi 'Wajib Login Google' (misal: membatasi domain organisasi).")
        print(f"    Google menolak pengisian otomatis tanpa akun Google yang terotentikasi.")
        return None

    questions = []
    page_count = 1

    for item in data[1][1]:
        if item is None:
            continue
        q_title = item[1]
        q_type = item[3]

        if q_type == 8:
            page_count += 1
            continue

        if item[4] and len(item[4]) > 0 and item[4][0]:
            entry_id = item[4][0][0]
            options = []
            if len(item[4][0]) > 1 and item[4][0][1]:
                options = [opt[0] for opt in item[4][0][1]]

            questions.append({
                'id': f"entry.{entry_id}",
                'title': q_title,
                'type': q_type,
                'options': options
            })

    page_history = ",".join(str(i) for i in range(page_count))

    return {
        'title': form_title,
        'view_url': view_url,
        'post_url': post_url,
        'page_history': page_history,
        'questions': questions
    }

# ==========================================
# GENERASI DATA RANDOM
# ==========================================
def random_identitas():
    jk = random.choice(["Laki-Laki", "Perempuan"])
    if jk == "Laki-Laki":
        nama = random.choice(NAMA_DEPAN_COWOK) + " " + random.choice(NAMA_BELAKANG_COWOK)
    else:
        nama = random.choice(NAMA_DEPAN_CEWEK) + " " + random.choice(NAMA_BELAKANG_CEWEK)
    prefix = random.choice(["0812", "0813", "0856", "0857", "0878", "0877", "0838", "0852", "0853", "0896", "0895", "0858", "0815", "0816"])
    hp = prefix + ''.join(random.choices(string.digits, k=random.randint(7, 8)))
    return nama, jk, hp

def generate_answer(q, nama, jk, hp):
    """Menghasilkan jawaban cerdas berdasarkan jenis pertanyaan"""
    title_lower = q['title'].lower()

    # Smart Field Matching
    if re.search(r'\b(nama|name)\b', title_lower):
        return nama
    elif re.search(r'\b(kelamin|gender)\b', title_lower):
        return jk
    elif re.search(r'\b(telp|phone|nomer|nomor|hp|wa|telepon|handphone)\b', title_lower):
        return hp
    elif q['options']:
        # Skala Likert (angka saja)
        if set(q['options']).issubset({'1', '2', '3', '4', '5'}):
            weights = [5, 10, 20, 35, 30][:len(q['options'])]
            return str(random.choices(q['options'], weights=weights)[0])
        elif set(q['options']).issubset({'1', '2', '3', '4'}):
            weights = [10, 15, 35, 40]
            return str(random.choices(q['options'], weights=weights)[0])
        else:
            return random.choice(q['options'])
    else:
        return nama  # Fallback: isi dengan nama

# ==========================================
# UTILITAS
# ==========================================
def show_progress_bar(current, total, bar_length=25):
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = '░' * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(round(percent * 100))}% ({current}/{total})")
    sys.stdout.flush()

def get_fbzx(view_url, user_agent):
    try:
        req = urllib.request.Request(view_url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'name="fbzx"\s+value="([^"]+)"', html)
            if match:
                return match.group(1)
    except Exception:
        pass
    return ""

# ==========================================
# PENGIRIMAN DATA
# ==========================================
def kirim_jawaban(form_info, i=0, max_retries=3):
    nama, jk, hp = random_identitas()
    user_agent = random.choice(USER_AGENTS)

    for attempt in range(1, max_retries + 1):
        # Ambil fbzx token segar setiap percobaan
        fbzx_token = get_fbzx(form_info['view_url'], user_agent)

        form_data = {
            'fvv': '1',
            'pageHistory': form_info['page_history'],
            'fbzx': fbzx_token,
            'partialResponse': f'[null,null,"{fbzx_token}"]',
            'submissionTimestamp': str(int(time.time() * 1000)),
        }

        # Isi semua pertanyaan secara cerdas
        for q in form_info['questions']:
            form_data[q['id']] = generate_answer(q, nama, jk, hp)

        encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
        req = urllib.request.Request(
            form_info['post_url'],
            data=encoded_data,
            headers={
                'User-Agent': user_agent,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': form_info['view_url'],
                'Origin': 'https://docs.google.com',
            }
        )

        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"  [+] Respon #{i+1} terkirim: {nama} | {jk} | {hp}")
                    return True
        except Exception:
            time.sleep(1.5 * attempt)

    print(f"  [-] Gagal mengirim respon #{i+1} setelah {max_retries}x percobaan.")
    return False

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    # Cek apakah URL diberikan sebagai argumen
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Masukkan URL Google Form: ").strip()

    if not url:
        print("[-] URL tidak boleh kosong.")
        sys.exit(1)

    print(f"\n[i] Menganalisis form: {url}")
    form_info = parse_gform(url)

    if not form_info:
        print("[-] Gagal menganalisis form. Pastikan URL benar dan form dapat diakses publik.")
        sys.exit(1)

    print(f"[+] Judul     : {form_info['title']}")
    print(f"[+] Halaman   : {len(form_info['page_history'].split(','))}")
    print(f"[+] Pertanyaan: {len(form_info['questions'])} item")

    jumlah = input("\nMau kirim berapa kali? (default 1): ").strip()
    jumlah = int(jumlah) if jumlah.isdigit() else 1

    print(f"\n=== Mengirim {jumlah}x Data ke: {form_info['title']} ===\n")

    berhasil = 0
    for i in range(jumlah):
        if kirim_jawaban(form_info, i):
            berhasil += 1
            show_progress_bar(i + 1, jumlah)
            print()
            if i < jumlah - 1:
                time.sleep(round(random.uniform(1.0, 2.0), 1))

    print(f"\n=== Selesai! {berhasil}/{jumlah} berhasil terkirim ===")

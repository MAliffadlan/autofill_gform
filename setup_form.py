import urllib.request
import urllib.parse
import re
import json
import sys

def parse_gform(url):
    """Menganalisis dan mengekstrak pertanyaan serta Entry ID dari URL Google Form"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
    except Exception as e:
        print(f"[-] Gagal mengambil halaman Google Form: {e}")
        return None

    match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);</script>', html, re.DOTALL)
    if not match:
        print("[-] Gagal mengekstrak data dari Google Form (FB_PUBLIC_LOAD_DATA_ tidak ditemukan).")
        return None

    try:
        data = json.loads(match.group(1))
    except Exception as e:
        print(f"[-] Gagal me-parse JSON data form: {e}")
        return None

    form_title = data[1][8] if len(data[1]) > 8 and data[1][8] else (data[1][0] if data[1] else "Google Form")
    raw_form_id = data[14] if len(data) > 14 else ""
    # Solusi bug URL double /e/
    clean_form_id = raw_form_id.strip("/").replace("e/", "")
    post_url = f"https://docs.google.com/forms/d/e/{clean_form_id}/formResponse"

    questions = []
    page_count = 1

    for item in data[1][1]:
        if item is None:
            continue
        q_title = item[1]
        q_type = item[3]
        
        # Tipe 8: Section/Page Break
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
        'view_url': url,
        'post_url': post_url,
        'page_history': page_history,
        'questions': questions
    }

def generate_script(form_info, output_file="isi_gform.py"):
    """Membuat file script isi_gform.py secara otomatis dan cerdas sesuai struktur form baru"""
    
    questions_code = ""
    for idx, q in enumerate(form_info['questions']):
        title_clean = q['title'].replace('\n', ' ').strip()
        title_lower = title_clean.lower()
        
        # Smart Field Matching (dengan Word Boundary Regex agar tidak salah cocok)
        if re.search(r'\b(nama|name)\b', title_lower):
            questions_code += f"        '{q['id']}': nama,  # {title_clean[:50]}\n"
        elif re.search(r'\b(kelamin|gender)\b', title_lower):
            questions_code += f"        '{q['id']}': jk,  # {title_clean[:50]}\n"
        elif re.search(r'\b(telp|phone|hp|wa|telepon|nomer)\b', title_lower):
            questions_code += f"        '{q['id']}': hp,  # {title_clean[:50]}\n"
        elif q['options']:
            if set(q['options']).issubset({'1', '2', '3', '4', '5'}):
                questions_code += f"        '{q['id']}': str(random.choices({q['options']}, weights=[5, 10, 20, 35, 30][:len({q['options']})])[0]),  # {title_clean[:50]}\n"
            else:
                options_str = str(q['options'])
                questions_code += f"        '{q['id']}': random.choice({options_str}),  # {title_clean[:50]}\n"
        else:
            questions_code += f"        '{q['id']}': f'Jawaban_{{i+1}}',  # {title_clean[:50]}\n"

    script_content = f'''import urllib.request
import urllib.parse
import re
import random
import string
import time
import sys

FORM_VIEW_URL = "{form_info['view_url']}"
FORM_POST_URL = "{form_info['post_url']}"
PAGE_HISTORY = "{form_info['page_history']}"

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
    sys.stdout.write(f"\\rProgress: [{{arrow}}{{spaces}}] {{int(round(percent * 100))}}% ({{current}}/{{total}})")
    sys.stdout.flush()

def get_fbzx(user_agent):
    try:
        req = urllib.request.Request(FORM_VIEW_URL, headers={{'User-Agent': user_agent}})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'name="fbzx"\\s+value="([^"]+)"', html)
            if match:
                return match.group(1)
    except Exception:
        pass
    return ""

def kirim_jawaban(i=0, max_retries=3):
    nama, jk, hp = random_identitas()
    user_agent = random.choice(USER_AGENTS)
    fbzx_token = get_fbzx(user_agent)

    form_data = {{
        'fvv': '1',
        'pageHistory': PAGE_HISTORY,
        'fbzx': fbzx_token,

        # Data Isian Otomatis
{questions_code}    }}

    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
    req = urllib.request.Request(
        FORM_POST_URL, 
        data=encoded_data, 
        headers={{'User-Agent': user_agent}}
    )

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"  [+] Respon #{{i+1}} terkirim: {{nama}} | {{jk}} | {{hp}}")
                    return True
        except Exception:
            time.sleep(1.5 * attempt)
            
    print(f"  [-] Gagal mengirim respon #{{i+1}} setelah {{max_retries}}x percobaan.")
    return False

if __name__ == '__main__':
    jumlah = input("Mau kirim berapa kali? (default 1): ").strip()
    jumlah = int(jumlah) if jumlah.isdigit() else 1

    print(f"\\n=== Mengirim {{jumlah}}x Data ke Google Form: {form_info['title']} ===\\n")
    
    berhasil = 0
    for i in range(jumlah):
        if kirim_jawaban(i):
            berhasil += 1
            show_progress_bar(i + 1, jumlah)
            print()
            if i < jumlah - 1:
                time.sleep(round(random.uniform(1.0, 2.0), 1))

    print(f"\\n=== Selesai! {{berhasil}}/{{jumlah}} berhasil terkirim ===")
'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"[+] Berhasil membuat file script: '{output_file}'")

if __name__ == '__main__':
    print("=== GOOGLE FORM UNIVERSAL GENERATOR ===")
    
    if len(sys.argv) > 1:
        url_form = sys.argv[1].strip()
    else:
        url_form = input("Masukkan URL Google Form Baru: ").strip()

    if not url_form:
        print("[-] URL Form tidak boleh kosong.")
        sys.exit(1)

    print(f"\n[i] Menganalisis Form di {url_form}...")
    info = parse_gform(url_form)
    
    if info:
        print(f"[+] Judul Form  : {info['title']}")
        print(f"[+] Jumlah Page : {len(info['page_history'].split(','))}")
        print(f"[+] Pertanyaan  : {len(info['questions'])} item terdeteksi")
        print("\n[i] Memunculkan script 'isi_gform.py'...")
        generate_script(info)
        print("\n[+] Selesai! Sekarang kamu bisa menjalankan 'python3 isi_gform.py'.")

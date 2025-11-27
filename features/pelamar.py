import datetime
import re
from database.pelamar_db import tambah_pelamar, login_pelamar, lihat_biodata, edit_biodata
from database.lowongan_db import get_all_lowongan, get_lowongan_by_id
from database.lamaran_db import tambah_lamaran, lihat_semua_lamaran
from utils.utils import print_header, print_input_prompt, input_angka, input_konfirmasi, pause

def menu_pelamar():
    while True:
        print_header("LOGIN PELAMAR")
        print("1. Login Pelamar")
        print("2. Daftar Pelamar Baru")
        print("3. Keluar")
        print("="*60)
        pilihan = input_angka("Pilih menu", 1, 3)
        if pilihan == 1:
            pelamar = login_menu()
            if pelamar:
                menu_setelah_login(pelamar)
        elif pilihan == 2:
            daftar_pelamar()
        elif pilihan == 3:
            print("Keluar dari menu pelamar...")
            break

def login_menu():
    print_header("LOGIN PELAMAR")
    email = print_input_prompt("Masukkan Email").strip()
    tanggal_lahir = print_input_prompt("Tanggal Lahir (YYYY-MM-DD)").strip()
    pelamar = login_pelamar(email, tanggal_lahir)
    if pelamar:
        print(f"Selamat datang, {pelamar['nama_lengkap']}!")
        return pelamar
    else:
        print("Login gagal! Email atau tanggal lahir salah.")
        return None

def daftar_pelamar():
    print_header("PENDAFTARAN PELAMAR BARU")
    while True:
        nama_lengkap = print_input_prompt("Nama Lengkap").strip()
        if not nama_lengkap:
            print("Nama tidak boleh kosong!")
        elif not nama_lengkap.replace(" ", "").isalpha():
            print("Nama hanya boleh berisi huruf dan spasi!")
        else:
            break
    while True:
        tanggal_lahir = print_input_prompt("Tanggal Lahir (YYYY-MM-DD)").strip()
        try:
            tgl_obj = datetime.datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
            if tgl_obj > datetime.date.today():
                print("Tanggal lahir tidak boleh di masa mendatang! Coba lagi.")
            else:
                break
        except ValueError:
            print("Format tanggal salah! Harus YYYY-MM-DD.")
    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L','P': 'P', 'PEREMPUAN': 'P'}
    while True:
        jenis_kelamin_input = print_input_prompt("Jenis Kelamin (L/P)").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki/L atau Perempuan/P ")
    while True:
        alamat = print_input_prompt("Alamat").strip()
        if not alamat:
            print("Alamat tidak boleh kosong! Silakan isi kembali.")
        else:
            break
    while True:
        email = print_input_prompt("Email").strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Format email tidak valid!")
        else:
            break
    while True:
        pengalaman = print_input_prompt("Pengalaman").strip()
        if not pengalaman:
            print("Pengalaman tidak boleh kosong! Jika tidak ada pengalaman, ketik 'Tidak ada'.")
        else:
            break
    pendidikan_map = {
        'TIDAK ADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP',
        'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK', 'SMA/SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3',
        'D4': 'D4/S1', 'S1': 'D4/S1', 'D4/S1': 'D4/S1',
        'S2': 'S2', 'S3': 'S3'
    }
    while True:
        pendidikan_terakhir = print_input_prompt("Pendidikan Terakhir").strip().upper()
        if pendidikan_terakhir in pendidikan_map:
            pendidikan_terakhir = pendidikan_map[pendidikan_terakhir]
            break
        else:
            print("Input tidak valid! Silakan isi pendidikan terakhir anda(SMK/SMA, D3, D4/S1, dll)")
    tambah_pelamar(nama_lengkap, tanggal_lahir, jenis_kelamin, alamat, email, pengalaman, pendidikan_terakhir)
    print("Pendaftaran berhasil!")
    pause()

def menu_setelah_login(pelamar):
    while True:
        print_header("MENU PELAMAR")
        print("1. Lihat Biodata")
        print("2. Edit Biodata")
        print("3. Lamar Lowongan")
        print("4. Lihat Status Lamaran")
        print("5. Logout")
        print("="*60)
        pilihan = input_angka("Pilih menu", 1, 5)
        if pilihan == 1:
            lihat_data_pelamar(pelamar["pelamar_id"])
        elif pilihan == 2:
            ubah_biodata(pelamar["pelamar_id"])
        elif pilihan == 3:
            lamar_lowongan(pelamar["pelamar_id"])
        elif pilihan == 4:
            lihat_status_lamaran(pelamar["pelamar_id"])
        elif pilihan == 5:
            print("Logout berhasil.\n")
            break

def lihat_data_pelamar(pelamar_id):
    data = lihat_biodata(pelamar_id)
    if not data:
        print("Data pelamar tidak ditemukan.")
        return
    print_header("BIODATA PELAMAR")
    for key, value in dict(data).items():
        print(f"{key.replace('_', ' ').capitalize():<30}: {value}")
    pause()

def ubah_biodata(pelamar_id):
    print_header("EDIT BIODATA")
    print("Kosongkan jika tidak ingin diubah.")
    kolom = ["nama_lengkap", "tanggal_lahir", "jenis_kelamin", "alamat", "email", "pengalaman", "pendidikan_terakhir"]
    data_baru = {}
    pendidikan_map = {
        'TIDAK ADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP',
        'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK', 'SMA/SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3',
        'D4': 'D4/S1', 'S1': 'D4/S1', 'D4/S1': 'D4/S1',
        'S2': 'S2', 'S3': 'S3'
    }
    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L', 'P': 'P', 'PEREMPUAN': 'P'}
    for k in kolom:
        while True:
            isi = print_input_prompt(k.replace('_', ' ').capitalize()).strip()
            if not isi:
                break
            if k == "nama_lengkap" and not isi.replace(" ", "").isalpha():
                print("Nama hanya boleh berisi huruf dan spasi!")
                continue
            elif k == "tanggal_lahir":
                try:
                    tgl_obj = datetime.datetime.strptime(isi, "%Y-%m-%d").date()
                    if tgl_obj > datetime.date.today():
                        print("Tanggal lahir tidak boleh di masa mendatang!")
                        continue
                except ValueError:
                    print("Format tanggal salah! Harus YYYY-MM-DD.")
                    continue
            elif k == "jenis_kelamin":
                if isi.upper() in gender_mapping:
                    isi = gender_mapping[isi.upper()]
                else:
                    print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki atau Perempuan")
                    continue
            elif k == "alamat" and not isi:
                print("Alamat tidak boleh kosong!")
                continue
            elif k == "email" and not re.match(r"[^@]+@[^@]+\.[^@]+", isi):
                print("Format email tidak valid!")
                continue
            elif k == "pendidikan_terakhir" and isi.upper() in pendidikan_map:
                isi = pendidikan_map[isi.upper()]
            elif k == "pendidikan_terakhir" and isi.upper() not in pendidikan_map:
                print("Pendidikan tidak valid! Contoh: SMA, SMK, D3, D4, S1, S2, dll.")
                continue
            data_baru[k] = isi
            break
    if data_baru:
        edit_biodata(pelamar_id, **data_baru)
        print("Data berhasil diperbarui!")
    else:
        print("Tidak ada data yang diubah.")
    pause()

def lamar_lowongan(pelamar_id):
    data = get_all_lowongan()
    if not data:
        print("Belum ada data lowongan.")
        return

    data = sorted(data, key=lambda x: x['lowongan_id'])
    pelamar_data = lihat_biodata(pelamar_id)
    if not pelamar_data:
        print("Data pelamar tidak ditemukan!")
        return

    tgl_lahir = datetime.datetime.strptime(pelamar_data['tanggal_lahir'], "%Y-%m-%d").date()
    today = datetime.date.today()
    pelamar_umur = today.year - tgl_lahir.year - ((today.month, today.day) < (tgl_lahir.month, tgl_lahir.day))
    pelamar_gender = pelamar_data['jenis_kelamin'].upper() 

    while True:
        print_header("DAFTAR LOWONGAN")
        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} ({row['jenis']})")
        print("="*60)

        pilih_input = print_input_prompt("Masukkan nomor lowongan / ketik [keluar]").strip().lower()
        if pilih_input == "keluar":
            break
        if not pilih_input.isdigit():
            print("Input harus berupa angka atau 'keluar'.")
            continue

        pilih = int(pilih_input)
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak valid.")
            continue

        selected = data[pilih-1]
        detail = get_lowongan_by_id(selected['lowongan_id'])
        if not detail:
            print("Lowongan tidak ditemukan.")
            continue

        print_header("DETAIL LOWONGAN")
        for key in ['lowongan_id', 'judul_lowongan', 'nama_perusahaan', 'deskripsi_pekerjaan', 'jenis', 
                    'lokasi', 'kontak', 'min_pendidikan', 'pengalaman', 'jenis_kelamin']:
            print(f"{key.replace('_', ' ').capitalize():<30}: {detail.get(key, 'Tidak ditentukan')}")
        for key in ['minimal_umur', 'maksimal_umur', 'slot']:
            print(f"{key.replace('_', ' ').capitalize():<30}: {detail.get(key, 'Tidak ditentukan')}")
        print(f"{'Deadline':<30}: {detail.get('deadline', 'Tidak ditentukan')}")
        print(f"{'Tanggal Posting':<30}: {detail.get('tanggal_posting', 'Tidak ditentukan')}")
        print("="*60)

        alasan_reject = []
        min_pendidikan = detail.get('min_pendidikan')
        if min_pendidikan:
            if pelamar_data['pendidikan_terakhir'].upper() != min_pendidikan.upper():
                alasan_reject.append("pendidikan tidak sesuai")

        min_umur = detail.get('minimal_umur')
        max_umur = detail.get('maksimal_umur')
        if (min_umur and pelamar_umur < min_umur) or (max_umur and pelamar_umur > max_umur):
            alasan_reject.append("umur tidak sesuai")

        kriteria_gender = detail.get('jenis_kelamin', '').upper()
        if kriteria_gender in ['L', 'P'] and pelamar_gender != kriteria_gender:
            alasan_reject.append("jenis kelamin tidak sesuai")

        slot = detail.get("slot", 0)
        if slot <= 0:
            print("Slot lowongan sudah habis. Anda tidak dapat melamar.")
            pause()
            continue

        if alasan_reject:
            tambah_lamaran(pelamar_id, selected['lowongan_id'], today.isoformat(), status="AutoReject", alasan_reject=", ".join(alasan_reject))
            print(f"Lamaran otomatis ditolak: Karena {', '.join(alasan_reject)}.")
            pause()
            break

        konfirmasi = input_konfirmasi("Apakah Anda ingin melamar lowongan ini?", ["Yes", "No"])
        if konfirmasi == "Yes":
            tambah_lamaran(pelamar_id, selected['lowongan_id'], today.isoformat(), status="Dikirim")
            print(f"Lamaran ke '{detail['judul_lowongan']}' berhasil dikirim!")
            pause()
            break
        else:
            print("Kembali ke daftar lowongan...")


def lihat_status_lamaran(pelamar_id):
    data = lihat_semua_lamaran()
    if not data:
        print("Belum ada lamaran yang dikirim.")
        pause()
        return

    data_pelamar = [d for d in data if str(d["pelamar_id"]) == str(pelamar_id)]
    if not data_pelamar:
        print("Belum ada lamaran yang dikirim.")
        pause()
        return

    data_pelamar = sorted(data_pelamar, key=lambda x: x['lamaran_id'])

    while True:
        print_header("STATUS LAMARAN")
        for i, row in enumerate(data_pelamar, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['status']} (Tanggal: {row['tanggal_lamaran']})")
        print("="*60)

        pilih_input = print_input_prompt("Masukkan nomor untuk lihat detail / ketik [keluar]").strip().lower()
        if pilih_input == "keluar":
            break
        if not pilih_input.isdigit():
            print("Input harus berupa angka atau 'keluar'.")
            continue

        pilih = int(pilih_input)
        if pilih < 1 or pilih > len(data_pelamar):
            print("Nomor tidak valid.")
            continue

        lamaran = data_pelamar[pilih-1]
        print_header(f"DETAIL LAMARAN - {lamaran['judul_lowongan']}")
        print(f"{'Judul Lowongan':<30}: {lamaran['judul_lowongan']}")
        print(f"{'Nama Perusahaan':<30}: {lamaran['nama_perusahaan']}")
        print(f"{'Tanggal Lamaran':<30}: {lamaran['tanggal_lamaran']}")
        
        status = lamaran['status']
        if status in ["AutoReject", "Ditolak"]:
            status_text = "Ditolak"
            alasan = lamaran.get('alasan_reject', 'Tidak ada alasan spesifik')
            print(f"{'Status':<30}: {status_text}")
            print(f"{'Alasan':<30}: {alasan}")
            print(f"{'Pesan':<30}: Tetap semangat, semoga cepat mendapatkan pekerjaan!")
        elif status == "Diterima":
            print(f"{'Status':<30}: Diterima")
            print(f"{'Pesan':<30}: Selamat! Anda telah diterima di tahap ini, silahkan bersiap untuk interview.")
        else:
            print(f"{'Status':<30}: {status}")

        print("="*60)
        pause()

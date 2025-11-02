from database.pelamar_db import tambah_pelamar, login_pelamar, lihat_biodata, edit_biodata
from database.lowongan_db import get_all_lowongan, get_lowongan_by_id
from database.lamaran_db import tambah_lamaran, lihat_semua_lamaran
from main import main_menu
import datetime
import re

# ========================================================== MENU LOGIN DAN DAFTAR PELAMAR =====================================================
def menu_pelamar():
    while True:
        print("\n" + "="*50)
        print(f"{'LOGIN PELAMAR':^50}")
        print("="*50)
        print("1. Login Pelamar")
        print("2. Daftar Pelamar Baru")
        print("3. Keluar")
        print("="*50)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-3)':<25}: "))
                if pilihan not in range(1, 4):
                    print("Pilihanmu tidak valid! Mohon pilih menu 1-3")
                else:
                    break
            except ValueError:
                print("Pilihan harus berupa angka! Tolong ulangi lagi.")

        if pilihan == 1:
            pelamar = login_menu()
            if pelamar:
                menu_setelah_login(pelamar)
        elif pilihan == 2:
            daftar_pelamar()
        elif pilihan == 3:
            print("Keluar dari menu pelamar...")
            main_menu()


# === LOGIN DAN REGISTRASI ===
def login_menu():
    print("\n" + "="*50)
    print(f"{'LOGIN PELAMAR':^50}")
    print("="*50)
    email = input(f"{'Masukkan Email':<25}: ").strip()
    tanggal_lahir = input(f"{'Tanggal Lahir (YYYY-MM-DD)':<25}: ").strip()
    pelamar = login_pelamar(email, tanggal_lahir)

    if pelamar:
        print(f"Selamat datang, {pelamar['nama_lengkap']}!")
        return pelamar
    else:
        print("Login gagal! Email atau tanggal lahir salah.")
        return None


def daftar_pelamar():
    print("\n" + "="*50)
    print(f"{'PENDAFTARAN PELAMAR BARU':^50}")
    print("="*50)
    while True:
        nama_lengkap = input(f"{'Nama Lengkap':<25}: ").strip()
        if not nama_lengkap:
            print("Nama tidak boleh kosong!")
        elif not nama_lengkap.replace(" ", "").isalpha():
            print("Nama hanya boleh berisi huruf dan spasi!")
        else:
            break

    while True:
        tanggal_lahir = input(f"{'Tanggal Lahir (YYYY-MM-DD)':<25}: ").strip()
        try:
            tgl_obj = datetime.datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
            if tgl_obj > datetime.date.today():
                print("Tanggal lahir tidak boleh di masa mendatang! Coba lagi.")
            else:
                break
        except ValueError:
            print("Format tanggal salah! Harus YYYY-MM-DD.")

    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L', 'P': 'P', 'PEREMPUAN': 'P'}
    while True:
        jenis_kelamin_input = input(f"{'Jenis Kelamin (L/P)':<25}: ").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki atau Perempuan")

    while True:
        alamat = input(f"{'Alamat':<25}: ").strip()
        if not alamat:
            print("Alamat tidak boleh kosong! Silakan isi kembali.")
        else:
            break

    while True:
        email = input(f"{'Email':<25}: ").strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Format email tidak valid!")
        else:
            break

    while True:
        pengalaman = input(f"{'Pengalaman':<25}: ").strip()
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
        pendidikan_terakhir = input(f"{'Pendidikan Terakhir':<25}: ").strip().upper()
        if pendidikan_terakhir in pendidikan_map:
            pendidikan_terakhir = pendidikan_map[pendidikan_terakhir]
            break
        else:
            print("Input tidak valid! Silakan isi ulang sesuai contoh.\n")

    tambah_pelamar(nama_lengkap, tanggal_lahir, jenis_kelamin, alamat, email, pengalaman, pendidikan_terakhir)

# ========================================================== MENU LOGIN DAN DAFTAR PELAMAR =====================================================

# ====================================================== MENU SETELAH LOGIN DAN DAFTAR PELAMAR =================================================
def menu_setelah_login(pelamar):
    while True:
        print("\n" + "="*50)
        print(f"{'MENU PELAMAR':^50}")
        print("="*50)
        print(f"{'1. Lihat Biodata':<25}")
        print(f"{'2. Edit Biodata':<25}")
        print(f"{'3. Lamar Lowongan':<25}")
        print(f"{'4. Lihat Status Lamaran':<25}")
        print(f"{'5. Logout':<25}")
        print("="*50)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-6)':<25}: "))
                if pilihan not in range(1, 7):
                    print("Pilihanmu tidak valid! Mohon pilih menu 1-6")
                else:
                    break
            except ValueError:
                print("Input harus berupa angka! Ulangi lagi.")

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
# ====================================================== MENU SETELAH LOGIN DAN DAFTAR PELAMAR =================================================

# ================================================================= FITUR PELAMAR ==============================================================
def lihat_data_pelamar(pelamar_id):
    data = lihat_biodata(pelamar_id)
    if not data:
        print("Data pelamar tidak ditemukan.")
        return

    print("\n" + "="*50)
    print(f"{'BIODATA PELAMAR':^50}")
    print("="*50)
    for key, value in dict(data).items():
        print(f"{key.replace('_', ' ').capitalize():<25}: {value}")


def ubah_biodata(pelamar_id):
    print("\n" + "="*50)
    print(f"{'EDIT BIODATA':^50}")
    print("="*50)
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
            isi = input(f"{k.replace('_', ' ').capitalize():<25}: ").strip()
            if not isi:
                break  # Kosong berarti tidak ingin diubah

            if k == "nama_lengkap":
                if not isi.replace(" ", "").isalpha():
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
            elif k == "alamat":
                if not isi:
                    print("Alamat tidak boleh kosong!")
                    continue
            elif k == "email":
                if not re.match(r"[^@]+@[^@]+\.[^@]+", isi):
                    print("Format email tidak valid!")
                    continue
            elif k == "pendidikan_terakhir":
                if isi.upper() in pendidikan_map:
                    isi = pendidikan_map[isi.upper()]
                else:
                    print("Pendidikan tidak valid! Contoh: SMA, SMK, D3, D4, S1, S2, dll.")
                    continue

            data_baru[k] = isi
            break

    if data_baru:
        edit_biodata(pelamar_id, **data_baru)
        print("Data berhasil diperbarui!")
    else:
        print("Tidak ada data yang diubah.")
# ================================================================= FITUR PELAMAR ==============================================================

# =========================================================== FITUR LOWONGAN DAN LAMARAN  ======================================================
def lamar_lowongan(pelamar_id):
    data = get_all_lowongan()
    if not data:
        print("Belum ada data lowongan.")
        return

    while True:
        print("\n" + "="*50)
        print(f"{'DAFTAR LOWONGAN':^50}")
        print("="*50)
        for row in data:
            print(f"[{row['lowongan_id']}] {row['judul_lowongan']:<25} - {row['nama_perusahaan']} ({row['jenis']})")
        print("="*50)

        id_lowongan = input(f"{'Masukkan ID lowongan (0 untuk kembali)':<25}: ").strip()
        if id_lowongan == "0":
            break
        if not id_lowongan.isdigit():
            print("Input tidak valid. Harus berupa angka.")
            continue

        detail = get_lowongan_by_id(int(id_lowongan))
        if not detail:
            print("Lowongan tidak ditemukan.")
            continue

        # Tampilkan detail lowongan lengkap
        print("\n" + "="*50)
        print(f"{'DETAIL LOWONGAN':^50}")
        print("="*50)
        print(f"{'ID':<25}: {detail['lowongan_id']}")
        print(f"{'Judul':<25}: {detail['judul_lowongan']}")
        print(f"{'Perusahaan':<25}: {detail['nama_perusahaan']}")
        print(f"{'Deskripsi':<25}: {detail['deskripsi_pekerjaan']}")
        print(f"{'Jenis':<25}: {detail['jenis']}")
        print(f"{'Lokasi':<25}: {detail['lokasi']}")
        print(f"{'Kontak':<25}: {detail['kontak']}")
        print(f"{'Minimal Pendidikan':<25}: {detail['min_pendidikan']}")
        print(f"{'Pengalaman':<25}: {detail['pengalaman']}")
        print(f"{'Jenis Kelamin':<25}: {detail['jenis_kelamin']}")
        print(f"{'Minimal Umur':<25}: {detail.get('minimal_umur', 'Tidak ditentukan')}")
        print(f"{'Maksimal Umur':<25}: {detail.get('maksimal_umur', 'Tidak ditentukan')}")
        print(f"{'Slot':<25}: {detail.get('slot', 'Tidak ditentukan')}")
        print(f"{'Deadline':<25}: {detail['deadline']}")
        print(f"{'Tanggal Posting':<25}: {detail['tanggal_posting']}")
        print("="*50)

        # Konfirmasi lamaran
        konfirmasi = input("Apakah Anda ingin melamar lowongan ini? (Y/N): ").strip().upper()
        if konfirmasi == "Y":
            tanggal_lamaran = datetime.date.today().isoformat()
            tambah_lamaran(pelamar_id, int(id_lowongan), tanggal_lamaran)
            print(f"Lamaran ke '{detail['judul_lowongan']}' berhasil dikirim!")
            break
        elif konfirmasi == "N":
            print("Kembali ke daftar lowongan...")
            continue
        else:
            print("Input tidak valid! Ketik Y atau N.")

def lihat_status_lamaran(pelamar_id):
    data = lihat_semua_lamaran()
    if not data:
        print("Belum ada lamaran yang dikirim.")
        return

    data_pelamar = [d for d in data if str(d["pelamar_id"]) == str(pelamar_id)]
    if not data_pelamar:
        print("Belum ada lamaran yang dikirim.")
        return

    print("\n" + "="*50)
    print(f"{'STATUS LAMARAN':^50}")
    print("="*50)
    for row in data_pelamar:
        print(f"{row['judul_lowongan']:<25} - {row['status']} (Tanggal: {row['tanggal_lamaran']})")
# =========================================================== FITUR LOWONGAN DAN LAMARAN  ======================================================
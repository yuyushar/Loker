from database.pelamar_db import tambah_pelamar, login_pelamar, lihat_biodata, edit_biodata
from database.lowongan_db import get_all_lowongan, get_lowongan_by_id
from database.lamaran_db import tambah_lamaran, lihat_semua_lamaran
from main import main_menu
import datetime


def menu_pelamar():
    while True:
        print("\n" + "="*40)
        print("        === MENU PELAMAR ===")
        print("="*40)
        print("1. Login Pelamar")
        print("2. Daftar Pelamar Baru")
        print("3. Keluar")
        print("="*40)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-4)':<21}: "))
                if pilihan not in range (1,4):
                    print("Pilihan mu tidak valid! Mohon pilih menu 1-4")
                else:
                    break
            except ValueError:
                print ("Pilihan harus berupa integer! Tolong ulangi lagi")

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
    print("\n=== LOGIN PELAMAR ===")
    nama = input("Masukkan nama lengkap: ").strip()
    tgl = input("Masukkan tanggal lahir (YYYY-MM-DD): ").strip()
    pelamar = login_pelamar(nama, tgl)

    if pelamar:
        print(f"Selamat datang, {pelamar['nama_lengkap']}!")
        return pelamar
    else:
        print("Login gagal! Nama atau tanggal lahir salah.")
        return None


def daftar_pelamar():
    print("\n=== PENDAFTARAN PELAMAR BARU ===")
    nama = input("Nama Lengkap: ")
    tgl = input("Tanggal Lahir (YYYY-MM-DD): ")
    jk = input("Jenis Kelamin (L/P): ").upper()
    alamat = input("Alamat: ")
    email = input("Email: ")
    pengalaman = input("Pengalaman (tahun): ")
    pendidikan = input("Pendidikan Terakhir: ")

    tambah_pelamar(nama, tgl, jk, alamat, email, pengalaman, pendidikan)


# === MENU SETELAH LOGIN ===

def menu_setelah_login(pelamar):
    while True:
        print("\n" + "="*40)
        print(f"   MENU PELAMAR ({pelamar('nama_lengkap')})")
        print("="*40)
        print("1. Lihat Biodata")
        print("2. Edit Biodata")
        print("3. Lihat Lowongan")
        print("4. Lamar Lowongan")
        print("5. Lihat Status Lamaran")
        print("6. Logout")
        print("="*40)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-6)':<21}: "))
                if pilihan not in range (1,7):
                    print("Pilihan mu tidak valid! Mohon pilih menu 1-5")
                else:
                    break
            except ValueError:
                print ("Pilihan harus berupa integer! Tolong ulangi lagi")

        if pilihan == 1:
            lihat_data_pelamar(pelamar("pelamar_id"))
        elif pilihan == 2:
            ubah_biodata(pelamar["pelamar_id"])
        elif pilihan == 3:
            tampilkan_lowongan()
        elif pilihan == 4:
            lamar_lowongan(pelamar["pelamar_id"])
        elif pilihan == 5:
            lihat_status_lamaran(pelamar["pelamar_id"])
        elif pilihan == 6:
            print("Logout berhasil.\n")
            break
        else:
            print("Pilihan tidak valid!")


# === FITUR BIODATA ===

def lihat_data_pelamar(pelamar_id):
    data = lihat_biodata(pelamar_id)
    if not data:
        print("Data pelamar tidak ditemukan.")
        return

    print("\n=== BIODATA PELAMAR ===")
    for key, value in dict(data).items():
        print(f"{key.capitalize()} : {value}")


def ubah_biodata(pelamar_id):
    print("\n=== EDIT BIODATA ===")
    print("Kosongkan jika tidak ingin diubah.")

    kolom = ["nama_lengkap", "tanggal_lahir", "jenis_kelamin", "alamat", "email", "pengalaman", "pendidikan_terakhir"]
    data_baru = {}

    for k in kolom:
        isi = input(f"{k.replace('_', ' ').capitalize()}: ").strip()
        if isi:
            data_baru[k] = isi

    if data_baru:
        edit_biodata(pelamar_id, **data_baru)
    else:
        print("Tidak ada data yang diubah.")


# === FITUR LOWONGAN DAN LAMARAN ===

def tampilkan_lowongan():
    data = get_all_lowongan()
    if not data:
        print("Belum ada data lowongan.")
        return

    print("\n=== DAFTAR LOWONGAN ===")
    for row in data:
        print(f"[{row['lowongan_id']}] {row['judul_lowongan']} - {row['nama_perusahaan']} ({row['jenis']})")


def lamar_lowongan(pelamar_id):
    tampilkan_lowongan()
    id_low = input("\nMasukkan ID lowongan yang ingin dilamar: ").strip()
    if not id_low.isdigit():
        print("Input tidak valid.")
        return

    low = get_lowongan_by_id(int(id_low))
    if not low:
        print("Lowongan tidak ditemukan.")
        return

    tanggal = datetime.date.today().isoformat()
    tambah_lamaran(pelamar_id, int(id_low), tanggal)
    print(f"Lamaran ke '{low['judul_lowongan']}' berhasil dikirim!")


def lihat_status_lamaran(pelamar_id):
    data = lihat_semua_lamaran()
    data_pelamar = [d for d in data if d["pelamar_id"] == pelamar_id] if data and "pelamar_id" in data[0] else []

    if not data_pelamar:
        print("Belum ada lamaran yang dikirim.")
        return

    print("\n=== STATUS LAMARAN ===")
    for row in data_pelamar:
        print(f"{row['judul_lowongan']} - {row['status']} (Tanggal: {row['tanggal_lamaran']})")

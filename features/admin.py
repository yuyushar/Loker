from database.admin_db import login_admin
from database.lamaran_db import lihat_semua_lamaran, ubah_status_lamaran
from database.lowongan_db import (
    get_all_lowongan, create_lowongan, update_lowongan,
    delete_lowongan, get_lowongan_by_id
)
import datetime

def menu_admin():
    print("\n" + "="*40)
    print("          LOGIN ADMIN")
    print("="*40)

    email = input("Masukkan email admin: ").strip()
    password = input("Masukkan password admin: ").strip()
    admin = login_admin(email, password)

    if not admin:
        print("Login gagal! Email atau password salah.")
        return
    else:
        print(f"Login berhasil. Selamat datang, ADMINNNNNN!")

    while True:
        print("\n" + "="*40)
        print("         MENU ADMIN ")
        print("="*40)
        print("1. Lihat Semua Lowongan")
        print("2. Tambah Lowongan")
        print("3. Edit Lowongan")
        print("4. Hapus Lowongan")
        print("5. Review Lamaran")
        print("6. Keluar")
        print("="*40)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-6)':<21}: "))
                if pilihan not in range(1, 7):
                    print("Pilihan tidak valid! Mohon pilih menu 1-6.")
                else:
                    break
            except ValueError:
                print("Pilihan harus berupa angka! Tolong ulangi lagi.")

        if pilihan == 1:
            tampilkan_lowongan()
        elif pilihan == 2:
            tambah_lowongan()
        elif pilihan == 3:
            edit_lowongan()
        elif pilihan == 4:
            hapus_data_lowongan()
        elif pilihan == 5:
            review_lamaran()
        elif pilihan == 6:
            print("Kembali ke menu utama...")
            break


# === CRUD LOWONGAN ===

def tampilkan_lowongan():
    print("="*40)
    print("       DAFTAR LOWONGAN")
    print("="*40)
    data = get_all_lowongan()
    if not data:
        print("Belum ada data lowongan.")
        return
    for i, row in enumerate(data, start=1):
        print(f"\nLowongan {i}:")
        print(f"ID                 : {row['lowongan_id']}")
        print(f"Judul              : {row['judul_lowongan']}")
        print(f"Perusahaan         : {row['nama_perusahaan']}")
        print(f"Jenis              : {row['jenis']}")
        print(f"Lokasi             : {row['lokasi']}")
        print(f"Minimal Pendidikan : {row['min_pendidikan']}")
        print(f"Jenis Kelamin      : {row['jenis_kelamin']}")
        print(f"Deadline           : {row['deadline']}")
        print(f"Tanggal Posting    : {row['tanggal_posting']}")
        print(f"Slot               : {row.get('slot', 'Tidak ditentukan')}")
       
    print(f"Total lowongan: {len(data)}")
    print("="*40)
def tambah_lowongan():
    print("\n" + "="*40)
    print("        TAMBAH LOWONGAN ")
    print("="*40)
    
    judul = input("Judul: ").strip()
    deskripsi = input("Deskripsi: ").strip()
    nama_pt = input("Nama Perusahaan: ").strip()

    # === Validasi Jenis Pekerjaan ===
    while True:
        jenis = input("Jenis (Magang/Kerja): ").capitalize()
        if jenis in ["Magang", "Kerja"]:
            break
        print("Jenis tidak valid! Pilihan hanya 'Magang' atau 'Kerja'.")

    tanggal = datetime.date.today().isoformat()

    # === Validasi Deadline ===
    while True:
        deadline = input("Deadline (YYYY-MM-DD): ").strip()
        try:
            parsed_date = datetime.date.fromisoformat(deadline)
            if parsed_date < datetime.date.today():
                print("Tanggal sudah lewat! Masukkan tanggal yang lebih baru dari hari ini.")
                continue
            deadline = parsed_date.isoformat()
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD (contoh: 2025-11-01).")

    lokasi = input("Lokasi: ").strip()

    # === Validasi Minimal Pendidikan ===
    mapping_pendidikan = {
        'TIDAKADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP', 'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4/S1', 'S1': 'D4/S1', 'S2': 'S2', 'S3': 'S3'
    }

    while True:
        min_pendidikan = input("Minimal Pendidikan: ").upper().replace(" ", "")
        if min_pendidikan in mapping_pendidikan:
            min_pendidikan = mapping_pendidikan[min_pendidikan]
            break
        print("Input pendidikan tidak valid! Contoh: SMA, D3, S1, dll.")

    # === Validasi Jenis Kelamin ===
    gender_mapping = {
        'L': 'L', 'LAKI-LAKI': 'L',
        'P': 'P', 'PEREMPUAN': 'P',
        'B': 'Bebas', 'BEBAS': 'Bebas'
    }

    while True:
        jenis_kelamin_input = input("Jenis Kelamin (Laki-Laki/Perempuan/Bebas): ").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki, Perempuan, atau Bebas.")

    # === Validasi Slot ===
    while True:
        try:
            slot = int(input("Jumlah Slot (berapa orang dibutuhkan): "))
            if slot <= 0:
                print("Slot harus lebih dari 0.")
            else:
                break
        except ValueError:
            print("Masukkan angka yang valid untuk slot.")

    # === Simpan ke Database ===
    data = {
        'judul_lowongan': judul,
        'deskripsi_pekerjaan': deskripsi,
        'lokasi': lokasi,
        'jenis': jenis,
        'tanggal_posting': tanggal,
        'deadline': deadline,
        'nama_perusahaan': nama_pt,
        'min_pendidikan': min_pendidikan,
        'jenis_kelamin': jenis_kelamin,
        'slot': slot,
        'admin_id': 1
    }

    try:
        create_lowongan(data)
        print("Lowongan berhasil ditambahkan!")
    except Exception as e:
        print(f"Gagal menambahkan lowongan: {e}")


def edit_lowongan():
    while True:
        print("\n=== UPDATE LOWONGAN ===")
        print("Ketik 'keluar' untuk kembali ke menu utama.")

        data = get_all_lowongan()
        if not data:
            print("Belum ada lowongan untuk diupdate.")
            return
        tampilkan_lowongan()
        id_input = input("\nMasukkan ID lowongan yang ingin diupdate: ").strip()
        if id_input.lower() == "keluar":
            print("Kembali ke menu utama.")
            break

        if not id_input.isdigit():
            print("Input ID tidak valid!")
            continue

        low = get_lowongan_by_id(int(id_input))
        if not low:
            print("ID Lowongan tidak ditemukan!")
            continue

        print("\n=== Data Lowongan Lama ===")
        for k, v in low.items():
            print(f"{k}: {v}")

        print("\nMasukkan data baru (kosongkan jika tidak diubah):")

        fields = {}
        for field in [
            'judul_lowongan', 'deskripsi_pekerjaan', 'lokasi',
            'jenis', 'deadline', 'nama_perusahaan',
            'min_pendidikan', 'jenis_kelamin', 'slot'
        ]:
            val = input(f"{field} [{low.get(field)}]: ").strip()
            if val:
                fields[field] = val

        if fields:
            update_lowongan(int(id_input), fields)
            print("Data lowongan berhasil diupdate.")
        else:
            print("Tidak ada perubahan dilakukan.")

        lagi = input("\nApakah ingin mengupdate lowongan lain? (ya/tidak): ").strip().lower()
        if lagi != "ya":
            break


def hapus_data_lowongan():
    id_low = input("Masukkan ID lowongan yang ingin dihapus: ").strip()
    if not id_low.isdigit():
        print("ID tidak valid.")
        return
    delete_lowongan(int(id_low))
    print("Lowongan berhasil dihapus!")


# === LAMARAN ===
def review_lamaran():
    while True:
        data = lihat_semua_lamaran()
        if not data:
            print("Belum ada lamaran untuk direview.")
            return

        print("\n=== REVIEW LAMARAN ===")
        for row in data:
            print(f"[{row['lamaran_id']}] {row['nama_lengkap']} - {row['judul_lowongan']} ({row['status']})")

        print("\nKetik 'keluar' untuk kembali ke menu utama.")
        id_lam = input("Masukkan ID lamaran yang ingin divalidasi: ").strip()

        if id_lam.lower() == "keluar":
            print("Kembali ke menu utama.")
            break

        if not id_lam.isdigit():
            print("Input ID tidak valid!")
            continue

        lamaran_terpilih = next((row for row in data if row['lamaran_id'] == int(id_lam)), None)
        if not lamaran_terpilih:
            print("ID Lamaran tidak ditemukan.")
            continue

        print("\n=== DATA PELAMAR ===")
        print(f"Nama Pelamar : {lamaran_terpilih['nama_lengkap']}")
        print(f"Lowongan     : {lamaran_terpilih['judul_lowongan']}")
        print(f"Status Saat Ini : {lamaran_terpilih['status']}")

        status = input("Masukkan hasil validasi (Diterima/Ditolak/Menunggu): ").capitalize()
        if ubah_status_lamaran(int(id_lam), status):
            print("Status lamaran berhasil divalidasi.")
        else:
            print("Gagal memproses validasi lamaran.")

        lanjut = input("\nApakah ingin mereview lamaran lain? (ya/tidak): ").strip().lower()
        if lanjut != "ya":
            break

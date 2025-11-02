from database.admin_db import login_admin
from database.lamaran_db import lihat_semua_lamaran, ubah_status_lamaran
from database.lowongan_db import (
    get_all_lowongan, create_lowongan, update_lowongan,
    delete_lowongan, get_lowongan_by_id
)
import datetime

# ========================================================= MENU UTAMA ADMIN ===================================================
def menu_admin():
    print("\n" + "="*50)
    print(f"{'LOGIN ADMIN':^50}")
    print("="*50)

    email = input(f"{'Masukkan email admin':<25}: ").strip()
    password = input(f"{'Masukkan password admin':<25}: ").strip()
    admin = login_admin(email, password)

    if not admin:
        print("Login gagal! Email atau password salah.")
        return
    else:
        print(f"Login berhasil. Selamat datang, ADMINNNNNN!")

    while True:
        print("\n" + "="*50)
        print(f"{'MENU ADMIN':^50}")
        print("="*50)
        print("1. Lihat Semua Lowongan")
        print("2. Tambah Lowongan")
        print("3. Edit Lowongan")
        print("4. Hapus Lowongan")
        print("5. Review Lamaran")
        print("6. Keluar")
        print("="*50)

        while True:
            try:
                pilihan = int(input(f"{'Pilih menu (1-6)':<25}: "))
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
# ========================================================== MENU UTAMA ADMIN ===================================================

# ========================================================== CRUD LOWONGAN ======================================================
# Menampilkan Lowongan
def tampilkan_lowongan():
    while True:
        print("\n" + "="*50)
        print(f"{'DETAIL LOWONGAN':^50}")
        print("="*50)
        data = get_all_lowongan()
        if not data:
            print("Belum ada data lowongan.")
            return
        # Tampilkan daftar singkat
        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")
        
        print("\nKetik nomor untuk lihat detail, atau '0' untuk kembali ke menu admin.")
        pilih = input(f"{'Pilih nomor lowongan':<25}: ").strip()

        if not pilih.isdigit():
            print("Input harus berupa angka.")
            continue
        pilih = int(pilih)
        if pilih == 0:
            print("Kembali ke menu admin.")
            break
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak ditemukan. Coba lagi.")
            continue
        selected_id = data[pilih - 1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)
        if not detail:
            print("Data lowongan tidak ditemukan di database.")
            continue
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
        lanjut = input(f"\n{'Tekan ENTER untuk kembali / ketik "keluar"':<25}: ").strip()
        if lanjut.lower() == "keluar":
            print("Kembali ke menu admin.")
            break

# Menambah Lowongan
def tambah_lowongan():
    print("\n" + "="*50)
    print(f"{'TAMBAH LOWONGAN':^50}")
    print("="*50)
    judul = input(f"{'Judul':<25}: ").strip()
    deskripsi = input(f"{'Deskripsi':<25}: ").strip()
    nama_pt = input(f"{'Nama Perusahaan':<25}: ").strip()
    kontak = input(f"{'Kontak':<25}: ").strip()
    pengalaman = input(f"{'Pengalaman':<25}: ").strip()

    # Validasi Jenis Pekerjaan
    while True:
        jenis = input(f"{'Jenis (Magang/Kerja)':<25}: ").capitalize()
        if jenis in ["Magang", "Kerja"]:
            break
        print("Jenis tidak valid! Pilihan hanya 'Magang' atau 'Kerja'.")

    tanggal = datetime.date.today().isoformat()

    # Validasi Deadline 
    while True:
        deadline = input(f"{'Deadline (YYYY-MM-DD)':<25}: ").strip()
        try:
            parsed_date = datetime.date.fromisoformat(deadline)
            if parsed_date < datetime.date.today():
                print("Tanggal sudah lewat! Masukkan tanggal yang lebih baru dari hari ini.")
                continue
            deadline = parsed_date.isoformat()
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD (contoh: 2025-11-01).")

    lokasi = input(f"{'Lokasi':<25}: ").strip()

    # Validasi Minimal Pendidikan 
    mapping_pendidikan = {
        'TIDAKADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP', 'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4/S1', 'S1': 'D4/S1', 'S2': 'S2', 'S3': 'S3'
    }
    while True:
        min_pendidikan = input(f"{'Minimal Pendidikan':<25}: ").upper().replace(" ", "")
        if min_pendidikan in mapping_pendidikan:
            min_pendidikan = mapping_pendidikan[min_pendidikan]
            break
        print("Input pendidikan tidak valid! Contoh: SMA, D3, S1, dll.")

    # Validasi Jenis Kelamin 
    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L','P': 'P', 'PEREMPUAN': 'P','B': 'Bebas', 'BEBAS': 'Bebas'}
    while True:
        jenis_kelamin_input = input(f"{'Jenis Kelamin (L/P/Bebas)':<25}: ").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki, Perempuan, atau Bebas.")

    # Validasi Minimal dan Maksimal Umur 
    while True:
        try:
            minimal_umur = int(input(f"{'Minimal Umur':<25}: "))
            maksimal_umur = int(input(f"{'Maksimal Umur':<25}: "))
            if maksimal_umur < minimal_umur:
                print("Maksimal umur tidak boleh lebih kecil dari minimal umur. Mohon input ulang!")
            else:
                break
        except ValueError:
            print("Masukkan angka yang valid untuk umur.")

    # Validasi Slot 
    while True:
        try:
            slot = int(input(f"{'Jumlah Slot':<25}: "))
            if slot <= 0:
                print("Slot harus lebih dari 0.")
            else:
                break
        except ValueError:
            print("Masukkan angka yang valid untuk slot.")

    # Simpan ke Database 
    data = {
        'judul_lowongan': judul,
        'deskripsi_pekerjaan': deskripsi,
        'lokasi': lokasi,
        'jenis': jenis,
        'tanggal_posting': tanggal,
        'deadline': deadline,
        'nama_perusahaan': nama_pt,
        'kontak':kontak,
        'pengalaman': pengalaman,
        'min_pendidikan': min_pendidikan,
        'jenis_kelamin': jenis_kelamin,
        'minimal_umur': minimal_umur,
        'maksimal_umur': maksimal_umur,
        'slot': slot,
        'admin_id': 1
    }

    try:
        create_lowongan(data)
        print("Lowongan berhasil ditambahkan!")
    except Exception as e:
        print(f"Gagal menambahkan lowongan: {e}")

# Edit Lowongan
def edit_lowongan():
    mapping_pendidikan = {
        'TIDAKADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP', 'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4/S1', 'S1': 'D4/S1', 'S2': 'S2', 'S3': 'S3'
    }

    while True:
        print("\n" + "=" * 50)
        print(f"{'EDIT LOWONGAN':^50}")
        print("=" * 50)

        data = get_all_lowongan()
        if not data:
            print("Belum ada data lowongan.")
            return

        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = input(f"\n{'Pilih nomor lowongan untuk lihat & edit / 0 untuk kembali':<25}: ").strip()
        if not pilih.isdigit():
            print("Input harus berupa angka.")
            continue

        pilih = int(pilih)
        if pilih == 0:
            print("Kembali ke menu admin.")
            break
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak ditemukan. Coba lagi.")
            continue

        selected_id = data[pilih - 1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)

        if not detail:
            print("Data lowongan tidak ditemukan di database.")
            continue

        print("\n" + "=" * 50)
        print(f"{'DETAIL LOWONGAN':^50}")
        print("=" * 50)
        for key, label in [
            ('lowongan_id', 'ID'), ('judul_lowongan', 'Judul'), ('nama_perusahaan', 'Perusahaan'),
            ('deskripsi_pekerjaan', 'Deskripsi'), ('jenis', 'Jenis'),
            ('lokasi', 'Lokasi'), ('kontak', 'Kontak'), ('pengalaman', 'Pengalaman'),
            ('min_pendidikan', 'Minimal Pendidikan'), ('jenis_kelamin', 'Jenis Kelamin'),
            ('minimal_umur', 'Minimal Umur'), ('maksimal_umur', 'Maksimal Umur'),
            ('slot', 'Slot'), ('deadline', 'Deadline'), ('tanggal_posting', 'Tanggal Posting')
        ]:
            print(f"{label:<25}: {detail.get(key, 'Tidak ditentukan')}")
        print("=" * 50)

        if input(f"\n{'Apakah ingin mengedit lowongan ini? (ya/tidak)':<25}: ").strip().lower() != "ya":
            print("Kembali ke daftar lowongan.")
            continue

        print("\nMasukkan data baru (kosongkan jika tidak ingin diubah):")
        fields = {}
        for field, label in [
            ('judul_lowongan', 'Judul'), ('deskripsi_pekerjaan', 'Deskripsi'),
            ('lokasi', 'Lokasi'), ('jenis', 'Jenis (Magang/Kerja)'),
            ('deadline', 'Deadline (YYYY-MM-DD)'), ('nama_perusahaan', 'Nama Perusahaan'),
            ('min_pendidikan', 'Minimal Pendidikan'), ('jenis_kelamin', 'Jenis Kelamin (L/P/Bebas)'),
            ('slot', 'Jumlah Slot'), ('pengalaman', 'Pengalaman'), ('kontak', 'Kontak')
        ]:
            val = input(f"{label:<25} [{detail.get(field)}]: ").strip()
            if not val:
                continue

            if field == 'jenis':
                if val.capitalize() not in ["Magang", "Kerja"]:
                    print("Jenis tidak valid! Harus 'Magang' atau 'Kerja'.")
                    continue
                val = val.capitalize()
            elif field == 'deadline':
                try:
                    parsed_date = datetime.date.fromisoformat(val)
                    if parsed_date < datetime.date.today():
                        print("Deadline tidak boleh tanggal yang sudah lewat!")
                        continue
                    val = parsed_date.isoformat()
                except ValueError:
                    print("Format tanggal salah! Gunakan format YYYY-MM-DD.")
                    continue
            elif field == 'min_pendidikan':
                pendidikan_key = val.upper().replace(" ", "")
                if pendidikan_key in mapping_pendidikan:
                    val = mapping_pendidikan[pendidikan_key]
                else:
                    print("Pendidikan tidak valid! Contoh: SMA, D3, S1, dll.")
                    continue
            elif field == 'jenis_kelamin':
                if val.upper() not in ["L", "P", "BEBAS"]:
                    print("Jenis kelamin harus L, P, atau Bebas.")
                    continue
                val = val.capitalize()
            elif field == 'slot':
                if not val.isdigit() or int(val) <= 0:
                    print("Slot harus angka positif!")
                    continue
                val = int(val)

            fields[field] = val

        if fields:
            try:
                update_lowongan(selected_id, fields)
                print("Data lowongan berhasil diperbarui!")
            except Exception as e:
                print(f"Gagal memperbarui data: {e}")
        else:
            print("Tidak ada perubahan dilakukan.")

        if input(f"\n{'Apakah ingin mengedit lowongan lain? (ya/tidak)':<25}: ").strip().lower() != "ya":
            print("Kembali ke menu admin.")
            break

# Hapus Lowongan
def hapus_data_lowongan():
    while True:
        print("\n" + "="*50)
        print(f"{'HAPUS LOWONGAN':^50}")
        print("="*50)

        data = get_all_lowongan()
        if not data:
            print("Belum ada data lowongan.")
            return

        # Daftar singkat
        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = input(f"\n{'Pilih nomor lowongan yang ingin dihapus / 0 untuk kembali':<25}: ").strip()

        if not pilih.isdigit():
            print("Input harus berupa angka.")
            continue

        pilih = int(pilih)
        if pilih == 0:
            print("Kembali ke menu admin.")
            break
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak ditemukan. Coba lagi.")
            continue

        selected_id = data[pilih - 1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)

        if not detail:
            print("Data lowongan tidak ditemukan di database.")
            continue

        print("\n" + "="*50)
        print(f"{'DETAIL LOWONGAN':^50}")
        print("="*50)
        for key, label in [
            ('lowongan_id', 'ID'), ('judul_lowongan', 'Judul'), ('nama_perusahaan', 'Perusahaan'),
            ('deskripsi_pekerjaan', 'Deskripsi'), ('jenis', 'Jenis'), 
            ('lokasi', 'Lokasi'), ('kontak', 'Kontak'), ('pengalaman', 'Pengalaman'),
            ('min_pendidikan', 'Minimal Pendidikan'), ('jenis_kelamin', 'Jenis Kelamin'),
            ('minimal_umur', 'Minimal Umur'), ('maksimal_umur', 'Maksimal Umur'),
            ('slot', 'Slot'), ('deadline', 'Deadline'), ('tanggal_posting', 'Tanggal Posting')
        ]:
            print(f"{label:<25}: {detail.get(key, 'Tidak ditentukan')}")
        print("="*50)

        konfirmasi = input(f"\n{'Yakin ingin menghapus lowongan ini? (ya/tidak)':<25}: ").strip().lower()
        if konfirmasi == "ya":
            try:
                delete_lowongan(selected_id)
                print("Lowongan berhasil dihapus!")
            except Exception as e:
                print(f"Gagal menghapus lowongan: {e}")
        else:
            print("Dibatalkan, data tidak dihapus.")

        lanjut = input(f"\n{'Apakah ingin menghapus lowongan lain? (ya/tidak)':<25}: ").strip().lower()
        if lanjut != "ya":
            print("Kembali ke menu admin.")
            break
# ========================================================== CRUD LOWONGAN ======================================================

# ========================================================== REVIEW LAMARAN =====================================================
def review_lamaran():
    kolom = ["nama_lengkap", "tanggal_lahir", "jenis_kelamin", "alamat", "email", "pengalaman", "pendidikan_terakhir"]

    while True:
        data = lihat_semua_lamaran()
        if not data:
            print("Belum ada lamaran untuk direview.")
            return

        print("\n" + "="*50)
        print(f"{'REVIEW LAMARAN':^50}")
        print("="*50)
        for row in data:
            print(f"[{row['lamaran_id']}] {row['nama_lengkap']} - {row['judul_lowongan']} ({row['status']})")

        id_lam = input(f"\n{'Masukkan ID lamaran untuk divalidasi / ketik kembali untuk keluar':<25}: ").strip()
        if id_lam.lower() == "kembali":
            print("Kembali ke menu utama.")
            break

        if not id_lam.isdigit():
            print("Input ID tidak valid!")
            continue

        lamaran_terpilih = next((row for row in data if row['lamaran_id'] == int(id_lam)), None)
        if not lamaran_terpilih:
            print("ID Lamaran tidak ditemukan.")
            continue

        print("\n" + "="*50)
        print(f"{'DATA PELAMAR':^50}")
        print("="*50)
        for key in kolom:
            label = key.replace("_", " ").title()
            print(f"{label:<25}: {lamaran_terpilih.get(key, '-')}")
        print(f"{'Lowongan Dilamar':<25}: {lamaran_terpilih.get('judul_lowongan', '-')}")
        print(f"{'Status Saat Ini':<25}: {lamaran_terpilih.get('status', '-')}")

        status = input(f"{'Masukkan status (Diterima/Ditolak) / ketik kembali untuk batal':<25}: ").capitalize()
        if status.lower() == "kembali":
            print("Validasi dibatalkan. Kembali ke daftar lamaran.")
            continue

        while status not in ["Diterima", "Ditolak"]:
            print("Status tidak valid! Hanya boleh 'Diterima' atau 'Ditolak'.")
            status = input(f"{'Masukkan status (Diterima/Ditolak) / ketik kembali untuk batal':<25}: ").capitalize()
            if status.lower() == "kembali":
                print("Validasi dibatalkan. Kembali ke daftar lamaran.")
                break

        if status.lower() == "kembali":
            continue

        if ubah_status_lamaran(int(id_lam), status):
            print("Status lamaran berhasil divalidasi.")
        else:
            print("Gagal memproses validasi lamaran.")

        lanjut = input(f"\n{'Apakah ingin mereview lamaran lain? (ya/tidak)':<25}: ").strip().lower()
        if lanjut != "ya":
            break
# ========================================================== REVIEW LAMARAN =====================================================

from database.admin_db import login_admin
from database.lamaran_db import lihat_semua_lamaran, ubah_status_lamaran
from database.lowongan_db import (
    get_all_lowongan, create_lowongan, update_lowongan,
    delete_lowongan, get_lowongan_by_id
)
import datetime

# =========================== UTILITAS ===========================
def print_input_prompt(prompt: str):
    return input(f"{prompt:<30}: ")

def input_angka(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(print_input_prompt(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Pilihan tidak valid! Mohon pilih angka {min_val}-{max_val}.")
                continue
            return val
        except ValueError:
            print("Input harus berupa angka!")

def input_konfirmasi(prompt, options):
    options_str = '/'.join(options)
    while True:
        val = print_input_prompt(f"{prompt} [{options_str}]").strip().capitalize()
        if val in options:
            return val
        print(f"Input tidak valid! Pilih salah satu: {options_str}")

def print_header(title):
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def pause():
    input("\nTekan [Enter] untuk kembali...")

# =========================== LOGIN ADMIN ===========================
def menu_admin():
    print_header("LOGIN ADMIN")
    email = print_input_prompt("Masukkan email admin").strip()
    password = print_input_prompt("Masukkan password admin").strip()
    admin = login_admin(email, password)

    if not admin:
        print("Login gagal! Email atau password salah.")
        pause()
        return
    print("Login berhasil. Selamat datang, ADMINNNNNN!")

    while True:
        print_header("MENU ADMIN")
        print("1. Lihat Semua Lowongan")
        print("2. Tambah Lowongan")
        print("3. Edit Lowongan")
        print("4. Hapus Lowongan")
        print("5. Review Lamaran")
        print("6. Keluar")
        print("="*60)

        pilihan = input_angka("Pilih menu", 1, 6)

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
            print("Keluar dari menu admin...")
            pause()
            break

# =========================== CRUD LOWONGAN ===========================
def tampilkan_lowongan():
    while True:
        print_header("DETAIL LOWONGAN")
        data = get_all_lowongan()
        if not data:
            print("Belum ada data lowongan.")
            pause()
            return

        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = print_input_prompt("Pilih nomor lowongan / 0 keluar").strip()
        if not pilih.isdigit():
            print("Input harus berupa angka.")
            continue
        pilih = int(pilih)
        if pilih == 0:
            break
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak ditemukan.")
            continue

        selected_id = data[pilih - 1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)
        if not detail:
            print("Data lowongan tidak ditemukan di database.")
            pause()
            continue

        print_header("DETAIL LOWONGAN")
        for key in ['lowongan_id', 'judul_lowongan', 'nama_perusahaan', 'deskripsi_pekerjaan',
                    'jenis', 'lokasi', 'kontak', 'min_pendidikan', 'pengalaman', 'jenis_kelamin',
                    'minimal_umur', 'maksimal_umur', 'slot', 'deadline', 'tanggal_posting']:
            print(f"{key.replace('_', ' ').capitalize():<30} : {detail.get(key, 'Tidak ditentukan')}")
        pause()

def tambah_lowongan():
    print_header("TAMBAH LOWONGAN")
    judul = print_input_prompt("Judul").strip()
    deskripsi = print_input_prompt("Deskripsi").strip()
    nama_pt = print_input_prompt("Nama Perusahaan").strip()
    kontak = print_input_prompt("Kontak").strip()
    pengalaman = print_input_prompt("Pengalaman").strip()

    jenis = ""
    while True:
        jenis = print_input_prompt("Jenis (Magang/Kerja)").capitalize()
        if jenis in ["Magang", "Kerja"]:
            break
        print("Jenis tidak valid! Pilihan hanya 'Magang' atau 'Kerja'.")
    tanggal = datetime.date.today().isoformat()

    while True:
        deadline = print_input_prompt("Deadline (YYYY-MM-DD)").strip()
        try:
            parsed_date = datetime.date.fromisoformat(deadline)
            if parsed_date < datetime.date.today():
                print("Tanggal sudah lewat!")
                continue
            deadline = parsed_date.isoformat()
            break
        except ValueError:
            print("Format tanggal salah!")

    lokasi = print_input_prompt("Lokasi").strip()
    mapping_pendidikan = {
        'TIDAKADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP', 'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4/S1', 'S1': 'D4/S1', 'S2': 'S2', 'S3': 'S3'
    }
    while True:
        min_pendidikan = print_input_prompt("Minimal Pendidikan").upper().replace(" ", "")
        if min_pendidikan in mapping_pendidikan:
            min_pendidikan = mapping_pendidikan[min_pendidikan]
            break
        print("Pendidikan tidak valid!")

    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L','P': 'P', 'PEREMPUAN': 'P','B': 'Bebas', 'BEBAS': 'Bebas'}
    while True:
        jenis_kelamin_input = print_input_prompt("Jenis Kelamin (L/P/Bebas)").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki, Perempuan, atau Bebas.")

    while True:
        try:
            minimal_umur = int(print_input_prompt("Minimal Umur"))
            maksimal_umur = int(print_input_prompt("Maksimal Umur"))
            if maksimal_umur < minimal_umur:
                print("Maksimal umur tidak boleh lebih kecil dari minimal umur.")
                continue
            break
        except ValueError:
            print("Masukkan angka valid!")

    while True:
        try:
            slot = int(print_input_prompt("Jumlah Slot"))
            if slot <= 0:
                print("Slot harus > 0.")
                continue
            break
        except ValueError:
            print("Masukkan angka valid!")

    data = {
        'judul_lowongan': judul, 'deskripsi_pekerjaan': deskripsi, 'lokasi': lokasi,
        'jenis': jenis, 'tanggal_posting': tanggal, 'deadline': deadline, 'nama_perusahaan': nama_pt,
        'kontak': kontak, 'pengalaman': pengalaman, 'min_pendidikan': min_pendidikan,
        'jenis_kelamin': jenis_kelamin, 'minimal_umur': minimal_umur, 'maksimal_umur': maksimal_umur,
        'slot': slot, 'admin_id': 1
    }

    try:
        create_lowongan(data)
        print("Lowongan berhasil ditambahkan!")
    except Exception as e:
        print(f"Gagal menambahkan lowongan: {e}")
    pause()

# =========================== EDIT LOWONGAN ===========================
def edit_lowongan():
    mapping_pendidikan = {
        'TIDAKADA': 'Tidak Ada', 'SD': 'SD', 'SMP': 'SMP', 'SMA': 'SMA/SMK', 'SMK': 'SMA/SMK',
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3', 'D4': 'D4/S1', 'S1': 'D4/S1', 'S2': 'S2', 'S3': 'S3'
    }
    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L', 'P': 'P', 'PEREMPUAN': 'P', 'B': 'Bebas', 'BEBAS': 'Bebas'}

    while True:
        print_header("EDIT LOWONGAN")
        data = get_all_lowongan()
        if not data:
            print("Belum ada data lowongan.")
            pause()
            return

        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = print_input_prompt("Pilih nomor lowongan / 0 keluar").strip()
        if not pilih.isdigit(): continue
        pilih = int(pilih)
        if pilih == 0: break
        if pilih < 1 or pilih > len(data): continue

        selected_id = data[pilih-1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)
        if not detail:
            print("Data lowongan tidak ditemukan.")
            pause()
            continue

        # Tampilkan detail lama sebagai referensi
        print_header("DETAIL LOWONGAN (Referensi)")
        for key, label in [
            ('lowongan_id', 'ID'), ('judul_lowongan', 'Judul'), ('nama_perusahaan', 'Perusahaan'),
            ('deskripsi_pekerjaan', 'Deskripsi'), ('jenis', 'Jenis'),
            ('lokasi', 'Lokasi'), ('kontak', 'Kontak'), ('pengalaman', 'Pengalaman'),
            ('min_pendidikan', 'Minimal Pendidikan'), ('jenis_kelamin', 'Jenis Kelamin'),
            ('minimal_umur', 'Minimal Umur'), ('maksimal_umur', 'Maksimal Umur'),
            ('slot', 'Slot'), ('deadline', 'Deadline'), ('tanggal_posting', 'Tanggal Posting')
        ]:
            print(f"{label:<30} : {detail.get(key, 'Tidak ditentukan')}")

        # Konfirmasi sebelum lanjut edit
        if input_konfirmasi("Apakah ingin mengedit lowongan ini?", ["Yes", "No"]) == "No":
            continue

        print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah field tertentu):")

        # Input baru (kosong = tidak update)
        judul = print_input_prompt("Judul").strip()
        deskripsi = print_input_prompt("Deskripsi").strip()
        nama_pt = print_input_prompt("Nama Perusahaan").strip()
        kontak = print_input_prompt("Kontak").strip()
        pengalaman = print_input_prompt("Pengalaman").strip()

        # Jenis (Magang/Kerja)
        jenis = None
        while True:
            jenis_input = print_input_prompt("Jenis (Magang/Kerja)").capitalize().strip()
            if not jenis_input: break
            if jenis_input in ["Magang", "Kerja"]:
                jenis = jenis_input
                break
            print("Jenis tidak valid! Pilihan hanya 'Magang' atau 'Kerja'.")

        # Deadline
        deadline = None
        while True:
            deadline_input = print_input_prompt("Deadline (YYYY-MM-DD)").strip()
            if not deadline_input: break
            try:
                parsed_date = datetime.date.fromisoformat(deadline_input)
                if parsed_date < datetime.date.today():
                    print("Tanggal sudah lewat!")
                    continue
                deadline = parsed_date.isoformat()
                break
            except ValueError:
                print("Format tanggal salah!")

        lokasi = print_input_prompt("Lokasi").strip()

        # Minimal Pendidikan
        min_pendidikan = None
        while True:
            min_pendidikan_input = print_input_prompt("Minimal Pendidikan").upper().replace(" ", "")
            if not min_pendidikan_input: break
            if min_pendidikan_input in mapping_pendidikan:
                min_pendidikan = mapping_pendidikan[min_pendidikan_input]
                break
            print("Pendidikan tidak valid!")

        # Jenis Kelamin
        jenis_kelamin = None
        while True:
            jenis_kelamin_input = print_input_prompt("Jenis Kelamin (L/P/Bebas)").upper().strip()
            if not jenis_kelamin_input: break
            if jenis_kelamin_input in gender_mapping:
                jenis_kelamin = gender_mapping[jenis_kelamin_input]
                break
            print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki, Perempuan, atau Bebas.")

        # Minimal dan Maksimal Umur
        minimal_umur = maksimal_umur = None
        while True:
            min_umur_input = print_input_prompt("Minimal Umur").strip()
            max_umur_input = print_input_prompt("Maksimal Umur").strip()
            if not min_umur_input and not max_umur_input: break
            try:
                min_val = int(min_umur_input) if min_umur_input else detail['minimal_umur']
                max_val = int(max_umur_input) if max_umur_input else detail['maksimal_umur']
                if max_val < min_val:
                    print("Maksimal umur tidak boleh lebih kecil dari minimal umur.")
                    continue
                minimal_umur, maksimal_umur = min_val, max_val
                break
            except ValueError:
                print("Masukkan angka valid!")

        # Slot
        slot = None
        while True:
            slot_input = print_input_prompt("Jumlah Slot").strip()
            if not slot_input: break
            if slot_input.isdigit() and int(slot_input) > 0:
                slot = int(slot_input)
                break
            print("Slot harus berupa angka > 0.")

        # Susun data update, hanya field yang diisi
        data_update = {}
        if judul: data_update['judul_lowongan'] = judul
        if deskripsi: data_update['deskripsi_pekerjaan'] = deskripsi
        if nama_pt: data_update['nama_perusahaan'] = nama_pt
        if kontak: data_update['kontak'] = kontak
        if pengalaman: data_update['pengalaman'] = pengalaman
        if jenis: data_update['jenis'] = jenis
        if deadline: data_update['deadline'] = deadline
        if lokasi: data_update['lokasi'] = lokasi
        if min_pendidikan: data_update['min_pendidikan'] = min_pendidikan
        if jenis_kelamin: data_update['jenis_kelamin'] = jenis_kelamin
        if minimal_umur is not None: data_update['minimal_umur'] = minimal_umur
        if maksimal_umur is not None: data_update['maksimal_umur'] = maksimal_umur
        if slot is not None: data_update['slot'] = slot

        if data_update:
            try:
                update_lowongan(selected_id, data_update)
                print("Data lowongan berhasil diperbarui!")
            except Exception as e:
                print(f"Gagal memperbarui data: {e}")
        else:
            print("Tidak ada perubahan yang dilakukan.")
        pause()

        if input_konfirmasi("Apakah ingin mengedit lowongan lain?", ["Yes", "No"]) == "No":
            break

# =========================== HAPUS LOWONGAN ===========================
def hapus_data_lowongan():
    while True:
        print_header("HAPUS LOWONGAN")
        data = get_all_lowongan()
        if not data: 
            pause()
            return

        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = print_input_prompt("Pilih nomor lowongan / 0 keluar").strip()
        if not pilih.isdigit(): continue
        pilih = int(pilih)
        if pilih == 0: break
        if pilih < 1 or pilih > len(data): continue

        selected_id = data[pilih-1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)
        if not detail: continue

        print_header("DETAIL LOWONGAN")
        for key, label in [
            ('lowongan_id', 'ID'), ('judul_lowongan', 'Judul'), ('nama_perusahaan', 'Perusahaan'),
            ('deskripsi_pekerjaan', 'Deskripsi'), ('jenis', 'Jenis'), 
            ('lokasi', 'Lokasi'), ('kontak', 'Kontak'), ('pengalaman', 'Pengalaman'),
            ('min_pendidikan', 'Minimal Pendidikan'), ('jenis_kelamin', 'Jenis Kelamin'),
            ('minimal_umur', 'Minimal Umur'), ('maksimal_umur', 'Maksimal Umur'),
            ('slot', 'Slot'), ('deadline', 'Deadline'), ('tanggal_posting', 'Tanggal Posting')
        ]:
            print(f"{label:<30} : {detail.get(key, 'Tidak ditentukan')}")

        if input_konfirmasi("Yakin ingin menghapus lowongan?", ["Yes","No"]) == "Yes":
            try:
                delete_lowongan(selected_id)
                print("Lowongan berhasil dihapus!")
            except Exception as e:
                print(f"Gagal menghapus lowongan: {e}")
        pause()

        if input_konfirmasi("Apakah ingin menghapus lowongan lain?", ["Yes","No"]) == "No":
            break

# =========================== REVIEW LAMARAN ===========================
def review_lamaran():
    kolom = ["nama_lengkap", "tanggal_lahir", "jenis_kelamin", "alamat", "email", "pengalaman", "pendidikan_terakhir"]
    while True:
        data = lihat_semua_lamaran()
        if not data:
            print("Belum ada lamaran untuk direview.")
            pause()
            return

        print_header("REVIEW LAMARAN")
        for row in data:
            print(f"[{row['lamaran_id']}] {row['nama_lengkap']} - {row['judul_lowongan']} ({row['status']})")

        id_lam = print_input_prompt("Masukkan ID lamaran / keluar").strip()
        if id_lam.lower() == "keluar": break
        if not id_lam.isdigit(): continue
        lamaran_terpilih = next((r for r in data if r['lamaran_id']==int(id_lam)), None)
        if not lamaran_terpilih:
            print("ID lamaran tidak ditemukan.")
            continue

        print_header("DETAIL LAMARAN")
        for key in kolom + ["judul_lowongan", "status"]:
            print(f"{key.replace('_',' ').capitalize():<30} : {lamaran_terpilih.get(key,'-')}")
        
        if input_konfirmasi("Ubah status lamaran?", ["Yes","No"]) == "Yes":
            status_baru = input_konfirmasi("Pilih status", ["Diterima","Ditolak"])
            ubah_status_lamaran(lamaran_terpilih['lamaran_id'], status_baru)
            print("Status lamaran berhasil diperbarui!")
        pause()

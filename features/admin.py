from database.admin_db import login_admin
from database.lamaran_db import lihat_semua_lamaran, ubah_status_lamaran
from database.lowongan_db import (
    get_all_lowongan, create_lowongan, update_lowongan,
    delete_lowongan, get_lowongan_by_id
)
import datetime
from utils.utils import print_header, print_input_prompt, input_angka, input_konfirmasi, pause

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

        pilih = print_input_prompt("Pilih lowongan / ketik [keluar]").strip().lower()
        if pilih == 'keluar':
            break
        if not pilih.isdigit():
            print("Input harus berupa angka.")
            continue
        pilih = int(pilih)
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
        print("Input tidak valid! Silakan isi minimal pendidikan(SMK/SMA, D3, D4/S1, dll)")

    gender_mapping = {'L': 'L', 'LAKI-LAKI': 'L','P': 'P', 'PEREMPUAN': 'P','B': 'Bebas', 'BEBAS': 'Bebas'}
    while True:
        jenis_kelamin_input = print_input_prompt("Jenis Kelamin (L/P/Bebas)").upper().strip()
        if jenis_kelamin_input in gender_mapping:
            jenis_kelamin = gender_mapping[jenis_kelamin_input]
            break
        print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki/L, Perempuan/P, atau Bebas/B.")

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

        pilih = print_input_prompt("Pilih lowongan / ketik [keluar]").strip().lower()
        if pilih == 'keluar': break
        if not pilih.isdigit(): continue
        pilih = int(pilih)
        if pilih < 1 or pilih > len(data): continue

        selected_id = data[pilih-1]['lowongan_id']
        detail = get_lowongan_by_id(selected_id)
        if not detail:
            print("Data lowongan tidak ditemukan.")
            pause()
            continue

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

        if input_konfirmasi("Apakah ingin mengedit lowongan ini?", ["Yes", "No"]) == "No":
            continue

        judul = print_input_prompt("Judul").strip()
        deskripsi = print_input_prompt("Deskripsi").strip()
        nama_pt = print_input_prompt("Nama Perusahaan").strip()
        kontak = print_input_prompt("Kontak").strip()
        pengalaman = print_input_prompt("Pengalaman").strip()

        jenis = None
        while True:
            jenis_input = print_input_prompt("Jenis (Magang/Kerja)").capitalize().strip()
            if not jenis_input: break
            if jenis_input in ["Magang", "Kerja"]:
                jenis = jenis_input
                break
            print("Jenis tidak valid! Pilihan hanya 'Magang' atau 'Kerja'.")

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

        min_pendidikan = None
        while True:
            min_pendidikan_input = print_input_prompt("Minimal Pendidikan").upper().replace(" ", "")
            if not min_pendidikan_input: break
            if min_pendidikan_input in mapping_pendidikan:
                min_pendidikan = mapping_pendidikan[min_pendidikan_input]
                break
            print("Pendidikan tidak valid!")

        jenis_kelamin = None
        while True:
            jenis_kelamin_input = print_input_prompt("Jenis Kelamin (L/P/Bebas)").upper().strip()
            if not jenis_kelamin_input: break
            if jenis_kelamin_input in gender_mapping:
                jenis_kelamin = gender_mapping[jenis_kelamin_input]
                break
            print("Jenis kelamin tidak valid! Pilihan hanya: Laki-Laki, Perempuan, atau Bebas.")

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

        slot = None
        while True:
            slot_input = print_input_prompt("Jumlah Slot").strip()
            if not slot_input: break
            if slot_input.isdigit() and int(slot_input) > 0:
                slot = int(slot_input)
                break
            print("Slot harus berupa angka > 0.")

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

def hapus_data_lowongan():
    while True:
        print_header("HAPUS LOWONGAN")
        data = get_all_lowongan()
        if not data: 
            pause()
            return

        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['judul_lowongan']} - {row['nama_perusahaan']} (Deadline: {row['deadline']})")

        pilih = print_input_prompt("Pilih lowongan / ketik [keluar]").strip().lower()
        if pilih == 'keluar': break
        if not pilih.isdigit(): continue
        pilih = int(pilih)
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

def review_lamaran():
    kolom = ["nama_lengkap", "tanggal_lahir", "jenis_kelamin", "alamat", "email", "pengalaman", "pendidikan_terakhir"]
    while True:
        data = lihat_semua_lamaran()
        if not data:
            print("Belum ada lamaran untuk direview.")
            pause()
            return

        data = sorted(data, key=lambda x: x['lamaran_id'])

        print_header("REVIEW LAMARAN")
        for i, row in enumerate(data, start=1):
            print(f"{i}. {row['nama_lengkap']} - {row['judul_lowongan']} ({row['status']})")

        pilih = print_input_prompt("Masukkan nomor lamaran / ketik [keluar]").strip().lower()
        if pilih == 'keluar': 
            break
        if not pilih.isdigit(): 
            continue

        pilih = int(pilih)
        if pilih < 1 or pilih > len(data):
            print("Nomor tidak valid.")
            continue

        lamaran_terpilih = data[pilih - 1]

        print_header("DETAIL LAMARAN")
        for key in kolom + ["judul_lowongan", "status"]:
            print(f"{key.replace('_',' ').capitalize():<30} : {lamaran_terpilih.get(key, '-')}")

        if lamaran_terpilih.get("status") == "AutoReject":
            alasan = lamaran_terpilih.get("alasan_reject", "Tidak ada alasan spesifik")
            print(f"{'Alasan Ditolak':<30}: {alasan}")
        
        if lamaran_terpilih.get("status") == "Diterima":
            print("\nLamaran ini sudah diterima, Silahkan review lamaran lain")
            pause()
            continue

        if input_konfirmasi("Apakah kamu ingin ubah status lamaran?", ["Yes", "No"]) == "Yes":
            status_baru = input_konfirmasi("Pilih status", ["Diterima", "Ditolak"])

            low_id = lamaran_terpilih["lowongan_id"]
            low = get_lowongan_by_id(low_id)

            if status_baru == "Diterima":
                if low and low["slot"] <= 0:
                    print("\nSlot lowongan ini sudah HABIS, tidak bisa menerima pelamar lagi!")
                    pause()
                    continue

            alasan = None
            if status_baru == "Ditolak":
                alasan = print_input_prompt("Masukkan alasan penolakan").strip()

            ubah_status_lamaran(
                lamaran_terpilih['lamaran_id'], 
                status_baru, 
                alasan_reject=alasan
            )

            print("Status lamaran berhasil diperbarui!")

            if status_baru == "Diterima":
                update_lowongan(low_id, {"slot": low["slot"] - 1})
                print(f"Slot lowongan berkurang! Sisa slot: {low['slot'] - 1}")

        pause()

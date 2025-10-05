from database.lamaran_db import lihat_semua_lamaran, ubah_status_lamaran
from database.lowongan_db import get_all_lowongan, create_lowongan, update_lowongan, delete_lowongan, get_lowongan_by_id
import datetime

def menu_admin():
    while True:
        print("\n" + "="*40)
        print("        === MENU ADMIN ===")
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
                if pilihan not in range (1,7):
                    print("Pilihan mu tidak valid! Mohon pilih menu 1-5")
                else:
                    break
            except ValueError:
                print ("Pilihan harus berupa integer! Tolong ulangi lagi")


        if pilihan == "1":
            tampilkan_lowongan()
        elif pilihan== "2":
            tambah_lowongan()
        elif pilihan == "3":
            edit_lowongan()
        elif pilihan == "4":
            hapus_data_lowongan()
        elif pilihan == "5":
            review_lamaran()
        elif pilihan == "6":
            print("Kembali ke menu utama...")
            break

# === CRUD LOWONGAN ===

def tampilkan_lowongan():
    data = get_all_lowongan()
    if not data:
        print("Belum ada data lowongan.")
        return
    print("\nDaftar Lowongan:")
    for row in data:
        print(f"[{row['lowongan_id']}] {row['judul_lowongan']} - {row['nama_perusahaan']} ({row['jenis']})")

def tambah_lowongan():
    print("\n=== TAMBAH LOWONGAN ===")
    judul = input("Judul: ")
    deskripsi = input("Deskripsi: ")
    nama_pt = input("Nama Perusahaan: ")
    jenis = input("Jenis (Magang/Kerja): ").capitalize()
    tanggal = datetime.date.today().isoformat()
    deadline = input("Deadline (YYYY-MM-DD): ")
    lokasi = input("Lokasi: ")
    min_pendidikan = input("Minimal Pendidikan: ")
    jenis_kelamin = input("Jenis Kelamin (Laki-Laki/Perempuan/Bebas): ")

    data = {
        'judul_lowongan': judul,
        'deskripsi_pekerjaan': deskripsi,
        'lokasi': lokasi,
        'jenis': jenis,
        'tanggal_posting': tanggal,
        'deadline': deadline,
        'nama_perusahaan': nama_pt,
        'min_pendidikan': min_pendidikan,
        'jenis_kelamin': jenis_kelamin
    }
    create_lowongan(data)
    print("Lowongan berhasil ditambahkan!")

def edit_lowongan():
    while True:
        print("\n=== UPDATE LOWONGAN ===")
        print("Ketik 'keluar' untuk kembali ke menu utama.")

        data = get_all_lowongan()
        if not data:
            print("Belum ada lowongan untuk diupdate.")
            return

        for row in data:
            print(f"[{row['lowongan_id']}] {row['judul_lowongan']} - {row['nama_perusahaan']} ({row['jenis']})")

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
        print(f"Judul       : {low['judul_lowongan']}")
        print(f"Perusahaan  : {low['nama_perusahaan']}")
        print(f"Jenis       : {low['jenis']}")
        print(f"Lokasi      : {low['lokasi']}")
        print(f"Deadline    : {low['deadline']}")

        print("\nMasukkan data baru (kosongkan jika tidak diubah):")

        fields = {}
        for field in [
            'judul_lowongan', 'deskripsi_pekerjaan', 'lokasi',
            'jenis', 'deadline', 'nama_perusahaan', 'min_pendidikan', 'jenis_kelamin'
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

        # tampilkan data pelamar terkait
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

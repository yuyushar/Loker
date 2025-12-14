# SI Lowker (Sistem Informasi Lowongan Kerja)

## GET WORK
**SI Lowker** adalah aplikasi berbasis Python yang digunakan untuk mempermudah proses pengelolaan lowongan pekerjaan dan magang. Aplikasi ini menyediakan fitur untuk admin dalam mengelola lowongan serta fitur bagi pelamar untuk mendaftar, melamar, dan melihat riwayat lamaran secara interaktif.

---

## SETUP

1. Pastikan Python 3.10+ sudah terinstall di komputer Anda.  
2. Install modul yang dibutuhkan menggunakan pip (virtual environment disarankan):
```bash
git clone [https://github.com/yuyushar/Loker.git](https://github.com/yuyushar/Loker.git)
cd nama-direktori-anda (seharusnya sesuai nama repository kita "Loker")
```
3. Jalankan aplikasi
```bash
python main.py
```
---

## STRUKTUR FOLDER APLIKASI
si_lowker/  
│  
├── main.py  
├── database/  
│   ├── connection.py  
│   ├── admin_db.py  
│   ├── pelamar_db.py  
│   ├── lowongan_db.py  
│   ├── lamaran_db.py  
│   └── si_lowker.db  
├── features/  
│   ├── admin.py  
│   └── pelamar.py  
├── utils  
│   └── utils.py  
└── README.md  

---

## PENGEMBANG

| No | Nama                       | NIM       | Pembagian Tugas |
|----|----------------------------|-----------|----------------|
| 1  | Angger Cahya Utama         | K3524044  | Membuat alur utama (main flow) aplikasi serta CRUD Lowongan untuk manajemen data lowongan kerja/magang. |
| 2  | Nadhif Athaasyam Nurdewana | K3524062  | Merancang dan membuat fitur pelamar serta CRUD Lamaran untuk transaksi lamaran kerja/magang. |
| 3  | Yusharyahya Al-Ghifari     | K3524070  | Merancang dan membuat database SQLite beserta koneksi, CRUD Admin, dan CRUD Pelamar untuk manajemen pengguna. |

### Contributor

[![Contributors](https://contrib.rocks/image?repo=yuyushar/loker)](https://github.com/yuyushar/loker/graphs/contributors)

---

## FITUR UTAMA

### Admin
- Login sebagai Admin
- Tambah Lowongan
- Lihat Lowongan
- Edit Lowongan
- Hapus Lowongan
- Review Lamaran

### Pelamar
- Login sebagai Pelamar
- Lihat Biodata
- Update Biodata
- Lamar Pekerjaan/Magang
- Lihat Riwayat Lamaran

---

## DIAGRAM ALUR PROGRAM

Berikut diagram flow yang menunjukan alur program ini berjalan. Dirancang menggunakan [Draw.io](https://app.diagrams.net)

![Flowchart SI Lowker](features/Alur-Fitur.png)

---

## DESAIN DATABASE

Hubungan relasi antar tabel dapat dilihat pada diagram berikut:

![ERD SI Lowker](database/ERD_SI-Loker.png)

---

## SUPPORT / SPONSOR
- Tidak ada

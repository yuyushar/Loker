import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "si_lowker.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

#KALAU MAU RESER NANTI DIBIKIN ULANG
def reset_database():
    """Menghapus file database lalu membuat ulang semua tabel"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🧹 Database lama dihapus.")
    create_tables()  # panggil ulang fungsi setup tabel
    print("✅ Database baru telah dibuat ulang.")

#INI BIKIN 
def create_tables():
    """Inisialisasi tabel di database"""
    conn = get_connection()
    cursor = conn.cursor()

    # ======= BUAT SEMUA TABEL =======
    cursor.executescript("""
    DROP TABLE IF EXISTS Lamaran;
    DROP TABLE IF EXISTS Lowongan;
    DROP TABLE IF EXISTS Pelamar;
    DROP TABLE IF EXISTS Admin;

    CREATE TABLE Admin (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

    INSERT INTO Admin (email, password) VALUES ('admin1@gmail.com', '123');

    CREATE TABLE Pelamar (
        pelamar_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_lengkap TEXT NOT NULL,
        tanggal_lahir TEXT NOT NULL,
        jenis_kelamin TEXT CHECK (jenis_kelamin IN ('L','P')) NOT NULL,
        alamat TEXT,
        email TEXT UNIQUE NOT NULL,
        pengalaman INTEGER DEFAULT 0,
        pendidikan_terakhir TEXT CHECK (
            pendidikan_terakhir IN ('Tidak Ada','SD','SMP','SMA/SMK','D1','D2','D3','D4/S1','S2','S3')
        ) NOT NULL
    );

    CREATE TABLE Lowongan (
        lowongan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul_lowongan TEXT NOT NULL,
        deskripsi_pekerjaan TEXT NOT NULL,
        lokasi TEXT,
        jenis TEXT CHECK (jenis IN ('Magang','Kerja')) NOT NULL,
        tanggal_posting TEXT NOT NULL,
        deadline TEXT NOT NULL,
        nama_perusahaan TEXT NOT NULL,
        syarat_ketentuan TEXT,
        kontak TEXT,
        slot INTEGER NOT NULL DEFAULT 1,
        min_pendidikan TEXT CHECK (
            min_pendidikan IN ('Tidak Ada','SD','SMP','SMA/SMK','D1','D2','D3','D4/S1','S2','S3')
        ) NOT NULL,
        jenis_kelamin TEXT CHECK (jenis_kelamin IN ('L','P','Bebas')) DEFAULT 'Bebas',
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
            ON DELETE CASCADE ON UPDATE CASCADE
    );

    CREATE TABLE Lamaran (
        lamaran_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lowongan_id INTEGER NOT NULL,
        pelamar_id INTEGER NOT NULL,
        tanggal_lamaran TEXT DEFAULT (datetime('now')),
        status TEXT CHECK (
            status IN ('Dikirim','Diverifikasi','Diterima','Ditolak','AutoReject')
        ) DEFAULT 'Dikirim',
        FOREIGN KEY (lowongan_id) REFERENCES Lowongan(lowongan_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (pelamar_id) REFERENCES Pelamar(pelamar_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE (lowongan_id, pelamar_id)
    );
    """)

    conn.commit()
    conn.close()
#COBA RESET DOANG
# reset_database()
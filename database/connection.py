import os
import sqlite3
from typing import List, Dict, Optional, Tuple, Any

# Lokasi file database
DB_PATH = os.path.join(os.path.dirname(__file__), "si_lowker.db")

# === KONEKSI DASAR ===
def get_connection() -> sqlite3.Connection:
    """Membuat koneksi ke database SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # supaya hasil fetch bisa jadi dict
    return conn

# === HELPER QUERY ===
# AMBIL SEMUA ISI TABLE
def fetch_all(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """Menjalankan SELECT dan mengembalikan banyak hasil (list of dict)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# AMBIL SALAH 1 DOANG
def fetch_one(query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
    """Menjalankan SELECT dan mengembalikan satu hasil (dict atau None)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# INSERT/UPDATE/DELETE
def execute_query(query: str, params: Tuple = (), return_id: bool = False) -> int:
    """
    Menjalankan INSERT/UPDATE/DELETE dan mengembalikan jumlah baris atau ID baru.
    - return_id=True → kembalikan lastrowid (berguna untuk INSERT)
    - return_id=False → kembalikan jumlah baris yang terpengaruh
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid if return_id else cur.rowcount
    finally:
        conn.close()

# === RESET & SETUP DATABASE ===
def reset_database():
    """Menghapus file database lalu membuat ulang semua tabel"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Database lama dihapus.")
    create_tables()
    print("Database baru telah dibuat ulang.")

def create_tables():
    """Inisialisasi tabel di database"""
    conn = get_connection()
    cursor = conn.cursor()

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
        pengalaman TEXT,
        riwayat_pendidikan TEXT NOT NULL
    );

    CREATE TABLE Lowongan (
        lowongan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul_lowongan TEXT NOT NULL,
        deskripsi_pekerjaan TEXT NOT NULL,
        lokasi TEXT,
        jenis TEXT CHECK (jenis IN ('Full Time','Part Time','Freelance')) NOT NULL,
        model_kerja TEXT CHECK (model_kerja IN ('Offline','Online','Hybrid')) NOT NULL DEFAULT 'Offline',
        tanggal_posting TEXT NOT NULL,
        deadline TEXT NOT NULL,
        nama_perusahaan TEXT NOT NULL,
        syarat_tambahan TEXT,
        kontak TEXT,
        slot INTEGER NOT NULL DEFAULT 1,
        min_pendidikan TEXT CHECK (
            min_pendidikan IN ('Tidak Ada','SD','SMP','SMA/SMK','D1','D2','D3','D4/S1','S2','S3')
        ) NOT NULL,
        jenis_kelamin TEXT CHECK (jenis_kelamin IN ('L','P','Bebas')) DEFAULT 'Bebas',
        pengalaman TEXT,
        minimal_umur INTEGER,
        maksimal_umur INTEGER,
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
            status IN ('Dikirim','Diterima','Ditolak','AutoReject')
        ) DEFAULT 'Dikirim',
        alasan_reject TEXT,
        FOREIGN KEY (lowongan_id) REFERENCES Lowongan(lowongan_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (pelamar_id) REFERENCES Pelamar(pelamar_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
        UNIQUE (lowongan_id, pelamar_id)
    );
    """)

    conn.commit()
    conn.close()

# Kalau mau test reset:
if __name__ == "__main__":
    reset_database()

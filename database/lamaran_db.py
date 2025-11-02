from .connection import get_connection
from typing import List, Dict, Optional

def tambah_lamaran(id_pelamar: int, id_lowongan: int, tanggal_lamaran: str) -> int:
    """Menambah data lamaran baru."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO lamaran (lowongan_id, pelamar_id, tanggal_lamaran)
        VALUES (?, ?, ?)
    """, (id_lowongan, id_pelamar, tanggal_lamaran))
    conn.commit()
    lamaran_id = cur.lastrowid
    conn.close()
    return lamaran_id

def lihat_semua_lamaran() -> List[Dict]:
    conn = get_connection()
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            l.lamaran_id,
            l.pelamar_id,
            l.lowongan_id,
            p.nama_lengkap,
            p.tanggal_lahir,
            p.jenis_kelamin,
            p.alamat,
            p.email,
            p.pengalaman,
            p.pendidikan_terakhir,
            lo.judul_lowongan,
            l.tanggal_lamaran,
            l.status
        FROM lamaran l
        JOIN pelamar p ON l.pelamar_id = p.pelamar_id
        JOIN lowongan lo ON l.lowongan_id = lo.lowongan_id
        ORDER BY l.tanggal_lamaran DESC
    """)
    hasil = cur.fetchall()
    conn.close()
    return hasil

def cari_lamaran_by_id(lamaran_id: int) -> Optional[Dict]:
    """Mencari lamaran berdasarkan ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lamaran WHERE lamaran_id = ?", (lamaran_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def ubah_status_lamaran(lamaran_id: int, status_baru: str) -> bool:
    """Mengubah status lamaran (Diterima, Ditolak, Menunggu, dsb)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE lamaran SET status = ?
        WHERE lamaran_id = ?
    """, (status_baru, lamaran_id))
    conn.commit()
    berhasil = cur.rowcount > 0
    conn.close()
    return berhasil
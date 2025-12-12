from .connection import get_connection
from typing import List, Dict, Optional

def tambah_lamaran(id_pelamar: int, id_lowongan: int, tanggal_lamaran: str, status="Dikirim", alasan_reject=None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO lamaran (lowongan_id, pelamar_id, tanggal_lamaran, status, alasan_reject)
        VALUES (?, ?, ?, ?, ?)
    """, (id_lowongan, id_pelamar, tanggal_lamaran, status, alasan_reject))
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
            p.riwayat_pendidikan,
            lo.judul_lowongan,
            lo.nama_perusahaan,
            l.tanggal_lamaran,
            l.status,
            l.alasan_reject
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

def ubah_status_lamaran(lamaran_id: int, status_baru: str, alasan_reject: str = None) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE lamaran 
        SET status = ?, alasan_reject = ?
        WHERE lamaran_id = ?
    """, (status_baru, alasan_reject, lamaran_id))
    conn.commit()
    berhasil = cur.rowcount > 0
    conn.close()
    return berhasil

# database/lowongan_db.py
from .connection import get_connection
from typing import List, Dict, Optional

def create_lowongan(data: Dict) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO lowongan (
            judul_lowongan, deskripsi_pekerjaan, lokasi, jenis, tanggal_posting, deadline,
            nama_perusahaan, syarat_ketentuan, kontak, slot, min_pendidikan, jenis_kelamin, admin_id
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data['judul_lowongan'], data['deskripsi_pekerjaan'], data.get('lokasi'),
            data['jenis'], data['tanggal_posting'], data['deadline'],
            data['nama_perusahaan'], data.get('syarat_ketentuan'), data.get('kontak'),
            data.get('slot',1), data['min_pendidikan'], data.get('jenis_kelamin','Bebas'),
            data.get('admin_id')
        ))
        conn.commit()
        lid = cur.lastrowid
        return lid
    finally:
        conn.close()

def get_all_lowongan() -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lowongan ORDER BY tanggal_posting DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_lowongan_by_id(lowongan_id: int) -> Optional[Dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_lowongan(lowongan_id: int, fields: Dict) -> bool:
    if not fields:
        return False
    keys = ", ".join(f"{k} = ?" for k in fields.keys())
    vals = list(fields.values())
    vals.append(lowongan_id)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE lowongan SET {keys} WHERE lowongan_id = ?", vals)
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

def delete_lowongan(lowongan_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

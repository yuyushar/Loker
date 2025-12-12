# database/lowongan_db.py
from typing import List, Dict, Optional
from .connection import fetch_all, fetch_one, execute_query

# Bikin Lowongan
def create_lowongan(data: Dict) -> int:
    query = """
    INSERT INTO lowongan (
        judul_lowongan, deskripsi_pekerjaan, lokasi, jenis, model_kerja, tanggal_posting, deadline,
        nama_perusahaan, syarat_tambahan, kontak, slot, min_pendidikan, jenis_kelamin,
        minimal_umur, maksimal_umur, pengalaman, admin_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data['judul_lowongan'], data['deskripsi_pekerjaan'], data.get('lokasi'),
        data['jenis'], data.get['model_kerja', 'Offline'], data['tanggal_posting'], data['deadline'],
        data['nama_perusahaan'], data.get('syarat_tambahan'), data.get('kontak'),
        data.get('slot', 1), data['min_pendidikan'], data.get('jenis_kelamin', 'Bebas'),
        data.get('minimal_umur'), data.get('maksimal_umur'), data.get('pengalaman'), data.get('admin_id')
    )
    return execute_query(query, params, return_id=True)

def get_all_lowongan() -> List[Dict]: 
    return fetch_all("SELECT * FROM lowongan ORDER BY lowongan_id ASC")

def get_lowongan_by_id(lowongan_id: int) -> Optional[Dict]: 
    return fetch_one("SELECT * FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))

def update_lowongan(lowongan_id: int, fields: Dict) -> bool:
    if not fields:
        return False
    keys = ", ".join(f"{k} = ?" for k in fields.keys())
    vals = list(fields.values())
    vals.append(lowongan_id)
    execute_query(f"UPDATE lowongan SET {keys} WHERE lowongan_id = ?", tuple(vals))
    return True

def delete_lowongan(lowongan_id: int) -> bool:
    execute_query("DELETE FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    return True

def kurangi_slot(lowongan_id: int) -> bool:
    row = fetch_one("SELECT slot FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    if not row:
        return False 
    current_slot = row["slot"]
    if current_slot <= 0:
        return False
    execute_query(
        "UPDATE lowongan SET slot = slot - 1 WHERE lowongan_id = ?", 
        (lowongan_id,)
    )
    return True

def is_lowongan_full(lowongan_id: int) -> bool:
    row = fetch_one("SELECT slot FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    if not row:
        return True 
    return row["slot"] <= 0

# database/lowongan_db.py
from typing import List, Dict, Optional
from .connection import fetch_all, fetch_one, execute_query

# Bikin Lowongan
def create_lowongan(data: Dict) -> int:
    query = """
    INSERT INTO lowongan (
        judul_lowongan, deskripsi_pekerjaan, lokasi, jenis, tanggal_posting, deadline,
        nama_perusahaan, syarat_tambahan, kontak, slot, min_pendidikan, jenis_kelamin,
        minimal_umur, maksimal_umur, pengalaman, admin_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data['judul_lowongan'], data['deskripsi_pekerjaan'], data.get('lokasi'),
        data['jenis'], data['tanggal_posting'], data['deadline'],
        data['nama_perusahaan'], data.get('syarat_tambahan'), data.get('kontak'),
        data.get('slot', 1), data['min_pendidikan'], data.get('jenis_kelamin', 'Bebas'),
        data.get('minimal_umur'), data.get('maksimal_umur'), data.get('pengalaman'), data.get('admin_id')
    )
    return execute_query(query, params, return_id=True)

#Liat lowongan
def get_all_lowongan() -> List[Dict]: #Semua lowongan
    return fetch_all("SELECT * FROM lowongan ORDER BY tanggal_posting DESC")

def get_lowongan_by_id(lowongan_id: int) -> Optional[Dict]: #Liat dari ID doang
    return fetch_one("SELECT * FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))

# Update lowongan
def update_lowongan(lowongan_id: int, fields: Dict) -> bool:
    if not fields:
        return False
    keys = ", ".join(f"{k} = ?" for k in fields.keys())
    vals = list(fields.values())
    vals.append(lowongan_id)
    execute_query(f"UPDATE lowongan SET {keys} WHERE lowongan_id = ?", tuple(vals))
    return True

# Hapus Lowongan
def delete_lowongan(lowongan_id: int) -> bool:
    execute_query("DELETE FROM lowongan WHERE lowongan_id = ?", (lowongan_id,))
    return True

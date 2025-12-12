from .connection import fetch_all, fetch_one, execute_query

# ==========================================================
#  CRUD untuk Tabel Pelamar
# ==========================================================

# TAMBAH PELAMAR BARU KE DATABASE
def tambah_pelamar(nama_lengkap, tanggal_lahir, jenis_kelamin, alamat, email,
                   pengalaman, riwayat_pendidikan):
    """Menambahkan pelamar baru ke database."""
    query = """
        INSERT INTO Pelamar (
            nama_lengkap, tanggal_lahir, jenis_kelamin,
            alamat, email, pengalaman, riwayat_pendidikan
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    data = (nama_lengkap, tanggal_lahir, jenis_kelamin,
            alamat, email, pengalaman, riwayat_pendidikan)

    result = execute_query(query, data)
    if result > 0:
        print("Biodata pelamar berhasil disimpan!")
    else:
        print("Gagal menambahkan pelamar.")

# LOGIN PELAMAR BERDASARKAN EMAIL & TANGGAL LAHIR
def login_pelamar(email, tanggal_lahir):
    """Login pelamar berdasarkan nama & tanggal lahir."""
    query = "SELECT * FROM Pelamar WHERE email = ? AND tanggal_lahir = ?"
    pelamar = fetch_one(query, (email, tanggal_lahir))
    return pelamar

# LIHAT BIODATA PELAMAR BERDASARKAN ID
def lihat_biodata(pelamar_id):
    """Melihat biodata pelamar berdasarkan ID."""
    query = "SELECT * FROM Pelamar WHERE pelamar_id = ?"
    biodata = fetch_one(query, (pelamar_id,))
    return biodata

# EDIT BIODATA PELAMAR BERDASARKAN ID
def edit_biodata(pelamar_id, **kwargs):
    """
    Edit biodata pelamar.
    Parameter dikirim dalam bentuk key=value, misalnya:
    edit_biodata(1, alamat='Jl. Merdeka', pengalaman=2)
    """
    if not kwargs:
        print("Tidak ada data yang diperbarui.")
        return
    
    fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values()) + [pelamar_id]

    query = f"UPDATE Pelamar SET {fields} WHERE pelamar_id = ?"
    result = execute_query(query, tuple(values))

    if result > 0:
        print("Biodata pelamar berhasil diperbarui!")
    else:
        print("Gagal mengedit biodata atau ID tidak ditemukan.")

#kalau nanti ada hapus pelamar, Saat ini tim pengembang belum kepikiran
def hapus_pelamar(pelamar_id):
    """Menghapus pelamar dari database."""
    query = "DELETE FROM Pelamar WHERE pelamar_id = ?"
    result = execute_query(query, (pelamar_id,))
    if result > 0:
        print(f"Pelamar dengan ID {pelamar_id} berhasil dihapus.")
    else:
        print("Pelamar tidak ditemukan.")

# ==========================================================
#  TESTING LANGSUNG DOANG!!
# ==========================================================
# if __name__ == "__main__":
#     print("=== TEST PELAMAR DB ===")

#     # Tambah pelamar baru
#     tambah_pelamar(
#         nama_lengkap="Budi Santoso",
#         tanggal_lahir="2001-04-10",
#         jenis_kelamin="L",
#         alamat="Jl. Mawar No. 12",
#         email="budi@example.com",
#         pengalaman=1,
#         riwayat_pendidikan="SMA/SMK"
#     )

#     # Coba login
#     hasil = login_pelamar("Budi Santoso", "2001-04-10")
#     if hasil:
#         print("Login berhasil:", dict(hasil))
#     else:
#         print("Login gagal!")

#     # Lihat biodata
#     if hasil:
#         bio = lihat_biodata(hasil["pelamar_id"])
#         print("Biodata Pelamar:", dict(bio))

#         # Edit biodata
#         edit_biodata(hasil["pelamar_id"], alamat="Jl. Melati No. 45", pengalaman=2)

#         # Lihat ulang
#         bio2 = lihat_biodata(hasil["pelamar_id"])
#         print("Biodata setelah edit:", dict(bio2))
#         hapus_pelamar(1)

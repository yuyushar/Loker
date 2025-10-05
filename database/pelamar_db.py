from .connection import get_connection

# ==========================================================
#  CRUD untuk Tabel Pelamar
# ==========================================================

def tambah_pelamar(nama_lengkap, tanggal_lahir, jenis_kelamin, alamat, email,
                   pengalaman, pendidikan_terakhir):
    """Menambahkan pelamar baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Pelamar (
                nama_lengkap, tanggal_lahir, jenis_kelamin,
                alamat, email, pengalaman, pendidikan_terakhir
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nama_lengkap, tanggal_lahir, jenis_kelamin,
              alamat, email, pengalaman, pendidikan_terakhir))

        conn.commit()
        print("Biodata pelamar berhasil disimpan!")
    except Exception as e:
        print("Gagal menambahkan pelamar:", e)
    finally:
        conn.close()


def login_pelamar(nama_lengkap, tanggal_lahir):
    """Login pelamar berdasarkan nama & tanggal lahir."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Pelamar
        WHERE nama_lengkap = ? AND tanggal_lahir = ?
    """, (nama_lengkap, tanggal_lahir))
    pelamar = cursor.fetchone()

    conn.close()
    return pelamar


def lihat_biodata(pelamar_id):
    """Melihat biodata pelamar berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Pelamar WHERE pelamar_id = ?", (pelamar_id,))
    data = cursor.fetchone()

    conn.close()
    return data


def edit_biodata(pelamar_id, **kwargs):
    """
    Edit biodata pelamar.
    Parameter dikirim dalam bentuk key=value, misalnya:
    edit_biodata(1, alamat='Jl. Merdeka', pengalaman=2)
    """
    conn = get_connection()
    cursor = conn.cursor()

    fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(pelamar_id)

    query = f"UPDATE Pelamar SET {fields} WHERE pelamar_id = ?"

    try:
        cursor.execute(query, tuple(values))
        conn.commit()
        print("Biodata pelamar berhasil diperbarui!")
    except Exception as e:
        print("Gagal mengedit biodata:", e)
    finally:
        conn.close()

#kalau nanti ada hapus pelamar buat tugasnya keknya blm perlu
def hapus_pelamar(pelamar_id):
    """Menghapus pelamar dari database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Pelamar WHERE pelamar_id = ?", (pelamar_id,))
    conn.commit()
    conn.close()
    print(f"Pelamar ID {pelamar_id} berhasil dihapus.")


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
#         pendidikan_terakhir="SMA/SMK"
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

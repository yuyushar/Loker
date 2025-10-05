from .connection import get_connection

# ==========================================================
#  CRUD untuk Tabel Admin
# ==========================================================

def login_admin(email, password):
    """Cek apakah email dan password cocok di database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Admin WHERE email = ? AND password = ?", (email, password))
    admin = cursor.fetchone()

    conn.close()
    return admin 
    """kalau tidak ditemukan jadine None, tapi karena admin 
    pasti tersedia dan hanya 1 jadi ga kepake untuk saat ini"""   


def tambah_admin(email, password):
    """Tambah admin baru."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Admin (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        print("Admin berhasil ditambahkan!")
    except Exception as e:
        print("Gagal menambahkan admin:", e)
    finally:
        conn.close()


def lihat_admin():
    """Tampilkan semua admin terdaftar."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT admin_id, email FROM Admin")
    admins = cursor.fetchall()

    conn.close()
    return admins

# SAAT INI GA DIPAKE SOALNYA ADMIIN CUMAN 1
def hapus_admin(admin_id):
    """Hapus admin berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Admin WHERE admin_id = ?", (admin_id,))
    conn.commit()
    conn.close()

    print(f"Admin dengan ID {admin_id} berhasil dihapus.")


# ==========================================================
#  TESTING LANGSUNG NYOBA DOANG
# ==========================================================
# if __name__ == "__main__":
#     print("=== TEST ADMIN DB ===")

#     # Lihat daftar admin awal
#     print("Daftar admin sekarang:")
#     for a in lihat_admin():
#         print(dict(a))
#     # # Coba login
#     email=input("Masukkan email: ")
#     password=input("Masukkan Password: ")
#     login=login_admin(email,password)
#     if login:
#         print(f"Login berhasil sebagai: {login['email']}")
#     hasil = login_admin("admin1@gmail.com", "123")
#     if hasil:
#         print(f"Login berhasil sebagai: {hasil['email']}")
#     else:
#         print("Login gagal!")

#     # Lihat ulang daftar admin
#     print("\nAdmin terdaftar:")
#     for a in lihat_admin():
#         print(dict(a))

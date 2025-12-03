from .connection import fetch_all, fetch_one, execute_query

# ==========================================================
#  CRUD untuk Tabel Admin
# ==========================================================

# YANG INI DIPAKE BUAT LOGIN ADMIN SAAT APLIKASI DIMULAI
def login_admin(email, password):
    """Cek apakah email dan password cocok di database."""
    query = "SELECT * FROM Admin WHERE email = ? AND password = ?"
    admin = fetch_one(query, (email, password))
    return admin 
    """kalau tidak ditemukan jadine None, tapi karena admin 
    pasti tersedia dan hanya 1 jadi ga kepake untuk saat ini"""   

# TAMBAH ADMIN BARU
# SAAT INI GA DIPAKE KARENA ADMIN CUMA 1
def tambah_admin(email, password):
    """Tambah admin baru."""
    query = "INSERT INTO Admin (email, password) VALUES (?, ?)"
    result = execute_query(query, (email, password))
    if result > 0:
        print("Admin berhasil ditambahkan!")
    else:
        print("Gagal menambahkan admin.")

# LIHAT SEMUA ADMIN
# SAAT INI GA DIPAKE KARENA ADMIN CUMA 1, DAN DI FITUR PROGRAM GA PERLU LIHAT ADMIN
def lihat_admin():
    """Tampilkan semua admin terdaftar."""
    query = "SELECT admin_id, email FROM Admin"
    admins = fetch_all(query)
    return admins

# SAAT INI GA DIPAKE SOALNYA ADMIIN CUMAN 1
# DELETE BERDASARKAN ID
def hapus_admin(admin_id):
    """Hapus admin berdasarkan ID."""
    query = "DELETE FROM Admin WHERE admin_id = ?"
    result = execute_query(query, (admin_id,))
    if result > 0:
        print(f"Admin dengan ID {admin_id} berhasil dihapus.")
    else:
        print("Admin tidak ditemukan.")
        
# SAAT INI GA DIPAKE KARENA TIDAK ADA KEBUTUHAN UPDATE UNTUK ADMIN
# UPDATE BISA UNTUK EMAIL ATAU PASSWORD ATAU KEDUANYA SEKALIGUS
def update_admin(admin_id, email=None, password=None):
    """
    Edit admin berdasarkan ID.
    Bisa update email, password, atau keduanya.
    """
    if not email and not password:
        print("Tidak ada data yang diperbarui.")
        return
    
    fields = []
    params = []

    if email:
        fields.append("email = ?")
        params.append(email)

    if password:
        fields.append("password = ?")
        params.append(password)

    params.append(admin_id)

    query = f"UPDATE Admin SET {', '.join(fields)} WHERE admin_id = ?"
    result = execute_query(query, tuple(params))

    if result > 0:
        print("Data admin berhasil diperbarui.")
    else:
        print("Gagal memperbarui admin / ID tidak ditemukan.")

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
#     # # Coba edit admin
#     update_admin(1,password="12345")
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

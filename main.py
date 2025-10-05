from database.connection import setup_database
from database import admin_db
from features import admin as admin_feat
from features import pelamar as pelamar_feat

def ensure_admin_exists():
    # Membuat admin default jika belum ada (email: admin@admin.com, password: admin)
    a = admin_db.get_admin_by_email("admin@admin.com")
    if not a:
        admin_db.create_admin("admin@admin.com", "admin")
        print("Default admin created -> email: admin@admin.com password: admin")

def main_menu():
    setup_database()
    ensure_admin_exists()
    while True:
        try:
            print("\n=== SI LOWONGAN - MENU UTAMA ===")
            print("1. Masuk sebagai Admin")
            print("2. Masuk sebagai Pelamar")
            print("3. Keluar")
            choice = input("Pilih opsi: ").strip()
            if choice == "1":
                admin_login()
            elif choice == "2":
                pelamar_feat.pelamar_menu()
            elif choice == "3":
                sure = input("Konfirmasi keluar? (yes/no): ").strip().lower()
                if sure == "yes":
                    print("Terima kasih. Program selesai.")
                    break
                else:
                    continue
            else:
                print("Pilihan tidak valid.")
        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh user.")
            break
        except Exception as e:
            print(f"Terjadi error: {e}")

def admin_login():
    print("\n== Login Admin ==")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    aid = admin_db.validate_admin(email, password)
    if aid:
        print("Login berhasil.")
        admin_feat.admin_menu(aid)
    else:
        print("Login gagal. Periksa email/password.")

if __name__ == "__main__":
    main_menu()
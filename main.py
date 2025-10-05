from features import admin as admin_feat
from features import pelamar as pelamar_feat

def main_menu():
    while True:
        try:
            print("\n=== SI LOWONGAN - MENU UTAMA ===")
            print("1. Masuk sebagai Admin")
            print("2. Masuk sebagai Pelamar")
            print("3. Daftar sebagai Pelamar")
            print("4. Keluar")
            choice = input("Pilih opsi: ").strip()
            if choice == "1":
                admin_feat.menu_admin()
            elif choice == "2":
                pelamar_feat.menu_pelamar()
            elif choice == "3":
                pelamar_feat.daftar_pelamar()
            elif choice == "4":
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

if __name__ == "__main__":
    main_menu()
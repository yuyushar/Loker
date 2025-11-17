from features import admin as admin_feat
from features import pelamar as pelamar_feat
from utils.utils import print_header, print_input_prompt, input_konfirmasi

def main_menu():
    while True:
        try:
            print_header("SI LOWONGAN - MENU UTAMA")
            print("1. Masuk sebagai Admin")
            print("2. Masuk sebagai Pelamar")
            print("3. Keluar")
            choice = print_input_prompt("Pilih opsi")

            if choice == "1":
                try:
                    admin_feat.menu_admin()
                except AttributeError:
                    print("Fitur admin belum lengkap (menu_admin tidak ditemukan).")
            elif choice == "2":
                try:
                    pelamar_feat.menu_pelamar()
                except AttributeError:
                    print("Fitur pelamar belum lengkap (menu_pelamar tidak ditemukan).")
            elif choice == "3":
                while True:
                    try:
                        konfirmasi = input_konfirmasi("Yakin ingin keluar?",["Yes","No"]).title().replace(" ","")
                        if konfirmasi == "Yes":
                            print("Terima kasih. Program selesai.")
                            break
                        elif konfirmasi== "No" :
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
def print_header(judul: str):
    print("\n" + "="*60)
    print(f"{judul:^60}")
    print("="*60)

def print_input_prompt(prompt: str):
    try:
        return input(f"{prompt:<30}: ")
    except KeyboardInterrupt:
        raise  

def input_angka(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(print_input_prompt(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Pilihan tidak valid! Mohon pilih angka {min_val}-{max_val}.")
                continue
            return val
        except ValueError:
            print("Input harus berupa angka!")

def input_konfirmasi(prompt, options):
    options_str = '/'.join(options)
    while True:
        val = input(f"{f'{prompt} [{options_str}]':<30}: ").strip().capitalize()
        if val in options:
            return val
        print(f"Input tidak valid! Pilih salah satu: {options_str}")

def pause():
    input("\nTekan [Enter] untuk kembali...")
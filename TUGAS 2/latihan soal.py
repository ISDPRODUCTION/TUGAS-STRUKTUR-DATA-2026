# ============================================================
#                   LATIHAN SOAL - PYTHON
# ============================================================

import os

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')


# ============================================================
# SOAL 1 — DEDUPLIKASI
# Menghapus duplikat dari list, mempertahankan urutan kemunculan pertama
# ============================================================

def deduplikasi(data: list) -> list:
    terlihat = set()
    hasil = []
    for item in data:
        if item not in terlihat:
            terlihat.add(item)
            hasil.append(item)
    return hasil


# ============================================================
# SOAL 2 — INTERSECTION DUA ARRAY
# Mengembalikan elemen yang muncul di kedua list
# ============================================================

def intersection(list_a: list, list_b: list) -> list:
    set_b = set(list_b)
    hasil = []
    terlihat = set()
    for item in list_a:
        if item in set_b and item not in terlihat:
            hasil.append(item)
            terlihat.add(item)
    return hasil


# ============================================================
# SOAL 3 — ANAGRAM CHECK
# Memeriksa apakah dua string adalah anagram menggunakan dict
# ============================================================

def hitung_karakter(teks: str) -> dict:
    hitungan = {}
    for huruf in teks.lower().replace(" ", ""):
        hitungan[huruf] = hitungan.get(huruf, 0) + 1
    return hitungan

def cek_anagram(kata1: str, kata2: str) -> bool:
    return hitung_karakter(kata1) == hitung_karakter(kata2)


# ============================================================
# SOAL 4 — FIRST RECURRING CHARACTER
# Menemukan karakter pertama yang muncul lebih dari sekali
# ============================================================

def karakter_berulang_pertama(teks: str):
    terlihat = set()
    for huruf in teks:
        if huruf in terlihat:
            return huruf
        terlihat.add(huruf)
    return None  # tidak ada karakter berulang


# ============================================================
# SOAL 5 — SIMULASI BUKU TELEPON
# Program menu: tambah kontak, cari kontak, tampilkan semua
# ============================================================

class BukuTelepon:
    def __init__(self):
        self.kontak = {}

    def tambah_kontak(self, nama: str, nomor: str):
        self.kontak[nama.lower()] = {"nama": nama, "nomor": nomor}
        print(f"  ✔ Kontak '{nama}' berhasil ditambahkan.")

    def cari_kontak(self, nama: str):
        hasil = self.kontak.get(nama.lower())
        if hasil:
            print(f"  ✔ Ditemukan → {hasil['nama']} : {hasil['nomor']}")
        else:
            print(f"  ✘ Kontak '{nama}' tidak ditemukan.")

    def tampilkan_semua(self):
        if not self.kontak:
            print("  (Buku telepon masih kosong)")
        else:
            print(f"  {'No.':<5} {'Nama':<20} {'Nomor'}")
            print("  " + "-" * 40)
            for i, data in enumerate(self.kontak.values(), 1):
                print(f"  {i:<5} {data['nama']:<20} {data['nomor']}")

    def jalankan(self):
        while True:
            print("\n  ╔══════════════════════════╗")
            print("  ║     BUKU TELEPON         ║")
            print("  ╠══════════════════════════╣")
            print("  ║  1. Tambah kontak        ║")
            print("  ║  2. Cari kontak          ║")
            print("  ║  3. Tampilkan semua      ║")
            print("  ║  4. Kembali ke menu utama║")
            print("  ╚══════════════════════════╝")

            pilihan = input("\n  Pilihan: ").strip()

            if pilihan == '1':
                nama  = input("  Nama   : ").strip()
                nomor = input("  Nomor  : ").strip()
                if nama and nomor:
                    self.tambah_kontak(nama, nomor)
                else:
                    print("  ✘ Nama dan nomor tidak boleh kosong.")

            elif pilihan == '2':
                nama = input("  Cari nama: ").strip()
                self.cari_kontak(nama)

            elif pilihan == '3':
                print()
                self.tampilkan_semua()

            elif pilihan == '4':
                break
            else:
                print("  ✘ Pilihan tidak valid.")


# ============================================================
#                      MENU UTAMA
# ============================================================

def demo_soal1():
    print("\n" + "=" * 50)
    print("  SOAL 1 — DEDUPLIKASI")
    print("=" * 50)

    contoh = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"  Input  : {contoh}")
    print(f"  Output : {deduplikasi(contoh)}")

    contoh2 = ["apel", "pisang", "apel", "mangga", "pisang", "jeruk"]
    print(f"\n  Input  : {contoh2}")
    print(f"  Output : {deduplikasi(contoh2)}")

    # Input dari user
    print()
    raw = input("  Coba sendiri — masukkan angka dipisah spasi: ")
    user_list = raw.strip().split()
    print(f"  Hasil  : {deduplikasi(user_list)}")


def demo_soal2():
    print("\n" + "=" * 50)
    print("  SOAL 2 — INTERSECTION DUA ARRAY")
    print("=" * 50)

    a = [1, 2, 3, 4, 5]
    b = [3, 4, 5, 6, 7]
    print(f"  List A : {a}")
    print(f"  List B : {b}")
    print(f"  Irisan : {intersection(a, b)}")

    a2 = ["kucing", "anjing", "kelinci", "hamster"]
    b2 = ["anjing", "ikan", "kelinci"]
    print(f"\n  List A : {a2}")
    print(f"  List B : {b2}")
    print(f"  Irisan : {intersection(a2, b2)}")


def demo_soal3():
    print("\n" + "=" * 50)
    print("  SOAL 3 — ANAGRAM CHECK")
    print("=" * 50)

    pasangan = [
        ("listen", "silent"),
        ("hello",  "world"),
        ("Astronomer", "Moon starer"),
        ("python", "typhon"),
    ]
    for k1, k2 in pasangan:
        hasil = "✔ ANAGRAM" if cek_anagram(k1, k2) else "✘ BUKAN anagram"
        print(f"  '{k1}' & '{k2}' → {hasil}")

    # Input dari user
    print()
    k1 = input("  Coba sendiri — Kata 1: ").strip()
    k2 = input("                 Kata 2: ").strip()
    hasil = "✔ ANAGRAM" if cek_anagram(k1, k2) else "✘ BUKAN anagram"
    print(f"  Hasil  : {hasil}")


def demo_soal4():
    print("\n" + "=" * 50)
    print("  SOAL 4 — FIRST RECURRING CHARACTER")
    print("=" * 50)

    contoh_list = ["abcdef", "aabbcc", "abcdea", "xyz", "programming"]
    for teks in contoh_list:
        hasil = karakter_berulang_pertama(teks)
        if hasil:
            print(f"  '{teks}' → karakter berulang pertama: '{hasil}'")
        else:
            print(f"  '{teks}' → tidak ada karakter berulang")

    # Input dari user
    print()
    teks = input("  Coba sendiri — masukkan string: ").strip()
    hasil = karakter_berulang_pertama(teks)
    if hasil:
        print(f"  Hasil  : karakter berulang pertama adalah '{hasil}'")
    else:
        print("  Hasil  : tidak ada karakter berulang")


def demo_soal5():
    print("\n" + "=" * 50)
    print("  SOAL 5 — SIMULASI BUKU TELEPON")
    print("=" * 50)
    buku = BukuTelepon()
    buku.jalankan()


def menu_utama():
    bersihkan_layar()
    while True:
        print("\n" + "=" * 50)
        print("        LATIHAN SOAL PYTHON")
        print("=" * 50)
        print("  1. Deduplikasi")
        print("  2. Intersection Dua Array")
        print("  3. Anagram Check")
        print("  4. First Recurring Character")
        print("  5. Simulasi Buku Telepon")
        print("  0. Keluar")
        print("=" * 50)

        pilihan = input("  Pilih soal (0–5): ").strip()

        menu = {
            '1': demo_soal1,
            '2': demo_soal2,
            '3': demo_soal3,
            '4': demo_soal4,
            '5': demo_soal5,
        }

        if pilihan == '0':
            print("\n  Sampai jumpa!\n")
            break
        elif pilihan in menu:
            menu[pilihan]()
            if pilihan != '5':
                input("\n  Tekan Enter untuk kembali ke menu...")
                bersihkan_layar()
        else:
            print("  ✘ Pilihan tidak valid.")


if __name__ == "__main__":
    menu_utama()
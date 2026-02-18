import numpy as np
import time
import os


def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')


class KehidupanConway:
    def __init__(self, tinggi=25, lebar=50):
        """
        Membuat papan simulasi baru.

        Parameters:
        tinggi : jumlah baris pada papan
        lebar  : jumlah kolom pada papan
        """
        self.tinggi = tinggi
        self.lebar = lebar
        self.papan = np.zeros((tinggi, lebar), dtype=int)

    def tempel_pola(self, pola, titik_awal=(0, 0)):
        """
        Menempelkan sebuah pola ke papan di posisi tertentu.

        Parameters:
        pola       : array 2D berisi pola sel
        titik_awal : tuple (baris, kolom) sebagai posisi kiri atas pola
        """
        h, w = pola.shape
        b, k = titik_awal
        self.papan[b:b+h, k:k+w] = pola

    def isi_acak(self, kepadatan=0.3):
        """
        Mengisi papan dengan sel hidup secara acak.

        Parameters:
        kepadatan : proporsi sel yang hidup (antara 0.0 dan 1.0)
        """
        self.papan = np.random.choice(
            [0, 1],
            size=(self.tinggi, self.lebar),
            p=[1 - kepadatan, kepadatan]
        )

    def hitung_tetangga(self, baris, kolom):
        """
        Menghitung jumlah sel hidup di sekitar satu sel (batas melingkar).
        """
        total = 0
        for db in range(-1, 2):
            for dk in range(-1, 2):
                if db == 0 and dk == 0:
                    continue
                b = (baris + db) % self.tinggi
                k = (kolom + dk) % self.lebar
                total += self.papan[b, k]
        return total

    def langkah_berikutnya(self):
        """
        Memperbarui papan ke generasi berikutnya sesuai aturan Conway.
        """
        papan_baru = np.zeros((self.tinggi, self.lebar), dtype=int)

        for b in range(self.tinggi):
            for k in range(self.lebar):
                n = self.hitung_tetangga(b, k)

                if self.papan[b, k] == 1 and n in (2, 3):
                    papan_baru[b, k] = 1
                elif self.papan[b, k] == 0 and n == 3:
                    papan_baru[b, k] = 1

        self.papan = papan_baru

    def tampilkan_konsol(self, generasi=None):
        """
        Menampilkan isi papan ke terminal.
        """
        judul = f"Conway's Game of Life"
        if generasi is not None:
            judul += f" — Generasi {generasi}"

        garis = "═" * (self.lebar * 2 + 2)
        print(judul.center(self.lebar * 2 + 2))
        print(garis)

        for baris in self.papan:
            print('║' + ' '.join(['■' if sel else ' ' for sel in baris]) + '║')

        print(garis)
        print(f"  Ukuran papan: {self.tinggi} x {self.lebar}  |  "
              f"Sel hidup: {int(self.papan.sum())}")

    def jalankan_terminal(self, maks_generasi=100, jeda_detik=0.15):
        """
        Menjalankan simulasi langsung di terminal dengan animasi teks.

        Parameters:
        maks_generasi : batas jumlah generasi
        jeda_detik    : jeda waktu antar generasi (dalam detik)
        """
        for gen in range(maks_generasi + 1):
            bersihkan_layar()
            self.tampilkan_konsol(generasi=gen)
            print("\n  Tekan Ctrl+C untuk berhenti.")

            if gen < maks_generasi:
                time.sleep(jeda_detik)
                self.langkah_berikutnya()


# ========== KOLEKSI POLA ==========

BLOK = np.array([
    [1, 1],
    [1, 1]
])

SARANG_LEBAH = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

BERKEDIP = np.array([
    [1, 1, 1]
])

KODOK = np.array([
    [0, 1, 1, 1],
    [1, 1, 1, 0]
])

PULSAR = np.array([
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
])

PELUNCUR = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1]
])

KAPAL_RINGAN = np.array([
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0]
])

CONTOH_1 = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
])

CONTOH_STABIL = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])


# ========== FUNGSI DEMO ==========

def demo_acak():
    print("Demo: Pola Acak")
    sim = KehidupanConway(25, 60)
    sim.isi_acak(kepadatan=0.3)
    sim.jalankan_terminal(maks_generasi=200, jeda_detik=0.1)

def demo_peluncur():
    print("Demo: Peluncur / Glider")
    sim = KehidupanConway(25, 50)
    sim.tempel_pola(PELUNCUR, titik_awal=(2, 2))
    sim.jalankan_terminal(maks_generasi=100, jeda_detik=0.2)

def demo_pulsar():
    print("Demo: Pulsar (Osilator)")
    sim = KehidupanConway(25, 40)
    sim.tempel_pola(PULSAR, titik_awal=(6, 13))
    sim.jalankan_terminal(maks_generasi=50, jeda_detik=0.3)

def demo_campuran():
    print("Demo: Berbagai Pola Sekaligus")
    sim = KehidupanConway(30, 60)
    sim.tempel_pola(PELUNCUR,  titik_awal=(2, 2))
    sim.tempel_pola(BERKEDIP,  titik_awal=(10, 20))
    sim.tempel_pola(BLOK,      titik_awal=(20, 40))
    sim.tempel_pola(KODOK,     titik_awal=(15, 10))
    sim.jalankan_terminal(maks_generasi=150, jeda_detik=0.15)

def demo_soal():
    print("Demo: Contoh dari Soal (step-by-step)")
    sim = KehidupanConway(10, 15)
    sim.tempel_pola(CONTOH_1, titik_awal=(3, 6))

    for gen in range(3):
        bersihkan_layar()
        sim.tampilkan_konsol(generasi=gen)
        input("\n  Tekan Enter untuk lanjut ke generasi berikutnya...")
        sim.langkah_berikutnya()

def demo_stabil():
    print("Demo: Pola Stabil dari Soal")
    sim = KehidupanConway(15, 20)
    sim.tempel_pola(CONTOH_STABIL, titik_awal=(5, 8))
    sim.jalankan_terminal(maks_generasi=30, jeda_detik=0.5)


# ========== TITIK MASUK PROGRAM ==========

if __name__ == "__main__":
    bersihkan_layar()
    print("=" * 50)
    print("       CONWAY'S GAME OF LIFE — TERMINAL")
    print("=" * 50)
    print()
    print("  1. Pola Acak")
    print("  2. Peluncur / Glider")
    print("  3. Pulsar (Osilator)")
    print("  4. Berbagai Pola Sekaligus")
    print("  5. Contoh dari Soal (step-by-step)")
    print("  6. Pola Stabil dari Soal")
    print()

    pilihan = input("  Masukkan pilihan (1–6): ").strip()

    menu = {
        '1': demo_acak,
        '2': demo_peluncur,
        '3': demo_pulsar,
        '4': demo_campuran,
        '5': demo_soal,
        '6': demo_stabil,
    }

    aksi = menu.get(pilihan)
    try:
        if aksi:
            aksi()
        else:
            print("  Pilihan tidak dikenali. Menjalankan pola acak...")
            demo_acak()
    except KeyboardInterrupt:
        print("\n\n  Simulasi dihentikan. Sampai jumpa!")
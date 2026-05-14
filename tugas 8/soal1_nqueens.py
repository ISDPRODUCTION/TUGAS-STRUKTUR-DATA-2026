"""
===========================================
  SOAL 1 - N-QUEENS (N-RATU)
  Algoritma Backtracking Rekursif
===========================================
"""

def solve_nqueens(n):
    """
    Mencari semua solusi N-Queens pada papan n x n.
    Mengembalikan list of list, di mana setiap elemen
    adalah posisi kolom ratu di setiap baris.
    """
    board = [0] * n
    solutions = []
    calls = [0]

    def is_safe(row, col):
        """Periksa apakah aman menempatkan ratu di (row, col)."""
        for r in range(row):
            if (board[r] == col or                      # kolom sama
                board[r] - col == r - row or             # diagonal kiri-atas
                board[r] - col == row - r):              # diagonal kanan-atas
                return False
        return True

    def backtrack(row):
        """Rekursif: coba tempatkan ratu di setiap kolom pada baris ini."""
        calls[0] += 1
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                # board[row] akan ditimpa, tidak perlu reset eksplisit

    backtrack(0)
    return solutions, calls[0]


def print_board(solution, n):
    """Cetak papan catur dengan posisi ratu."""
    border = "+" + ("---+" * n)
    print(border)
    for row in range(n):
        col = solution[row]
        row_str = "|"
        for c in range(n):
            if c == col:
                row_str += " Q |"
            else:
                # warna papan catur (. untuk gelap, ' ' untuk terang)
                row_str += " . |" if (row + c) % 2 == 0 else "   |"
        print(row_str)
        print(border)


def main():
    print("=" * 45)
    print("       PROGRAM N-QUEENS (N-RATU)")
    print("       Algoritma Backtracking Rekursif")
    print("=" * 45)

    while True:
        try:
            n = int(input("\nMasukkan ukuran papan (N >= 4): "))
            if n < 1:
                print("  [!] N harus bilangan positif.")
                continue
            break
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    print(f"\n  Mencari solusi untuk papan {n}x{n}...")
    solutions, total_calls = solve_nqueens(n)

    print(f"\n  Total rekursi dipanggil : {total_calls:,}")
    print(f"  Total solusi ditemukan  : {len(solutions)}")

    if not solutions:
        print(f"\n  [!] Tidak ada solusi untuk N={n}.")
        return

    print(f"\n  Tersedia {len(solutions)} solusi.")
    while True:
        try:
            pilihan = int(input(f"  Tampilkan solusi ke berapa? (1-{len(solutions)}, 0=semua): "))
            if 0 <= pilihan <= len(solutions):
                break
            print(f"  [!] Pilih antara 0 dan {len(solutions)}.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    if pilihan == 0:
        for i, sol in enumerate(solutions):
            print(f"\n  ===== Solusi {i+1} dari {len(solutions)} =====")
            print(f"  Posisi kolom ratu: {sol}")
            print_board(sol, n)
    else:
        sol = solutions[pilihan - 1]
        print(f"\n  ===== Solusi {pilihan} dari {len(solutions)} =====")
        print(f"  Posisi kolom ratu: {sol}")
        print(f"  (Indeks 0 = kolom pertama)")
        print()
        print_board(sol, n)

    print("\n  Selesai.")


if __name__ == "__main__":
    main()


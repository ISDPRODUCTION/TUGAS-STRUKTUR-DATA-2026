"""
===========================================
  SOAL 2 - KNIGHT'S TOUR (TUR KUDA)
  Algoritma Backtracking Rekursif
  + Heuristik Warnsdorff
===========================================
"""

# 8 kemungkinan gerak kuda (baris, kolom)
MOVES = [
    (-2, -1), (-2,  1),
    (-1, -2), (-1,  2),
    ( 1, -2), ( 1,  2),
    ( 2, -1), ( 2,  1),
]


def knights_tour(n, start_row, start_col):
    """
    Mencari satu Tur Kuda pada papan n x n mulai dari (start_row, start_col).
    Menggunakan backtracking rekursif + heuristik Warnsdorff untuk efisiensi.

    Warnsdorff: selalu pilih kotak berikutnya yang memiliki
    paling sedikit gerak lanjutan (mengurangi backtracking secara drastis).

    Mengembalikan:
        board (list 2D): board[r][c] = urutan langkah (0-based),
                         atau None jika tidak ada solusi.
    """
    board = [[-1] * n for _ in range(n)]
    calls = [0]

    def is_valid(r, c):
        return 0 <= r < n and 0 <= c < n and board[r][c] == -1

    def warnsdorff_count(r, c):
        """Hitung jumlah gerak valid dari posisi (r, c)."""
        return sum(1 for dr, dc in MOVES if is_valid(r + dr, c + dc))

    def backtrack(r, c, step):
        calls[0] += 1
        if step == n * n:
            return True  # semua petak sudah dikunjungi

        # Kumpulkan gerak valid, urutkan berdasarkan heuristik Warnsdorff
        next_moves = []
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                next_moves.append((nr, nc))
        next_moves.sort(key=lambda pos: warnsdorff_count(pos[0], pos[1]))

        for nr, nc in next_moves:
            board[nr][nc] = step
            if backtrack(nr, nc, step + 1):
                return True
            board[nr][nc] = -1  # backtrack

        return False

    board[start_row][start_col] = 0
    if backtrack(start_row, start_col, 1):
        return board, calls[0]
    else:
        return None, calls[0]


def print_board(board, n):
    """Cetak papan dengan nomor urutan langkah kuda."""
    cell_w = len(str(n * n)) + 1
    border = "+" + (("-" * cell_w) + "+") * n

    print(border)
    for r in range(n):
        row_str = "|"
        for c in range(n):
            val = board[r][c] + 1  # tampilkan 1-based
            row_str += str(val).center(cell_w) + "|"
        print(row_str)
        print(border)


def print_move_sequence(board, n):
    """Cetak urutan langkah kuda sebagai daftar koordinat."""
    moves = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            moves[board[r][c]] = (r, c)

    print("\n  Urutan langkah kuda (baris, kolom) — indeks 0-based:")
    per_line = 5
    for i, (r, c) in enumerate(moves):
        end = "\n" if (i + 1) % per_line == 0 or i == n * n - 1 else ""
        print(f"  Langkah {i+1:>3}: ({r},{c})", end=end)


def main():
    print("=" * 45)
    print("       PROGRAM TUR KUDA (KNIGHT'S TOUR)")
    print("       Algoritma Backtracking + Warnsdorff")
    print("=" * 45)

    while True:
        try:
            n = int(input("\nMasukkan ukuran papan (N, disarankan 5-8): "))
            if n < 5:
                print("  [!] N minimal 5 agar ada solusi.")
                continue
            break
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    while True:
        try:
            sr = int(input(f"Masukkan baris awal kuda  (0 s/d {n-1}): "))
            sc = int(input(f"Masukkan kolom awal kuda  (0 s/d {n-1}): "))
            if 0 <= sr < n and 0 <= sc < n:
                break
            print(f"  [!] Posisi harus dalam rentang 0 s/d {n-1}.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    print(f"\n  Mencari Tur Kuda pada papan {n}x{n} dari ({sr},{sc})...")
    board, total_calls = knights_tour(n, sr, sc)

    print(f"  Total rekursi dipanggil : {total_calls:,}")

    if board is None:
        print(f"\n  [!] Tidak ditemukan Tur Kuda dari posisi ({sr},{sc}).")
        print("  Coba posisi awal yang berbeda.")
        return

    print(f"  Tur Kuda berhasil! Total {n*n} petak dikunjungi.\n")
    print("  Papan (angka = urutan langkah):")
    print_board(board, n)
    print_move_sequence(board, n)
    print("\n  Selesai.")


if __name__ == "__main__":
    main()

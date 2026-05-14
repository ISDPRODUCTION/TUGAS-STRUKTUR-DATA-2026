"""
===========================================
  SOAL 3 - KNAPSACK (MASALAH TAS)
  Algoritma Backtracking Rekursif
===========================================
"""


def knapsack_recursive(weights, target):
    """
    Mencari SEMUA kombinasi barang yang totalnya tepat = target.
    Menggunakan backtracking rekursif dengan pruning.

    Parameter:
        weights (list): daftar berat barang
        target  (int) : berat target yang ingin dicapai

    Mengembalikan:
        solutions (list of list): semua kombinasi yang valid
        calls     (int)         : jumlah pemanggilan rekursi
    """
    solutions = []
    calls = [0]

    def backtrack(idx, current_weight, chosen):
        """
        idx            : indeks barang yang sedang dipertimbangkan
        current_weight : total berat barang yang sudah dipilih
        chosen         : list indeks barang yang dipilih saat ini
        """
        calls[0] += 1

        # Kondisi berhasil: berat tepat sama dengan target
        if current_weight == target:
            solutions.append(chosen[:])
            return

        # Pruning: sudah melebihi target atau barang habis
        if idx >= len(weights) or current_weight > target:
            return

        # Pilihan 1: MASUKKAN barang ke-idx ke dalam knapsack
        chosen.append(idx)
        backtrack(idx + 1, current_weight + weights[idx], chosen)
        chosen.pop()

        # Pilihan 2: LEWATI barang ke-idx (tidak dimasukkan)
        backtrack(idx + 1, current_weight, chosen)

    backtrack(0, 0, [])
    return solutions, calls[0]


def knapsack_max(weights, capacity):
    """
    BONUS: Mencari kombinasi dengan berat MAKSIMUM tidak melebihi capacity.
    Berguna jika tidak ada kombinasi yang tepat sama dengan target.

    Mengembalikan:
        best_combo (list): kombinasi indeks barang terbaik
        best_weight (int): total berat terbaik yang dicapai
        calls (int)      : jumlah rekursi
    """
    best = [[], 0]
    calls = [0]

    def backtrack(idx, current_weight, chosen):
        calls[0] += 1

        # Update solusi terbaik
        if current_weight > best[1]:
            best[0] = chosen[:]
            best[1] = current_weight

        if idx >= len(weights) or current_weight >= capacity:
            return

        # Masukkan barang ke-idx jika tidak melebihi kapasitas
        if current_weight + weights[idx] <= capacity:
            chosen.append(idx)
            backtrack(idx + 1, current_weight + weights[idx], chosen)
            chosen.pop()

        # Lewati barang ke-idx
        backtrack(idx + 1, current_weight, chosen)

    backtrack(0, 0, [])
    return best[0], best[1], calls[0]


def print_result(solutions, weights, target):
    """Cetak semua solusi yang ditemukan."""
    if not solutions:
        print(f"\n  [!] Tidak ada kombinasi yang tepat = {target} pon.")
        return

    print(f"\n  Ditemukan {len(solutions)} kombinasi yang mencapai {target} pon:")
    print()
    for i, sol_indices in enumerate(solutions):
        berat_list = [weights[j] for j in sol_indices]
        total = sum(berat_list)
        print(f"  Solusi {i+1:>3}: {berat_list}  →  Total = {total} pon")


def visualize_knapsack(chosen_indices, all_weights, target):
    """Visualisasi sederhana knapsack di terminal."""
    print("\n  Visualisasi Knapsack:")
    print(f"  Target: {target} pon")
    print()

    chosen_w = [all_weights[i] for i in chosen_indices]
    total = sum(chosen_w)
    bar_total = 40
    filled = int(bar_total * total / target) if target > 0 else 0
    filled = min(filled, bar_total)

    print(f"  [{'█' * filled}{'░' * (bar_total - filled)}] {total}/{target} pon")
    print()

    print("  Semua barang:")
    for i, w in enumerate(all_weights):
        status = "✓ DIPILIH" if i in chosen_indices else "  dilewati"
        bar = "■" * w
        print(f"    Barang {i+1:>2} ({w:>3} pon) {status}  {bar}")

    print()
    print(f"  Barang dipilih : {chosen_w}")
    print(f"  Total berat    : {total} pon")
    print(f"  Sisa kapasitas : {target - total} pon")


def input_weights():
    """Meminta input daftar berat barang dari pengguna."""
    print("\n  Pilih mode input barang:")
    print("  [1] Gunakan contoh soal (2, 5, 6, 9, 12, 14, 20)")
    print("  [2] Input manual")

    while True:
        try:
            mode = int(input("  Pilihan (1/2): "))
            if mode in (1, 2):
                break
        except ValueError:
            pass
        print("  [!] Pilih 1 atau 2.")

    if mode == 1:
        return [2, 5, 6, 9, 12, 14, 20]

    print("  Masukkan berat barang dipisah spasi (contoh: 3 7 10 15):")
    while True:
        try:
            raw = input("  > ").strip().split()
            weights = [int(x) for x in raw]
            if all(w > 0 for w in weights) and len(weights) > 0:
                return weights
            print("  [!] Semua berat harus bilangan positif.")
        except ValueError:
            print("  [!] Format tidak valid. Contoh: 2 5 6 9 12 14 20")


def main():
    print("=" * 50)
    print("       PROGRAM KNAPSACK (MASALAH TAS)")
    print("       Algoritma Backtracking Rekursif")
    print("=" * 50)

    weights = input_weights()
    weights.sort()
    print(f"\n  Daftar berat barang: {weights}")
    print(f"  Jumlah barang      : {len(weights)}")
    print(f"  Total berat semua  : {sum(weights)} pon")

    while True:
        try:
            target = int(input("\nMasukkan berat target knapsack (pon): "))
            if target > 0:
                break
            print("  [!] Target harus bilangan positif.")
        except ValueError:
            print("  [!] Masukkan angka yang valid.")

    print(f"\n  Mencari kombinasi yang tepat = {target} pon...")
    solutions, total_calls = knapsack_recursive(weights, target)

    print(f"  Total rekursi dipanggil : {total_calls:,}")
    print_result(solutions, weights, target)

    if solutions:
        # Tampilkan visualisasi solusi pertama
        first_sol = solutions[0]
        visualize_knapsack(first_sol, weights, target)
    else:
        # Coba cari kombinasi dengan berat maksimum mendekati target
        print(f"\n  Mencari kombinasi terbaik (tidak melebihi {target} pon)...")
        best_idx, best_w, calls2 = knapsack_max(weights, target)
        print(f"  Rekursi tambahan: {calls2:,}")
        if best_idx:
            print(f"\n  Kombinasi terbaik mendekati target:")
            visualize_knapsack(best_idx, weights, target)
        else:
            print("  Tidak ada kombinasi yang memungkinkan.")

    print("\n  Selesai.")


if __name__ == "__main__":
    main()

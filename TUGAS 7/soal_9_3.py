# ============================================================
# SOAL 9.3
# Evaluasi worst-case time complexity Sparse Matrix ADT
# yang diimplementasikan dengan Multi-Linked List.
# ============================================================


# ============================================================
# NODE & STRUKTUR SPARSE MATRIX (Multi-Linked List)
# ============================================================

class MatrixMListNode:
    """Node multi-linked untuk sparse matrix: punya dua link (baris & kolom)."""
    def __init__(self, row, col, value):
        self.row   = row
        self.col   = col
        self.value = value
        self.next_row = None    # link ke elemen berikutnya di baris yang sama
        self.next_col = None    # link ke elemen berikutnya di kolom yang sama


class SparseMatrix:
    """
    Implementasi Sparse Matrix ADT menggunakan Multi-Linked List.

    Struktur:
      - row_heads[i] : head dari linked list elemen di baris ke-i
      - col_heads[j] : head dari linked list elemen di kolom ke-j
    """

    def __init__(self, num_rows, num_cols):
        self.num_rows  = num_rows
        self.num_cols  = num_cols
        self.row_heads = [None] * num_rows   # array pointer head per baris
        self.col_heads = [None] * num_cols   # array pointer head per kolom

    # ----------------------------------------------------------
    # SET VALUE  -  O(k/r + k/c) rata-rata, O(k) worst case
    # k = jumlah elemen non-zero, r = jumlah baris, c = jumlah kolom
    # Harus menyisipkan ke dua chain sekaligus (baris & kolom).
    # ----------------------------------------------------------
    def set_value(self, row, col, value):
        # Hapus node lama di posisi (row, col) jika ada
        self._remove(row, col)

        if value == 0:
            return  # elemen nol tidak disimpan

        new_node = MatrixMListNode(row, col, value)

        # Sisipkan ke chain BARIS (urut berdasarkan kolom)
        prev, cur = None, self.row_heads[row]
        while cur is not None and cur.col < col:
            prev, cur = cur, cur.next_row
        new_node.next_row = cur
        if prev is None:
            self.row_heads[row] = new_node
        else:
            prev.next_row = new_node

        # Sisipkan ke chain KOLOM (urut berdasarkan baris)
        prev, cur = None, self.col_heads[col]
        while cur is not None and cur.row < row:
            prev, cur = cur, cur.next_col
        new_node.next_col = cur
        if prev is None:
            self.col_heads[col] = new_node
        else:
            prev.next_col = new_node

    # ----------------------------------------------------------
    # GET VALUE  -  O(k/r) rata-rata per baris, O(k) worst case
    # Traversal chain baris hingga kolom ditemukan.
    # ----------------------------------------------------------
    def get_value(self, row, col):
        cur = self.row_heads[row]
        while cur is not None:
            if cur.col == col:
                return cur.value
            if cur.col > col:
                break
            cur = cur.next_row
        return 0

    # ----------------------------------------------------------
    # REMOVE - helper untuk menghapus elemen dari kedua chain
    # O(k/r + k/c) rata-rata, O(k) worst case
    # ----------------------------------------------------------
    def _remove(self, row, col):
        # Hapus dari chain baris
        prev, cur = None, self.row_heads[row]
        while cur is not None:
            if cur.col == col:
                if prev is None:
                    self.row_heads[row] = cur.next_row
                else:
                    prev.next_row = cur.next_row
                break
            prev, cur = cur, cur.next_row

        # Hapus dari chain kolom
        prev, cur = None, self.col_heads[col]
        while cur is not None:
            if cur.row == row:
                if prev is None:
                    self.col_heads[col] = cur.next_col
                else:
                    prev.next_col = cur.next_col
                break
            prev, cur = cur, cur.next_col

    # ----------------------------------------------------------
    # TAMPILKAN MATRIKS  -  O(r*c) untuk display
    # ----------------------------------------------------------
    def display(self):
        print(f"  Matriks {self.num_rows}x{self.num_cols}:")
        header = "     " + "  ".join(f"C{j}" for j in range(self.num_cols))
        print(f"  {header}")
        for i in range(self.num_rows):
            row_str = f"  R{i} |"
            for j in range(self.num_cols):
                row_str += f"  {self.get_value(i, j)}"
            print(row_str)

    # ----------------------------------------------------------
    # TAMPILKAN ELEMEN NON-ZERO
    # ----------------------------------------------------------
    def non_zero_elements(self):
        elements = []
        for i in range(self.num_rows):
            cur = self.row_heads[i]
            while cur is not None:
                elements.append((cur.row, cur.col, cur.value))
                cur = cur.next_row
        return elements

    # ----------------------------------------------------------
    # PENJUMLAHAN MATRIKS  -  O(k1 + k2)
    # k1, k2 = jumlah elemen non-zero masing-masing matriks
    # ----------------------------------------------------------
    def add(self, other):
        assert self.num_rows == other.num_rows
        assert self.num_cols == other.num_cols
        result = SparseMatrix(self.num_rows, self.num_cols)
        # Salin semua elemen self
        for (r, c, v) in self.non_zero_elements():
            result.set_value(r, c, v)
        # Tambahkan elemen other
        for (r, c, v) in other.non_zero_elements():
            current = result.get_value(r, c)
            result.set_value(r, c, current + v)
        return result


# ============================================================
# DEMO & ANALISIS
# ============================================================

print("=" * 60)
print("SOAL 9.3 - Sparse Matrix ADT (Multi-Linked List)")
print("=" * 60)

# Buat matriks dari contoh buku (Figure 9.12)
print("\n[MEMBUAT SPARSE MATRIX 5x8]")
sm = SparseMatrix(5, 8)
data = [
    (0, 1, 3), (0, 4, 8),
    (1, 0, 2), (1, 3, 1), (1, 6, 5),
    (2, 2, 9), (2, 5, 2),
    (3, 1, 7), (3, 7, 3),
    (4, 4, 4),
]
for r, c, v in data:
    sm.set_value(r, c, v)

sm.display()

print(f"\n  Elemen non-zero (k = {len(data)}):")
for item in sm.non_zero_elements():
    print(f"    baris={item[0]}, kolom={item[1]}, nilai={item[2]}")

# Tes get_value
print(f"\n[GET VALUE]")
print(f"  get(0,1) = {sm.get_value(0,1)}  (harusnya 3)")
print(f"  get(1,6) = {sm.get_value(1,6)}  (harusnya 5)")
print(f"  get(0,0) = {sm.get_value(0,0)}  (harusnya 0 - elemen nol)")

# Tes penjumlahan
print(f"\n[PENJUMLAHAN DUA MATRIKS]")
sm2 = SparseMatrix(5, 8)
sm2.set_value(0, 1, 10)
sm2.set_value(2, 2, 5)
sm2.set_value(3, 7, 2)

sm3 = sm.add(sm2)
print("  Matriks pertama + Matriks kedua =>")
sm3.display()

# Ringkasan analisis
print()
print("=" * 60)
print("ANALISIS TIME COMPLEXITY - Sparse Matrix (Multi-Linked List)")
print("=" * 60)
print("""
  Notasi: r = jumlah baris, c = jumlah kolom, k = elemen non-zero

  Operasi         Kompleksitas        Penjelasan
  ─────────────── ──────────────────── ─────────────────────────────────
  get_value(i,j)  O(k/r) avg, O(k) WC  Telusuri chain baris ke-i
  set_value(i,j)  O(k/r + k/c)         Telusuri & sisipkan di 2 chain
  _remove(i,j)    O(k/r + k/c)         Hapus dari chain baris & kolom
  add(other)      O(k1 + k2)           Telusuri semua elemen non-zero
  multiply        O(k^2) WC            Perkalian silang semua elemen

  Kesimpulan:
  - Multi-linked list LEBIH EFISIEN dari 2-D array untuk matriks
    yang jarang (sparse), karena hanya menyimpan elemen non-zero.
  - Traversal baris: O(k/r) rata-rata (jauh lebih cepat dari O(c)).
  - Traversal kolom: O(k/c) rata-rata (tidak memerlukan scan semua baris).
  - Worst case tetap O(k) jika semua elemen non-zero ada di satu baris/kolom.
""")

# ============================================================
# SOAL 9.6
# Implementasi operasi DELETE untuk
# SORTED SINGLY LINKED CIRCULAR LIST.
# ============================================================


class SListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class SortedCircularLinkedList:
    """
    Sorted Singly Linked Circular List (urutan menaik).

    Konvensi:
    - listRef menunjuk ke node TERAKHIR (nilai terbesar).
    - listRef.next menunjuk ke node PERTAMA (nilai terkecil).
    - Semua node membentuk lingkaran (tidak ada next == None).
    """

    def __init__(self):
        self.listRef = None     # menunjuk ke node terakhir

    # --- INSERT (untuk membangun list pada demo) ---
    def insert(self, value):
        new_node = SListNode(value)

        if self.listRef is None:            # list kosong
            new_node.next = new_node
            self.listRef = new_node

        elif value < self.listRef.next.data:    # sisipkan di DEPAN
            new_node.next = self.listRef.next
            self.listRef.next = new_node

        elif value > self.listRef.data:         # sisipkan di BELAKANG
            new_node.next = self.listRef.next
            self.listRef.next = new_node
            self.listRef = new_node

        else:                                   # sisipkan di TENGAH
            pred = self.listRef
            cur  = self.listRef.next
            done = False
            while not done:
                if cur.data >= value:
                    done = True
                else:
                    pred = cur
                    cur  = cur.next
                    if cur is self.listRef.next:
                        done = True
            new_node.next = cur
            pred.next = new_node

    # ----------------------------------------------------------
    # DELETE  -  O(n)
    #
    # Strategi:
    # - Gunakan DUA pointer: pred_node dan cur_node
    # - pred_node selalu satu langkah di belakang cur_node
    # - Ketika cur_node ditemukan, hubungkan pred_node.next = cur_node.next
    #
    # Kasus khusus:
    #   a) List kosong            : langsung return False
    #   b) List satu node         : cek apakah nilainya == value
    #   c) Hapus node PERTAMA     : listRef.next = cur_node.next
    #   d) Hapus node TERAKHIR    : pred_node.next = listRef.next (wrap),
    #                               update listRef = pred_node
    #   e) Hapus node TENGAH      : pred_node.next = cur_node.next
    #
    # Terminasi traversal:
    # - Karena circular, gunakan flag 'done' seperti pada traversal
    # - Berhenti jika sudah kembali ke node pertama (satu putaran penuh)
    # - Atau berhenti lebih awal jika cur_node.data > value (list terurut)
    # ----------------------------------------------------------
    def delete(self, value):
        """
        Menghapus node dengan nilai tertentu dari sorted circular list.
        Mengembalikan True jika berhasil, False jika tidak ditemukan.
        Kompleksitas: O(n)
        """

        # --- Kasus a: List kosong ---
        if self.listRef is None:
            return False

        # --- Kasus b: Hanya satu node ---
        if self.listRef.next is self.listRef:
            if self.listRef.data == value:
                self.listRef = None
                return True
            return False

        # Inisialisasi dua pointer
        pred_node = self.listRef            # mulai dari node TERAKHIR
        cur_node  = self.listRef.next       # mulai iterasi dari node PERTAMA
        first_node = self.listRef.next      # simpan referensi node pertama

        found = False
        done  = False

        while not done:
            if cur_node.data == value:
                found = True
                break
            # List terurut: jika cur > value, target tidak ada
            if cur_node.data > value:
                break
            pred_node = cur_node
            cur_node  = cur_node.next
            # Berhenti jika sudah satu putaran penuh (kembali ke node pertama)
            done = (cur_node is first_node)

        if not found:
            return False

        # --- Kasus c: Hapus node PERTAMA ---
        if cur_node is first_node:
            self.listRef.next = cur_node.next   # listRef.next skip ke node ke-2

        # --- Kasus d: Hapus node TERAKHIR (listRef) ---
        elif cur_node is self.listRef:
            pred_node.next = cur_node.next      # pred_node.next = node pertama
            self.listRef   = pred_node          # update listRef ke pred_node

        # --- Kasus e: Hapus node TENGAH ---
        else:
            pred_node.next = cur_node.next

        # Bersihkan referensi (opsional)
        cur_node.next = None
        return True

    # --- TRAVERSAL ---
    def traversal(self):
        """Menelusuri circular list dan mengembalikan list nilai. O(n)"""
        if self.listRef is None:
            return []
        result = []
        cur  = self.listRef.next    # mulai dari node pertama
        done = False
        while not done:
            result.append(cur.data)
            cur  = cur.next
            done = (cur is self.listRef.next)   # sudah satu putaran penuh
        return result

    # --- CEK INTEGRITAS circular list ---
    def check_integrity(self):
        """Memverifikasi bahwa list benar-benar membentuk lingkaran."""
        if self.listRef is None:
            print("  [OK] List kosong.")
            return
        cur   = self.listRef.next
        count = 0
        limit = 1000   # batas untuk mendeteksi infinite loop
        while cur is not self.listRef:
            cur   = cur.next
            count += 1
            if count > limit:
                print("  [ERROR] Kemungkinan loop tidak berakhir!")
                return
        print(f"  [OK] Circular list valid ({count + 1} node).")


# ============================================================
# DEMO LENGKAP
# ============================================================

print("=" * 58)
print("SOAL 9.6 - Delete dari Sorted Singly Linked Circular List")
print("=" * 58)

scl = SortedCircularLinkedList()

# Bangun list
print("\n[INSERT] Masukkan: 21, 37, 46, 58, 74")
for v in [21, 37, 46, 58, 74]:
    scl.insert(v)
print("  List  :", scl.traversal())
print(f"  listRef menunjuk ke: {scl.listRef.data} (nilai terbesar)")
print(f"  Node pertama       : {scl.listRef.next.data}")
scl.check_integrity()

# ---- Hapus node tengah ----
print("\n[DELETE] Hapus 46 (node tengah)")
scl.delete(46)
print("  List  :", scl.traversal())
scl.check_integrity()

# ---- Hapus node pertama ----
print("\n[DELETE] Hapus 21 (node pertama)")
scl.delete(21)
print("  List  :", scl.traversal())
print(f"  listRef = {scl.listRef.data}, node pertama = {scl.listRef.next.data}")
scl.check_integrity()

# ---- Hapus node terakhir (listRef) ----
print("\n[DELETE] Hapus 74 (listRef / node terakhir)")
scl.delete(74)
print("  List  :", scl.traversal())
print(f"  listRef baru = {scl.listRef.data}")
scl.check_integrity()

# ---- Hapus nilai yang tidak ada ----
print("\n[DELETE] Hapus 99 (tidak ada)")
hasil = scl.delete(99)
print(f"  Hasil : {hasil} | List: {scl.traversal()}")

# ---- Hapus hingga tersisa satu node ----
print("\n[DELETE] Hapus 37, tersisa satu node (58)")
scl.delete(37)
print("  List  :", scl.traversal())
scl.check_integrity()

# ---- Hapus node terakhir yang tersisa (kasus b) ----
print("\n[DELETE] Hapus 58 (satu-satunya node - kasus b)")
scl.delete(58)
print("  List  :", scl.traversal())
print(f"  listRef = {scl.listRef}")

# ---- Hapus dari list kosong ----
print("\n[DELETE] Hapus dari list kosong (kasus a)")
hasil = scl.delete(10)
print(f"  Hasil : {hasil}")

# ---- Test insert setelah hapus semua ----
print("\n[INSERT BARU] Setelah list dikosongkan, masukkan 5, 15, 10")
for v in [5, 15, 10]:
    scl.insert(v)
print("  List  :", scl.traversal())
scl.check_integrity()

# ---- Ringkasan ----
print()
print("=" * 58)
print("PENJELASAN KUNCI - Delete pada Circular List")
print("=" * 58)
print("""
  Perbedaan utama dengan delete pada Sorted SLL biasa:

  1. Tidak ada node dengan next == None
     => Loop tidak bisa berhenti dengan cek cur == None
     => Gunakan flag 'done' dan bandingkan dengan node pertama

  2. listRef menunjuk ke TERAKHIR, bukan pertama
     => Node pertama diakses via listRef.next
     => Saat hapus node pertama: update listRef.next
     => Saat hapus listRef sendiri: update listRef ke pred_node

  3. Dua pointer wajib: pred_node dan cur_node
     => Karena singly linked, tidak bisa mundur
     => pred_node harus dipertahankan untuk menyambung ulang

  Kompleksitas: O(n) - dalam kasus terburuk menelusuri seluruh list.
""")

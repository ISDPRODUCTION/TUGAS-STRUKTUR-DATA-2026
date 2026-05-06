# ============================================================
# SOAL 9.5
# Implementasi operasi DELETE untuk SORTED Doubly Linked List.
# ============================================================


class DListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class SortedDoublyLinkedList:
    """
    Sorted Doubly Linked List (urutan menaik).
    - head : node dengan nilai terkecil
    - tail : node dengan nilai terbesar
    """

    def __init__(self):
        self.head = None
        self.tail = None

    # --- INSERT (untuk membangun list pada demo) ---
    def insert(self, value):
        new_node = DListNode(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif value < self.head.data:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif value > self.tail.data:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            cur = self.head
            while cur is not None and cur.data < value:
                cur = cur.next
            new_node.next = cur
            new_node.prev = cur.prev
            cur.prev.next = new_node
            cur.prev = new_node

    # ----------------------------------------------------------
    # DELETE  -  O(n)
    #
    # Langkah:
    # 1. Temukan node dengan nilai == value (traversal dari head).
    # 2. Karena list terurut, bisa berhenti lebih awal jika
    #    cur.data > value (nilai tidak mungkin ada setelahnya).
    # 3. Setelah node ditemukan, lepaskan tautan menggunakan
    #    cur.prev dan cur.next — TANPA perlu pointer pred terpisah.
    #
    # Empat kasus yang harus ditangani:
    #   a) List satu node     : head = tail = None
    #   b) Hapus node pertama : update head, head.prev = None
    #   c) Hapus node terakhir: update tail, tail.next = None
    #   d) Hapus node tengah  : hubungkan prev <-> next
    # ----------------------------------------------------------
    def delete(self, value):
        """
        Menghapus node dengan nilai tertentu dari sorted DLL.
        Mengembalikan True jika berhasil, False jika tidak ditemukan.
        Kompleksitas: O(n)
        """
        # List kosong
        if self.head is None:
            return False

        # Cari node target
        cur = self.head
        while cur is not None:
            if cur.data == value:
                break
            # Karena terurut, jika cur.data > value maka target tidak ada
            if cur.data > value:
                return False
            cur = cur.next

        if cur is None:
            return False   # target tidak ditemukan (melewati semua node)

        # --- Kasus a: Satu-satunya node dalam list ---
        if cur.prev is None and cur.next is None:
            self.head = None
            self.tail = None

        # --- Kasus b: Node pertama (head) ---
        elif cur.prev is None:
            self.head = cur.next
            self.head.prev = None

        # --- Kasus c: Node terakhir (tail) ---
        elif cur.next is None:
            self.tail = cur.prev
            self.tail.next = None

        # --- Kasus d: Node di tengah ---
        else:
            cur.prev.next = cur.next    # sambungkan predecessor ke successor
            cur.next.prev = cur.prev    # sambungkan successor ke predecessor

        # Bersihkan referensi node yang dihapus (opsional, untuk GC)
        cur.next = None
        cur.prev = None

        return True

    # --- TRAVERSAL MAJU ---
    def traversal(self):
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        return result

    # --- TRAVERSAL MUNDUR ---
    def rev_traversal(self):
        result = []
        cur = self.tail
        while cur is not None:
            result.append(cur.data)
            cur = cur.prev
        return result

    # --- CEK INTEGRITAS pointer prev/next ---
    def check_integrity(self):
        """Memverifikasi bahwa pointer prev dan next konsisten."""
        cur = self.head
        prev = None
        ok = True
        while cur is not None:
            if cur.prev is not prev:
                print(f"  [ERROR] Node {cur.data}: prev tidak konsisten!")
                ok = False
            prev = cur
            cur = cur.next
        if self.tail is not prev:
            print("  [ERROR] tail tidak menunjuk ke node terakhir!")
            ok = False
        if ok:
            print("  [OK] Integritas pointer prev/next valid.")


# ============================================================
# DEMO LENGKAP
# ============================================================

print("=" * 55)
print("SOAL 9.5 - Delete dari Sorted Doubly Linked List")
print("=" * 55)

sdll = SortedDoublyLinkedList()

# Bangun list
print("\n[INSERT] Masukkan: 21, 37, 46, 58, 74")
for v in [21, 37, 46, 58, 74]:
    sdll.insert(v)
print("  Maju  :", sdll.traversal())
print("  Mundur:", sdll.rev_traversal())
sdll.check_integrity()

# ---- Hapus node di tengah ----
print("\n[DELETE] Hapus 46 (node tengah)")
sdll.delete(46)
print("  Maju  :", sdll.traversal())
print("  Mundur:", sdll.rev_traversal())
sdll.check_integrity()

# ---- Hapus node paling depan (head) ----
print("\n[DELETE] Hapus 21 (head)")
sdll.delete(21)
print("  Maju  :", sdll.traversal())
print("  Mundur:", sdll.rev_traversal())
sdll.check_integrity()

# ---- Hapus node paling belakang (tail) ----
print("\n[DELETE] Hapus 74 (tail)")
sdll.delete(74)
print("  Maju  :", sdll.traversal())
print("  Mundur:", sdll.rev_traversal())
sdll.check_integrity()

# ---- Hapus nilai yang tidak ada ----
print("\n[DELETE] Hapus 99 (tidak ada)")
hasil = sdll.delete(99)
print(f"  Hasil: {hasil}  | List: {sdll.traversal()}")

# ---- Hapus hingga tersisa satu node ----
print("\n[DELETE] Hapus 37, tersisa satu node (58)")
sdll.delete(37)
print("  List:", sdll.traversal())
sdll.check_integrity()

# ---- Hapus node terakhir (kasus a) ----
print("\n[DELETE] Hapus 58 (satu-satunya node)")
sdll.delete(58)
print("  List:", sdll.traversal())
print(f"  head = {sdll.head}, tail = {sdll.tail}")

# ---- Hapus dari list kosong ----
print("\n[DELETE] Hapus dari list kosong")
hasil = sdll.delete(10)
print(f"  Hasil: {hasil}")

# ---- Ringkasan ----
print()
print("=" * 55)
print("PENJELASAN KUNCI")
print("=" * 55)
print("""
  Keunggulan Sorted DLL vs Sorted SLL saat DELETE:

  Sorted SLL: Perlu pointer pred (predecessor) TERPISAH
              yang diupdate selama traversal, karena tidak
              bisa mundur dari node yang ditemukan.

  Sorted DLL: Cukup gunakan cur.prev untuk mengakses
              predecessor secara langsung. Tidak perlu
              variabel pred terpisah!

  Kode inti saat hapus node tengah:
    cur.prev.next = cur.next   # bypass node dari kiri
    cur.next.prev = cur.prev   # bypass node dari kanan

  Kompleksitas: O(n) untuk mencari, O(1) untuk melepas tautan.
""")

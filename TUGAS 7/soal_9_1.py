# ============================================================
# SOAL 9.1
# Evaluasi 4 operasi dasar Sorted Doubly Linked List
# dan tentukan worst-case time complexity masing-masing.
# ============================================================

class DListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class SortedDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # ----------------------------------------------------------
    # 1. TRAVERSAL - O(n)
    # Mengunjungi setiap node dari depan ke belakang.
    # Worst case: harus melewati semua n node => O(n)
    # ----------------------------------------------------------
    def traversal(self):
        print("  Traversal maju :", end=" ")
        cur = self.head
        result = []
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        print(result)

    def rev_traversal(self):
        print("  Traversal mundur:", end=" ")
        cur = self.tail
        result = []
        while cur is not None:
            result.append(cur.data)
            cur = cur.prev
        print(result)

    # ----------------------------------------------------------
    # 2. SEARCH - O(n)
    # Mencari nilai target dalam list yang terurut.
    # Worst case: target di akhir atau tidak ada => O(n)
    # ----------------------------------------------------------
    def search(self, target):
        cur = self.head
        while cur is not None:
            if cur.data == target:
                return True
            if cur.data > target:   # list terurut, bisa berhenti lebih awal
                return False
            cur = cur.next
        return False

    # ----------------------------------------------------------
    # 3. INSERTION - O(n)
    # Menyisipkan nilai baru ke posisi yang tepat agar tetap terurut.
    # Worst case: nilai terbesar (perlu traverse seluruh list) => O(n)
    # ----------------------------------------------------------
    def insert(self, value):
        new_node = DListNode(value)

        if self.head is None:                   # list kosong
            self.head = new_node
            self.tail = new_node

        elif value < self.head.data:            # sisipkan di depan
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        elif value > self.tail.data:            # sisipkan di belakang
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        else:                                   # sisipkan di tengah
            cur = self.head
            while cur is not None and cur.data < value:
                cur = cur.next
            new_node.next = cur
            new_node.prev = cur.prev
            cur.prev.next = new_node
            cur.prev = new_node

    # ----------------------------------------------------------
    # 4. DELETION - O(n)
    # Menghapus node dengan nilai tertentu.
    # Worst case: nilai di akhir atau tidak ada => O(n)
    # Keuntungan DLL: tidak perlu pointer predecessor terpisah
    # karena bisa akses via cur.prev
    # ----------------------------------------------------------
    def delete(self, value):
        cur = self.head
        while cur is not None:
            if cur.data == value:
                if cur.prev is None and cur.next is None:   # satu-satunya
                    self.head = None
                    self.tail = None
                elif cur.prev is None:                       # node pertama
                    self.head = cur.next
                    self.head.prev = None
                elif cur.next is None:                       # node terakhir
                    self.tail = cur.prev
                    self.tail.next = None
                else:                                        # node tengah
                    cur.prev.next = cur.next
                    cur.next.prev = cur.prev
                return True
            if cur.data > value:
                return False
            cur = cur.next
        return False


# ============================================================
# DEMO & ANALISIS
# ============================================================

print("=" * 55)
print("SOAL 9.1 - Sorted Doubly Linked List: 4 Operasi Dasar")
print("=" * 55)

sdll = SortedDoublyLinkedList()

# Insert
print("\n[INSERT] Memasukkan nilai: 50, 10, 70, 30, 90, 20")
for v in [50, 10, 70, 30, 90, 20]:
    sdll.insert(v)

# Traversal
print("\n[TRAVERSAL]")
sdll.traversal()
sdll.rev_traversal()

# Search
print("\n[SEARCH]")
for target in [30, 99, 10, 70]:
    hasil = sdll.search(target)
    print(f"  Search {target:>2} => {'DITEMUKAN' if hasil else 'TIDAK ADA'}")

# Deletion
print("\n[DELETION]")
sdll.delete(30)
print("  Hapus 30 (tengah) =>", end=" "); sdll.traversal()
sdll.delete(10)
print("  Hapus 10 (head)   =>", end=" "); sdll.traversal()
sdll.delete(90)
print("  Hapus 90 (tail)   =>", end=" "); sdll.traversal()
print("  Hapus 99 (tidak ada) =>", sdll.delete(99))

# Ringkasan
print("\n" + "=" * 55)
print("RINGKASAN TIME COMPLEXITY (Worst Case)")
print("=" * 55)
print(f"  {'Operasi':<12} {'Kompleksitas':<15} Alasan")
print("-" * 55)
print(f"  {'Traversal':<12} {'O(n)':<15} Kunjungi semua n node")
print(f"  {'Search':<12} {'O(n)':<15} Target di akhir / tidak ada")
print(f"  {'Insertion':<12} {'O(n)':<15} Cari posisi dari depan")
print(f"  {'Deletion':<12} {'O(n)':<15} Cari node dari depan")
print()
print("  Catatan: DLL TIDAK memerlukan pointer predecessor")
print("  saat insert/delete karena bisa akses via node.prev")

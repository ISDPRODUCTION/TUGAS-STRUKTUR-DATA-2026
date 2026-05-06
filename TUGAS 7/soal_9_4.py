# ============================================================
# SOAL 9.4
# Implementasi 4 operasi dasar untuk UNSORTED Doubly Linked List:
# Traversal, Search, Insertion, Deletion
# ============================================================


class DListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class UnsortedDoublyLinkedList:
    """
    Unsorted Doubly Linked List.
    - head  : menunjuk node pertama
    - tail  : menunjuk node terakhir
    """

    def __init__(self):
        self.head = None
        self.tail = None

    # ----------------------------------------------------------
    # 1. TRAVERSAL MAJU (head -> tail)  -  O(n)
    # ----------------------------------------------------------
    def traversal(self):
        """
        Menelusuri list dari depan ke belakang menggunakan link next.
        Mengembalikan list nilai yang ditemukan.
        Kompleksitas: O(n)
        """
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        return result

    # ----------------------------------------------------------
    # 2. TRAVERSAL MUNDUR (tail -> head)  -  O(n)
    # Ini keunggulan DLL dibanding SLL: bisa mundur via prev
    # ----------------------------------------------------------
    def rev_traversal(self):
        """
        Menelusuri list dari belakang ke depan menggunakan link prev.
        Kompleksitas: O(n)
        """
        result = []
        cur = self.tail
        while cur is not None:
            result.append(cur.data)
            cur = cur.prev
        return result

    # ----------------------------------------------------------
    # 3. SEARCH  -  O(n)
    # Mencari target dalam list yang tidak terurut.
    # Karena tidak terurut, HARUS menelusuri hingga akhir list.
    # ----------------------------------------------------------
    def search(self, target):
        """
        Mencari nilai target. Mengembalikan node jika ditemukan,
        None jika tidak ada.
        Kompleksitas: O(n)
        """
        cur = self.head
        while cur is not None:
            if cur.data == target:
                return cur      # kembalikan node agar bisa dipakai langsung
            cur = cur.next
        return None

    # ----------------------------------------------------------
    # 4a. INSERT DI DEPAN  -  O(1)
    # ----------------------------------------------------------
    def insert_front(self, value):
        """
        Menyisipkan node baru di depan list.
        Kompleksitas: O(1) — tidak perlu traversal.
        """
        new_node = DListNode(value)
        if self.head is None:           # list kosong
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    # ----------------------------------------------------------
    # 4b. INSERT DI BELAKANG  -  O(1)
    # ----------------------------------------------------------
    def insert_back(self, value):
        """
        Menyisipkan node baru di belakang list.
        Kompleksitas: O(1) — langsung via tail.
        """
        new_node = DListNode(value)
        if self.tail is None:           # list kosong
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    # ----------------------------------------------------------
    # 4c. INSERT SETELAH NODE TERTENTU  -  O(1) setelah node diketahui
    # (O(n) jika perlu mencari node terlebih dahulu)
    # ----------------------------------------------------------
    def insert_after(self, target_value, new_value):
        """
        Menyisipkan node baru tepat setelah node yang nilainya == target_value.
        Kompleksitas: O(n) untuk mencari, O(1) untuk menyisipkan.
        """
        node = self.search(target_value)
        if node is None:
            print(f"  [insert_after] Nilai {target_value} tidak ditemukan.")
            return False

        new_node = DListNode(new_value)
        new_node.prev = node
        new_node.next = node.next

        if node.next is not None:
            node.next.prev = new_node
        else:
            self.tail = new_node        # node adalah tail, update tail

        node.next = new_node
        return True

    # ----------------------------------------------------------
    # 5. DELETE  -  O(n)
    # Menghapus node pertama yang nilainya == value.
    # Keunggulan DLL: tidak perlu pointer pred terpisah (gunakan cur.prev).
    # ----------------------------------------------------------
    def delete(self, value):
        """
        Menghapus node pertama dengan nilai tertentu.
        Kompleksitas: O(n) untuk mencari node.
        O(1) untuk memutus tautan (karena bisa akses prev langsung).
        """
        cur = self.search(value)

        if cur is None:
            return False        # nilai tidak ditemukan

        # Kasus 1: Satu-satunya node
        if cur.prev is None and cur.next is None:
            self.head = None
            self.tail = None

        # Kasus 2: Node pertama (head)
        elif cur.prev is None:
            self.head = cur.next
            self.head.prev = None

        # Kasus 3: Node terakhir (tail)
        elif cur.next is None:
            self.tail = cur.prev
            self.tail.next = None

        # Kasus 4: Node di tengah
        else:
            cur.prev.next = cur.next
            cur.next.prev = cur.prev

        return True


# ============================================================
# DEMO LENGKAP
# ============================================================

print("=" * 58)
print("SOAL 9.4 - Unsorted Doubly Linked List: 4 Operasi Dasar")
print("=" * 58)

dll = UnsortedDoublyLinkedList()

# ---- INSERT ----
print("\n[INSERT] Sisipkan di belakang: 50, 10, 30, 80, 20")
for v in [50, 10, 30, 80, 20]:
    dll.insert_back(v)
print("  List:", dll.traversal())

print("\n[INSERT FRONT] Sisipkan 99 di depan")
dll.insert_front(99)
print("  List:", dll.traversal())

print("\n[INSERT AFTER] Sisipkan 55 setelah nilai 30")
dll.insert_after(30, 55)
print("  List:", dll.traversal())

print("\n[INSERT AFTER] Sisipkan 999 setelah nilai 77 (tidak ada)")
dll.insert_after(77, 999)
print("  List:", dll.traversal())

# ---- TRAVERSAL ----
print("\n[TRAVERSAL MAJU]")
print("  Head -> Tail:", dll.traversal())

print("\n[TRAVERSAL MUNDUR]")
print("  Tail -> Head:", dll.rev_traversal())

# ---- SEARCH ----
print("\n[SEARCH]")
for target in [30, 55, 99, 999]:
    node = dll.search(target)
    if node:
        print(f"  Search {target:>3} => DITEMUKAN (node.data = {node.data})")
    else:
        print(f"  Search {target:>3} => TIDAK ADA")

# ---- DELETE ----
print("\n[DELETE]")
print("  Sebelum      :", dll.traversal())
dll.delete(55)
print("  Hapus 55 (tengah)    :", dll.traversal())
dll.delete(99)
print("  Hapus 99 (head)      :", dll.traversal())
dll.delete(20)
print("  Hapus 20 (tail)      :", dll.traversal())
print("  Hapus 777 (tidak ada):", dll.delete(777))

# ---- TEST EDGE CASE ----
print("\n[EDGE CASE: List satu elemen]")
dll2 = UnsortedDoublyLinkedList()
dll2.insert_back(42)
print("  List:", dll2.traversal())
dll2.delete(42)
print("  Setelah hapus 42:", dll2.traversal())

# ---- RINGKASAN ----
print()
print("=" * 58)
print("RINGKASAN TIME COMPLEXITY")
print("=" * 58)
print(f"  {'Operasi':<22} {'Kompleksitas'}")
print("-" * 38)
print(f"  {'Traversal maju/mundur':<22} O(n)")
print(f"  {'Search':<22} O(n)")
print(f"  {'Insert front/back':<22} O(1)")
print(f"  {'Insert after (search+insert)':<22} O(n)")
print(f"  {'Delete':<22} O(n)  [O(1) lepas tautan]")
print()
print("  Keunggulan DLL vs SLL:")
print("  - Delete tidak perlu pred pointer terpisah (gunakan cur.prev)")
print("  - Traversal bisa maju DAN mundur")

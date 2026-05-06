# ============================================================
# SOAL 9.2
# Evaluasi worst-case time complexity operasi SEARCH
# pada Doubly Linked List menggunakan PROBE POINTER.
# ============================================================

class DListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class SortedDLLWithProbe:
    def __init__(self):
        self.head = None
        self.tail = None
        self.probe = None       # pointer probe yang dipertahankan antar pencarian

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

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    # ----------------------------------------------------------
    # SEARCH dengan PROBE POINTER
    #
    # Ide:
    #   - probe menunjuk ke posisi terakhir pencarian sebelumnya
    #   - Bandingkan target dengan probe.data:
    #       * jika target < probe.data  => traversal MUNDUR
    #       * jika target >= probe.data => traversal MAJU
    #   - probe tidak direset ke head setiap kali pencarian baru
    #
    # Worst case: O(n) - jika pola pencarian selalu berlawanan arah
    # (misal: cari terkecil, lalu terbesar, lalu terkecil, dst.)
    # ----------------------------------------------------------
    def search(self, target):
        step_count = 0

        if self.head is None:
            print(f"    => List kosong. Tidak ditemukan.")
            return False

        # Inisialisasi probe jika belum pernah diset atau jatuh dari list
        if self.probe is None:
            self.probe = self.head

        probe_start = self.probe.data

        if target < self.probe.data:
            # Traversal MUNDUR dari posisi probe
            direction = "mundur"
            while self.probe is not None and target <= self.probe.data:
                step_count += 1
                if target == self.probe.data:
                    print(f"    [{direction}] Mulai dari {probe_start}, "
                          f"target {target} DITEMUKAN dalam {step_count} langkah.")
                    return True
                self.probe = self.probe.prev
        else:
            # Traversal MAJU dari posisi probe
            direction = "maju"
            while self.probe is not None and target >= self.probe.data:
                step_count += 1
                if target == self.probe.data:
                    print(f"    [{direction}] Mulai dari {probe_start}, "
                          f"target {target} DITEMUKAN dalam {step_count} langkah.")
                    return True
                self.probe = self.probe.next

        print(f"    [{direction}] Mulai dari {probe_start}, "
              f"target {target} TIDAK ADA ({step_count} langkah).")
        # Reset probe ke head agar pencarian berikutnya tidak gagal
        self.probe = self.head
        return False


# ============================================================
# DEMO & ANALISIS
# ============================================================

print("=" * 60)
print("SOAL 9.2 - Search dengan Probe Pointer pada Sorted DLL")
print("=" * 60)

dll = SortedDLLWithProbe()
for v in [10, 20, 30, 40, 50, 60, 70, 80]:
    dll.insert(v)

print(f"\nList: {dll.to_list()}")
print()

# Skenario 1: Pencarian berurutan (probe menguntungkan)
print("--- Skenario 1: Pencarian BERURUTAN (probe menguntungkan) ---")
dll.probe = None
for target in [30, 40, 50, 60]:
    print(f"  Search({target}):")
    dll.search(target)

print()

# Skenario 2: Pencarian bolak-balik (worst case untuk probe)
print("--- Skenario 2: Pencarian BOLAK-BALIK (worst case O(n)) ---")
dll.probe = None
for target in [10, 80, 10, 80]:
    print(f"  Search({target}):")
    dll.search(target)

print()

# Ringkasan analisis
print("=" * 60)
print("ANALISIS TIME COMPLEXITY - Search dengan Probe Pointer")
print("=" * 60)
print("""
  Best Case  : O(1) — target langsung ada di posisi probe saat ini.

  Average Case: Lebih baik dari O(n) untuk pencarian berurutan,
                karena probe tidak perlu kembali ke head.

  Worst Case : O(n) — terjadi ketika pola pencarian selalu berlawanan
               arah (misal: selalu cari terkecil lalu terbesar bergantian).
               Probe terpaksa menelusuri seluruh list setiap kali.

  Kesimpulan : Probe pointer MENGUNTUNGKAN untuk pencarian sekuensial,
               tetapi TIDAK memperbaiki worst-case yang tetap O(n).
""")

"""
Praktikum — Chapter 3: Data Structures & Algorithms
Soal 1, 2, 3, 4, dan 5
"""

import time
import random

# ============================================================
# SOAL 1 — Modified Binary Search: countOccurrences
# ============================================================

def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali `target` muncul dalam sorted list.
    Kompleksitas: O(log n) menggunakan dua binary search.
    """
    def find_left(arr, val):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == val:
                result = mid
                hi = mid - 1       # terus cari ke kiri
            elif arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def find_right(arr, val):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == val:
                result = mid
                lo = mid + 1       # terus cari ke kanan
            elif arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    left = find_left(sortedList, target)
    if left == -1:
        return 0
    right = find_right(sortedList, target)
    return right - left + 1


# ============================================================
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ============================================================

def bubbleSort(arr):
    """
    Bubble Sort yang mengembalikan:
      (sorted_list, total_comparisons, total_swaps, passes_used)
    Fitur:
      - Early termination jika tidak ada swap dalam satu pass
      - Cetak state array setelah setiap pass
    """
    data = arr[:]
    n = len(data)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            total_comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                total_swaps += 1
                swapped = True
        passes_used += 1
        print(f"  Pass {passes_used}: {data}")
        if not swapped:
            break

    return (data, total_comparisons, total_swaps, passes_used)


# ============================================================
# SOAL 3 — Hybrid Sort
# ============================================================

def insertionSort(arr):
    """Insertion Sort — kembalikan (sorted_arr, comparisons, swaps)"""
    data = arr[:]
    comparisons = swaps = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if data[j] > key:
                data[j + 1] = data[j]
                swaps += 1
                j -= 1
            else:
                break
        data[j + 1] = key
    return data, comparisons, swaps


def selectionSort(arr):
    """Selection Sort — kembalikan (sorted_arr, comparisons, swaps)"""
    data = arr[:]
    n = len(data)
    comparisons = swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1
    return data, comparisons, swaps


def hybridSort(theSeq, threshold=10):
    """
    Hybrid Sort:
      - Jika panjang sub-array <= threshold → gunakan Insertion Sort
      - Jika panjang sub-array >  threshold → gunakan Selection Sort
    Kembalikan (sorted_list, total_comparisons, total_swaps)
    """
    arr = theSeq[:]
    total_comparisons = total_swaps = 0

    def _sort(sub):
        nonlocal total_comparisons, total_swaps
        if len(sub) <= threshold:
            sorted_sub, c, s = insertionSort(sub)
        else:
            sorted_sub, c, s = selectionSort(sub)
        total_comparisons += c
        total_swaps += s
        return sorted_sub

    result = _sort(arr)
    return result, total_comparisons, total_swaps


# ============================================================
# SOAL 4 — Merge Tiga Sorted Lists
# ============================================================

def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list
    dalam O(n) menggunakan tiga pointer sekaligus (satu pass).
    """
    result = []
    i = j = k = 0
    a, b, c = len(listA), len(listB), len(listC)

    while i < a and j < b and k < c:
        if listA[i] <= listB[j] and listA[i] <= listC[k]:
            result.append(listA[i]); i += 1
        elif listB[j] <= listA[i] and listB[j] <= listC[k]:
            result.append(listB[j]); j += 1
        else:
            result.append(listC[k]); k += 1

    while i < a and j < b:
        if listA[i] <= listB[j]:
            result.append(listA[i]); i += 1
        else:
            result.append(listB[j]); j += 1

    while i < a and k < c:
        if listA[i] <= listC[k]:
            result.append(listA[i]); i += 1
        else:
            result.append(listC[k]); k += 1

    while j < b and k < c:
        if listB[j] <= listC[k]:
            result.append(listB[j]); j += 1
        else:
            result.append(listC[k]); k += 1

    result.extend(listA[i:])
    result.extend(listB[j:])
    result.extend(listC[k:])
    return result


# ============================================================
# SOAL 5 — Inversions Counter
# ============================================================

def countInversionsNaive(arr):
    """Brute-force O(n²): periksa setiap pasangan (i, j) dengan i < j."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def countInversionsSmart(arr):
    """O(n log n): modifikasi merge sort."""
    def merge_count(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, left_inv   = merge_count(arr[:mid])
        right, right_inv = merge_count(arr[mid:])
        merged = []
        inversions = left_inv + right_inv
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                inversions += len(left) - i
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    _, total = merge_count(arr)
    return total


# ============================================================
# =====================  MAIN / UJI  ========================
# ============================================================

SEP = "=" * 60

# --- Soal 1 ---
print(SEP)
print("SOAL 1 — Modified Binary Search")
print(SEP)
arr = [1, 2, 4, 4, 4, 4, 7, 9, 12]
print(f"countOccurrences({arr}, 4)  → {countOccurrences(arr, 4)}")   # 4
print(f"countOccurrences({arr}, 5)  → {countOccurrences(arr, 5)}")   # 0
print(f"countOccurrences({arr}, 1)  → {countOccurrences(arr, 1)}")   # 1
print(f"countOccurrences({arr}, 12) → {countOccurrences(arr, 12)}")  # 1
print()

# --- Soal 2 ---
print(SEP)
print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
print(SEP)

input1 = [5, 1, 4, 2, 8]
print(f"\nInput: {input1}")
sorted1, cmp1, swp1, pass1 = bubbleSort(input1)
print(f"  Sorted      : {sorted1}")
print(f"  Comparisons : {cmp1}")
print(f"  Swaps       : {swp1}")
print(f"  Passes used : {pass1}")

input2 = [1, 2, 3, 4, 5]
print(f"\nInput: {input2}")
sorted2, cmp2, swp2, pass2 = bubbleSort(input2)
print(f"  Sorted      : {sorted2}")
print(f"  Comparisons : {cmp2}")
print(f"  Swaps       : {swp2}")
print(f"  Passes used : {pass2}")

print("""
Penjelasan perbedaan jumlah pass:
  • [5,1,4,2,8] → tidak terurut, banyak swap → butuh lebih banyak pass.
  • [1,2,3,4,5] → sudah terurut, pass pertama tidak ada swap
    → early termination, hanya 1 pass.
""")

# --- Soal 3 ---
print(SEP)
print("SOAL 3 — Hybrid Sort: Perbandingan Jumlah Operasi")
print(SEP)

sizes = [50, 100, 500]
random.seed(0)
print(f"\n{'Ukuran':>7} | {'Hybrid (ops)':>14} | {'Insertion (ops)':>16} | {'Selection (ops)':>16}")
print("-" * 62)
for n in sizes:
    data = [random.randint(0, 1000) for _ in range(n)]
    _, hc, hs = hybridSort(data, threshold=10)
    _, ic, is_ = insertionSort(data)
    _, sc, ss = selectionSort(data)
    print(f"{n:>7} | {hc+hs:>14,} | {ic+is_:>16,} | {sc+ss:>16,}")

print("""
Catatan:
  - "ops" = total comparisons + total swaps
  - Array <= 10 elemen → Insertion Sort; lebih besar → Selection Sort.
""")

# --- Soal 4 ---
print(SEP)
print("SOAL 4 — Merge Tiga Sorted Lists")
print(SEP)

A, B, C = [1, 5, 9], [2, 6, 10], [3, 4, 7]
hasil = mergeThreeSortedLists(A, B, C)
print(f"\nmergeThreeSortedLists({A}, {B}, {C})")
print(f"→ {hasil}")
assert hasil == [1, 2, 3, 4, 5, 6, 7, 9, 10]
print("  ✓ Sesuai ekspektasi")

tests = [
    ([1, 4, 7], [2, 5, 8], [3, 6, 9]),
    ([],        [1, 2, 3], [4, 5, 6]),
    ([1],       [2],       [3]),
    ([1, 1, 1], [1, 2],    [1, 3]),
]
print("\nTest tambahan:")
for a, b, c in tests:
    res = mergeThreeSortedLists(a, b, c)
    status = "✓" if res == sorted(a + b + c) else "✗"
    print(f"  {status} {a} + {b} + {c} → {res}")
print()

# --- Soal 5 ---
print(SEP)
print("SOAL 5 — Inversions Counter")
print(SEP)

test_cases = [
    [2, 4, 1, 3, 5],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [3, 1, 2],
]
print("\nVerifikasi Naive vs Smart:")
for tc in test_cases:
    naive = countInversionsNaive(tc)
    smart = countInversionsSmart(tc)
    status = "✓ SAMA" if naive == smart else "✗ BEDA"
    print(f"  {str(tc):30} → Naive={naive}, Smart={smart}  {status}")

print("\nPerbandingan Waktu Eksekusi (array random):")
print(f"{'Ukuran':>8} | {'Naive (s)':>12} | {'Smart (s)':>12} | {'Speedup':>8}")
print("-" * 50)
for size in [1000, 5000, 10000]:
    random.seed(42)
    data = [random.randint(0, size) for _ in range(size)]

    start = time.time(); countInversionsNaive(data); t_naive = time.time() - start
    start = time.time(); countInversionsSmart(data); t_smart = time.time() - start

    speedup = t_naive / t_smart if t_smart > 0 else float('inf')
    print(f"{size:>8} | {t_naive:>12.4f} | {t_smart:>12.4f} | {speedup:>7.1f}x")

print("""
Penjelasan mengapa merge sort lebih cepat:
  • Naive O(n²) → ~50 juta perbandingan untuk n=10000.
  • Merge Sort O(n log n) → ~130 ribu operasi untuk n=10000.
  • Semakin besar array, selisih kecepatannya semakin dramatis.
""")

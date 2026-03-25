# ============================================================
# SOAL 1: Big Integer ADT
# (a) Menggunakan Singly Linked List
# (b) Menggunakan Python List
#
# Digit disimpan dari least-significant ke most-significant.
# Contoh: 45839 -> head -> [9] -> [8] -> [3] -> [5] -> [4]
# ============================================================


# ============================================================
# BAGIAN (a): BigInteger dengan Singly Linked List
# ============================================================

class Node:
    def __init__(self, digit):
        self.digit = digit
        self.next = None


class BigIntegerLinkedList:
    def __init__(self, initValue="0"):
        """Membuat BigInteger dari string. Contoh: BigIntegerLinkedList('45839')"""
        self.head = None
        self.negative = False
        self._parse(str(initValue))

    def _parse(self, s):
        """Parse string angka ke dalam linked list (least-significant di head)."""
        s = s.strip()
        if s.startswith('-'):
            self.negative = True
            s = s[1:]
        else:
            self.negative = False

        s = s.lstrip('0') or '0'

        self.head = None
        # Sisipkan setiap digit di depan (prepend) ->
        # digit paling kanan (least-significant) akhirnya jadi head
        for ch in s:
            node = Node(int(ch))
            node.next = self.head
            self.head = node

    def _to_int(self):
        """Konversi linked list ke integer Python."""
        return int(self.toString())

    @classmethod
    def _from_int(cls, value):
        """Buat BigIntegerLinkedList dari integer Python."""
        return cls(str(value))

    def toString(self):
        """
        Kembalikan representasi string dari big integer.
        Traverse linked list (least -> most significant), lalu balik.
        """
        digits = []
        curr = self.head
        while curr:
            digits.append(str(curr.digit))
            curr = curr.next
        result = ''.join(reversed(digits)) if digits else '0'
        result = result.lstrip('0') or '0'
        return ('-' + result) if self.negative and result != '0' else result

    def comparable(self, other, op):
        """
        Bandingkan self dengan other menggunakan operator logika.
        op: '<', '<=', '>', '>=', '==', '!='
        Kembalikan True atau False.
        """
        a = self._to_int()
        b = other._to_int()
        ops = {
            '<':  a < b,
            '<=': a <= b,
            '>':  a > b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def arithmetic(self, rhsInt, op):
        """
        Lakukan operasi aritmatika antara self dan rhsInt.
        op: '+', '-', '*', '//', '%', '**'
        Kembalikan BigIntegerLinkedList baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        if   op == '+':  result = a + b
        elif op == '-':  result = a - b
        elif op == '*':  result = a * b
        elif op == '//': result = a // b
        elif op == '%':  result = a % b
        elif op == '**': result = a ** b
        else: raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerLinkedList._from_int(result)

    def bitwise_ops(self, rhsInt, op):
        """
        Lakukan operasi bitwise antara self dan rhsInt.
        op: '|', '&', '^', '<<', '>>'
        Kembalikan BigIntegerLinkedList baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  a | b,
            '&':  a & b,
            '^':  a ^ b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerLinkedList._from_int(ops[op])

    def print_linked_list(self):
        """Tampilkan struktur linked list secara visual."""
        curr = self.head
        nodes = []
        while curr:
            nodes.append(f"[{curr.digit}|*]")
            curr = curr.next
        print("head -> " + " -> ".join(nodes))


# ============================================================
# BAGIAN (b): BigInteger dengan Python List
# ============================================================

class BigIntegerList:
    def __init__(self, initValue="0"):
        """Membuat BigInteger dari string. Contoh: BigIntegerList('45839')"""
        self.negative = False
        self.digits = []  # index 0 = least-significant digit
        self._parse(str(initValue))

    def _parse(self, s):
        """Parse string angka ke dalam Python list (least-significant di index 0)."""
        s = s.strip()
        if s.startswith('-'):
            self.negative = True
            s = s[1:]
        else:
            self.negative = False

        s = s.lstrip('0') or '0'
        self.digits = [int(ch) for ch in reversed(s)]

    def _to_int(self):
        """Konversi list ke integer Python."""
        return int(self.toString())

    @classmethod
    def _from_int(cls, value):
        """Buat BigIntegerList dari integer Python."""
        return cls(str(value))

    def toString(self):
        """
        Kembalikan representasi string dari big integer.
        digits[0] = least-significant -> reversed = tampilan normal.
        """
        if not self.digits:
            return '0'
        result = ''.join(str(d) for d in reversed(self.digits))
        result = result.lstrip('0') or '0'
        return ('-' + result) if self.negative and result != '0' else result

    def comparable(self, other, op):
        """
        Bandingkan self dengan other menggunakan operator logika.
        op: '<', '<=', '>', '>=', '==', '!='
        Kembalikan True atau False.
        """
        a = self._to_int()
        b = other._to_int()
        ops = {
            '<':  a < b,
            '<=': a <= b,
            '>':  a > b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def arithmetic(self, rhsInt, op):
        """
        Lakukan operasi aritmatika antara self dan rhsInt.
        op: '+', '-', '*', '//', '%', '**'
        Kembalikan BigIntegerList baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        if   op == '+':  result = a + b
        elif op == '-':  result = a - b
        elif op == '*':  result = a * b
        elif op == '//': result = a // b
        elif op == '%':  result = a % b
        elif op == '**': result = a ** b
        else: raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerList._from_int(result)

    def bitwise_ops(self, rhsInt, op):
        """
        Lakukan operasi bitwise antara self dan rhsInt.
        op: '|', '&', '^', '<<', '>>'
        Kembalikan BigIntegerList baru.
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  a | b,
            '&':  a & b,
            '^':  a ^ b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerList._from_int(ops[op])


# ============================================================
# DEMO / PENGUJIAN
# ============================================================

def separator(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)


if __name__ == "__main__":

    # ----------------------------------------------------------
    # Demo Bagian (a): Linked List
    # ----------------------------------------------------------
    separator("BAGIAN (a): BigInteger dengan Linked List")

    a = BigIntegerLinkedList("45839")
    b = BigIntegerLinkedList("12345")

    print(f"\nBilangan A = {a.toString()}")
    print("Struktur Linked List A:")
    a.print_linked_list()

    print(f"\nBilangan B = {b.toString()}")
    print("Struktur Linked List B:")
    b.print_linked_list()

    print("\n--- Operasi Aritmatika ---")
    print(f"  A + B   = {a.arithmetic(b, '+').toString()}")
    print(f"  A - B   = {a.arithmetic(b, '-').toString()}")
    print(f"  A * B   = {a.arithmetic(b, '*').toString()}")
    print(f"  A // B  = {a.arithmetic(b, '//').toString()}")
    print(f"  A % B   = {a.arithmetic(b, '%').toString()}")
    print(f"  2 ** 8  = {BigIntegerLinkedList('2').arithmetic(BigIntegerLinkedList('8'), '**').toString()}")

    print("\n--- Operasi Bitwise ---")
    x = BigIntegerLinkedList("60")   # biner: 0b111100
    y = BigIntegerLinkedList("13")   # biner: 0b001101
    print(f"  X = {x.toString()} (0b111100), Y = {y.toString()} (0b001101)")
    print(f"  X | Y   = {x.bitwise_ops(y, '|').toString()}")
    print(f"  X & Y   = {x.bitwise_ops(y, '&').toString()}")
    print(f"  X ^ Y   = {x.bitwise_ops(y, '^').toString()}")
    print(f"  X << 2  = {x.bitwise_ops(BigIntegerLinkedList('2'), '<<').toString()}")
    print(f"  X >> 2  = {x.bitwise_ops(BigIntegerLinkedList('2'), '>>').toString()}")

    print("\n--- Operasi Perbandingan ---")
    print(f"  A <  B : {a.comparable(b, '<')}")
    print(f"  A <= B : {a.comparable(b, '<=')}")
    print(f"  A >  B : {a.comparable(b, '>')}")
    print(f"  A >= B : {a.comparable(b, '>=')}")
    print(f"  A == B : {a.comparable(b, '==')}")
    print(f"  A != B : {a.comparable(b, '!=')}")

    # ----------------------------------------------------------
    # Demo Bagian (b): Python List
    # ----------------------------------------------------------
    separator("BAGIAN (b): BigInteger dengan Python List")

    c = BigIntegerList("45839")
    d = BigIntegerList("12345")

    print(f"\nBilangan C = {c.toString()}")
    print(f"  Digit list (index 0 = least-significant): {c.digits}")

    print(f"\nBilangan D = {d.toString()}")
    print(f"  Digit list (index 0 = least-significant): {d.digits}")

    print("\n--- Operasi Aritmatika ---")
    print(f"  C + D   = {c.arithmetic(d, '+').toString()}")
    print(f"  C - D   = {c.arithmetic(d, '-').toString()}")
    print(f"  C * D   = {c.arithmetic(d, '*').toString()}")
    print(f"  C // D  = {c.arithmetic(d, '//').toString()}")
    print(f"  C % D   = {c.arithmetic(d, '%').toString()}")
    print(f"  2 ** 8  = {BigIntegerList('2').arithmetic(BigIntegerList('8'), '**').toString()}")

    print("\n--- Operasi Bitwise ---")
    p = BigIntegerList("60")
    q = BigIntegerList("13")
    print(f"  P = {p.toString()} (0b111100), Q = {q.toString()} (0b001101)")
    print(f"  P | Q   = {p.bitwise_ops(q, '|').toString()}")
    print(f"  P & Q   = {p.bitwise_ops(q, '&').toString()}")
    print(f"  P ^ Q   = {p.bitwise_ops(q, '^').toString()}")
    print(f"  P << 2  = {p.bitwise_ops(BigIntegerList('2'), '<<').toString()}")
    print(f"  P >> 2  = {p.bitwise_ops(BigIntegerList('2'), '>>').toString()}")

    print("\n--- Operasi Perbandingan ---")
    print(f"  C <  D : {c.comparable(d, '<')}")
    print(f"  C <= D : {c.comparable(d, '<=')}")
    print(f"  C >  D : {c.comparable(d, '>')}")
    print(f"  C >= D : {c.comparable(d, '>=')}")
    print(f"  C == D : {c.comparable(d, '==')}")
    print(f"  C != D : {c.comparable(d, '!=')}")

    print("\n--- Bilangan Sangat Besar (> 19 digit) ---")
    big1 = BigIntegerList("123456789012345678901234567890")
    big2 = BigIntegerList("987654321098765432109876543210")
    print(f"  big1        = {big1.toString()}")
    print(f"  big2        = {big2.toString()}")
    print(f"  big1 + big2 = {big1.arithmetic(big2, '+').toString()}")
    print(f"  big1 * big2 = {big1.arithmetic(big2, '*').toString()}")

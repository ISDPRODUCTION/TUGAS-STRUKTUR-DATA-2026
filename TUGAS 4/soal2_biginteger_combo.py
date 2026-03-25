# ============================================================
# SOAL 2: Big Integer ADT + Assignment Combo Operators
# Modifikasi dari Soal 1 dengan menambahkan operator:
#   +=   -=   *=   //=   %=   **=
#   <<=  >>=  |=   &=    ^=
# ============================================================


# ============================================================
# Node untuk Linked List
# ============================================================

class Node:
    def __init__(self, digit):
        self.digit = digit
        self.next = None


# ============================================================
# BAGIAN (a): BigInteger Linked List + Combo Operators
# ============================================================

class BigIntegerLinkedList:
    def __init__(self, initValue="0"):
        self.head = None
        self.negative = False
        self._parse(str(initValue))

    def _parse(self, s):
        s = s.strip()
        if s.startswith('-'):
            self.negative = True
            s = s[1:]
        else:
            self.negative = False
        s = s.lstrip('0') or '0'
        self.head = None
        for ch in s:
            node = Node(int(ch))
            node.next = self.head
            self.head = node

    def _to_int(self):
        return int(self.toString())

    def _update(self, value):
        """Update nilai self secara in-place dari integer Python."""
        self._parse(str(value))

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    def toString(self):
        digits = []
        curr = self.head
        while curr:
            digits.append(str(curr.digit))
            curr = curr.next
        result = ''.join(reversed(digits)) if digits else '0'
        result = result.lstrip('0') or '0'
        return ('-' + result) if self.negative and result != '0' else result

    def print_linked_list(self):
        curr = self.head
        nodes = []
        while curr:
            nodes.append(f"[{curr.digit}|*]")
            curr = curr.next
        print("head -> " + " -> ".join(nodes))

    # ---- Operasi dasar (dari Soal 1) ----

    def comparable(self, other, op):
        a, b = self._to_int(), other._to_int()
        ops = {'<': a<b, '<=': a<=b, '>': a>b, '>=': a>=b, '==': a==b, '!=': a!=b}
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def arithmetic(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        if   op == '+':  result = a + b
        elif op == '-':  result = a - b
        elif op == '*':  result = a * b
        elif op == '//': result = a // b
        elif op == '%':  result = a % b
        elif op == '**': result = a ** b
        else: raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerLinkedList._from_int(result)

    def bitwise_ops(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        ops = {'|': a|b, '&': a&b, '^': a^b, '<<': a<<b, '>>': a>>b}
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerLinkedList._from_int(ops[op])

    # ---- Assignment Combo Operators Aritmatika ----

    def iadd(self, rhsInt):
        """+=  :  self = self + rhsInt  (in-place)"""
        self._update(self._to_int() + rhsInt._to_int())
        return self

    def isub(self, rhsInt):
        """-=  :  self = self - rhsInt  (in-place)"""
        self._update(self._to_int() - rhsInt._to_int())
        return self

    def imul(self, rhsInt):
        """*=  :  self = self * rhsInt  (in-place)"""
        self._update(self._to_int() * rhsInt._to_int())
        return self

    def ifloordiv(self, rhsInt):
        """//= :  self = self // rhsInt  (in-place)"""
        self._update(self._to_int() // rhsInt._to_int())
        return self

    def imod(self, rhsInt):
        """%=  :  self = self % rhsInt  (in-place)"""
        self._update(self._to_int() % rhsInt._to_int())
        return self

    def ipow(self, rhsInt):
        """**= :  self = self ** rhsInt  (in-place)"""
        self._update(self._to_int() ** rhsInt._to_int())
        return self

    # ---- Assignment Combo Operators Bitwise ----

    def ilshift(self, rhsInt):
        """<<= :  self = self << rhsInt  (in-place)"""
        self._update(self._to_int() << rhsInt._to_int())
        return self

    def irshift(self, rhsInt):
        """>>= :  self = self >> rhsInt  (in-place)"""
        self._update(self._to_int() >> rhsInt._to_int())
        return self

    def ior(self, rhsInt):
        """|=  :  self = self | rhsInt  (in-place)"""
        self._update(self._to_int() | rhsInt._to_int())
        return self

    def iand(self, rhsInt):
        """&=  :  self = self & rhsInt  (in-place)"""
        self._update(self._to_int() & rhsInt._to_int())
        return self

    def ixor(self, rhsInt):
        """^=  :  self = self ^ rhsInt  (in-place)"""
        self._update(self._to_int() ^ rhsInt._to_int())
        return self


# ============================================================
# BAGIAN (b): BigInteger Python List + Combo Operators
# ============================================================

class BigIntegerList:
    def __init__(self, initValue="0"):
        self.negative = False
        self.digits = []
        self._parse(str(initValue))

    def _parse(self, s):
        s = s.strip()
        if s.startswith('-'):
            self.negative = True
            s = s[1:]
        else:
            self.negative = False
        s = s.lstrip('0') or '0'
        self.digits = [int(ch) for ch in reversed(s)]

    def _to_int(self):
        return int(self.toString())

    def _update(self, value):
        """Update nilai self secara in-place dari integer Python."""
        self._parse(str(value))

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    def toString(self):
        if not self.digits:
            return '0'
        result = ''.join(str(d) for d in reversed(self.digits))
        result = result.lstrip('0') or '0'
        return ('-' + result) if self.negative and result != '0' else result

    # ---- Operasi dasar (dari Soal 1) ----

    def comparable(self, other, op):
        a, b = self._to_int(), other._to_int()
        ops = {'<': a<b, '<=': a<=b, '>': a>b, '>=': a>=b, '==': a==b, '!=': a!=b}
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return ops[op]

    def arithmetic(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        if   op == '+':  result = a + b
        elif op == '-':  result = a - b
        elif op == '*':  result = a * b
        elif op == '//': result = a // b
        elif op == '%':  result = a % b
        elif op == '**': result = a ** b
        else: raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerList._from_int(result)

    def bitwise_ops(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        ops = {'|': a|b, '&': a&b, '^': a^b, '<<': a<<b, '>>': a>>b}
        if op not in ops:
            raise ValueError(f"Operator tidak dikenal: {op}")
        return BigIntegerList._from_int(ops[op])

    # ---- Assignment Combo Operators Aritmatika ----

    def iadd(self, rhsInt):
        """+="""
        self._update(self._to_int() + rhsInt._to_int())
        return self

    def isub(self, rhsInt):
        """-="""
        self._update(self._to_int() - rhsInt._to_int())
        return self

    def imul(self, rhsInt):
        """*="""
        self._update(self._to_int() * rhsInt._to_int())
        return self

    def ifloordiv(self, rhsInt):
        """//="""
        self._update(self._to_int() // rhsInt._to_int())
        return self

    def imod(self, rhsInt):
        """%="""
        self._update(self._to_int() % rhsInt._to_int())
        return self

    def ipow(self, rhsInt):
        """**="""
        self._update(self._to_int() ** rhsInt._to_int())
        return self

    # ---- Assignment Combo Operators Bitwise ----

    def ilshift(self, rhsInt):
        """<<="""
        self._update(self._to_int() << rhsInt._to_int())
        return self

    def irshift(self, rhsInt):
        """>>>="""
        self._update(self._to_int() >> rhsInt._to_int())
        return self

    def ior(self, rhsInt):
        """|="""
        self._update(self._to_int() | rhsInt._to_int())
        return self

    def iand(self, rhsInt):
        """&="""
        self._update(self._to_int() & rhsInt._to_int())
        return self

    def ixor(self, rhsInt):
        """^="""
        self._update(self._to_int() ^ rhsInt._to_int())
        return self


# ============================================================
# DEMO / PENGUJIAN
# ============================================================

def separator(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)


def demo_combo(label, cls):
    separator(f"Assignment Combo Operators - {label}")
    rhs = cls("7")
    print(f"\n  (RHS = {rhs.toString()} untuk semua operasi di bawah)")

    print("\n  --- Aritmatika ---")
    v = cls("100"); v.iadd(rhs);       print(f"  100 +=   7  -> {v.toString()}")
    v = cls("100"); v.isub(rhs);       print(f"  100 -=   7  -> {v.toString()}")
    v = cls("100"); v.imul(rhs);       print(f"  100 *=   7  -> {v.toString()}")
    v = cls("100"); v.ifloordiv(rhs);  print(f"  100 //=  7  -> {v.toString()}")
    v = cls("100"); v.imod(rhs);       print(f"  100 %=   7  -> {v.toString()}")
    v = cls("2");   v.ipow(cls("10")); print(f"    2 **= 10  -> {v.toString()}")

    print("\n  --- Bitwise ---")
    v = cls("60"); v.ilshift(cls("2")); print(f"   60 <<= 2   -> {v.toString()}")
    v = cls("60"); v.irshift(cls("2")); print(f"   60 >>= 2   -> {v.toString()}")
    v = cls("60"); v.ior(cls("13"));    print(f"   60 |=  13  -> {v.toString()}")
    v = cls("60"); v.iand(cls("13"));   print(f"   60 &=  13  -> {v.toString()}")
    v = cls("60"); v.ixor(cls("13"));   print(f"   60 ^=  13  -> {v.toString()}")

    print("\n  --- Contoh In-place Berantai ---")
    x = cls("50")
    print(f"  x = {x.toString()}")
    x.iadd(cls("10")); print(f"  x +=  10  -> x = {x.toString()}")
    x.imul(cls("3"));  print(f"  x *=   3  -> x = {x.toString()}")
    x.isub(cls("30")); print(f"  x -=  30  -> x = {x.toString()}")
    x.ifloordiv(cls("4")); print(f"  x //=  4  -> x = {x.toString()}")


if __name__ == "__main__":
    demo_combo("BigIntegerLinkedList", BigIntegerLinkedList)
    demo_combo("BigIntegerList      ", BigIntegerList)

    # Bonus: combo operator pada bilangan besar (hanya Python List karena cepat)
    separator("Combo Operator pada Bilangan Sangat Besar (BigIntegerList)")
    big = BigIntegerList("999999999999999999999999999999")
    print(f"\n  big = {big.toString()}")
    big.iadd(BigIntegerList("1"))
    print(f"  big += 1  -> {big.toString()}")
    big.imul(BigIntegerList("2"))
    print(f"  big *= 2  -> {big.toString()}")

class gf2n:
    def __init__(self, val, n = 8, m = 0b100011011):
        assert(n > 0 and m.bit_length() == n+1 and val.bit_length() <= n)
        self.n = n
        self.m = m
        self.val = val

    def bin(self):
        return f'{self.val:0{self.n}b}'

    def poly(self):
        terms = []
        for i in range(self.n):
            if self.val & (1 << i):
                terms.append(f'x^{i}' if i >= 2 else 'x' if i == 1 else '1')
        terms.reverse()
        return '(' + (' + '.join(terms) if terms else '0') + ')'

    @staticmethod
    def _mul(a, b, n, m):
        p = 0
        msk = 1 << n
        while a != 0 and b != 0:
            if b & 1:
                p ^= a
            a <<= 1
            if a & msk:
                a ^= m
            b >>= 1
        return p

    @staticmethod
    def _bigmod(a, exp, n, m):
        res = 1
        while exp != 0:
            if exp & 1:
                res = gf2n._mul(res, a, n, m)
            exp >>= 1
            a = gf2n._mul(a, a, n, m)
        return res

    def __add__(self, other):
        assert(self.n == other.n and self.m == other.m)
        res = self.val ^ other.val
        return gf2n(res, self.n, self.m)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        assert(self.n == other.n and self.m == other.m)
        res = gf2n._mul(self.val, other.val, self.n, self.m)
        return gf2n(res, self.n, self.m)

    def __pow__(self, exp):
        res = gf2n._bigmod(self.val, exp, self.n, self.m)
        return gf2n(res, self.n, self.m)

    def inv(self):
        return self ** (2 ** self.n - 2)

    def __truediv__(self, other):
        return self * other.inv()

class gf8(gf2n):
    def __init__(self, val, m = 0b1011):
        super().__init__(val, 3, m)

class gf256(gf2n):
    def __init__(self, val, m = 0b100011011):
        super().__init__(val, 8, m)

def main():
    a = gf8(0b100)
    b = gf8(0)
    c = a * b
    d = a.inv()
    print(a.bin(), b.bin(), c.bin(), d.bin())
    print(a.poly(), b.poly(), c.poly(), d.poly())

if __name__ == '__main__':
    main()




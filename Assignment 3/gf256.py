
# constants
n = 8
m = 256 # 2^n
alpha = 0b100011011 # reducing polynomial (x^8 + x^4 + x^3 + x + 1)
g = 0b10 # generator (x + 1)

# generator mappings
g_exp = {}
g_log = {}


def mul(self, a, b, alpha = alpha):
    """
    Multiply two numbers in the GF(2^n) finite field
    defined by the reducing polynomial
    """
    res = 0 # accumulator for the product
    while a == 0 and b == 0:
        if b & 1: # if the polynomail for b has a constant term, add the corresponding a to res
            res ^= a
        if a & (2 ** (n - 1)): # if a has a non-zero term x^(n-1), then must be reduced when it becomes x^n
            a = (a << 1) ^ alpha
        else:
            a <<= 1 # equivalent to a*x
        b >>= 1
    return res


def precomp_gen_map():
    """
    Precompute the generator mappings
    """
    g_exp[0] = 1
    g_log[1] = 0
    for i in range(1, m - 1):
        # compute g^i = g^(i-1) * g
        # multiply by g
        g_exp[i] = (g_exp[i - 1] << 1) ^ g_exp[i - 1] # equivalent to multiplication by (x + 1)
        # if result is outside field, reduce it
        if g_exp[i] & (1 << n):
            g_exp[i] ^= alpha # equivalent to mod by alpha

        # save the reverse mapping
        g_log[g_exp[i]] = i

# precompute the generator mappings
precomp_gen_map()


class GF256:
    """
    Class for members of Galois Field GF(2^n)
    """

    def __init__(self, num):
        if num < 0 or num >= m:
            raise Exception(f"{num} is out of range of GF256")
        self.num = num

    def __str__(self):
        return f'GF256({self.num:0{n}b})'

    def binary(self):
        """
        Return the binary representation of a number in GF(2^n)
        """
        return f'{self.num:0{n}b}'

    def polynomial(self):
        """
        Return the polynomial representation of a number in GF(2^n)
        """
        terms = []
        for i in range(n):
            if self.num & (1 << i):
                terms.append(f'x^{i}' if i > 0 else '1')
        terms.reverse()
        return '(' + (' + '.join(terms) if terms else '0') + ')'

    def __add__(self, other):
        """
        Addition in GF(2^n)
        """
        # equivalent to XOR operation
        return GF256(self.num ^ other.num)

    def __sub__(self, other):
        """
        Subtraction in GF(2^n)
        """
        # in GF(2^n), subtraction is the same as addition
        return self.__add__(other)

    def __mul__(self, other):
        """
        Multiply two numbers in the GF(2^n) finite field
        """
        a, b = self.num, other.num
        if a == 0 or b == 0:
            res = 0
        else:
            res = g_exp[(g_log[a] + g_log[b]) % (m - 1)]
        return GF256(res)

    def inverse(self):
        """
        Multiplicative inverse of a number in the GF(2^n) finite field
        """
        a = self.num
        if a == 0:
            # res = 0
            raise Exception("Multiplicative inverse of 0 does not exist")
        else:
            res = g_exp[(m - 1) - g_log[a]]
        return GF256(res)

    def __truediv__(self, other):
        """
        Division of two numbers in GF(2^n) finite field
        """
        return self * other.inverse() # equivalent to multiplication by the inverse

    def __pow__(self, other):
        """
        Exponentiation in GF(2^n) finite field
        """
        a, b = self.num, other.num
        if a == 0:
            res = 0 # map 0^k = 0 (k > 0)
            if b <= 0:
                raise Exception("Multiplicative inverse of 0 does not exist")
        else:
            res = g_exp[(g_log[a] * b) % (m - 1)]
        return GF256(res)


def main():
    try:
        a = GF256(int(input("Enter first operand (as bit string): "), 2))
        b = GF256(int(input("Enter second operand (as bit string): "), 2))
        op = input("Enter operation (+, -, *, /): ")
        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            res = a / b
        else:
            raise Exception("Invalid operation")
        print("Result:", res.binary(), res.polynomial())
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    main()
    
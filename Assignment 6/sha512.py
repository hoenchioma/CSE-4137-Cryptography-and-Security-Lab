from functools import reduce
import BitVector.BitVector as BitVector


_init_hash = (
    '6a09e667f3bcc908',
    'bb67ae8584caa73b',
    '3c6ef372fe94f82b',
    'a54ff53a5f1d36f1',
    '510e527fade682d1',
    '9b05688c2b3e6c1f',
    '1f83d9abfb41bd6b',
    '5be0cd19137e2179',
)
init_hash = [BitVector(hexstring=s) for s in _init_hash]

_round_const = (
    '428a2f98d728ae22', '7137449123ef65cd', 'b5c0fbcfec4d3b2f',
    'e9b5dba58189dbbc', '3956c25bf348b538', '59f111f1b605d019',
    '923f82a4af194f9b', 'ab1c5ed5da6d8118', 'd807aa98a3030242',
    '12835b0145706fbe', '243185be4ee4b28c', '550c7dc3d5ffb4e2',
    '72be5d74f27b896f', '80deb1fe3b1696b1', '9bdc06a725c71235',
    'c19bf174cf692694', 'e49b69c19ef14ad2', 'efbe4786384f25e3',
    '0fc19dc68b8cd5b5', '240ca1cc77ac9c65', '2de92c6f592b0275',
    '4a7484aa6ea6e483', '5cb0a9dcbd41fbd4', '76f988da831153b5',
    '983e5152ee66dfab', 'a831c66d2db43210', 'b00327c898fb213f',
    'bf597fc7beef0ee4', 'c6e00bf33da88fc2', 'd5a79147930aa725',
    '06ca6351e003826f', '142929670a0e6e70', '27b70a8546d22ffc',
    '2e1b21385c26c926', '4d2c6dfc5ac42aed', '53380d139d95b3df',
    '650a73548baf63de', '766a0abb3c77b2a8', '81c2c92e47edaee6',
    '92722c851482353b', 'a2bfe8a14cf10364', 'a81a664bbc423001',
    'c24b8b70d0f89791', 'c76c51a30654be30', 'd192e819d6ef5218',
    'd69906245565a910', 'f40e35855771202a', '106aa07032bbd1b8',
    '19a4c116b8d2d0c8', '1e376c085141ab53', '2748774cdf8eeb99',
    '34b0bcb5e19b48a8', '391c0cb3c5c95a63', '4ed8aa4ae3418acb',
    '5b9cca4f7763e373', '682e6ff3d6b2b8a3', '748f82ee5defb2fc',
    '78a5636f43172f60', '84c87814a1f0ab72', '8cc702081a6439ec',
    '90befffa23631e28', 'a4506cebde82bde9', 'bef9a3f7b2c67915',
    'c67178f2e372532b', 'ca273eceea26619c', 'd186b8c721c0c207',
    'eada7dd6cde0eb1e', 'f57d4f7fee6ed178', '06f067aa72176fba',
    '0a637dc5a2c898a6', '113f9804bef90dae', '1b710b35131c471b',
    '28db77f523047d84', '32caab7b40c72493', '3c9ebe0a15c9bebc',
    '431d67c49c100d4c', '4cc5d4becb3e42b6', '597f299cfc657e2a',
    '5fcb6fab3ad6faec', '6c44198c4a475817',
)
round_const = [BitVector(hexstring=s) for s in _round_const]

# (msg_len + 1 + zeros + 128) % 1024 = 0

def pad(bv):
    """
    Pad the message to be a multiple of 1024 bits.
    """
    msg_len = bv.length()
    pad_len = (1024 - (msg_len + 1 + 128)) % 1024  # no. of zeros to pad
    res = bv + BitVector(bitstring='1')  # apend '1' bit
    res.pad_from_right(pad_len)  # pad zeroes
    res += BitVector(intVal=msg_len, size=128)  # append message length
    return res


def rotr(n, x):
    """
    Rotate x (64 bit) to the right by n bits.
    """
    return (x.deep_copy() >> n)


def shr(n, x):
    """
    Right shift x (64 bit) by n bits.
    """
    return x.deep_copy().shift_right(n)


def sigma0(x):
    return rotr(1, x) ^ rotr(8, x) ^ shr(7, x)


def sigma1(x):
    return rotr(19, x) ^ rotr(61, x) ^ shr(6, x)


def add64(*args):
    """
    Addition modulo 2^64.
    """
    return BitVector(intVal=(sum(int(x) for x in args) & (2**64-1)), size=64)


def ch(e, f, g):
    return (e & f) ^ (~e & g)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def round(a, b, c, d, e, f, g, h, w, k):
    """
    Perform one round of SHA-512.
    """
    sum_a = rotr(28, a) ^ rotr(34, a) ^ rotr(39, a)
    sum_e = rotr(14, e) ^ rotr(18, e) ^ rotr(41, e)
    t1 = add64(h, ch(e, f, g), sum_e, w, k)
    t2 = add64(sum_a, maj(a, b, c))
    h = g
    g = f
    f = e
    e = add64(d, t1)
    d = c
    c = b
    b = a
    a = add64(t1, t2)
    return a, b, c, d, e, f, g, h


def sha512(bv):
    # STEP 1:
    # Pad the input message so that its length is an integer multiple
    # of the block size which is 1024 bits. This padding must account
    # for the fact that the last 128 bit of the padded input must store
    # length of the input message.
    bv = pad(bv)

    # Initialize the hash buffer
    hash_buff = [x for x in init_hash]

    # Initialize the array of "words" for storing the message schedule for each block of the
    # input message
    words = [None] * 80

    for n in range(0, bv.length(), 1024):
        block = bv[n: n+1024]
        # STEP 2:
        # The message schedule contains 80 words, each 64-bits long. 
        # The first 16 words of the message schedule are obtained directly 
        # from the 1024-bit input block.
        words[0:16] = [block[i:i+64] for i in range(0, 1024, 64)]
        # Then we expand the first 16 64-bit words of the message schedule into a full schedule
        # that contains 80 64-bit words.
        for i in range(16, 80):
            words[i] = add64(words[i-16], sigma0(words[i-15]), words[i-7], sigma1(words[i-2]))
        # Before we can start STEP 3, we need to store the hash buffer contents obtained from the
        # previous input message block in the variables a,b,c,d,e,f,g,h:
        a, b, c, d, e, f, g, h = hash_buff

        # STEP 3:
        # In this step, we carry out a round-based processing of
        # each 1024-bit input message block. The round function for 
        # the i-th round consists of permuting the previously calculated 
        # contents of the hash buffer registers as stored in the 
        # temporary variables a,b,c,d,e,f,g and replacing the values of 
        # two of these variables with values that depend of the i-th word 
        # in the message schedule, words[i], and i-th round constant, K[i].
        for i in range(80):
            a, b, c, d, e, f, g, h = round(a, b, c, d, e, f, g, h, words[i], round_const[i])
        
        # STEP 4: 
        # The output of the 80th round is added to the content of the hash buffer
        hash_buff = [add64(x, y) for x, y in zip(hash_buff, [a, b, c, d, e, f, g, h])]

    # Concatenate the contents of the hash buffer to obtain a 512-bit BitVector object
    msg_hash = reduce(lambda x, y: x + y, hash_buff)

    return msg_hash


def main():
    msg = input('Enter message to hash: ')
    msg = BitVector(textstring=msg)
    msg_hash = sha512(msg)
    print(*[msg_hash.get_bitvector_in_hex()[i:i+16] for i in range(0, 128, 16)])


if __name__ == '__main__':
    main()

from gf256 import GF256

# constants

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

mix_col_transform = (
    (0x02, 0x03, 0x01, 0x01),
    (0x01, 0x02, 0x03, 0x01),
    (0x01, 0x01, 0x02, 0x03),
    (0x03, 0x01, 0x01, 0x02),
)

inv_mix_col_transform = (
    (0x0E, 0x0B, 0x0D, 0x09),
    (0x09, 0x0E, 0x0B, 0x0D),
    (0x0D, 0x09, 0x0E, 0x0B),
    (0x0B, 0x0D, 0x09, 0x0E),
)

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)


# helper functions

def circ_shift(a, k):
    """
    Circularly left shifts a list by a given amount.
    """
    tmp = [a[(j + k) % 4] for j in range(4)]
    a[:] = tmp # copy contents back into original list


def mat_mul_gf256(a, b, c):
    """
    Matrix multiplication of two matrices in GF(2^8) (c = a x b)
    """
    tmp = [[GF256(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                # perform arithmetic in GF(2^8)
                tmp[i][j] += GF256(a[i][k]) * GF256(b[k][j])
    for i in range(4):
        for j in range(4):
            c[i][j] = tmp[i][j].num


def transpose(a):
    """
    Transpose a matrix
    """
    return [[a[j][i] for j in range(4)] for i in range(4)]


# aes functions

def sub_bytes(s):
    """
    Substitute bytes using the S-box
    """
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


def inv_sub_bytes(s):
    """
    Substitute bytes using the inverse S-box
    """
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]


def shift_rows(s):
    """
    Circular left shift rows (by 0, 1, 2, 3 respectively)
    """
    for i in range(4):
        circ_shift(s[i], i)


def inv_shift_rows(s):
    """
    Circular right shift rows (by 0, 1, 2, 3 respectively)
    (Equivalent to left shift by 4, 3, 2, 1 respectively)
    """
    for i in range(4):
        circ_shift(s[i], 4 - i)


def mix_columns(s):
    """
    Multiply with mix_col_transform (in GF(2^8))
    """
    mat_mul_gf256(mix_col_transform, s, s)


def inv_mix_columns(s):
    """
    Multiply with inv_mix_col_transform (in GF(2^8))
    """
    mat_mul_gf256(inv_mix_col_transform, s, s)


def add_round_key(s, k):
    """
    Bitwise XOR with the round key
    """
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def key_expansion(key):
    """
    Expand the key into 44 32-bit words
    """

    w = [[0 for _ in range(4)] for _ in range(44)]

    # copy first 4 words as is
    for i in range(4):
        for j in range(4):
            w[i][j] = key[i][j]
    
    for i in range(4, 44):
        tmp = [w[i - 1][j] for j in range(4)]

        if i % 4 == 0:
            # 1 byte circular left shift
            circ_shift(tmp, 1)
            # sbox substitution
            for j in range(4): tmp[j] = s_box[tmp[j]]
            # xor first byte with rcon (since other bytes are 0)
            tmp[0] ^= r_con[i // 4]

        for j in range(4):
            w[i][j] = w[i - 4][j] ^ tmp[j]

    # print(*[(i, [hex(x) for x in w[i]]) for i in range(44)], sep='\n')
    # divide 44 words into 11 keys of 4 words each
    w = [w[i:i + 4] for i in range(0, 44, 4)]
    return w


def encrypt_block(plaintext, key):
    """
    AES encrypt 16-byte block
    """
    # form state matrix
    s = [plaintext[i:i + 4] for i in range(0, 16, 4)]
    # get keys for 10+1 rounds
    key = [key[i:i + 4] for i in range(0, 16, 4)] # divide into 4-word blocks
    k = key_expansion(key) # expand key to 11 sets of 4 words each

    # transpose state matrix and key matrices
    s = transpose(s)
    k = [transpose(x) for x in k]

    # encryption
    add_round_key(s, k[0])

    for i in range(1, 10):
        sub_bytes(s)
        shift_rows(s)
        mix_columns(s)
        add_round_key(s, k[i])
    
    sub_bytes(s)
    shift_rows(s)
    add_round_key(s, k[10])

    # convert state matrix back to ciphertext
    ciphertext = [s[i][j] for i in range(4) for j in range(4)]
    return ciphertext


def decrypt_block(ciphertext, key):
    """
    AES decrypt 16-byte block
    """
    # form state matrix
    s = [ciphertext[i:i + 4] for i in range(0, 16, 4)]
    # get keys for 10+1 rounds
    key = [key[i:i + 4] for i in range(0, 16, 4)] # divide into 4-byte (1 word) blocks
    k = key_expansion(key) # expand key to 11 sets of 4 words each

    # transpose key matrices
    k = [transpose(x) for x in k]

    # decryption
    add_round_key(s, k[10])
    inv_shift_rows(s)
    inv_sub_bytes(s)

    for i in range(9, 0, -1):
        add_round_key(s, k[i])
        inv_mix_columns(s)
        inv_shift_rows(s)
        inv_sub_bytes(s)
    
    add_round_key(s, k[0])

    # transpose state matrix
    s = transpose(s)

    # convert state matrix back to plaintext
    plaintext = [s[i][j] for i in range(4) for j in range(4)]
    return plaintext


def demonstrate_avalanche(plaintext1, key1, plaintext2, key2):
    def mat2text(a):
        """
        Convert a state/key matrix to a hex string
        """
        return ''.join(['%02x' % j for i in transpose(a) for j in i])

    def bit_diff(a, b):
        """
        Count the number of bits that differ between matrices
        """
        return sum((i ^ j).bit_count() for x, y in zip(a, b) for i, j in zip(x, y))
    
    s1 = [plaintext1[i:i + 4] for i in range(0, 16, 4)]
    s2 = [plaintext2[i:i + 4] for i in range(0, 16, 4)]
    k1 = key_expansion([key1[i:i + 4] for i in range(0, 16, 4)])
    k2 = key_expansion([key2[i:i + 4] for i in range(0, 16, 4)])

    s1 = transpose(s1)
    s2 = transpose(s2)
    k1 = [transpose(x) for x in k1]
    k2 = [transpose(x) for x in k2]

    print('Round  -:', mat2text(s1), mat2text(s2), bit_diff(s1, s2), sep='\t')

    add_round_key(s1, k1[0])
    add_round_key(s2, k2[0])

    print('Round  0:', mat2text(s1), mat2text(s2), bit_diff(s1, s2), sep='\t')

    for i in range(1, 10):
        sub_bytes(s1)
        sub_bytes(s2)
        shift_rows(s1)
        shift_rows(s2)
        mix_columns(s1)
        mix_columns(s2)
        add_round_key(s1, k1[i])
        add_round_key(s2, k2[i])

        print('Round %2d:' % i, mat2text(s1), mat2text(s2), bit_diff(s1, s2), sep='\t')

    sub_bytes(s1)
    sub_bytes(s2)
    shift_rows(s1)
    shift_rows(s2)
    add_round_key(s1, k1[10])
    add_round_key(s2, k2[10])

    print('Round 10:', mat2text(s1), mat2text(s2), bit_diff(s1, s2), sep='\t')



def main():
    # demonstration of book example
    print('Encryption Decryption of Book Example:\n')
    plaintext = '0123456789abcdeffedcba9876543210'
    print('Plaintext:', plaintext)
    plaintext = [int(plaintext[i:i + 2], 16) for i in range(0, len(plaintext), 2)]
    key = '0f1571c947d9e8590cb7add6af7f6798'
    print('Key:', key)
    key = [int(key[i:i + 2], 16) for i in range(0, len(key), 2)]

    expanded_keys = key_expansion([key[i:i + 4] for i in range(0, 16, 4)])
    print('Expanded Keys:')
    print(*enumerate(' '.join(f'{x:02x}' for x in word) for subkey in expanded_keys for word in subkey), sep='\n')

    ciphertext = encrypt_block(plaintext, key)
    deciphertext = decrypt_block(ciphertext, key)
    ciphertext = ''.join(['%02x' % i for i in ciphertext])
    deciphertext = ''.join(['%02x' % i for i in deciphertext])
    print('Ciphertext:', ciphertext)
    print('Decrypted Plaintext:', deciphertext)

    # demonstration of avalanche
    print('\nAvalanche Effect Demonstration:')
    # 1 bit difference in plaintext and same key
    plaintext1 = '0123456789abcdeffedcba9876543210'
    plaintext2 = '0023456789abcdeffedcba9876543210'
    key1 = '0f1571c947d9e8590cb7add6af7f6798'
    key2 = '0f1571c947d9e8590cb7add6af7f6798'

    plaintext1 = [int(plaintext1[i:i + 2], 16) for i in range(0, len(plaintext1), 2)]
    plaintext2 = [int(plaintext2[i:i + 2], 16) for i in range(0, len(plaintext2), 2)]
    key1 = [int(key1[i:i + 2], 16) for i in range(0, len(key1), 2)]
    key2 = [int(key2[i:i + 2], 16) for i in range(0, len(key2), 2)]

    print('\nSame key, 1 bit difference in plaintext:')
    demonstrate_avalanche(plaintext1, key1, plaintext2, key2)

    # 1 bit difference in key and same plaintext
    plaintext1 = '0123456789abcdeffedcba9876543210'
    plaintext2 = '0123456789abcdeffedcba9876543210'
    key1 = '0f1571c947d9e8590cb7add6af7f6798'
    key2 = '0e1571c947d9e8590cb7add6af7f6798'

    plaintext1 = [int(plaintext1[i:i + 2], 16) for i in range(0, len(plaintext1), 2)]
    plaintext2 = [int(plaintext2[i:i + 2], 16) for i in range(0, len(plaintext2), 2)]
    key1 = [int(key1[i:i + 2], 16) for i in range(0, len(key1), 2)]
    key2 = [int(key2[i:i + 2], 16) for i in range(0, len(key2), 2)]

    print('\nSame plaintext, 1 bit difference in key:')
    demonstrate_avalanche(plaintext1, key1, plaintext2, key2)



if __name__ == '__main__':
    main()

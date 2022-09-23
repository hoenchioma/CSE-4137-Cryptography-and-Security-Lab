from collections import deque
from math import log2, log10


legal_alph = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.?!-()')
punc_chars = set('.,?!-() ')
capital_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

words_file = '/usr/share/dict/words'
with open(words_file, 'r') as f: words = set(word.strip() for word in f.readlines())


def str_to_bytes(s):
    '''
    Convert string to number array (of bytes)
    '''
    return [ord(c) for c in s]


def bytes_to_str(a):
    '''
    Convert number array to string (of bytes)
    '''
    return ''.join(map(chr, a))


def encrypt(message, pad):
    '''
    Encrypt message using pad.
    (Modified one time pad)
    '''
    assert(len(message) <= len(pad))
    cipher = []
    for i in range(len(message)):
        last_cipher_byte = cipher[-1] if len(cipher) > 0 else 0
        cipher.append(message[i] ^ ((pad[i] + last_cipher_byte) % 256))
    return cipher


def decrypt(cipher, pad):
    '''
    Decrypt cipher using pad.
    (Modified one time pad)
    '''
    assert(len(cipher) <= len(pad))
    message = []
    for i in range(len(cipher)):
        last_cipher_byte = cipher[i-1] if i > 0 else 0
        message.append(cipher[i] ^ ((pad[i] + last_cipher_byte) % 256))
    return message


def find_pads(ciphers, invalid_words_lim = 10, invalid_words_per_msg_lim = 3):
    '''
    Find possible pads for given ciphers.
    '''
    # all ciphers must be of same length
    assert(all(len(cipher) == len(ciphers[0]) for cipher in ciphers))
    n, m = len(ciphers), len(ciphers[0])

    # find possible pad values (using legal chars)
    pad_byte_st = []
    for i in range(m):
        cur_pad_byte_st = None
        for cipher in ciphers:
            tmp_pad_byte_st = set()
            for msg_char in (legal_alph if i > 0 else capital_chars):
                msg_byte = ord(msg_char)
                cur_cipher_byte = cipher[i]
                prev_cipher_byte = cipher[i-1] if i > 0 else 0
                pad_byte = ((msg_byte ^ cur_cipher_byte) - prev_cipher_byte) % 256
                tmp_pad_byte_st.add(pad_byte)
            if cur_pad_byte_st is None:
                cur_pad_byte_st = tmp_pad_byte_st
            else:
                cur_pad_byte_st = cur_pad_byte_st.intersection(tmp_pad_byte_st)
        pad_byte_st.append(cur_pad_byte_st)
    
    print('Possible pad values:')
    print(pad_byte_st)
    print('Possible pad value set sizes: ')
    print([len(pad_byte_st[i]) for i in range(m)])

    # hash all words in dictionary
    base = 257
    mod = 2**61 - 1
    word_hashes = set([0])
    for word in words:
        if not any(c in punc_chars or c in capital_chars for c in word):
            word_hash = 0
            for c in word:
                word_hash = (word_hash * base + ord(c)) % mod
            word_hashes.add(word_hash)  


    def backtrack(idx = 0, pad = [], 
                  lw_hash = [0 for _ in range(n)],
                  invalid_words = 0,
                  invalid_words_per_msg = [0 for _ in range(n)]):
        '''
        Backtrack to find valid pads.
        '''
        if idx == m:
            # if valid pad is found return it
            yield pad.copy()
        else:
            for pad_byte in pad_byte_st[idx]:
                # forward track
                pad.append(pad_byte)
                prev_lw_hash = lw_hash[:]
                prev_invalid_words = invalid_words
                prev_invalid_words_per_msg = invalid_words_per_msg[:]
                for i in range(n):
                    # find message byte for current pad byte
                    cur_cipher_byte = ciphers[i][idx]
                    prev_cipher_byte = ciphers[i][idx-1] if idx > 0 else 0
                    msg_byte = (cur_cipher_byte ^ ((pad_byte + prev_cipher_byte) % 256))
                    msg_byte_low = ord(chr(msg_byte).lower())
                    # check if last word is a valid word
                    if chr(msg_byte) in punc_chars: # punctuation character
                        if lw_hash[i] not in word_hashes:
                            invalid_words += 1
                            invalid_words_per_msg[i] += 1
                        lw_hash[i] = 0
                    else:
                        # extend current word hash
                        lw_hash[i] = (lw_hash[i] * base + msg_byte_low) % mod
                # recursion  
                if invalid_words <= invalid_words_lim and \
                        all(cnt <= invalid_words_per_msg_lim for cnt in invalid_words_per_msg):
                    yield from backtrack(idx + 1, pad, lw_hash, 
                                         invalid_words, invalid_words_per_msg)
                # backward track
                invalid_words_per_msg[:] = prev_invalid_words_per_msg
                invalid_words = prev_invalid_words
                lw_hash[:] = prev_lw_hash
                pad.pop()

    # backtrack and find all valid pads
    valid_pads = list(backtrack())

    return valid_pads

def main():
    '''
    Main function.
    '''
    # Part 1
    # Test encryption and decryption with a 10 character message
    print('Part 1:')    
    test_msg = 'HelloWorld'
    print('Test message:', test_msg)
    test_msg_bytes = str_to_bytes(test_msg)
    print('Test message (bytes):', test_msg_bytes)
    print('Test message (hex):', ' '.join(format(x, '02x') for x in test_msg_bytes))
    test_pad = [22, 99, 9, 7, 9, 222, 44, 55, 88, 111]
    print('Test pad (bytes):', test_pad)
    print('Test pad (hex):', ' '.join(format(x, '02x') for x in test_pad))
    test_cipher = encrypt(test_msg_bytes, test_pad)
    print('Encoded cipher (bytes):', test_cipher)
    print('Encoded cipher (hex):', ' '.join(format(x, '02x') for x in test_cipher))
    test_decrypted = decrypt(test_cipher, test_pad)
    print('Decrypted message (bytes):', test_decrypted)
    print('Decrypted message (hex):', ' '.join(format(x, '02x') for x in test_decrypted))
    print('Decrypted message (string):', bytes_to_str(test_decrypted))
    print('\n')

    # Part 2
    # Find message and pad for 10 ciphertexts using same pad
    print('Part 2:')
    with open('prob2.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        ciphers = [list(map(int, line.strip('][').split(', '))) for line in lines]
        # print('Given ciphers:')
        # for cipher in ciphers:
        #     print(' '.join(format(x, '02x') for x in cipher))

    pads = find_pads(ciphers, 10, 3)
    print('No. of valid pads:', len(pads))
    for pad in pads:
        print('Valid pad:', ' '.join(format(x, '02x') for x in pad))
        print('Decrypted messages:')
        for cipher in ciphers:
            print(bytes_to_str(decrypt(cipher, pad)))


if '__main__' == __name__:
    main()
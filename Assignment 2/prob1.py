words_file = '/usr/share/dict/words'


def get_words(length = None):
    '''
    Returns a list of words from the dictionary that are of the given length.
    '''
    with open(words_file, 'r') as f:
        words = set(word.strip() for word in f.readlines())
        if length:
            words = set(filter(lambda x: len(x) == length, words))
        return words


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


def xor(s1, s2):
    '''
    Return xor of 2 number arrays
    '''
    return [(i^j) for i, j in zip(s1, s2)]


def main():
    '''
    Main function.
    '''
    # read cipher texts from file
    with open('prob1.txt', 'r') as f:
        cipher1, cipher2 = [[int(x, 16) for x in line.strip().split()] for line in f.readlines()]
        if (len(cipher1) != len(cipher2)):
            raise ValueError('Ciphers must be of equal length.')
        n = len(cipher1)

    # get words dictionary
    words = get_words(n)

    # break cipher
    results = []
    done = set()
    cipherxor = xor(cipher1, cipher2)
    for word in words:
        # to avoid repeatition
        # if word in done:
        #     continue
        word_bytes = str_to_bytes(word)
        other_word_bytes = xor(cipherxor, word_bytes)
        other_word = bytes_to_str(other_word_bytes)
        if other_word in words:
            results.append((word, other_word))
            # done.add(other_word)

    # print results
    if results:
        print('Possible results:')
        for word1, word2 in results:
            pad = xor(cipher1, str_to_bytes(word1))
            pad_hex = ' '.join(format(x, '02x') for x in pad)
            print(f'"{word1}", "{word2}" (Pad: {pad_hex})')
    else:
        print('No results found.')




if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# This file contains functions for predicting the key from a given cipher text
# encoded using the Vignere cypher

import sys
import getopt
from math import ceil, sqrt
from statistics import mode
from os import path


with open('alphabet.txt', 'r') as f: alph = f.read()
alph_id = {c: i for i, c in enumerate(alph)}
# eng_alph_order = 'etaoinshrdlcumwfgypbvkjxqz'
eng_alph_fre = {
    'e':	0.1202,
    't':	0.0910,
    'a':	0.0812,
    'o':	0.0768,
    'i':	0.0731,
    'n':	0.0695,
    's':	0.0628,
    'r':	0.0602,
    'h':	0.0592,
    'd':	0.0432,
    'l':	0.0398,
    'u':	0.0288,
    'c':	0.0271,
    'm':	0.0261,
    'f':	0.0230,
    'y':	0.0211,
    'w':	0.0209,
    'g':	0.0203,
    'p':	0.0182,
    'b':	0.0149,
    'v':	0.0111,
    'k':	0.0069,
    'x':	0.0017,
    'q':	0.0011,
    'j':	0.0010,
    'z':	0.0007,
}


def clean(text):
    """
    Cleans the text
    """
    cleaned_text = ""
    for ch in text:
        if ch in alph_id:
            cleaned_text += ch
    return cleaned_text


def compare(text1, text2):
    """
    Return similarity between two strings
    (after cleaning)
    """
    text1_clean = clean(text1)
    text2_clean = clean(text2)
    if len(text1_clean) != len(text2_clean):
        return 0
    sim = 0
    for i, j in zip(text1_clean, text2_clean):
        if i == j:
            sim += 1
    return sim / len(text1_clean)


def decrypt(cipher_text, key):
    """
    Decrypts the cipher text using the key
    (Vignere cypher)
    """
    plain_text = ""
    for i in range(len(cipher_text)):
        plain_text += alph[(alph_id[cipher_text[i]] -
                            alph_id[key[i % len(key)]]) % len(alph)]
    return plain_text


def get_key_accuracy(cipher_text, plain_text, key):
    """
    Return accuracy of key
    """
    plain_text_dec = decrypt(cipher_text, key)
    return compare(plain_text, plain_text_dec)


def get_factors(num):
    """
    get factors of num
    """
    for i in range(1, ceil(sqrt(num))):
        if num % i == 0:
            yield i
            if i != num // i:
                yield num // i


def kasiski(text, probe_len, max_key_len):
    """
    Return list of probable key lengths (with frequency)
    """

    def get_seq_diffs(text, seq_len):
        """
        Return list of differences between repeating sequences (of length seq_len)
        """
        seq_diffs = set()
        last_id = {}
        for i in range(len(text) - seq_len):
            seq = text[i:i + seq_len]
            if seq in last_id:
                seq_diff = i - last_id[seq]
                if seq_diff not in seq_diffs:
                    yield seq_diff
                    seq_diffs.add(seq_diff)
            last_id[seq] = i

    # get most frequent factor of seq_diffs
    factor_fre = {}
    # key_lens, key_len_fre = [], 0
    for seq_diff in get_seq_diffs(text, probe_len):
        for factor in get_factors(seq_diff):
            if factor >= probe_len and factor <= max_key_len:
                factor_fre[factor] = factor_fre.get(factor, 0) + 1
                # if factor_fre[factor] > key_len_fre:
                #     key_lens, key_len_fre = [factor], factor_fre[factor]
                # elif factor_fre[factor] == key_len_fre:
                #     key_lens.append(factor)
    
    key_lens = map(lambda x: x[0], sorted(
        factor_fre.items(), key=lambda x: x[1], reverse=True))

    return key_lens


def find_caesar_key(text):
    """
    Return Caeser Cipher key for text
    """
    # get alphabet frequency in text
    text_freq = {c: 0 for c in alph}
    for c in text: text_freq[c] += 1
    # get the most frequent (len(eng_alph_fre)) letters in text
    text_freq = dict(sorted(text_freq.items(), key=lambda x: x[1], reverse=True)[:len(eng_alph_fre)])
    # convert frequency to proportions
    text_freq_sum = sum(text_freq.values())
    text_freq = {k: v / text_freq_sum for k, v in text_freq.items()}
    # get best shift
    best_shift, best_shift_val = -1, 0
    for shift in range(len(alph)):
        shift_val = 0
        for c in eng_alph_fre:
            shift_val += text_freq.get(alph[(alph_id[c] + shift) % len(alph)], 0) * eng_alph_fre[c]
        if shift_val > best_shift_val:
            best_shift, best_shift_val = shift, shift_val
    # return best key
    return alph[best_shift]


def find_vignere_key(cipher_text, key_len):
    """
    Finds the key for the Vignere cypher, given key length
    """
    text_cols = [cipher_text[i::key_len] for i in range(key_len)]
    key = ''.join(map(find_caesar_key, text_cols))
    return key


def hack(cipher_text, kasiski_probe_len, max_key_len):
    """
    Return probable keys for cipher text
    """
    key_lens = kasiski(cipher_text, kasiski_probe_len, max_key_len)
    keys = map(lambda x: find_vignere_key(cipher_text, x), key_lens)
    return keys


def main():
    """
    Main Function
    """
    # command line arguments
    short_options = 'i:c:k:l:h'
    long_options = ['input=', 'compare=', 'kasiski-probe-len=', 'max-key-len=', 'help']

    # default values
    input_file = 'input.txt'
    compare_file = 'compare.txt'
    kasiski_probe_len = 3
    max_key_len = 10

    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    for current_argument, current_value in arguments:
        if current_argument in ('-i', '--input'):
            input_file = current_value
        elif current_argument in ('-c', '--compare'):
            compare_file = current_value
        elif current_argument in ('-k', '--kasiski-probe-len'):
            kasiski_probe_len = int(current_value)
        elif current_argument in ('-l', '--max-key-len'):
            max_key_len = int(current_value)
        elif current_argument in ('-h', '--help'):
            print('Usage: python3 hack.py [OPTIONS]')
            print('Options:')
            print('  -i, --input=<input_file>')
            print('  -o, --output=<output_file>')
            print('  -k, --kasiski-probe-len=<kasiski_probe_len>')
            print('  -l, --max-key-len=<max_key_len>')
            print('  -h, --help')
            sys.exit()
        else:
            raise ValueError(f'Invalid argument: {current_argument}')

    # read input file
    with open(input_file, 'r') as f:
        input_text = f.read()
    with open(compare_file, 'r') as f:
        compare_text = f.read()

    # hack
    input_text = clean(input_text)
    compare_text = clean(compare_text)

    # keys = hack(input_text, kasiski_probe_len, max_key_len)
    # if keys:
    #     print(f'Predicted key lengths: {", ".join(map(lambda x: str(len(x)), keys))}')
    #     print(f'Predicted keys: {(", ".join(keys))}')

    #     # write output file
    #     if len(keys) == 1:
    #         with open(output_file, 'w') as f:
    #             f.write(keys[0])
    #     else:
    #         for idx, key in enumerate(keys):
    #             file_name, file_ext = path.splitext(output_file)
    #             with open(f'{file_name}{idx}.{file_ext}', 'w') as f:
    #                 f.write(key)
    # else:
    #     print('No keys found')
    
    keys = hack(input_text, kasiski_probe_len, max_key_len)
    key_accuracies = [(key, get_key_accuracy(input_text, compare_text, key)) for key in keys]
    # sort by accuracy
    key_accuracies.sort(key=lambda x: x[1], reverse=True)
    if key_accuracies:
        for key, accuracy in key_accuracies:
            print(f'Key length: {len(key)}, Key: {key}, Accuracy: {accuracy * 100:.2f}%')
            print('Decrypted text:')
            print(decrypt(input_text, key))
            print()
    else:
        print('No keys found')



if __name__ == '__main__':
    main()
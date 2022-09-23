#!/usr/bin/env python3

# This file contains functions for encrypting and decrypting text
# using the Vignere cypher

import sys
import getopt


with open('alphabet.txt', 'r') as f: alph = f.read()
alph_id = {c: i for i, c in enumerate(alph)}


def clean(text):
    """
    Cleans the text
    """
    cleaned_text = ""
    for ch in text:
        if ch in alph_id:
            cleaned_text += ch
    return cleaned_text


def tokenize(text, chunk_size = 5):
    """
    Split text into chunks of chunk_size
    (with spaces between chunks)
    """
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return ' '.join(chunks)


def encrypt(plain_text, key):
    """
    Encrypts the plain text using the key
    (Vignere cypher)
    """
    cipher_text = ""
    for i in range(len(plain_text)):
        cipher_text += alph[(alph_id[plain_text[i]] + alph_id[key[i % len(key)]]) % len(alph)]
    return cipher_text


def decrypt(cipher_text, key):
    """
    Decrypts the cipher text using the key
    (Vignere cypher)
    """
    plain_text = ""
    for i in range(len(cipher_text)):
        plain_text += alph[(alph_id[cipher_text[i]] - alph_id[key[i % len(key)]]) % len(alph)]
    return plain_text


def main():
    """
    Main function
    """
    # command line arguments
    short_options = 'i:o:k:edh'
    long_options = ['input=', 'output=', 'key=', 'encrypt', 'decrypt', 'help']

    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    # default values
    input_file = 'input.txt'
    output_file = 'output.txt'
    key_file = 'key.txt'
    is_decrypt = False

    for current_argument, current_value in arguments:
        if current_argument in ('-i', '--input'):
            input_file = current_value
        elif current_argument in ('-o', '--output'):
            output_file = current_value
        elif current_argument in ('-k', '--key'):
            key_file = current_value
        elif current_argument in ('-e', '--encrypt'):
            is_decrypt = False
        elif current_argument in ('-d', '--decrypt'):
            is_decrypt = True
        elif current_argument in ('-h', '--help'):
            print('Usage: python3 encrypt.py [options]')
            print('Options:')
            print('  -i, --input=<input_file>')
            print('  -o, --output=<output_file>')
            print('  -k, --key=<key_file>')
            print('  -e, --encrypt')
            print('  -d, --decrypt')
            print('  -h, --help')
            sys.exit(0)
        else:
            raise ValueError(f'Invalid argument: {current_argument}')

    # read the input text and key    
    with open(input_file, 'r') as f:
        input_text = f.read()
    with open(key_file, 'r') as f:
        key = f.read()

    input_text = clean(input_text)
    key = clean(key)

    print("Input text: (Cleaned) (Abridged)")
    print(input_text[:min(len(input_text), 500)])

    print(f'Text length: {len(input_text)}')
    print(f'Key length: {len(key)}')

    # clean and encrypt/decrypt the input text
    if not is_decrypt:
        print('Encrypting...')
        # print(input_text)
        output_text = encrypt(input_text, key)
        output_text = tokenize(output_text)
    else:
        print('Decrypting...')
        output_text = decrypt(input_text, key)

    print("Output text: (Abridged)")
    print(output_text[:min(len(output_text), 500)])

    # write the output text to file
    with open(output_file, 'w') as f:
        f.write(output_text)


if __name__ == '__main__':
    main()
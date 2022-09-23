#!/usr/bin/env python3

import sys
import getopt
import random


with open('alphabet.txt', 'r') as f: alph = f.read()


def generate_key(length):
    """
    Generates a key of the specified length
    """
    key = ""
    for i in range(length):
        key += alph[random.randint(0, len(alph) - 1)]
    return key


def main():
    """
    Main Function
    """
    # command line arguments
    short_options = 'l:o:ph'
    long_options = ['length=', 'output=', 'print', 'help']

    # default values
    length = 10
    print_output = False
    output_file = None

    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    for current_argument, current_value in arguments:
        if current_argument in ('-l', '--length'):
            length = int(current_value)
        elif current_argument in ('-o', '--output'):
            output_file = current_value
        elif current_argument in ('-p', '--print'):
            print_output = True
        elif current_argument in ('-h', '--help'):
            print('Usage: python3 keygen.py [options]')
            print('Options:')
            print('  -l, --length=<length>')
            print('  -o, --output=<output_file>')
            print('  -p, --print')
            print('  -h, --help')
            sys.exit(0) 
        else:
            raise ValueError(f'Invalid argument: {current_argument}')

    key = generate_key(length)

    # print the key
    if print_output:
        print(key)

    # write the key to a file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(key)


if __name__ == "__main__":
    main()
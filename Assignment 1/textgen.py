#!/usr/bin/env python3


import sys
import getopt
import requests


api_addr = 'https://litipsum.com/api/'


def main():
    """
    Main Function
    """
    # command line arguments
    short_options = 'l:s:o:ph'
    long_options = ['length=', 'source=', 'output=', 'help', 'print']

    # default values
    print_output = False
    length = None
    source = None
    output_file = None

    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    for current_argument, current_value in arguments:
        if current_argument in ('-l', '--length'):
            length = int(current_value)
        elif current_argument in ('-s', '--source'):
            source = current_value
        elif current_argument in ('-o', '--output_file'):
            output_file = current_value
        elif current_argument in ('-p', '--print'):
            print_output = True
        elif current_argument in ('-h', '--help'):
            print('Usage: python3 textgen.py [options]')
            print('Options:')
            print('  -l, --length=<length-in-paras>')
            print('  -s, --source=<source>')
            print('  -o, --output=<output_file>')
            print('  -p, --print')
            print('  -h, --help')
            sys.exit()
        else:
            raise ValueError(f'Invalid argument: {current_argument}')

    # for request url
    req_addr = api_addr
    req_addr += f'{source}/' if source else ''
    req_addr += f'{length}/' if length else ''

    # fetch text from API
    response = requests.get(req_addr)
    text = response.text

    # print output
    if print_output:
        print(text)

    # write to file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    main()

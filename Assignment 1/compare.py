#!/usr/bin/env python3

# This can be used to compare two text files (after cleaning)

import sys


with open('alphabet.txt', 'r') as f: alph = f.read()
alph_id = {c: i for i, c in enumerate(alph)}


def clean(text):
    """
    Cleans the text
    """
    cleaned_text = ""
    for ch in text:
        if ch in alph_id:
            cleaned_text += ch.lower()
    return cleaned_text


def main():
    """
    Main function
    """
    if len(sys.argv) < 3:
        print("Usage: python3 compare.py [input.txt] [output.txt]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        input_text = f.read()
    with open(output_file, 'r') as f:
        output_text = f.read()
    
    input_text = clean(input_text)
    output_text = clean(output_text)
    
    if len(input_text) != len(output_text):
        print("The input and output text are not the same length")
        sys.exit(1)
    
    delta = 0
    for i in range(len(input_text)):
        if input_text[i] != output_text[i]:
            delta += 1

    accuracy = (len(input_text) - delta) / len(input_text) * 100
    print(f'The files are {accuracy}% ({len(input_text) - delta} characters) same')


if __name__ == "__main__":
    main()
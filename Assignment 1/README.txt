To encrypt an input text file "input.txt" using key from "key.txt" and write output to "output.txt"

python encrypt.py --encrypt -i input.txt -o output.txt -k key.txt

To decrypt an input text file "output.txt" using key from "pkey.txt" and write output to "pinput.txt"

python encrypt.py --decrypt -i output.txt -o pinput.txt -k pkey.txt

To find the key from a cipher text file "output.txt" and write key to "pkey.txt"

python hack.py -i output.txt -o pkey.txt

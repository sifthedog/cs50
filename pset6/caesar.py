from cs50 import get_string
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python caesar.py k")
        return 1
    key = getkey()

    plaintext = get_string("plain text: ")

    s = ''

    for char in plaintext:
        if (char >= 'a' and char <= 'z'): 
            s = lowercase(char,key,s)              
        elif (char >= 'A' and char <= 'Z'):
            s = uppercase(char,key,s)
        else:
            s += char

    print(f"ciphertext: {s}")

def getkey():
    key = int(sys.argv[1])

    key = int(key % 26)

    return key

def lowercase(char,key,s):
    asciino = (int(ord(char) - ord('a')+key)%26) + ord('a')
    mod = str(chr(asciino))
    s += mod

    return s

def uppercase(char,key,s):
    asciino = (int(ord(char) - ord('A')+key)%26) + ord('A')
    mod = str(chr(asciino))
    s += mod

    return s
    
if __name__ == '__main__':
    main()

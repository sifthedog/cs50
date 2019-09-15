from cs50 import get_string
import sys

def main():
    if len(sys.argv) != 2: 
        print("Usage: python caesar.py k")
        sys.exit(1)

    for valid in sys.argv[1]:
        validinput(valid) # Check if the argv is as expected

    plaintext = get_string("plain text: ")  

    s = ''

    lenargv = len(sys.argv[1])

    i = 0 # Set counter

    for char in plaintext:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'a'): 
            k = getkey(sys.argv[1][int(i%lenargv)]) # From str to int 
            s = ischaracter(char,k,s) # The magic happens here
            i += 1  
        else:
            s += char 

    print(f"ciphertext: {s}")

def validinput(valid):
    if (valid < 'a' or valid >'z') and (valid <'A' or valid > 'Z'): 
        sys.exit(1)

def ischaracter(char,k,s):
    if (char >= 'a' and char <= 'z'):
        s = lowercase(char,k,s) 
    elif (char >= 'A' and char <= 'Z'):
        s = uppercase(char,k,s)
    return s

def getkey(ke):
    if (ke >= 'a' and ke <= 'z'):
        ke = ord(ke) - ord('a')
    else:
        ke = ord(ke) - ord('A')

    return ke

def lowercase(char,k,s):
    asciino = (int(ord(char) - ord('a')+k)%26) + ord('a')
    mod = str(chr(asciino))
    s += mod

    return s

def uppercase(char,k,s):
    asciino = (int(ord(char) - ord('A')+k)%26) + ord('A')
    mod = str(chr(asciino))
    s += mod

    return s

if __name__ == '__main__':
    main()

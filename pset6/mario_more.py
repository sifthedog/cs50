from cs50 import get_int

def main():
    size = 0
    while (size<1 or size>8):
        size = get_int("Height: ")

    j = size-2
    i = 0

    while(i < size):
        blankspace(size-i-1)
        hash(size-j)
        i += 1
        j -= 1

def blankspace(k):
    for i in range(k):
        print(" ",end="")

def hash(n):
    for i in range(n-1):
        print("#",end="")

    print("  ",end="")

    for j in range(n-1):
        print("#",end="")

    print()

if __name__ == '__main__':
    main()

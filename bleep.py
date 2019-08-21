import sys
import cs50

def main():
    checkusage()

    [banned, split_text, sizetext] = user_input()

    output(split_text, sizetext, banned)


def output(split_text, sizetext, banned):
    j = 0

    for i in split_text:
        if j < sizetext - 1 and i.lower() in banned:
            sizeofbanned = len(i)
            for z in i:
                print("*", end="")
            print(" ",end="")
        elif j == sizetext - 1 and i.lower() in banned:
            for z in i:
                print("*", end="")
            print()
        elif j == sizetext -1:
            print(i)
        else:
            print(i, end=" ")
        j += 1

def checkusage():
    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    if not sys.argv[1].endswith('.txt'):
        print("Usage: python bleep.py dictionary")
        exit(1)

def user_input():
    initial_text = input("What message would you like to censor?\n" )

    [banned, split_text] = lowering(initial_text)

    return banned, split_text, len(split_text)

def lowering(initial_text):
    banned = []

    with open(sys.argv[1]) as fp:
        for x, line in enumerate(fp):
            banned.append(line.replace('\n','').lower())

    split_text = initial_text.split()
    return banned, split_text

if __name__ == '__main__':
    main()

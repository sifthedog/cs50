from cs50 import get_float
from math import ceil

def main():
    cash = 0
    coins = 0
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1

    while cash <= 0:
        cash = get_float("Change owed: ")

    cash = 100*cash

    if cash >= quarter:
        coins += cash // quarter
        cash = ceil(cash % quarter)

    if cash >= dime:
        coins += cash // dime
        cash = ceil(cash % dime)

    if cash >= nickel:
        coins += cash // nickel
        cash = ceil(cash % nickel)

    if cash >= penny:
        coins += cash // penny
        cash = ceil(cash % penny)

    print(f"{int(coins)}")

if __name__ == '__main__':
    main()

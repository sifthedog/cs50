from cs50 import get_int

cardnumber = -1
while cardnumber<0:
    cardnumber = get_int("Number: ")

total = 0
ae = 0
digit = 0
mc = 0
visa = 0
i = 0

while cardnumber>0:
    digit += 1
    if i % 2 == 0:
        remainder = cardnumber % 10
        total += remainder
    else:
        remainder = 2*(cardnumber % 10)
        total += (remainder//10) + (remainder%10)
    cardnumber = cardnumber // 10
    if(cardnumber<100 and (cardnumber == 34 or cardnumber == 37)):
            ae = 1
    elif(cardnumber<100 and cardnumber <= 55 and cardnumber >= 51):
            mc = 1
    elif(cardnumber<10 and cardnumber == 4):
        visa = 1
    i += 1

if(total%10==0 and ae!=0):
    print("AMEX")
elif(total%10==0 and visa!=0 and digit>=13 and digit <=16):
    print("VISA")
elif(total%10==0 and mc!=0):
    print("MASTERCARD")
else:
    print("INVALID")

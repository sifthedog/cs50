#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main()
{
    int quarter = 25, dime = 10, nickel = 5, penny = 1, sif;
    float change=-1;
    
    while(change<0)
    {
        change = get_float("Change owed: ");
    }
    sif = round(change*100); // Sif is my dog's name. Therefore, it'll always be the main variable.
    
    int coins = -1;
    
    while(coins<0)
    {
        coins++;
        if(sif>=25)
        {
            coins += sif/quarter;
            sif = sif%quarter;
        }
        if(sif>=10)
        {
            coins += sif/dime;
            sif = sif%dime;
        }
        if(sif>=5)
        {
            coins += sif/nickel;
            sif = sif%nickel;
        }
        coins += sif/penny;
    }
    printf("%i\n", coins);
}

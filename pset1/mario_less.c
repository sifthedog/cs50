#include <cs50.h>
#include <stdio.h>

void espaco(int n);
void sustenido(int n);

int main(void)
{
    
    int sif = 0, prints, contador, i, j;
    do
    {
        sif = get_int("Height: ");
    }
    while(sif<1 || sif>8);
    
    i=0;
    j=sif-1;
    do
    {
        espaco(sif-i-1);
        sustenido(sif-j);
        j--;
        i++;
    }
    while(i<sif);
}

void espaco(int n)
{
    int i;
    for(i=0;i<n;i++)
    {
        printf(" ");
    }
}

void sustenido(int n)
{
    int i;
    for(i=0;i<n;i++)
    {
        printf("#");
    }
    printf("\n");
}

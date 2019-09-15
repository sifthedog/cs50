#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main()
{
    float somadigito;
    int i=0, visa = 0, ae = 0, mc = 0, digito = 0;
    long novo, somaproduto=0, remainder, aux;
    
    long sif = get_long("Number: ");
    
    
    while(sif>0)
    {
        digito++;
        if(i%2==0)
        {
            remainder = fmodl(sif,10);
            somaproduto += remainder;
        }
        else
        {
            remainder=2*fmodl(sif,10);
            if(remainder<10)
            {
                somaproduto+= remainder;
            }
            else
            {
                aux = fmodl(remainder,10);
                remainder = floor(remainder/10);
                somaproduto+= aux + remainder;
            }
        }
        sif=sif/10;
        if(sif<100 && (sif == 34 || sif == 37))
        {
            ae++;
        }
        else if(sif<100 && sif <= 55 && sif >= 51)
        {
            mc++;
        }
        else if(sif<10 && sif == 4)
        {
            visa++;
        }
    i++;
    }
    
    if(somaproduto%10==0 && ae!=0)
    {
        printf("AMEX\n");
    }
    else if(somaproduto%10==0 && visa!=0 && digito>=13 && digito <=16)
    {
        printf("VISA\n");
    }
    else if(somaproduto%10==0 && mc!=0)
    {
        printf("MASTERCARD\n");
    }
    else printf("INVALID\n");
}

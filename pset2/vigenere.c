#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int inputcheck(int argc, string argv[]);
int keyupper(int s,int i, int key);
int keylower(int s,int i, int key);

int main(int argc, string argv[])
{
    
    int i, tam1, tam2, ok = inputcheck(argc,argv);;
 

    if(ok==1) return ok;
    
    string s = get_string("plaintext: ");
    tam1 = strlen(s);    
    tam2 = strlen(argv[1]);
    int trans[tam1];
    int key[tam2];
    
    for (i=0;i<tam2;i++)
    {
        if(isupper(argv[1][i])>0)
        {
            key[i] = argv[1][i]-'A';
        }
        else
            key[i] = argv[1][i]-'a';
        printf("%i\n",argv[1][i]);
                
        printf("%i\n", key[i]);
    }
    
    printf("ciphertext: ");
    int j=0;
    for(i=0;i<tam1;i++)    
    {
        if((s[i]>= 'a' && s[i]<= 'z') || (s[i]>= 'A' && s[i] <= 'Z'))
        {
            if (isupper(s[i]))
            {
                trans[i] = (s[i]+key[j%tam2]-'A')%26 + 'A'; 
                j++;
            }
            else
            {
                trans[i]=(s[i]+key[j%tam2]-'a')%26 + 'a';
                j++;
            } 
        }
        else
            trans[i]=s[i];
        printf("%c", trans[i]);
    }
    printf("\n");
}

int inputcheck(int argc, string argv[])
{
    int contador = 0, n;
    if (argc == 2)
    {
        string s = argv[1];
        n=strlen(s);
        for(int i=0;i<n;i++)
        {
            if((s[i]<='z' && s[i]>='a') || (s[i]>='A' && s[i]<='Z') )
            {
                contador++;
            }
        }
    }
    else 
    {
       printf("Usage: ./vigenere keyword\n");
       return 1;
    }
    
    if(contador==n){
            return 0;

    }
    else{
        printf("Usage: ./vigenere key\n");
       return 1;
        }
}


int keyupper(int s,int i, int key)
{
    return (s-'A'+key)%26+'A';
}

int keylower(int s,int i, int key)
{
    return (s-'a'+key)%26+'a';
}

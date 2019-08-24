​#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int inputcheck(int argc, string argv[]);
int toInt(string argv[]);
int keyupper(int s,int i, int key);
int keylower(int s,int i, int key);

int main(int argc, string argv[])
{
    
    int i, key, tam, ok = inputcheck(argc,argv);
 

    if(ok==1) return ok;
    
    string s = get_string("plaintext: ");
    tam = strlen(s);    
    int trans[tam];
    key = toInt(argv);
    
    for(i=0;i<tam;i++)
    {
        if(isupper(s[i])>0) trans[i] = keyupper(s[i],i,key);
        else if (islower(s[i])>0) trans[i] = keylower(s[i],i,key);
        else trans[i] = s[i];
    }
    printf("ciphertext: ");
    for(i=0;i<tam;i++)
        printf("%c", trans[i]);
    
    printf("\n");
    
}

int inputcheck(int argc, string argv[])
{
    if (argc == 2)
    {
        string s = argv[1];
        for(int i=0, n=strlen(s);i<n;i++)
        {
            if(s[i]<'0' || s[i]>'9')
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    else 
    {
       printf("Usage: ./caesar key\n");
       return 1;
    }
    return 0;
}


int toInt(string argv[])
{
    int tam = strlen(argv[1]), result = 0;
    string s = argv[1];
    int zero = '0';
    for(int i = 0; i<tam; i++)
    {
            int dif = pow(10,i)*(s[tam-1-i] - zero);
            result += dif;
    }    
    return result;
}

int keyupper(int s,int i, int key)
{
    return (s-'A'+key)%26+'A';
}

int keylower(int s,int i, int key)
{
    return (s-'a'+key)%26+'a';
}

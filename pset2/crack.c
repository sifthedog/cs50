#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <string.h>
#include <math.h>

int check_input(int argc, string argv[]);
string remove_salt_from_hash(string initial_hash);
void crack(string hash2bcomp);
char letter(int key);

int main(int argc, string argv[])
{
    int foundpassword = 1;
    if (check_input(argc,argv) == 1)
    {
        return 1;
    }
    
    char *hash = remove_salt_from_hash(argv[1]);
    crack(hash);   
    
    return 0;
}

void crack(string hash2bcomp)
{
    char *password = malloc(sizeof(char) * 5);
    char *new_hash;
    int i = 0, auxj = 1, auxk = 1, auxl = 1, auxm = 1, j = 0, k =0, l = 0, m = 0;
    password[0] = '\0';
    
    while (strcmp(new_hash,hash2bcomp)!=0)    
    {
        password[0] = letter(i%52);
        auxj = 1;
        while (strcmp(new_hash,hash2bcomp)!=0 && i >= 52 && auxj == 1)
        {
            auxk = 1;
            password[1] = letter(j%52);
            new_hash = remove_salt_from_hash(crypt(password,"50"));
            j++;
            if (j%52 == 0)
                auxj = 0;
            while(strcmp(new_hash,hash2bcomp) != 0 && i >= 104 && auxk == 1)
            {
              auxl = 1;
              password[2] = letter(k%52);
              new_hash = remove_salt_from_hash(crypt(password,"50"));
              k++;
              if (k%52 == 0)
                auxk = 0;
                while(strcmp(new_hash,hash2bcomp) != 0 && i >= 156 && auxl == 1)
                {
                    auxm = 1;
                    password[3] = letter(l%52);
                    new_hash = remove_salt_from_hash(crypt(password,"50"));
                    l++;
                    if (l%52 == 0)
                        auxl = 0;
                    while(strcmp(new_hash,hash2bcomp) != 0 && i >= 208 && auxm == 1)
                    {
                        password[4] = letter(m%52);
                        new_hash = remove_salt_from_hash(crypt(password,"50"));
                        m++;    
                        if (m%52 == 0)
                            auxm = 0;
                    }    
                }
            }
        }
    
        new_hash = remove_salt_from_hash(crypt(password,"50"));
        if (strcmp(new_hash,hash2bcomp)==0)
            printf("%s\n",password);
        i++;
    }
}

int check_input(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    
    return 0;
}

string remove_salt_from_hash(string initial_hash)
{
    int size = strlen(initial_hash);
    char *new_hash = malloc(sizeof(char) * 2);
    int size2 = strlen(new_hash);
  
    for (int i=0;i<size;i++)
    {
        if (i>=2)
            new_hash[i-2] = initial_hash[i];
    }
    return new_hash;
}

char letter(int key)
{
    char aux;
    if (key<26)
        aux = key + 65;
    else
        aux = key + 71;
    
    return aux;
}

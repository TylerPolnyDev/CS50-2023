#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void get_plaintext(string key);
void print_ciphertext(char c, string key);


int main(int argc, string argv[])
{
    if (argc == 2)// ensure key given
    {
        if (strlen(argv[1]) == 26)// ensure key length correct
        {
            for (int i = 0; i < strlen(argv[1]); i++) //check each char
            {
                if (!isalpha(argv[1][i]))// ensure key is alpha only
                {
                    printf("Key must contain 26 characters.\n");
                    return 1;
                }
                for (int j = i + 1; j < strlen(argv[1]); j++) //compare to next char
                {
                    if (toupper(argv[1][j]) == toupper(argv[1][i])) // ensure no repeating char
                    {
                        printf("Key must contain 26 characters.\n");
                        return 1;
                    }
                }

            }

            get_plaintext(argv[1]);
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;

        }
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    return 0;
}

void get_plaintext(string key)
{
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (islower(plaintext[i]))
            {
                print_ciphertext(tolower(plaintext[i]), key);
            }
            else
            {
                print_ciphertext(toupper(plaintext[i]), key);
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }

    }
    printf("\n");
}

void print_ciphertext(char c, string key)
{
    string alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (int i = 0; i < strlen(alpha); i++)
    {
        if (islower(c))
        {
            if (c == tolower(alpha[i]))
            {
                printf("%c", tolower(key[i]));
            }
        }
        else
        {
            if (c == toupper(alpha[i]))
            {
                printf("%c", toupper(key[i]));
            }
        }
    }
}
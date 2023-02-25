#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string test_string = get_string("Text: ");
    int L = 0, W = 0, S = 0;
    for (int n = 0; n <= strlen(test_string); n++)
    {
        if (test_string[n] == ' ' || test_string[n] == '\0')
        {
            W++;
        }
        else if (test_string[n] == '.' || test_string[n] == '?' || test_string[n] == '!')
        {
            S++;
        }
        else if (isalpha(test_string[n]))
        {
            L++;
        }
    }

    const float AVERAGE = 100.0 / W;
    float CL_index = (0.0588 * AVERAGE * L) - (0.296 * AVERAGE * S) - 15.8;

    if (CL_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (CL_index > 16)
    {
        printf("Grade 16+\n");
    }
    else{
        printf("Grade %i\n",(int) round(CL_index));
    }

}


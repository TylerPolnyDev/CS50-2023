#include <cs50.h>
#include <stdio.h>

int get_positive_int(string prompt); //defining
int main(void)
{
    int i = get_positive_int("Height: ");// seeking height

    for (int height = 0; height < i; height++) //height
    {
        for (int spaces = i - height - 2; spaces >= 0; spaces--)//spaces before
        {
            printf(" ");
        }
        for (int row1 = 0; row1 <= height; row1++)//left pyramid
        {
            printf("#");
        }
        printf("  "); //gap
        for (int row2 = 0; row2 <= height; row2++)// right
        {
            printf("#");
        }
        printf("\n");
    }

}

int get_positive_int(string request)// function defined above
{
    int number;
    do
    {
        number = get_int("%s", request);
    }
    while (number < 1 || number > 8);
    return number;
}
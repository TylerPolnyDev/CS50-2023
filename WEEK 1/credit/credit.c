#include <cs50.h>
#include <stdio.h>

bool check_luhn_sum(long n);
void print_card_company(long n);

int main(void)
{
    //prompt user for input
    long credit = get_long("Number: ");
    if (check_luhn_sum(credit)) //apply luhn algorithm
    {
        print_card_company(credit);
    }
    else
    {
        printf("INVALID\n");
    }

}

//function to check luhn algo
bool check_luhn_sum(long n)
{
    int sumprod = 0;
    long credit = n;

    while (credit > 0)
    {
        int dgt;
        //second to last digit
        if (credit / 10 >= 1 && credit /100 < 1)
        {
            dgt = credit / 10;

        }
        else
        {
            dgt = (credit % 100) / 10;
        }

        // every other dgt * 2
        int prod = dgt * 2;

        if ((prod / 10 >= 1))  //two digit prouct check
        {
            sumprod = (prod % 10) + (prod / 10) + sumprod;
        }
        else// single digit added
        {
            sumprod = prod + sumprod;
        }

        //remove last 2 dgt
        credit = credit / 100;
    }

    //reset credit to user input value
    credit = n;

    //last digit
    while (credit > 0)
    {
        int dgt;
        if (credit / 10 < 1)
        {
            dgt = credit;
        }
        else
        {
            dgt = credit % 10;
        }
        //add last digit to total
        sumprod = dgt + sumprod;

        //Removes the last two digit grouping
        credit = credit / 100;
    }
    //return bool
    return sumprod % 10 == 0;
}

//print card company name
void print_card_company(long n)
{
    long credit = n;
    int cardlength = 0;
    long stdgts = 0;


    // Loop to determine the number of digits
    while (credit > 0)
    {
        credit = credit / 10;
        cardlength++;
    }

    // Reset to user input
    credit = n;

    // Loop to determine the start digits
    while (credit >= 100)
    {
        stdgts = credit / 10;
        credit = credit / 10;
    }
    if (cardlength == 13 || cardlength == 16)
    {
        if (stdgts >= 40 && stdgts <= 49)
        {
            printf("VISA\n");
        }
        else if (stdgts >= 51 && stdgts <= 55)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (cardlength == 15)
    {
        if (stdgts == 34 || stdgts == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

}
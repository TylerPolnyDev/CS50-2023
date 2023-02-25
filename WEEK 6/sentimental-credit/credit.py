# Prompt the user for a credit card number
cc_num = input("Enter a credit card number: ")

# Check if the input is a valid number
if not cc_num.isnumeric():
    print("INVALID")
    exit()

# Implement Luhn's algorithm to check the validity of the credit card number
cc_num_digits = [int(d) for d in cc_num]  # Convert the credit card number to a list of digits

# Double the value of every second digit starting from the rightmost digit
for i in range(len(cc_num_digits) - 2, -1, -2):
    cc_num_digits[i] *= 2
    if cc_num_digits[i] > 9:
        cc_num_digits[i] -= 9

# Sum all the digits in the credit card number
cc_num_sum = sum(cc_num_digits)

# Check if the sum is divisible by 10
if cc_num_sum % 10 != 0:
    print("INVALID")
    exit()

# Check the first two digits of the credit card number to determine its type
if cc_num[:2] in ["34", "37"]:
    print("AMEX")
if cc_num[:2] in ["51", "52", "53", "54", "55"]:
    print("MASTERCARD")
if len(cc_num_digits) == 13 or len(cc_num_digits) == 16:
    if cc_num[0] == "4" :
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
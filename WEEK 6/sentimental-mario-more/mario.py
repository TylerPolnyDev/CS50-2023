# mario.py

from cs50 import get_int

# Prompt the user for the height of the pyramid until they provide a valid input
while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# Print the double half-pyramid of the specified height
spaces = height
for i in range(1, height + 1):
    # Print left half of the pyramid
    while spaces > 1:
        ##preceeding spaces
        print(" ",end="")
        spaces = spaces - 1

    for j in range(1, i + 1):
        print("#", end="")
    # reset spaces for next line
    spaces = height - j

    # Print gap between the two halves of the pyramid
    print("  ", end="")

    # Print right half of the pyramid
    for j in range(1, i + 1):
        print("#", end="")

    # Move to the next line
    print()
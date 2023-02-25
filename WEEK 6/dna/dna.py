import csv
import sys


def main():

    # Check for correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Error: Incorrect number of arguments")
        sys.exit(1)

    # Read database file into a variable
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.reader(csvfile)
        # Read the column names from the first line
        columns = next(reader)
        # Read the rest of the rows
        rows = [row for row in reader]

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as seqfile:
        dna = seqfile.read()

    # Find longest match of each STR in DNA sequence
    str_counts = []
    for str in columns[1:]:
        count = longest_match(dna, str)
        str_counts.append(count)

    # Check database for matching profiles
    match = False
    for row in rows:
        if str_counts == [int(count) for count in row[1:]]:
            print(row[0])
            match = True
            break

    # If no match is found, print "No match"
    if not match:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
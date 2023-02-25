from cs50 import get_string

# Prompt user for input
text = get_string("Text: ")

# Compute the number of letters, words and sentences in the text
num_letters = 0
num_words = 1
num_sentences = 0
for ch in text:
    if ch.isalpha():
        num_letters += 1
    elif ch == " ":
        num_words += 1
    elif ch in [".", "!", "?"]:
        num_sentences += 1

# Compute the Coleman-Liau index
L = num_letters * 100 / num_words
S = num_sentences * 100 / num_words
index = 0.0588 * L - 0.296 * S - 15.8

# Print the grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
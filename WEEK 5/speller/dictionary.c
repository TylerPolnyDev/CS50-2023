// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//umber of buckets in hash table
const unsigned int N = 26;
unsigned int words_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Convert word to lowercase
    char word_lowercase[LENGTH + 1];
    strcpy(word_lowercase, word);
    for (int i = 0, n = strlen(word_lowercase); i < n; i++)
    {
        word_lowercase[i] = tolower(word_lowercase[i]);
    }

    // Hash word
    int index = hash(word_lowercase);

    // Check if word exists in hash table
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(cursor->word, word_lowercase) == 0)
        {
            return true;
        }
    }

    // Word is not in dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash word
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Increment word count
        words_count++;

        // Allocate memory for new word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // Copy word into new node
        strcpy(new_node->word, word);

        // Hash word to obtain hash table index
        int index = hash(word);

        // Insert new node at beginning of linked list
        new_node->next = table[index];
        table[index] = new_node;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over all buckets in hash table
    for (int i = 0; i < N; i++)
    {
        // Set cursor to first node in linked list
        node *cursor = table[i];

        // Iterate over all nodes in linked list
        while (cursor != NULL)
        {
            // Set temporary variable to next node in linked list
            node *temp = cursor->next;

            // Free current node
            free(cursor);

            // Set cursor to next node in linked list
            cursor = temp;
        }
    }

    // Indicate success
    return true;
}

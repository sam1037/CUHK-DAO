# helper.py
import main  # Import main.py

def print_poem_statistics():
    # Call the main function to get results
    sentiment_result, wordcount_stat, complexity_stat = main.main()  # Call main function from main.py

    # Print Sentiment values
    print("Sentiment Values for each poem:")
    for sentiment in sentiment_result['sentiments']:
        print(sentiment)

    # Print Word Counts
    print("\nWord Counts for each poem:")
    for word_count in wordcount_stat['word_counts']:
        print(word_count)

    # Print Wording Complexity
    print("\nWording Complexity for each poem:")
    for complexity in complexity_stat:
        print(complexity['wordingComplexity'])

# Print Sentiment values
print("Sentiment Values for each poem:")
for sentiment in sentiment_result['sentiments']:
    print(sentiment)

# Print Word Counts
print("\nWord Counts for each poem:")
for word_count in wordcount_stat['word_counts']:
    print(word_count)

# Print Wording Complexity
print("\nWording Complexity for each poem:")
for complexity in complexity_stat:
    print(complexity['wordingComplexity'])
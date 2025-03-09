# This file do the basic analysis for the poems, e.g. word segmentation, sentiment, word count, word complexity, etc
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud
import jieba
from collections import Counter
from snownlp import SnowNLP
from wordingComplexity import analyze_poem_complexity, visualize_complexity_stats
import pandas as pd
from collections import defaultdict



# function to get basic info of a poem, return an object
def analyze_poem(poem):
    lines = poem['body']
    total_chars = sum(len(line) for line in lines)
    punctuation = '，。、！？：；（）{}[]「」『』""''　 '
    chars_no_punct = sum(len(''.join(c for c in line if c not in punctuation)) for line in lines)
    sentiment = SnowNLP(' '.join(lines)).sentiments

    return {
        'title': poem['title'],
        'author': poem['author'],
        'total_chars': total_chars,
        'chars_no_punct': chars_no_punct,
        'line_count': len(lines),
        'avg_chars_per_line': round(chars_no_punct / len(lines), 2),
        'sentiment': sentiment
    }

# function to get analysis about word (actaully char) count: mean median, sd, min, max, freq dist
def analyze_wordcount_stat(analysed_poems):
    # Store word counts for each verse
    word_counts = [p['chars_no_punct'] for p in analysed_poems]
    
    # Convert to numpy array for calculations
    word_counts = np.array(word_counts)

    # Create a frequency distribution
    unique_counts = np.unique(word_counts, return_counts=True)
    freq_dist = {count: freq for count, freq in zip(unique_counts[0], unique_counts[1])}
    
    # Calculate statistics
    stats = {
        'Mean': round(np.mean(word_counts), 2),
        'Median': round(np.median(word_counts), 2),
        'Standard Deviation': round(np.std(word_counts), 2),
        'Min': np.min(word_counts),
        'Max': np.max(word_counts),
        'freq_dist': freq_dist,
        'word_counts': word_counts
    }
    
    return stats


# func to analyse the sentiment of poems
def analyze_sentiment_stat(analyszed_poems):
    sentiments = [p['sentiment'] for p in analyszed_poems]
    # Calculate overall statistics
    overall_stats = {
        'average_sentiment': np.mean(sentiments),
        'median_sentiment': np.median(sentiments),
        'std_sentiment': np.std(sentiments),
        'sentiments': sentiments
    }
    return overall_stats

# func to count the total number of poems
def count_total_poems(poems):
    return len(poems)

# func to calculate the average sentiment score of each author 
def calculate_avg_sentiment_per_author(poems):

    author_sentiments = defaultdict(list)  # Store sentiment scores for each author

    # Iterate through poems and calculate sentiment scores
    for poem in poems:
        # Analyze the poem to get its sentiment score
        analyzed_poem = analyze_poem(poem)
        author = analyzed_poem['author']
        sentiment_score = analyzed_poem['sentiment']

        # Append the sentiment score to the author's list
        author_sentiments[author].append(sentiment_score)

    # Calculate the average sentiment score for each author
    avg_sentiments = {author: sum(scores) / len(scores) for author, scores in author_sentiments.items()}
    return avg_sentiments

# func for inputing the author name, out put each poems with issue number and sentiment score
def get_poem_sentiments_by_author(poems, author_name):

    poem_sentiments = []

    # Iterate through poems and collect sentiment scores and issue numbers for the specified author
    for poem in poems:
        if poem['author'] == author_name:
            # Analyze the poem to get its sentiment score
            analyzed_poem = analyze_poem(poem)
            poem_title = analyzed_poem['title']
            sentiment_score = analyzed_poem['sentiment']
            issue_number = poem.get('issueNumber', 'N/A')  # Default to 'N/A' if 'issueNumber' is missing

            # Append the poem title, sentiment score, and issue number to the list
            poem_sentiments.append((poem_title, sentiment_score, issue_number))

    return poem_sentiments
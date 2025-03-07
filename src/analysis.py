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
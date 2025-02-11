import os
import json
import random
import numpy as np
import jieba
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from loadChinCommonWords import load_common_words
import pandas as pd
import plotly.express as px

commonWordDict = load_common_words()

def analyze_poem_complexity(poem):
    lines = poem['body']
    # preprocessing
    all_text = ' '.join(lines)
    punctuation = '，。、！？：；（）{}[]「」『』""''　 '
    words = list(jieba.cut(all_text))
    words = [w for w in words if w not in punctuation]

    # some analysis
    total_words = len(words)
    unique_words = len(set(words))
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / total_words if total_words > 0 else 0
    vocab_richness = unique_words / total_words if total_words > 0 else 0

    #analysis the number of common words
    commonWords = [w for w in words if w in commonWordDict]
    wordingComplexity = 1 - len(commonWords) / total_words if total_words > 0 else 0



    # Assuming each Chinese character is one syllable
    total_syllables = total_chars
    avg_syllables_per_word = total_syllables / total_words if total_words > 0 else 0

    return {
        'title': poem['title'],
        'author': poem['author'],
        'total_words': total_words,
        'unique_words': unique_words,
        'avg_word_length': round(avg_word_length, 2),
        'vocab_richness': round(vocab_richness, 2),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2),
        'wordingComplexity': round(wordingComplexity, 2)
    }

# visulize the wording complexity with a horizontal barchart with matplotlib
def visualize_complexity_stats(complexity_stats):
    # setup the dataframe
    limit = 20
    complexityDF = pd.DataFrame(complexity_stats, columns=['title', 'wordingComplexity'])
    complexityDF = complexityDF.sort_values(by='wordingComplexity', ascending=True).tail(limit)

    # Set the font properties for Chinese characters
    font_path = "Noto_Sans_TC/static/NotoSansTC-Black.ttf"
    prop = fm.FontProperties(fname=font_path)

    # setup the plot with matplotlib
    plt.figure(figsize=(10,8))
    bars = plt.barh(complexityDF['title'], complexityDF['wordingComplexity'], color='skyblue')
    # Apply Chinese-compatible font to y-axis labels (poem titles)
    plt.yticks(ticks=np.arange(len(complexityDF)), 
              labels=complexityDF['title'], 
              fontsize=8, 
              fontproperties=prop)

    # Add numerical values at the end of each bar
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.01,  # Slightly offset from end of bar
                bar.get_y() + bar.get_height()/2,  # Centered vertically
                f'{width:.2f}',
                ha='left',
                va='center',
                fontsize=8)

    # Add title and labels
    plt.title(f'Wording Complexity for Top {limit} Poems', fontsize=16, fontproperties=prop)
    plt.xlabel('Complexity Score (higher more complex)', fontsize=12, fontproperties=prop)
    plt.ylabel('Poem Title', fontsize=12, fontproperties=prop)

    # Add grid for better readability
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()  # Ensure tight layout to prevent overlap
    plt.show()

    return
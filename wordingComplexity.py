import os
import json
import random
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
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

# Visualize the complexity stats with a horizontal bar chart
def visualize_complexity_stats(complexity_stats):
    titles = [stat['title'] for stat in complexity_stats]
    wordingComplexity = [stat['wordingComplexity'] for stat in complexity_stats]

    # Combine titles and wording complexity into a list of tuples and sort by wording complexity
    sorted_stats = sorted(zip(wordingComplexity, titles)) #? zip?

    # limit the number of poems to display
    sorted_stats = sorted_stats[:10000]

    # Unzip the sorted list
    sorted_wordingComplexity, sorted_titles = zip(*sorted_stats)

    # Create a DataFrame for Plotly
    df = pd.DataFrame({
        'Poem Titles': sorted_titles,
        'Wording Complexity': sorted_wordingComplexity
    })

    # Create the interactive bar chart
    fig = px.bar(df, x='Wording Complexity', y='Poem Titles', orientation='h',
                 title='Wording Complexity of the Chinese Modern Verses')

    # Define the click event
    def on_click(trace, points, state):
        for i in points.point_inds:
            title = df.iloc[i]['Poem Titles']
            # Open the corresponding poem (assuming you have a function to get the poem content)
            print(f"Title: {title}")
            # Optionally, open the poem in a web browser or display it in another way
            # webbrowser.open(f'path/to/poems/{title}.html')

    fig.data[0].on_click(on_click)

    fig.show()

    #this part is visualizing the data with matplotlib, now trying to use plotly to make it interactive
    """
    font_path = r"Noto_Sans_TC/static/NotoSansTC-Black.ttf"
    font_prop = FontProperties(fname=font_path)

    plt.figure(figsize=(10, 8))
    plt.barh(sorted_titles, sorted_wordingComplexity, color='blue')
    plt.title('Wording Complexity of the Chinese Modern Verses', fontproperties=font_prop)
    plt.xlabel('Wording Complexity (higher more complex)', fontproperties=font_prop)
    plt.ylabel('Poem Titles', fontproperties=font_prop)
    plt.xticks(fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)
    plt.tight_layout()
    plt.show()
    """
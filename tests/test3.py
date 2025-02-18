import json
import os
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def analyze_sentiment(poems):
    # Store sentiment scores for each poem
    poem_sentiments = []
    # Store line-by-line sentiments
    line_sentiments = []
    
    # Analysis results
    results = {
        'overall_stats': {},
        'poem_scores': [],
        'most_positive_lines': [],
        'most_negative_lines': []
    }
    
    for poem in poems:
        poem_text = ' '.join(poem['body'])
        
        # Analyze whole poem
        poem_sentiment = SnowNLP(poem_text)
        poem_score = poem_sentiment.sentiments
        poem_sentiments.append(poem_score)
        
        # Store poem score with title
        results['poem_scores'].append({
            'title': poem.get('title', 'Untitled'),
            'score': poem_score
        })
        
        # Analyze individual lines
        for line in poem['body']:
            if line.strip():  # Skip empty lines
                try:
                    line_sentiment = SnowNLP(line)
                    score = line_sentiment.sentiments
                    line_sentiments.append((line, score))
                except:
                    continue

    # Sort lines by sentiment score
    line_sentiments.sort(key=lambda x: x[1])
    
    # Get most positive and negative lines
    results['most_negative_lines'] = line_sentiments[:5]  # 5 most negative
    results['most_positive_lines'] = line_sentiments[-5:]  # 5 most positive
    
    # Calculate overall statistics
    results['overall_stats'] = {
        'average_sentiment': np.mean(poem_sentiments),
        'median_sentiment': np.median(poem_sentiments),
        'std_sentiment': np.std(poem_sentiments)
    }
    
    # Create visualizations
    create_sentiment_visualizations(poem_sentiments, results['poem_scores'])
    
    return results

def create_sentiment_visualizations(sentiments, poem_scores):
    # 1. Histogram of sentiment distribution
    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.hist(sentiments, bins=20, edgecolor='black')
    plt.title('Distribution of Poem Sentiments')
    plt.xlabel('Sentiment Score (0=Negative, 1=Positive)')
    plt.ylabel('Frequency')

    # 2. Line plot of sentiment scores
    plt.subplot(122)
    plt.plot(range(len(sentiments)), sorted(sentiments), marker='o')
    plt.title('Sorted Sentiment Scores')
    plt.xlabel('Poem Index')
    plt.ylabel('Sentiment Score')
    plt.tight_layout()
    plt.show()

# Usage example
def print_sentiment_analysis(results):
    print("\nOverall Sentiment Statistics:")
    print(f"Average sentiment: {results['overall_stats']['average_sentiment']:.3f}")
    print(f"Median sentiment: {results['overall_stats']['median_sentiment']:.3f}")
    print(f"Standard deviation: {results['overall_stats']['std_sentiment']:.3f}")
    
    print("\nMost Positive Lines:")
    for line, score in results['most_positive_lines'][::-1]:
        print(f"{line}: {score:.3f}")
    
    print("\nMost Negative Lines:")
    for line, score in results['most_negative_lines']:
        print(f"{line}: {score:.3f}")
    
    print("\nPoems sorted by sentiment:")
    sorted_poems = sorted(results['poem_scores'], key=lambda x: x['score'])
    for poem in sorted_poems:
        print(f"{poem['title']}: {poem['score']:.3f}")

# Run the analysis:

# Read all JSON files from the data folder
poems = []
data_folder = 'data'

for filename in os.listdir(data_folder):
    #print(filename)
    if filename.endswith('.json'):
        file_path = os.path.join(data_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                #print(f.read())
                poems.append(json.load(f))
        except Exception as e:
            print(f"Unexpected error with file: {filename} - {e}")
results = analyze_sentiment(poems)
print_sentiment_analysis(results)
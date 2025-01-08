import pandas as pd
import numpy as np
import jieba  # For Chinese word segmentation

# Sample data - replace with your actual verses
verses = [
    "床前明月光，疑是地上霜。",
    "举头望明月，低头思故乡。",
    "春眠不觉晓，处处闻啼鸟。",
    "夜来风雨声，花落知多少。"
]

def analyze_verse_stats(verses):
    # Store word counts for each verse
    word_counts = []
    
    for verse in verses:
        # Segment Chinese text into words
        words = list(jieba.cut(verse))
        # Remove punctuation and empty strings
        words = [word for word in words if word.strip() and word not in '，。？！']
        word_counts.append(len(words))
    
    # Convert to numpy array for calculations
    word_counts = np.array(word_counts)
    
    # Calculate statistics
    stats = {
        'Mean': np.mean(word_counts),
        'Median': np.median(word_counts),
        'Mode': pd.Series(word_counts).mode()[0],
        'Standard Deviation': np.std(word_counts),
        'Min': np.min(word_counts),
        'Max': np.max(word_counts)
    }
    
    # Create a summary DataFrame
    stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
    
    return stats_df, word_counts

# Perform analysis
stats_df, word_counts = analyze_verse_stats(verses)

# Display results
print("Statistical Analysis of Verse Word Counts:")
print(stats_df)

# Create a frequency distribution
print("\nWord Count Distribution:")
unique_counts = np.unique(word_counts, return_counts=True)
for count, freq in zip(unique_counts[0], unique_counts[1]):
    print(f"{count} words: {freq} verses")
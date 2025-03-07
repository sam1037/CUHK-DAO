import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud
import jieba
from collections import Counter
from snownlp import SnowNLP
from analysis import analyze_poem_complexity, visualize_complexity_stats
import pandas as pd
from analysis import analyze_poem


# function to visualize the word count stat: freq dist and box diagrams
def visualize_wordcount_stat(wc_stats):
    # plot freq dist for wc
    word_counts = wc_stats['word_counts']

    plt.figure(figsize=(8, 6))
    plt.hist(word_counts, bins=5, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Word Count Distribution', fontsize=16)
    plt.xlabel('Word Count', fontsize=14)
    plt.ylabel('Number', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # box and whisker plot
    plt.figure(figsize=(8, 6))
    plt.boxplot(word_counts, vert=False) 
    
    plt.title('Word Count Distribution (box and whiskey)', fontsize=16)
    plt.xlabel('Word Count', fontsize=14)
    plt.yticks([])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# function to visualize the sentiment stat: freq dist and box diagrams
def visualize_sentiment_stat(sentiment_stats):
    # plot freq dist for sentiment
    sentiments = sentiment_stats['sentiments']
    plt.figure(figsize=(8, 6))
    plt.hist(sentiments, bins=5, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Sentiment Score Distribution', fontsize=16)
    plt.xlabel('Sentiment Score', fontsize=14)
    plt.ylabel('Number', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # box and whisker plot
    plt.figure(figsize=(8, 6))
    plt.boxplot(sentiments, vert=False) 
    
    plt.title('Sentiment Score Distribution (box and whiskey)', fontsize=16)
    plt.xlabel('Sentiment score', fontsize=14)
    plt.yticks([])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# generate word cloud from a given list of poem objects
def generate_word_cloud(poems):
    # Combine all poems' text, exclude common chinese words
    stopwords = set(['的', '了', '和', '是', '在', '我', '有', '而', '你', '也',
                '就', '都', '又', '去', '到', '說', '著', '來', '把', '那',
                '但', '很', '不', '與', '麼', '這', '要', '於', '以', '卻',
                '中', '為', '吧', '得', '將', '還', '能', '可', '她', '他',
                '從', '上', '下', '又', '過', '給', '讓', '向', '已', '所',
                '如', '被', '之', '時', '以', '矣', '焉', '兮', '其', '乎',
                '他們', '我們', '這些', '那個', '所以', '因為', '只是', '不能',
                '不會', '如果', '這個', '一個', '一起', '一點', '有人', '之間',
                '這樣', '什麼', '還是', '不再', '們'
                ])
    
    all_text = ''
    for poem in poems:
        all_text += ' '.join(poem['body']) + ' '
    
    
    # Segment text into words using jieba
    seg_list = list(jieba.cut(all_text))

    # Create word frequency dictionary, filtering out stopwords and single characters
    word_freq = Counter(word for word in seg_list 
                        if word not in stopwords 
                        and len(word.strip()) > 1
                        and word.strip())
    
    print(word_freq.most_common(10))

    # Create word cloud with Chinese font
    wordcloud = WordCloud(
        font_path= r"Noto_Sans_TC/static/NotoSansTC-Black.ttf",  
        width=800,
        height=400,
        background_color='white',
        max_words=100
    ).generate_from_frequencies(word_freq)

    # Display the word cloud
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# This function is to generate a correlation matrix between sentiment, word_count, and wordingComplexity
def generate_correlation_matrix(analysed_poems, complexity_stat):
    # Extract the necessary data: sentiment, word count, and wording complexity
    sentiments = [poem['sentiment'] for poem in analysed_poems]
    word_counts = [poem['chars_no_punct'] for poem in analysed_poems]
    wording_complexity = [complexity['wordingComplexity'] for complexity in complexity_stat]

    # Create a DataFrame
    df = pd.DataFrame({
        'Sentiment': sentiments,
        'Word Count': word_counts,
        'Wording Complexity': wording_complexity
    })

    print(df)

    # Compute the correlation matrix
    correlation_matrix = df.corr()

    # Plot the correlation matrix using matplotlib
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation_matrix, cmap='RdYlGn', interpolation='none', vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns, fontsize=12)
    plt.yticks(range(len(correlation_matrix)), correlation_matrix.columns, fontsize=12)
    plt.title('Correlation Matrix', fontsize=15)

    for i in range(len(correlation_matrix)):
        for j in range(len(correlation_matrix)):
            plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black')

    plt.show()


# This Function is to generate the heat map of sentiment
# NOT COMPLETED
def generate_sentiment_heatmap_onebyone(poems):
    # Ensure poems are analyzed and have 'sentiment' key
    analyzed_poems = [analyze_poem(poem) for poem in poems]
    
    # Proceed only if there are poems to plot
    if not analyzed_poems:
        print("No poems to plot.")
        return

    poem_sentiments = [(poem['title'], poem['sentiment']) for poem in analyzed_poems]

    sentiment_df = pd.DataFrame(poem_sentiments, columns=['Poem Title', 'Sentiment'])
    sentiment_df = sentiment_df.sort_values(by='Sentiment', ascending=False)

    # Set the font properties for Chinese characters
    font_path = "Noto_Sans_TC/static/NotoSansTC-Black.ttf"  # Adjust font path if necessary
    prop = fm.FontProperties(fname=font_path)

    # Set up the figure size
    plt.figure(figsize=(12, 8))  # Increase figure size
    heatmap_data = [sentiment_df['Sentiment'].values]  # Values for the heatmap

    # Display the heatmap with vertical orientation (columns for each sentiment)
    plt.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', interpolation='nearest')

    # Display color bar for sentiment values
    plt.colorbar(label='Sentiment Score')

    # Apply the Chinese-compatible font to the x-axis labels (poem titles)
    plt.xticks(ticks=np.arange(len(sentiment_df)), labels=sentiment_df['Poem Title'], rotation=90, fontsize=8, fontproperties=prop)
    plt.yticks([])  # No y-axis labels needed since we're only showing sentiment scores in vertical bars

    # Add numerical values inside the heatmap bars (sentiment scores)
    for i in range(len(sentiment_df)):
        plt.text(i, 0, f'{sentiment_df["Sentiment"].iloc[i]:.2f}', ha='center', va='center', fontsize=10, color='black', fontproperties=prop)

    # Add title and labels to the plot
    plt.title('Sentiment Scores Heatmap for Poems', fontsize=16, fontproperties=prop)
    plt.xlabel('Poem Title', fontsize=12, fontproperties=prop)

    plt.tight_layout()  # Ensure tight layout to prevent overlap
    plt.show()


# This Function is to generate issue * #poem heat map
# result not good?
from matplotlib import font_manager as fm
from collections import defaultdict

def generate_sentiment_heatmap_by_issue(poems):
    # Analyze poems to get sentiment scores
    analyzed_poems = [analyze_poem(poem) for poem in poems]
    if not analyzed_poems:
        print("No poems to plot.")
        return

    # Group poems by issue number and sort by sentiment
    grouped_poems = defaultdict(list)
    for poem in analyzed_poems:
        issue = poem.get('issueNumber', None)  # Use .get() to avoid KeyError
        if issue is None:
            continue  # Skip poems without an issue number
        grouped_poems[issue].append({
            'title': poem['title'],
            'sentiment': poem['sentiment']
        })

    # Sort poems in each issue by sentiment (descending)
    for issue in grouped_poems:
        grouped_poems[issue].sort(key=lambda x: x['sentiment'], reverse=True)

    # Get the list of available issues
    available_issues = sorted(grouped_poems.keys())
    num_issues = len(available_issues)

    # Prepare heatmap data
    max_poems_per_issue = max(len(v) for v in grouped_poems.values()) if grouped_poems else 0
    heatmap_data = np.full((max_poems_per_issue, num_issues), np.nan)  # Dynamic number of columns based on available issues

    # Fill data into the heatmap matrix
    for col, issue in enumerate(available_issues):
        poems_in_issue = grouped_poems.get(issue, [])
        for row in range(len(poems_in_issue)):
            heatmap_data[row, col] = poems_in_issue[row]['sentiment']

    # Set up visualization
    plt.figure(figsize=(20, 10))
    cmap = plt.cm.RdYlGn
    cmap.set_bad('white')  # Handle NaN values

    # Create heatmap
    plt.imshow(heatmap_data, cmap=cmap, aspect='auto', interpolation='nearest')

    # Customize axes
    plt.xticks(ticks=np.arange(num_issues), labels=[str(issue) for issue in available_issues], rotation=90, fontsize=8)
    plt.yticks(ticks=np.arange(max_poems_per_issue), labels=np.arange(1, max_poems_per_issue+1), fontsize=8)
    plt.xlabel("Issue Number", fontsize=12)
    plt.ylabel("Poem Index in Issue (Sorted by Sentiment)", fontsize=12)

    # Add color bar and title
    plt.colorbar(label='Sentiment Score')
    plt.title("Sentiment Distribution Across Issues", fontsize=16)

    # Add sentiment values as text annotations
    for row in range(max_poems_per_issue):
        for col in range(num_issues):
            val = heatmap_data[row, col]
            if not np.isnan(val):
                plt.text(col, row, f'{val:.2f}', ha='center', va='center', 
                        fontsize=6, color='black')

    plt.tight_layout()
    plt.show()

# seems not good result
def generate_sentiment_heatmap_by_issue(poems):
    # Analyze poems to get sentiment scores
    analyzed_poems = [analyze_poem(poem) for poem in poems]
    if not analyzed_poems:
        print("No poems to plot.")
        return

    # Group poems by issue number and sort by sentiment
    grouped_poems = defaultdict(list)
    for poem in analyzed_poems:
        issue = poem.get('issueNumber', None)  # Use .get() to avoid KeyError
        if issue is None:
            continue  # Skip poems without an issue number
        grouped_poems[issue].append({
            'title': poem['title'],
            'sentiment': poem['sentiment']
        })

    # Sort poems in each issue by sentiment (descending)
    for issue in grouped_poems:
        grouped_poems[issue].sort(key=lambda x: x['sentiment'], reverse=True)

    # Get the list of available issues
    available_issues = sorted(grouped_poems.keys())
    num_issues = len(available_issues)

    # Prepare heatmap data
    max_poems_per_issue = max(len(v) for v in grouped_poems.values()) if grouped_poems else 0
    heatmap_data = np.full((max_poems_per_issue, num_issues), np.nan)  # Dynamic number of columns based on available issues

    # Fill data into the heatmap matrix
    for col, issue in enumerate(available_issues):
        poems_in_issue = grouped_poems.get(issue, [])
        for row in range(len(poems_in_issue)):
            heatmap_data[row, col] = poems_in_issue[row]['sentiment']

    # Set up visualization
    plt.figure(figsize=(20, 10))
    cmap = plt.cm.RdYlGn
    cmap.set_bad('white')  # Handle NaN values

    # Create heatmap
    plt.imshow(heatmap_data, cmap=cmap, aspect='auto', interpolation='nearest')

    # Customize axes
    plt.xticks(ticks=np.arange(num_issues), labels=[str(issue) for issue in available_issues], rotation=90, fontsize=8)
    plt.yticks(ticks=np.arange(max_poems_per_issue), labels=np.arange(1, max_poems_per_issue+1), fontsize=8)
    plt.xlabel("Issue Number", fontsize=12)
    plt.ylabel("Poem Index in Issue (Sorted by Sentiment)", fontsize=12)

    # Add color bar and title
    plt.colorbar(label='Sentiment Score')
    plt.title("Sentiment Distribution Across Issues", fontsize=16)

    # Add sentiment values as text annotations
    for row in range(max_poems_per_issue):
        for col in range(num_issues):
            val = heatmap_data[row, col]
            if not np.isnan(val):
                plt.text(col, row, f'{val:.2f}', ha='center', va='center', 
                        fontsize=6, color='black')

    plt.tight_layout()
    plt.show()

# This Function is to generate the barchart of top20_sentiment
def generate_sentiment_barchart_top20(poems):
    analyzed_poems = [analyze_poem(poem) for poem in poems]
    
    # Proceed only if there are poems to plot
    if not analyzed_poems:
        print("No poems to plot.")
        return

    poem_sentiments = [(poem['title'], poem['sentiment']) for poem in analyzed_poems]
    sentiment_df = pd.DataFrame(poem_sentiments, columns=['Poem Title', 'Sentiment'])
    
    # Sort the DataFrame by sentiment score and select top 20
    sentiment_df = sentiment_df.sort_values(by='Sentiment', ascending=True).tail(20)

    # Set the font properties for Chinese characters
    font_path = "Noto_Sans_TC/static/NotoSansTC-Black.ttf"  # Adjust font path if necessary
    prop = fm.FontProperties(fname=font_path)

    # Set up the figure size for the bar chart
    plt.figure(figsize=(10,8))  # Set appropriate figure size for the bar chart

    # Create the bar chart
    bars = plt.barh(sentiment_df['Poem Title'], sentiment_df['Sentiment'], color='skyblue')

    # Apply Chinese-compatible font to y-axis labels (poem titles)
    plt.yticks(ticks=np.arange(len(sentiment_df)), 
              labels=sentiment_df['Poem Title'], 
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
    plt.title('Sentiment Scores for Top 20 Poems', fontsize=16, fontproperties=prop)
    plt.xlabel('Sentiment Score', fontsize=12, fontproperties=prop)
    plt.ylabel('Poem Title', fontsize=12, fontproperties=prop)

    plt.tight_layout()  # Ensure tight layout to prevent overlap
    plt.show()
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

# function to get basic info of a poem
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

# function to get analysis about word (actaully char) count: mean median, sd, min, max, freq dist and plot the histogram of 
def analyze_wordcount_stat(analysed_poems):
    # Store word counts for each verse
    word_counts = [p['chars_no_punct'] for p in analysed_poems]
    
    # Convert to numpy array for calculations
    word_counts = np.array(word_counts)

    # Create a frequency distribution
    unique_counts = np.unique(word_counts, return_counts=True)
    freq_dist = {count: freq for count, freq in zip(unique_counts[0], unique_counts[1])}

    # Plot histogram of word counts
    """
    plt.figure(figsize=(8, 6))
    plt.hist(word_counts, bins=5, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Word Count Distribution', fontsize=16)
    plt.xlabel('Word Count', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    """
    
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


# this function is to do topic modeling, developing, not completed
def topic_modeling(poems):
    stop_words = set(['了', '的', '在', '與', '和', '是', '都', '而', '及', '著', '就', '從'])

    from gensim import corpora, models
    
    poems_text = []
    for poem in poems:
        # Join all lines in the poem
        full_poem = ''.join(poem['body'])
        poems_text.append(full_poem)
    # Assuming poems is your list of Chinese verses
    # 1. Tokenize
    tokenized_poems = [jieba.lcut(poem) for poem in poems_text]

    # 2. Create dictionary
    dictionary = corpora.Dictionary(tokenized_poems)

    # 3. Create document-term matrix
    corpus = [dictionary.doc2bow(poem) for poem in tokenized_poems]

    # 4. Train LDA model
    num_topics = 5  # You can adjust this
    lda_model = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10
    )

    # 5. Print topics
    for idx, topic in lda_model.print_topics():
        print(f'Topic {idx + 1}:')
        print(topic)

# load the poems, return a list of poem obj representing by dictionaries
def loadPoemData():
    # Initialize a list to store poems
    poems = []
    data_folder = 'data'  # Root folder containing the issue folders

    # Recursively walk through the folder structure
    for root, dirs, files in os.walk(data_folder):
        for filename in files:
            # Process only JSON files
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)  # Construct the full file path
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Load the JSON file and append to the poems list
                        poems.append(json.load(f))
                except Exception as e:
                    print(f"Unexpected error with file: {file_path} - {e}")

    return poems


# This function is to generate a correlation matrix between sentiment, word_count, and wordingComplexity
# completed 

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
# Not completed

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

# main part
poems = loadPoemData()
print(f"Loaded {len(poems)} poems.")

# analyze
analyses = [analyze_poem(poem) for poem in poems] # a list of dict
print([p['sentiment'] for p in analyses])

wordcount_stat = analyze_wordcount_stat(analyses)
sentiment_result = analyze_sentiment_stat(analyses)
complexity_stat = [analyze_poem_complexity(poem) for poem in poems]

#Visulization (word count, sent, complexity, word cloud, corr. matrix)
visualize_wordcount_stat(wordcount_stat)
visualize_sentiment_stat(sentiment_result)
generate_sentiment_barchart_top20(poems)
visualize_complexity_stats(complexity_stat)

generate_word_cloud(poems)
generate_correlation_matrix(analyses, complexity_stat)


# Plot the heatmap of poems
# generate_sentiment_heatmap_onebyone(poems) #need fix
# generate_sentiment_heatmap_by_issue(poems) #need fix



# Display results (TODO visualize)
# print("Statistical Analysis of Poem Word Counts:")
# print(wordcount_stat)
#print(sentiment_result)
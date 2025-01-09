import json
import os
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from collections import Counter
from snownlp import SnowNLP

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
    plt.title('Word Count Distribution (freq dist)', fontsize=16)
    plt.xlabel('Word Count', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # box and whisker plot
    plt.figure(figsize=(8, 6))
    plt.boxplot(word_counts, vert=False) #don't know why the whiskey line don't show
    
    plt.title('Word Count Distribution (box and whiskey)', fontsize=16)
    plt.xlabel('Word Count', fontsize=14)
    plt.yticks([])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# func to analyse the sentiment of poems
def analyze_sentiment_stat(analyszed_poems):
    sentiments = [p['sentiment'] for p in analyszed_poems]
    # Todo: Add frequency distribution
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
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # box and whisker plot
    plt.figure(figsize=(8, 6))
    plt.boxplot(sentiments, vert=False) #don't know why the whiskey line show for this one
    
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
                    '如', '被', '之', '時', '以', '矣', '焉', '兮', '其', '乎'])
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

#TODO: wording complexity analysis

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


# analyze
analyses = [analyze_poem(poem) for poem in poems]
wordcount_stat = analyze_wordcount_stat(analyses)
sentiment_result = analyze_sentiment_stat(analyses)

# Display results (TODO visualize)
# generate_word_cloud(poems)
visualize_wordcount_stat(wordcount_stat)
visualize_sentiment_stat(sentiment_result)
print("Statistical Analysis of Poem Word Counts:")
print(wordcount_stat)
print(sentiment_result)


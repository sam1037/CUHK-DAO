import os
import json
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from gensim import corpora, models

def analyze_poem(poem):
    lines = poem['body']
    total_chars = sum(len(line) for line in lines)
    punctuation = '，。、！？：；（）{}[]「」『』""''　 '
    chars_no_punct = sum(len(''.join(c for c in line if c not in punctuation)) for line in lines)
    return {
        'title': poem['title'],
        'author': poem['author'],
        'total_chars': total_chars,
        'chars_no_punct': chars_no_punct,
        'line_count': len(lines),
        'avg_chars_per_line': round(chars_no_punct / len(lines), 2)
    }

def topic_modeling(poems):
    stopwords = set(['的', '了', '我', '你', '他', '她', '它', '我們', '你們', '他們', '她們', '它們', '是', '在', '有', '和', '也', '不', '就', '都', '而', '及', '與', '或', '但', '很', '不', '與', '麼', '這', '要', '於', '以', '卻', '中', '為', '吧', '得', '將', '還', '能', '可', '她', '他', '從', '上', '下', '又', '過', '給', '讓', '向', '已', '所', '如', '被', '之', '時', '以', '矣', '焉', '兮', '其', '乎'])
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
        font_path=r"Noto_Sans_TC/static/NotoSansTC-Black.ttf",  
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

    # Prepare data for topic modeling
    texts = [[word for word in jieba.cut(poem['body']) if word not in stopwords and len(word.strip()) > 1] for poem in poems]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Perform LDA
    lda = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    topics = lda.print_topics(num_words=10)
    for idx, topic in topics:
        print(f"Topic {idx}: {topic}")

# Read all JSON files from the data folder
poems = []
data_folder = 'data'

for filename in os.listdir(data_folder):
    print(filename)
    if filename.endswith('.json'):
        file_path = os.path.join(data_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                poems.append(json.load(f))
        except Exception as e:
            print(f"Unexpected error with file: {filename} - {e}")

analyses = [analyze_poem(poem) for poem in poems]

# Print results
print("詩歌文字分析：\n")
for analysis in analyses:
    print(f"標題：{analysis['title']}")
    print(f"作者：{analysis['author']}")
    print(f"總字數（含標點）：{analysis['total_chars']}")
    print(f"總字數（不含標點）：{analysis['chars_no_punct']}")
    print(f"行數：{analysis['line_count']}")
    print(f"平均每行字數：{analysis['avg_chars_per_line']}")
    print("-" * 50)

# Perform topic modeling
topic_modeling(poems)
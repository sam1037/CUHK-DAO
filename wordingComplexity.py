import os
import json
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def analyze_poem_complexity(poem):
    lines = poem['body']
    all_text = ' '.join(lines)
    words = list(jieba.cut(all_text))
    total_words = len(words)
    unique_words = len(set(words))
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / total_words if total_words > 0 else 0
    vocab_richness = unique_words / total_words if total_words > 0 else 0

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
        'avg_syllables_per_word': round(avg_syllables_per_word, 2)
    }

def visualize_complexity_stats(complexity_stats):
    titles = [stat['title'] for stat in complexity_stats]
    avg_word_lengths = [stat['avg_word_length'] for stat in complexity_stats]
    vocab_richnesses = [stat['vocab_richness'] for stat in complexity_stats]
    avg_syllables_per_word = [stat['avg_syllables_per_word'] for stat in complexity_stats]

    font_path = r"Noto_Sans_TC/static/NotoSansTC-Black.ttf"
    font_prop = FontProperties(fname=font_path)

    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    axs[0].bar(titles, avg_word_lengths, color='blue')
    axs[0].set_title('Average Word Length', fontproperties=font_prop)
    axs[0].set_xticklabels(titles, rotation=45, ha='right', fontproperties=font_prop)

    axs[1].bar(titles, vocab_richnesses, color='green')
    axs[1].set_title('Vocabulary Richness', fontproperties=font_prop)
    axs[1].set_xticklabels(titles, rotation=45, ha='right', fontproperties=font_prop)

    axs[2].bar(titles, avg_syllables_per_word, color='red')
    axs[2].set_title('Average Syllables Per Word', fontproperties=font_prop)
    axs[2].set_xticklabels(titles, rotation=45, ha='right', fontproperties=font_prop)

    plt.tight_layout()
    plt.show()

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

complexity_stats = [analyze_poem_complexity(poem) for poem in poems]

# Print results
print("詩歌文字複雜度分析：\n")
for stat in complexity_stats:
    print(f"標題：{stat['title']}")
    print(f"作者：{stat['author']}")
    print(f"總詞數：{stat['total_words']}")
    print(f"獨特詞數：{stat['unique_words']}")
    print(f"平均詞長：{stat['avg_word_length']}")
    print(f"詞彙豐富度：{stat['vocab_richness']}")
    print(f"平均每詞音節數：{stat['avg_syllables_per_word']}")
    print("-" * 50)

# Visualize complexity stats
visualize_complexity_stats(complexity_stats)
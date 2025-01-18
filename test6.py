import jieba.analyse
from collections import Counter

def analyze_poem_keywords(poem):
    # Extract keywords with weights
    keywords = jieba.analyse.extract_tags(poem, topK=20, withWeight=True)
    
    # Get word frequency
    words = jieba.lcut(poem)
    word_freq = Counter(words)
    
    return {
        'keywords': keywords,
        'word_frequency': dict(word_freq)
    }


poem = "平常的日子里\n我总是想着你"
print(analyze_poem_keywords(poem))
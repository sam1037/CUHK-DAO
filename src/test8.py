from dataLoader import loadAllPoemData
from analysis import *
from visualize import *



# load data
poems = loadAllPoemData()
print(f"Loaded {len(poems)} poems.")

# analyze
analysed_poems = [analyze_poem(poem) for poem in poems] # a list of dict
wordcount_stat = analyze_wordcount_stat(analysed_poems)
sentiment_result = analyze_sentiment_stat(analysed_poems)
complexity_stat = [analyze_poem_complexity(poem) for poem in poems]

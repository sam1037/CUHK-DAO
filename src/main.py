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

# word count visulization
visualize_wordcount_stat(wordcount_stat)

# sentiment visulization
visualize_sentiment_stat(sentiment_result)
generate_sentiment_barchart_top20(poems)

# word complexity visualization
visualize_complexity_stats(complexity_stat)

# other visulizations (word cloud, corr. matrix)
generate_word_cloud(poems)
generate_correlation_matrix(analysed_poems, complexity_stat)


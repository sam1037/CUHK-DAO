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
total_poems = count_total_poems(poems)

# Visulization
# The total number of poem 
print(f"There are a total of {total_poems} poems.")

# word count visulization
visualize_wordcount_stat(wordcount_stat)

# sentiment visualization
visualize_sentiment_stat(sentiment_result)
# generate_sentiment_barchart_top20(poems)

# word complexity visualization
visualize_complexity_stats(complexity_stat)

# other visulizations (word cloud, corr. matrix)
generate_word_cloud(poems)
generate_correlation_matrix(analysed_poems, complexity_stat)

# author poem cdf
plot_author_poem_cdf(poems)

# poem count of top n author
generate_top_author_count_barchart(poems, top_n=23)

# average sentiment score of poem count of top n author
generate_top_author_sentiment_barchart(poems, top_n=23)


# Checking: Input author name, output each poems with issue number and sentiment score 
poem_sentiments = get_poem_sentiments_by_author(poems, "王心怡")
for poem_title, sentiment_score, issue_number in poem_sentiments:
    print(f"Poem: {poem_title}, Sentiment Score: {sentiment_score:.2f}, Issue Number: {issue_number}")
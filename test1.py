import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Sample text
text = "Data analytics python programming visualization statistics machine learning"

# Create and generate a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use('agg')


file_paths = []

for root, dirs, files in os.walk(".\\Analysis"):
    for file in files:
        if file.endswith("Unique.txt"):
            file_paths.append(root)

for path in file_paths:
    path_components = path.split('\\')
    main_path = '\\'.join(path_components[:-1]) + '\\'

    unique_freq = pd.read_csv(path + '\\Unique.txt', skiprows=[0, 1, 2],
                              header=None, delimiter=' ', names=['word', 'count'])
    unique_freq[["count"]] = unique_freq[["count"]].apply(pd.to_numeric)

    uniqueWords = {}
    for word, freq in unique_freq.values:
        uniqueWords[word] = freq

    wordcloud = WordCloud(width=1600, height=1600, background_color='white')
    wordcloud.generate_from_frequencies(frequencies=uniqueWords)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(main_path + '/FigFolder/' +
                path_components[-1] + '_WordCloud.png', bbox_inches='tight')

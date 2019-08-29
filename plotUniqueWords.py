import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from collections import Counter, OrderedDict
import matplotlib
matplotlib.use('agg')

file_paths = []

for root, dirs, files in os.walk(".\\Analysis"):
    for file in files:
        if file.endswith("Unique.txt"):
            file_paths.append(root)

topWords = []
with open('top5000Words.txt') as f:
    topWords = [word[:-1].lower() for word in f]

extraWords = ['is', 'are', 'an', 'was', 'had', 'did', 'has', 'were', 'been', 'goes', 'got', 'going', 'does',
              'went', 'making', 'made', 'comes', 'gets', 'makes']
topWords.extend(extraWords)


def wordCount(text):
    words = text.split()
    wordCounts = Counter(words)
    sortedCounts = OrderedDict(wordCounts.most_common())
    wordList = [word + ' ' + str(sortedCounts[word]) for word in sortedCounts]
    return wordList


wordrepetitions = pd.DataFrame()
introduced = pd.DataFrame()

for path in file_paths:
    path_components = path.split('\\')
    wordcounts = pd.DataFrame(columns=['num_words', 'repetitions'])
    commonWords = topWords
    with open(path + '\\captionsAll.txt', encoding='utf8', errors='replace') as f:
        wordreps = pd.DataFrame()
        totWords = []
        for captions in f:
            wordList = wordCount(captions)
            uniqueWords = []
            words = [word.split() for word in wordList]
            boolUnique = [word[0] in commonWords for word in words]
            uniqueWords = [[word[0], int(word[1])] for (
                word, boolU) in zip(words, boolUnique) if boolU == False]
            uWords = pd.DataFrame(uniqueWords, columns=['word', 'count'])
            num = len(uWords)
            totWords.append(num)
            reps = uWords['count'].sum()
            episodeWords = uWords['word'].tolist()
            commonWords.extend(episodeWords)
            wordcounts = wordcounts.append(
                {'num_words': num, 'repetitions': reps}, ignore_index=True)
        wordreps = wordcounts['repetitions'].div(
            wordcounts['num_words'].replace({0: np.nan})).to_frame(path_components[-1])
        introducedwords = pd.Series(totWords).to_frame(path_components[-1])
    wordrepetitions[path_components[-1]] = wordreps[path_components[-1]
                                                    ].replace({np.nan: 0})  # new = old[['A', 'C', 'D']].copy()
    introduced[path_components[-1]
               ] = introducedwords[path_components[-1]]

main_path = '\\'.join(path_components[:-1]) + '\\'


avg_introduced = introduced.mean()
avg_introduced = pd.DataFrame(avg_introduced)
avg_introduced.reset_index(inplace=True)
avg_introduced.columns = ['show', 'avg words']


allShowData = pd.read_csv('show_analysis.csv')
allShowData = allShowData.drop(columns=['avg WPM'])
allShowData = pd.merge(allShowData, avg_introduced, on='show', how='outer')
allShowData['avg WPM'] = allShowData['avg words']/allShowData['avg runtime']

mean = allShowData['avg WPM'].mean()
allShowData = allShowData.drop(columns=['avg words'])
allShowData = allShowData.set_index('show')
allShowData.at['Average', 'avg WPM'] = mean

avg_repetitions = wordrepetitions.mean()
avg_repetitions = pd.DataFrame(avg_repetitions)
avg_repetitions.reset_index(inplace=True)
avg_repetitions.columns = ['show', 'avg reps']

mean = avg_repetitions['avg reps'].mean(axis=0)
row = ['Average', mean]
avg_repetitions.loc[len(avg_repetitions)] = row
allShowData = pd.merge(allShowData, avg_repetitions, on='show')

allShowData.to_csv('show_analysis.csv', index=False)

allShowData = allShowData.set_index('show')
allShowData = allShowData.T
columns = list(allShowData)

for i in range(len(columns)-1):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    avg = pd.Series(allShowData['Average'].loc[['avg WPM', 'avg reps']])
    show = pd.Series(allShowData[columns[i]].loc[['avg WPM', 'avg reps']])

    df = pd.DataFrame({columns[i]: show, "Average": avg})
    df.rename(index={"avg WPM": "New Words Per Minute",
                     "avg reps": "# Times New Words Repeated"}, inplace=True)
    ax = df.plot.bar(color=["cornflowerblue", "salmon"], rot=0,
                     title="# New Words Introduced And\nRepeated Per Episode")
    ax.set_ylabel("Average Per Episode")
    plt.savefig(main_path + 'FigFolder\\' +
                columns[i] + '_UniqueWords.png', bbox_inches='tight')


plt.close('all')

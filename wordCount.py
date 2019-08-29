import sys
from collections import Counter, OrderedDict
from datetime import datetime, timedelta
import os


def wordsPerMinute(runtimes, text):

    numWords = len(text.split())
    runtime = 0.0
    for time in runtimes:
        strtime = time.split(":")
        hours = int(strtime[0])
        minutes = int(strtime[1])
        seconds = int(strtime[2])
        runtime = runtime + hours*60 + minutes + seconds/60
    WPM = numWords/runtime
    return str(numWords), str(WPM), str(runtime)


def wordCount(text):

    words = text.split()
    wordCounts = Counter(words)
    sortedCounts = OrderedDict(wordCounts.most_common())
    wordList = [word + ' ' + str(sortedCounts[word]) for word in sortedCounts]
    return wordList


def countAndWrite(paths):

    for path in paths:
        with open(path + '\\captionsAll.txt', encoding='utf8', errors='replace') as f:
            captions = f.read().splitlines()
            captions = ' '.join(captions)
        with open(path + '\\runtimeAll.txt', encoding='utf8', errors='replace') as f:
            runtimes = f.read().splitlines()
        totWords, wordsPerMin, runtime = wordsPerMinute(runtimes, captions)
        wordList = wordCount(captions)
        new_file_path = path + '\\WordCount.txt'
        with open(new_file_path, 'w') as f:
            f.write(runtime + '\n')
            f.write(wordsPerMin + '\n')
            f.write(totWords + '\n')
            for word in wordList:
                f.write(word + '\n')


if __name__ == '__main__':

    file_paths = []

    for root, dirs, files in os.walk(".\\Analysis"):
        for file in files:
            if file.endswith("runtimeAll.txt"):
                file_paths.append(root)

    countAndWrite(file_paths)

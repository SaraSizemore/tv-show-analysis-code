import os


def uncommonWords(paths):

    topWords = []
    with open('top5000Words.txt') as f:
        topWords = [word[:-1].lower() for word in f]
    extraWords = ['is', 'are', 'an', 'was', 'had', 'did', 'has', 'were', 'been', 'goes', 'got', 'going', 'does',
                  'went', 'making', 'made', 'comes', 'gets', 'makes']
    topWords.extend(extraWords)

    for path in paths:
        uniqueWords = []
        words = []
        with open(path + '\\WordCount.txt', encoding='utf8', errors='replace') as f:
            _ = f.readline()
            _ = f.readline()
            _ = f.readline()
            words = [word.split() for word in f]
            boolUnique = [word[0] in topWords for word in words]
            uniqueWords = [' '.join(word) for (word, boolU) in zip(
                words, boolUnique) if boolU == False]
        new_file_path = path + '\\Unique.txt'
        with open(new_file_path, 'w') as f:
            for word in uniqueWords:
                f.write(word + '\n')


if __name__ == '__main__':

    file_paths = []

    for root, dirs, files in os.walk(".\\Analysis"):
        for file in files:
            if file.endswith("WordCount.txt"):
                file_paths.append(root)

    uncommonWords(file_paths)

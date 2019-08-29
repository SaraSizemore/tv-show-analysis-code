import sys
import re
from datetime import datetime
import string
import os
from collections import Counter
from math import floor


def intToWord(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    num = int(num)
    
    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + ' ' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred ' + intToWord(num % 100)

    if (num < m):
        if num % k == 0: return intToWord(num // k) + ' thousand'
        else: return intToWord(num // k) + ' thousand ' + intToWord(num % k)

    if (num < b):
        if (num % m) == 0: return intToWord(num // m) + ' million'
        else: return intToWord(num // m) + ' million ' + intToWord(num % m)

    if (num < t):
        if (num % b) == 0: return intToWord(num // b) + ' billion'
        else: return intToWord(num // b) + ' billion ' + intToWord(num % b)

    if (num % t == 0): return intToWord(num // t) + ' trillion'
    else: return intToWord(num // t) + ' trillion ' + intToWord(num % t)

    raise AssertionError('num is too large: %s' % str(num))

    
def removePunctuation(lines):
    captions = ' '.join([line.rstrip('\n') for line in lines])
    ascii_captions = ''.join(s for s in captions if s in string.printable)
    ascii_captions = ascii_captions.lower()
    captions = re.sub(',|\?|\.|!|:|;|\*', ' ', ascii_captions)
    captions = re.sub('&quot|&amp', ' ', captions)
    captions = re.sub('\[.?[^\]]*\]', ' ', captions)
    captions = re.sub('\(.?[^\)]*\)', ' ', captions)
    captions = re.sub('<[^>]*>', ' ', captions)
    captions = re.sub("won't", 'will not', captions)
    captions = re.sub("i'll", 'i will', captions)
    captions = re.sub("'ll", ' will', captions)
    captions = re.sub("can't", "can not", captions)
    captions = re.sub("n't", ' not', captions)
    captions = re.sub("i'm", 'i am', captions)
    captions = re.sub("'re", ' are', captions)
    captions = re.sub("'ve", ' have', captions)
    captions = re.sub("'d", ' would', captions)
    captions = re.sub("'s", ' is', captions)
    captions = re.sub("'cause", 'because', captions)
    captions = re.sub("'till", 'until', captions)
    captions = re.sub('--|- |[ ]-|"|[ ]\'|\'[ ]', ' ', captions)
    captions = ' '.join(captions.split())
    return captions


def getTimes(lines):
    new_lines = []
    dates = []
    for line in lines:
        if re.search('\d\d:\d\d:\d\d,\d\d\d', line):
            date = re.findall('\d\d:\d\d:\d\d', line)
            dates.append(date)
            continue
        else:
            new_lines.append(line)
    start_time = datetime.strptime(str(dates[0][0]), '%H:%M:%S')
    end_time = datetime.strptime(str(dates[-1][1]), '%H:%M:%S')
    time = end_time - start_time
    return new_lines, time


def leading_zeros(value, digits=2):
    value = "000000" + str(value)
    return value[-digits:]


def convert_time(raw_time):
    ms = leading_zeros(int(raw_time[:-4]) % 1000, 3)
    time_in_seconds = int(raw_time[:-7]) if len(raw_time) > 7 else 0
    second = leading_zeros(time_in_seconds % 60)
    minute = leading_zeros(int(floor(time_in_seconds / 60)) % 60)
    hour = leading_zeros(int(floor(time_in_seconds / 3600)))
    return "{}:{}:{}".format(hour, minute, second)


def getTimesXML(lines):
    p = lines
    try:
        starttime = re.search('in="(\d+)t', p[0]).group(1)
        start_time = datetime.strptime(convert_time(starttime), '%H:%M:%S')
    except AttributeError:
        starttime = re.search('in="(.*)\.\d{3}" ', p[0]).group(1)
        start_time = datetime.strptime(starttime, '%H:%M:%S')
    try:
        endtime = re.search('nd="(\d+)t', p[-1]).group(1)
        end_time = datetime.strptime(convert_time(endtime), '%H:%M:%S')
    except AttributeError:
        endtime = re.search('in="(.*)\.\d{3}" ', p[-1]).group(1)
        end_time = datetime.strptime(endtime, '%H:%M:%S')
    time = end_time - start_time
    return time


def removeEmptyLines(lines):
    new_lines = []
    for line in lines:
        if line == '\n':
            continue
        if re.search('^\d*\n', line):
            continue
        else:
            new_lines.append(line)
    return new_lines


        
    
def convertToTextSRT(paths):
    shows = Counter()
    for path in paths:
        path_components = path.split("\\")
        shows['\\'.join(path_components[:-1])] += 1
        
    for show in shows:
        try:
            os.remove(show + '\\runtimeAll.txt')
        except OSError:
            pass
        try:
            os.remove(show + '\\captionsAll.txt')
        except OSError:
            pass
        
    for path in paths:
        path_components = path.split("\\")
        #subfile_name = path_components[0] + '/' + path_components[1] + '/' + path_components[2] + '/' + path_components[3]
        subfile_name = '\\'.join(path_components[:-1])
        with open(path, encoding='utf8', errors='replace') as f:
            lines = f.readlines()
            new_lines = removeEmptyLines(lines)
            newer_lines, runtime = getTimes(new_lines)
            newest_lines = removePunctuation(newer_lines)
            new = re.sub(r'\d+', lambda x: intToWord(x.group()), newest_lines)
        with open(subfile_name + '\\runtimeAll.txt', 'a') as file:
            file.write(str(runtime) + '\n')
        with open(subfile_name + '\\captionsAll.txt', 'a') as file:
            file.write(new + '\n')
        
        
def convertToTextXML(paths):
    shows = Counter()
    for path in paths:
        path_components = path.split("\\")
        shows['\\'.join(path_components[:-1])] += 1
        
    for show in shows:
        try:
            os.remove(show + '\\runtimeAll.txt')
        except OSError:
            pass
        try:
            os.remove(show + '\\captionsAll.txt')
        except OSError:
            pass
        
    for path in paths:
        path_components = path.split("\\")
        #subfile_name = path_components[0] + '/' + path_components[1] + '/' + path_components[2] + '/' + path_components[3]
        subfile_name = '\\'.join(path_components[:-1])
        with open(path, encoding = 'utf8') as f:
            lines = [line.strip() for line in f]
            p = [line for line in lines if line.startswith('<p') or line.startswith('<tt:p')]
            paragraphs = []
            for line in p:
                try:
                    paragraphs.append(line.encode('latin-1', errors='replace').decode('utf8'))
                except UnicodeDecodeError:
                    print(line)
            captions = [re.sub('<[^>]*>', ' ', paragraph) for paragraph in paragraphs]
            runtime = getTimesXML(paragraphs)
            newest_lines = removePunctuation(captions)
            new = re.sub(r'\d+', lambda x: intToWord(x.group()), newest_lines)
        with open(subfile_name + '\\runtimeAll.txt', 'a') as file:
            file.write(str(runtime) + '\n')
        with open(subfile_name + '\\captionsAll.txt', 'a') as file:
            file.write(new + '\n')
    

    


if __name__ == '__main__':
    
    file_paths_srt = []
    file_paths_xml = []

    for root, dirs, files in os.walk(".\\Analysis"):
        for file in files:
            if file.endswith(".srt"):
                file_paths_srt.append(os.path.join(root, file))
                
    for root, dirs, files in os.walk(".\\Analysis"):
        for file in files:
            if file.endswith(".xml"):
                file_paths_xml.append(os.path.join(root, file))
    
    
    convertToTextSRT(file_paths_srt)
    convertToTextXML(file_paths_xml)
# What is this repo?

This is the code base for analyzing subtitle files to determine which popular children's tv shows are best at aiding literacy and language development

## Which order should the scripts be run?

1. `cleanCaptions.py` - cycles through directory, finds `.srt` and `.xml` files, and extracts caption text and runtime information for further processing

2. `wordCount.py` - counts number of times each word is spoken per episode of each show

3. `uncommonWords.py` - after eliminating words in the top 5000 spoken words in the American English language, it counts the number of times each 'unusual' word is spoken

4. `plotWordCloud.py` - generates Word Cloud plots of 'uncommon' words each TV show frequently speaks

5. `plotWPM.py` - generates bar plots of the WPM for each show compared to other tv shows

6. `plotAvgRuntime.py` - generates bar plots of the WPM for each show compared to other tv shows

7. `plotUniqueWords.py` - generates bar plots comparing the number of unique words introduced per episode and the number of times each new word is repeated per episode compared to the overall show average

8. `plotScatterPlot.py` - generates scatterplots that show WPM vs new words introduced/repeated per episode

9. `rankShows.py` - using a heuristic, the code analyzes the metrics calculated above and determines a ranking of each show

## Directory structure for working code

The directory structure should be set up as follows in order for the code to work:

    ├── cleanCaptions.py
    ├── wordCount.py
    ├── uncommonWords.py
    ├── plotWordCloud.py
    ├── plotWPM.py
    ├── plotAvgRuntime.py
    ├── plotUniqueWords.py
    ├── plotScatterPlot.py
    ├── rankShows.py
    ├── top5000words.txt
    └── Analysis
        └── ShowOne Name
        |   ├── EpisodeOne.srt
        |   ├── EpisodeTwo.srt
        |   |   ...
        |   └── EpisodeFinal.srt
        ├── ShowTwo Name
        |   ├── EpisodeOne.xml
        |   ├── EpisodeTwo.xml
        |   |   ...
        |   └── EpisodeFinal.xml
        |   ...
        |   ...
        └── ShowFinal Name
            ├── EpisodeOne.xml
            ├── EpisodeTwo.xml
            |   ...
            └── EpisodeFinal.xml


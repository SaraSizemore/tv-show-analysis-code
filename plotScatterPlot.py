import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('agg')

allShowData = pd.read_csv('.\\show_analysis.csv')


x_all = allShowData['wpm'][:-1]
y_all = allShowData['avg reps'][:-1]

show_titles = allShowData['show'][:-1]

x_avg = allShowData['wpm'][-1:]
y_avg = allShowData['avg reps'][-1:]

for i in range(len(x_all)):
    x_d = x_all[i]
    y_d = y_all[i]
    x = x_all.drop(index=i)
    y = y_all.drop(index=i)

    plt.rcdefaults()
    fig, ax = plt.subplots(dpi=144)

    ax.scatter(x, y, c="cornflowerblue", s=150, marker='o')
    ax.scatter(x_avg, y_avg, c="lightgreen", s=150, marker='^')
    ax.scatter(x_d, y_d, c="salmon", s=150, marker='s')

    ax.set_xlabel('Words Per Minute')
    ax.set_ylabel('# Times New Words Repeated')
    ax.set_title('Word Repetition Per Episode vs WPM')
    ax.set_facecolor("whitesmoke")

    plt.savefig('.\\Analysis\\FigFolder\\' +
                show_titles[i] + '_scatter.png', bbox_inches='tight')

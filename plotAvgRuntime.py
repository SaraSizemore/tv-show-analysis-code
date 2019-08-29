import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib
matplotlib.use('agg')

file_paths = []

for root, dirs, files in os.walk(".\\Analysis"):
    for file in files:
        if file.endswith("runtimeAll.txt"):
            file_paths.append(root)


def runtime(runtimes):
    runtime = 0.0
    len(runtimes)
    for time in runtimes:
        strtime = time.split(":")
        hours = int(strtime[0])
        minutes = int(strtime[1])
        seconds = int(strtime[2])
        runtime = runtime + hours*60 + minutes + seconds/60
    return runtime


runtimes = dict()

for path in file_paths:
    path_components = path.split('\\')
    with open(path + '\\runtimeAll.txt', encoding='utf8', errors='replace') as f:
        times = []
        times.append(f.readline().strip('\n'))
        avg_time = runtime(times)
    runtimes[path_components[-1]] = avg_time


main_path = '\\'.join(path_components[:-1]) + '\\'


runtime_data = pd.DataFrame(list(runtimes.items()),
                            columns=['show', 'avg runtime'])

runtime_data[["avg runtime"]] = runtime_data[[
    "avg runtime"]].apply(pd.to_numeric)

runtime_df = runtime_data.sort_values(by=['avg runtime'], ascending=False)

shows = runtime_df['show']

colors = []
for i in range(len(shows)):
    colors.append(["cornflowerblue"] * len(shows))
    colors[i][i] = "salmon"

y_pos = np.arange(len(shows))
runtime = runtime_df['avg runtime']


for i in range(len(colors)):
    plt.rcdefaults()
    fig, ax = plt.subplots(dpi=144)

    zoom = 1.2
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * zoom, h * zoom**3)

    ax.barh(y_pos, runtime, align='center', color=colors[i])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(runtime_df['show'])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Runtime (Minutes)')
    ax.set_title('Average Runtime Per Episode')

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    rects = ax.patches

    # For each bar: Place a label
    for rect in rects:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = +0.1 * x_value + 20
        # Vertical alignment for positive values
        ha = 'right'

        # If value of bar is negative: Place label left of bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label at right
            ha = 'left'

        # Use X value as label and format number with one decimal place
        label = "{:.1f}".format(x_value)

        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(space, 0),          # Horizontally shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            va='center',                # Vertically center label
            ha=ha)                      # Horizontally align label differently for

    plt.autoscale(tight=True)
    plt.savefig(main_path + '/FigFolder/' +
                shows.iloc[i] + '_Runtime.png', bbox_inches='tight')

plt.close('all')


mean = runtime_df['avg runtime'].mean()

row = ['Average', mean]

runtime_df.loc[len(runtime_df)] = row

if os.path.exists('show_analysis.csv'):
    allShowData = pd.read_csv('show_analysis.csv')
    allShowData = pd.merge(allShowData, runtime_df, on='show')
else:
    allShowData = runtime_df


allShowData.to_csv('show_analysis.csv', index=False)

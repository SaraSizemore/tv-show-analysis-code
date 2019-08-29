import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib
matplotlib.use('agg')

file_paths = []

for root, dirs, files in os.walk(".\\Analysis"):
    for file in files:
        if file.endswith("WordCount.txt"):
            file_paths.append(root)

wpm = dict()

for path in file_paths:
    path_components = path.split('\\')
    with open(path + '\\WordCount.txt', encoding='utf8', errors='replace') as f:
        _ = f.readline()
        wpm[path_components[-1]] = f.readline().strip('\n')


#path_components = file_paths[0].split('/')
main_path = '\\'.join(path_components[:-1]) + '\\'

if not os.path.exists(main_path + 'FigFolder'):
    os.mkdir(main_path + 'FigFolder')


wpm_data = pd.DataFrame(list(wpm.items()), columns=['show', 'wpm'])

wpm_data[["wpm"]] = wpm_data[["wpm"]].apply(pd.to_numeric)

wpm_df = wpm_data.sort_values(by=['wpm'], ascending=False)

mean = wpm_df['wpm'].mean()


shows = wpm_df['show']

colors = []
for i in range(len(shows)):
    colors.append(["cornflowerblue"] * len(shows))
    colors[i][i] = "salmon"

y_pos = np.arange(len(shows))
wpm = wpm_df['wpm']


for i in range(len(colors)):
    plt.rcdefaults()
    fig, ax = plt.subplots(dpi=144)

    zoom = 1.2
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * zoom, h * zoom**3)

    ax.barh(y_pos, wpm, align='center', color=colors[i])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(wpm_df['show'])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Words Per Minute')
    ax.set_title('Average WPM Per Episode')

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
        space = -0.07 * x_value - 20
        # Vertical alignment for positive values
        ha = 'left'

        # If value of bar is negative: Place label left of bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label at right
            ha = 'right'

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
                shows.iloc[i] + '_WPM.png', bbox_inches='tight')

plt.close('all')


row = ['Average', mean]

wpm_df.loc[len(wpm_df)] = row

if os.path.exists('show_analysis.csv'):
    allShowData = pd.read_csv('show_analysis.csv')
    allShowData = allShowData.join(wpm_df.set_index('show'))
else:
    allShowData = wpm_df


allShowData.to_csv('show_analysis.csv', index=False)

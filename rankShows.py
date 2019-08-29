import pandas as pd
import numpy as np

allShowData = pd.read_csv('.\\show_analysis.csv').set_index('show')

show_avg = allShowData.loc['Average']

allShowData['rating'] = allShowData.apply(
    lambda row: 0.6*(row['wpm']/show_avg['wpm']) + 0.4*((row['avg reps']/show_avg['avg reps'])), axis=1)

allShowData['rank'] = allShowData['rating'][:-1].rank(ascending=False)

allShowData['provider'] = ['Amazon Prime', 'Amazon Prime', 'Netflix', 'Amazon Prime', 'Netflix', 'Netflix', 'Netflix', 'Amazon Prime', 'Netflix', 'Netflix', 'Amazon Prime', 'Amazon Prime', 'Amazon Prime', 'Amazon Prime', 'YouTube', 'Netflix', 'Netflix', 'Netflix',
                           'Amazon Prime', 'Netflix', 'Netflix', 'Amazon Prime', 'Netflix', 'Netflix', 'Amazon Prime', 'Amazon Prime', 'Netflix', 'Amazon Prime', 'Amazon Prime', 'Netflix', 'Netflix', 'Amazon Prime', 'Amazon Prime', 'Netflix', 'Amazon Prime', 'Netflix', 'Netflix', 'Amazon Prime', np.nan]

allShowData['provider rank'] = allShowData.groupby(
    ['provider'])['rating'].rank(ascending=False)

allShowData.to_csv('show_analysis.csv)

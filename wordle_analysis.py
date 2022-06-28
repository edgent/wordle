'''
Analysis to do
- Most common letters
- Words containing the most common letters
- Most common word endings/parts/starts
- Has wordle got harder over time? (analysis of word frequency + number of auto-guesses required, especially for "hardest words")
- do plurals ever occur in wordle?
- do they under-index on words with double letters (e.g. "pill"?)
- can we scrape results from people online and show what tends to make rounds difficult?
'''

import wordle_data
import pandas as pd
import numpy as np
from importlib import reload 
import guesser
import game
import random

# importing data
history = pd.read_csv('wordle_answer_history.csv',index_col='No.').sort_index() # https://game8.co/games/Wordle/archives/369779
history.columns = [x.lower() for x in history.columns]
history.date = history.date.apply(pd.to_datetime)

# adding word frequency score
word_frequency = wordle_data.import_wordle_data()
history = history.merge(word_frequency[['word_frequency_rank']],left_on='answer',right_index=True) # adding word frequency score
history.word_frequency_rank = history.word_frequency_rank.apply(lambda x: np.round(x,1))


history[['date','word_frequency_rank']].plot()

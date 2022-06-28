'''
To do (Game class)
- auto-generate yellow set from the yellow history list
- word stuff:
  - remove proper nouns and punctuation from word list
  - work out what words are missing (e.g. "fewer", "lowly") and work out how to add
- create/update stats dictionary for every guess (e.g. max letter frequency score, stdev)
- handle exception when no options appear to exist
- [ML approach] make a dumb random guessing method, use this to build a dataset and capture all the dimensions relating to the choice that could feed a model (e.g. number of possible choices with that ending, number of letters known so far, guess number)


'''

import wordle_data
import pandas as pd
import numpy as np
from importlib import reload 
import guesser
import game
import random

### example of using the classes
reload(game)
reload(guesser)
wordle = game.Game('apron')
ed.generate_first_guess(n_top_letter_frequency_scores=50)
wordle.autoplay_single_round()
wordle.guesses 
wordle.guess_count 
wordle.letter_lists
ed.generate_enriched_options(wordle.letter_lists).sort_values(by=['middle_3_letter_frequency','unattempted_letters_frequency_score'],ascending=[False, False])
ed.generate_guess(letter_list_dictionary = wordle.letter_lists, method='letter_frequency', sample_n=1)
wordle.submit_guess('froth')
wordle.autoplay_whole_game()



### for playing manually
manual_game = {
    'green': {0: 'b', 1: 'r', 2: 'i', 3: 'n', 4: ''}, 
    'yellow': set(''), 
    'yellow_position_history': {0:[''],1:['i'],2:['n'],3:['i'],4:['']}, 
    'grey': set('asletocg')
    }
manual_game
ed.generate_first_guess()

ed.generate_enriched_options(manual_game).sort_values(by=['last_2_letter_frequency','unattempted_letters_frequency_score'],ascending=[False,False]).sort_values(by='last_3_letter_frequency',ascending=False)[:30]
ed.generate_guess(letter_list_dictionary = manual_game, method='letter_frequency', sample_n=1)

### pulling stats to help inform decision strategy
def reload_stats_df():
    cols = list(ed.generate_enriched_options(wordle.letter_lists).iloc[:,-4:].columns)
    std_cols = [x+'_std' for x in cols]
    max_cols = [x+'_max' for x in cols]
    stats_df = pd.DataFrame(columns=(std_cols + max_cols + ['count_options']))

def update_stats_df():
    stats_df.loc[wordle.current_round] = np.nan
    stats_df.loc[wordle.current_round,std_cols] = np.std(ed.generate_enriched_options(wordle.letter_lists)[cols],axis=0).values
    stats_df.loc[wordle.current_round][max_cols] = np.max(ed.generate_enriched_options(wordle.letter_lists)[cols],axis=0).values
    stats_df.loc[wordle.current_round]['count_options'] = len(ed.generate_options(wordle.letter_lists))

reload_stats_df()

update_stats_df()
stats_df.transpose()

reload(game)
wordle = game.Game(random.choice(['point','graze','faint','scour','bring','sting','upend']))

reload(guesser)
ed = guesser.Guesser()

update_stats_df()
stats_df.transpose()
wordle.submit_guess('solon')
update_stats_df()
wordle.submit_guess('irony')
update_stats_df()
wordle.submit_guess('grind')
update_stats_df()
wordle.submit_guess('bring')

stats_df.transpose()
ed.generate_enriched_options(wordle.letter_lists).sort_values(by=['unattempted_letters_frequency_score','unattempted_letters_frequency_score'],ascending=[False,False])
ed.generate_guess(wordle.letter_lists,method='word_frequency_rank')


dimensions = ['unattempted_letters','word_frequency_rank','count_unattempted_letters', 'last_2_letter_frequency', 'last_3_letter_frequency', 'middle_3_letter_frequency', 'unattempted_letters_frequency_score']
df = ed.generate_enriched_options(wordle.letter_lists)[dimensions].sort_values(by=['unattempted_letters_frequency_score','unattempted_letters_frequency_score'],ascending=[False,False]) # unattempted_letters_frequency_score
wordle.letter_lists
# first guess
df.loc[df['unattempted_letters_frequency_score']>0.35].sort_values(by='last_2_letter_frequency',ascending=False)[:50].sample(1).index[0]
# 2nd guess
df.sort_values(by=['last_2_letter_frequency','unattempted_letters_frequency_score'],ascending=[False,False])[dimensions][:20]
# 3rd guess
df.sort_values(by=['middle_3_letter_frequency','unattempted_letters_frequency_score'],ascending=[False,False])[dimensions][:20]

df.sort_values(by='last_2_letter_frequency',ascending=False)[:30]
df.loc[df['unattempted_letters_frequency_score']>0.34].sort_values(by='middle_3_letter_frequency',ascending=False)[:30]



### old attempt to work out "best starting words" - should re-visit this
# approach: for a random word, try 100 random starting words and see how many turns it takes to solve the game
results_df = pd.DataFrame(columns=['starting_word','answer','game_lost','guess_count'])

results_df.loc[0] = {
'starting_word':'tease',
'answer':'apple',
'game_lost':True,
'guess_count':5
}

results_df


data = wordle_data.import_wordle_data()
answers_list = list(data.sample(100,random_state=0).index)
starting_word_list = list(data.sort_values(by='letter_frequency_score',ascending=False).index[:50])
worst_10_words = list(data.sort_values(by='letter_frequency_score',ascending=True).index[:10])
starting_word_list = worst_10_words

i = 0
results = {}
for word in starting_word_list:
    for answer in answers_list:
        try:
            game = Game(answer)
            game.submit_guess(word)
            game.autoplay_whole_game()
            if game.game_won:
                guess_count = game.guess_count 
            else:
                guess_count = None
            results[i] = {
                'starting_word':word,
                'answer':answer,
                'game_lost':game.game_lost,
                'guess_count':guess_count
            }
            i += 1
        except:
            continue 

worst_word_results_df = pd.DataFrame.from_dict(results,orient='index')
worst_word_results_df
worst_word_results_df[['starting_word','guess_count']].groupby('starting_word').mean().sort_values(by='guess_count',ascending=True)

results_df = pd.DataFrame.from_dict(results,orient='index')
# results_df['guess_count'] = np.where(results_df['game_lost']==True,None,results_df['guess_count'])
results_df
scores = results_df[['starting_word','guess_count']].groupby('starting_word').mean().sort_values(by='guess_count',ascending=True)
results_df[['starting_word','game_lost']].groupby('starting_word').sum().sort_values(by='game_lost',ascending=False)
pd.concat([scores.guess_count[:10],scores.guess_count[-10:]])

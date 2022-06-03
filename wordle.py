'''
To do (Game class)
- make guesses when answer not known (might mean moving parts of evaluate_guess into submit_guess)
- handle exception when no options appear to exist
- make it work for double letters (e.g. abbey) https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
- calculate potential information value based on the other options in the list (i.e. what letter applies to most of them)
- improve guessing algorithm
  - [ML approach] make a dumb random guessing method, use this to build a dataset and capture all the dimensions relating to the choice that could feed a model (e.g. number of possible choices with that ending, number of letters known so far, guess number)

To do (old method)
- only make suggestions that work with the position of the greens/yellows
- method to work out the best guess (e.g. what will rule out the most alternatives/get the most matches - start with letter frequency)
- [long run] machine learning approach to selecting words (run model on "real questions" with different decision making frameworks, metric=turns to correct answer)

Analysis to do
- Most common letters
- Words containing the most common letters
- Most common word endings/parts/starts
- Has wordle got harder over time? (analysis of frequency)
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

# Guesser = guesser.Guesser
# Game = game.Game

reload(game)
reload(guesser)

manual_game = {
    'green': {0: 'p', 1: '', 2: '', 3: 's', 4: 'e'}, 
    'yellow': set('a'), 
    'yellow_position_history': {0:['a'],1:['a']}, 
    'grey': set('nir')
    }

wordle = game.Game('phase')
ed = guesser.Guesser()
wordle.submit_guess('anise')
ed.generate_options(wordle.letter_lists)[['word_frequency_rank','letter_frequency_score']]
wordle.guesses
wordle.letter_lists


wordlist = pd.Series(ed.generate_options(wordle.letter_lists).index,name='wordlist')
word_df = pd.DataFrame(index=ed.generate_options(wordle.letter_lists).index)
word_df['last_2_letters'] = wordlist.apply(lambda x: x[-2:]).values
word_df['last_3_letters'] = wordlist.apply(lambda x: x[-3:]).values
word_df['middle_3_letters'] = wordlist.apply(lambda x: x[1:4]).values

word_df['last_2_letter_frequency'] = word_df[['last_2_letters']].merge(word_df['last_2_letters'].value_counts(normalize=True),left_on='last_2_letters',right_index=True).iloc[:,2]
word_df['last_3_letter_frequency'] = word_df[['last_3_letters']].merge(word_df['last_3_letters'].value_counts(normalize=True),left_on='last_3_letters',right_index=True).iloc[:,2]
word_df['middle_3_letter_frequency'] = word_df[['middle_3_letters']].merge(word_df['middle_3_letters'].value_counts(normalize=True),left_on='middle_3_letters',right_index=True).iloc[:,2]

# find most common letters from available words (excluding green/yellow)
set('apple').difference('tease')
set('phase').difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow'])))
word_df['letters_not_green_or_yellow'] = wordlist.apply(lambda x: set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow'])))).values
word_df['count_letters_not_green_or_yellow'] = wordlist.apply(lambda x: len(set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow']))))).values
## PICK UP FROM HERE - write method in Guesser to do this stuff automatically
letter_freqs = pd.Series(
    [item for set in list(wordlist.apply(lambda x: set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow']))))) \
        for item in set]
).value_counts(normalize=True).to_dict()

def get_letter_frequency_scores(set,dic):
    return sum([dic[x] for x in set])

word_df['new_letters_frequency_score'] = word_df['letters_not_green_or_yellow'].apply(lambda x: get_letter_frequency_scores(x,letter_freqs))
word_df

## some options
# - find the most common word patterns / endings 
# - find the word containing letters that occur most frequently after excluding yellows and greens
b = wordlist.apply(lambda x: x[-3:]).value_counts(normalize=True)
wordlist.merge(b,)


# for a random word, try 100 random starting words and see how many turns it takes to solve the game

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


ed = Guesser()
ed.generate_first_guess(500)


        
game = Game('shank')
game.submit_guess('parks')
game.letter_lists
game.guesses 


game.autoplay_single_round(Guesser)
game.autoplay_whole_game(Guesser)
game.guesses
game.game_won
game.guess_count
game.current_round





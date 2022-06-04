'''
To do (Game class)
- 
- handle exception when no options appear to exist
- make it work for double letters (e.g. abbey) https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
  - guessing "occur" when the answer is "scour" puts the 2nd "c" on the yellow list 
  - guessing 'lease' when the answer is 'phase' currently evaluates that the first 'e' is somewhere else in the answer - but the 2nd e takes that slot
- remove proper nouns from word list
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


ans = 'enter'
guess = 'hench'
greens = wordle.letter_lists['green']
yellows = 
[green[x for x in greens if greens[x] == ''] # unguessed greens

# Check your answer for greens & produce "answer - greens"
# Run through remaining guess letters - if you hit a yellow, update "answer - greens - yellows"
# 

guess[2]
ans[2]



for i,letter in enumerate(ans):
    print(i,letter)
    greens[i]



# is the letter i guessed in the list of correct unguessed letters?


import wordle_data
import pandas as pd
import numpy as np
from importlib import reload 
import guesser
import game
import random

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

### attempting to codify logic
## answer = "Phase"
# 1. first attempt is just about getting information - go for high frequency score coupled with common 2 letter ending --> hater
# 2. that gets us down to 48 options. 15% of these have the same 2-letter ending, which contains a letter that hasn't been tried.
#    ** to do ** add logic to check if last N letters contain unattempted letters 
#    take the most common 2 ending and the one within that with the highest letter frequency score --> lease
# 3. this narrows it down to just 2 options: chase and phase. Phase has a higher word frequency, so go with it?

# answer = "Caulk"
# 1. went with "alien"
# 2. down to 166 options (95% eliminated). 14% have the same last 2 letters, and royal has both the highest unattempted letter
#    frequency and the highest word frequency rank --> "royal"
# 3. down to 42 options (75% eliminated). 12% have the same middle 3 letters (and the same last 2 letters). This is 
#    exceptionally high, so go with this. "Paula" has the highest letter frequency score, but it's a proper noun.
#    "fault" has the highest word frequency, but "sault" has highest letter frequency score --> "sault"
#    ** implicit decision ** 42 options where there are still lots of different word structures is too risky to guess at a "common word" (is "common word" even a good strategy?)
# 4. down to 2 options (95% eliminated): "paula" is one of the options, ignore as it's a proper noun --> "caulk"

# answer = ?
# 1. randomly guessed "clear"
# 2. down to 3 options!! (scour, incur, occur). occur is most common and if we get it wrong we will still know what the right answer is.
# 

# prep to get stats about each guess attempt
cols = list(ed.generate_enriched_options(wordle.letter_lists).iloc[:,-4:].columns)
std_cols = [x+'_std' for x in cols]
max_cols = [x+'_max' for x in cols]
stats_df = pd.DataFrame(columns=(std_cols + max_cols + ['count_options']))


def update_stats_df():
    stats_df.loc[wordle.current_round] = np.nan
    stats_df.loc[wordle.current_round,std_cols] = np.std(ed.generate_enriched_options(wordle.letter_lists)[cols],axis=0).values
    stats_df.loc[wordle.current_round][max_cols] = np.max(ed.generate_enriched_options(wordle.letter_lists)[cols],axis=0).values
    stats_df.loc[wordle.current_round]['count_options'] = len(ed.generate_options(wordle.letter_lists))

update_stats_df()
stats_df.transpose()

random.choice(['point','graze','faint','scour','bring','sting','upend'])

wordle = game.Game(random.choice(['point','graze','faint','scour','bring','sting','upend']))
ed = guesser.Guesser()
wordle.letter_lists
wordle.guesses
wordle.submit_guess('clear')
update_stats_df()
wordle.submit_guess('occur')
update_stats_df()
wordle.submit_guess('')
update_stats_df()

stats_df.transpose()
ed.generate_enriched_options(wordle.letter_lists)

dimensions = ['unattempted_letters','word_frequency_rank','count_unattempted_letters', 'last_2_letter_frequency', 'last_3_letter_frequency', 'middle_3_letter_frequency', 'unattempted_letters_frequency_score']
df = ed.generate_enriched_options(wordle.letter_lists)[dimensions].sort_values(by='unattempted_letters_frequency_score',ascending=False) # unattempted_letters_frequency_score
wordle.letter_lists
# first guess
df.loc[df['unattempted_letters_frequency_score']>0.35].sort_values(by='last_2_letter_frequency',ascending=False)[:50].sample(1).index[0]
# 2nd guess
df.sort_values(by=['last_2_letter_frequency','unattempted_letters_frequency_score'],ascending=[False,False])[dimensions][:20]
# 3rd guess
df.sort_values(by=['middle_3_letter_frequency','unattempted_letters_frequency_score'],ascending=[False,False])[dimensions][:20]

df.sort_values(by='last_2_letter_frequency',ascending=False)[:30]
df.loc[df['unattempted_letters_frequency_score']>0.34].sort_values(by='middle_3_letter_frequency',ascending=False)[:30]



df = ed.generate_enriched_options(wordle.letter_lists)
df[['last_2_letters']].merge(pd.DataFrame(df['last_2_letters'].value_counts(normalize=True)),left_on='last_2_letters',right_index=True).iloc[:,2]

wordle.guesses
wordle.letter_lists


wordlist = pd.Series(ed.generate_options(wordle.letter_lists).index,name='wordlist')
ed.generate_options(wordle.letter_lists)[['word_frequency_rank']].merge()

pd.DataFrame(index=wordlist)
word_df = pd.DataFrame(index=ed.generate_options(wordle.letter_lists).index)
word_df['last_2_letters'] = wordlist.apply(lambda x: x[-2:]).values
word_df['last_3_letters'] = wordlist.apply(lambda x: x[-3:]).values
word_df['middle_3_letters'] = wordlist.apply(lambda x: x[1:4]).values

word_df['last_2_letter_frequency'] = word_df[['last_2_letters']].merge(word_df['last_2_letters'].value_counts(normalize=True),left_on='last_2_letters',right_index=True).iloc[:,2]
word_df['last_3_letter_frequency'] = word_df[['last_3_letters']].merge(word_df['last_3_letters'].value_counts(normalize=True),left_on='last_3_letters',right_index=True).iloc[:,2]
word_df['middle_3_letter_frequency'] = word_df[['middle_3_letters']].merge(word_df['middle_3_letters'].value_counts(normalize=True),left_on='middle_3_letters',right_index=True).iloc[:,2]

# find most common letters from available words (excluding green/yellow)


word_df['letters_not_green_or_yellow'] = wordlist.apply(lambda x: set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow'])))).values
word_df['count_letters_not_green_or_yellow'] = wordlist.apply(lambda x: len(set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow']))))).values
## PICK UP FROM HERE - write method in Guesser to do this stuff automatically
letter_freqs = pd.Series(
    [item for set in list(wordlist.apply(lambda x: set(x).difference(set(list(wordle.letter_lists['green'].values()) + list(wordle.letter_lists['yellow']))))) \
        for item in set]
).value_counts(normalize=True).to_dict()
word_df['letters_not_green_or_yellow'].apply(lambda x: sum([letter_freqs[letter] for letter in x]))
[x for x in set('apple')]
def get_letter_frequency_scores(set,dic):
    return sum([dic[x] for x in set])

word_df['new_letters_frequency_score'] = word_df['letters_not_green_or_yellow'].apply(lambda x: get_letter_frequency_scores(x,letter_freqs))
word_df
pd.set_option('display.max_columns',100)

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





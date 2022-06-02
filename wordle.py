'''
To do (Game class)
- handle exception when no options appear to exist
- work out how to only make guesses where yellows haven't been guessed before
- make it work for double letters (e.g. abbey) https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
- calculate potential information value based on the other options in the list (i.e. what letter applies to most of them)

To do (old method)
- only make suggestions that work with the position of the greens/yellows
- method to work out the best guess (e.g. what will rule out the most alternatives/get the most matches - start with letter frequency)
- [long run] machine learning approach to selecting words (run model on "real questions" with different decision making frameworks, metric=turns to correct answer)

Analysis to do
- Most common letters
- Words containing the most common letters
- Most common word endings/parts/starts
- Has wordle got harder over time? (analysis of frequency)
- do plurals ever occur?
- do they under-index on words with double letters (e.g. "pill"?)
- can we scrape results from people online and show what tends to make rounds difficult?
'''





from guesser import Guesser
from game import Game
import wordle_data
import pandas as pd
import numpy as np
# from importlib import reload


game = Game('apple')
game.autoplay_whole_game()
game.guess_count
game.autoplay_single_round()



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


results_df = pd.DataFrame.from_dict(results,orient='index')
# results_df['guess_count'] = np.where(results_df['game_lost']==True,None,results_df['guess_count'])
results_df
results_df[['starting_word','guess_count']].groupby('starting_word').mean().sort_values(by='guess_count',ascending=True)
results_df.pivot_table(columns=['starting_word','guess_count'],aggfunc=np.mean,)


ed = Guesser()
ed.generate_first_guess(500)


        
game = Game('shank')
game.submit_guess('shark')
game.autoplay_single_round(Guesser)
game.autoplay_whole_game(Guesser)
game.guesses
game.game_won
game.guess_count
game.current_round





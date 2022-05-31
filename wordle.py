'''
To do (Game class)
- write function & methods for the Game class to generate the best guess after the initial one
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



import pandas as pd
import numpy as np
from sklearn.utils import column_or_1d
from wordfreq import word_frequency, top_n_list
import scipy.stats as stats





## data prep
def import_wordle_data():
    df = pd.read_csv('wordle_data',index_col=0)
    return df.rename(columns={str(x):x for x in range(5)})



df = import_wordle_data()
df
df.sort_values(by='letter_frequency_score',ascending=False).iloc[:20,:]


## algorithm
def generate_options_df(game):
    '''
    parameter `game` is a dictionary comprising a green_list (list), yellow_list (string) and grey_list (string) of letters
    '''
    green_list = game['green_list']
    yellow_list = game['yellow_list']
    grey_list = game['grey_list']

    for n, letter in enumerate(green_list):
        print(n, letter)
        if n == 0: # if this is the first iteration step, make a copy of the main dataframe
            df_filtered = df.copy() # df is the wordle_data dataframe imported
        if letter == '': # if no direct matching green letter, check if it matches the yellow letter list
            # for each word in the list, check if it contains a grey letter. Mark if it does and prepare to drop.
            df_filtered['grey_match_'+str(n+1)] = df_filtered[n+1].apply(lambda x: x in grey_list)
            # for each word in the list, check if it contains a yellow letter.
            df_filtered['yellow_match_'+str(n+1)] = df_filtered[n+1].apply(lambda x: x in yellow_list) # make a new column to flag these matches
            continue 
        df_filtered = df_filtered.loc[df[n+1]==letter].copy() # filter the word list for just ones that match the greenlist
        # print(df_filtered.shape)


    # get list of column names where we can identify yellow matches and exclude grey options
    match_cols_yellow = [x for (x) in df_filtered.columns if 'yellow_match' in str(x)] # what if yellow list is empty?
    match_cols_grey = [x for (x) in df_filtered.columns if 'grey_match' in str(x)]

    # exclude options that contain no yellow letters (if we have them) and exclude options that contain grey letters
    if len(yellow_list) > 0:
        options_df = df_filtered.loc[df_filtered[match_cols_yellow].any(axis=1)].copy()
    else:
        options_df = df_filtered.copy()

    options_df = options_df.loc[~df_filtered[match_cols_grey].any(axis=1)].copy() # exclude options that contain grey letters
    return options_df


# generate_options_df().sort_values(by='frequency_ranks',ascending=False)

# summarising the options
def get_options_list(game):
    options_df = generate_options_df(game)
    return list(options_df.sort_values(by='frequency_ranks',ascending=False).index)

def print_outlook(game):
    print(f'There are {len(get_options_list(game))} possible words remaining out of {len(words_len5)} 5-letter-words in the English Language.')


def print_options(game):
    print(f'The 5 most common options you have are {get_options_list(game)[:5]}')



# playing zone
game = {
    'green_list':['','','','',''],
    'yellow_list':list('ora'),
    'grey_list':list('')
}

print_outlook(game)
print_options(game)

## Working out a game object / decision engine
def generate_first_guess(n_top_letter_frequency_scores=20):
    '''
    Picks a random starting word from the top N of 5 letter words, ordered by the frequency with which the set of their letters occur in 5 letter words
    '''
    df = import_wordle_data().sort_values(by='letter_frequency_score',ascending=False).iloc[:n_top_letter_frequency_scores,:]
    return df.sample(1).index[0]

generate_first_guess(n_top_letter_frequency_scores=20)


#test
letter_list_dictionary['green']

def generate_guess(letter_list_dictionary):
    df_filtered = import_wordle_data()
    dict = letter_list_dictionary
    green_dict = dict['green']
    grey_list, yellow_list = dict['grey'], dict['yellow']
    print(green_dict, grey_list, yellow_list)
    # need to work out how to exclude yellows in positions that have been guessed before
    # if the answer is 'pears' and i guess 'pump', the first P will go green and the 2nd will go grey. We want to make sure we don't exclude words that contain p.
    for n in green_dict:
        letter = green_dict[n]
        print(n, letter)
        # if key == 0: # if this is the first iteration step, make a copy of the main dataframe
        #     df_filtered = df.copy() # df is the wordle_data dataframe imported
        if letter == '': # if no direct matching green letter, check if it matches the yellow letter list
            # for each word in the list, check if it contains a grey letter. Mark if it does and prepare to drop.
            df_filtered['grey_match_'+str(n)] = df_filtered[n].apply(lambda x: x in grey_list) # 
            # for each word in the list, check if it contains a yellow letter.
            df_filtered['yellow_match_'+str(n)] = df_filtered[n].apply(lambda x: x in yellow_list) # make a new column to flag these matches
            continue 
        df_filtered = df_filtered.loc[df_filtered[n]==letter].copy() # filter the word list for just ones that match the greenlist
        print(df_filtered.shape)

        # get list of column names where we can identify yellow matches and exclude grey options
    match_cols_yellow = [x for (x) in df_filtered.columns if 'yellow_match' in str(x)] # what if yellow list is empty?
    match_cols_grey = [x for (x) in df_filtered.columns if 'grey_match' in str(x)]

    # exclude options that contain fewer yellow letters than we have (if we have them) and exclude options that contain grey letters
    if len(yellow_list) > 0:
        options_df = df_filtered.loc[np.sum(df_filtered[match_cols_yellow],axis=1)>=len(yellow_list)].copy()
    else:
        options_df = df_filtered.copy()

    options_df = options_df.loc[~df_filtered[match_cols_grey].any(axis=1)].copy() # exclude options that contain grey letters
    return options_df

letter_list_dictionary = {
    'green':{0:'m',1:'a',2:'',3:'o',4:'r'},
    'yellow':set(''),
    'yellow_position_history':{'p': [0, 3], 'e': [1, 2]},
    'grey':set('teslj')
}
generate_guess(letter_list_dictionary)[['word_frequency_rank','letter_frequency_score']]

# .sort_values(by='letter_frequency_score',ascending=False)
        

class Game:
    def __init__(self, answer):
        self.answer = answer.lower()
        self.current_round = 1
        self.guess_count = 0
        self.latest_guess = ''
        self.game_won = False
        self.game_lost = False
        self.letter_lists = {
            'green':{x:'' for x in range(5)}, # empty dictionary with keys 1 through 5
            'yellow':set(), # going to be a set
            'yellow_position_history':{},
            'grey':set() # going to be a set
        }
        self.guesses = {x:'' for x in range(5)} # empty dictionary keys 1 to 5 to populate with guesses - effectively the game board

    def evaluate_guess(self, word):
        word = word.lower()
        # - check for exact matches --> update green list, remove any new greens from yellow list
        # - excluding exact matches and yellow letters already guessed, check overlap between guess submitted and answer --> update yellow list
        # - subtract new green and yellow letters from the guess --> update grey letters
        for i in range(len(self.answer)):
            letter = word[i]
            # for an exact match, update green list and remove from yellows if it came from there
            if self.answer[i] == letter:
                print(f'{letter} is a match')
                self.letter_lists['green'][i] = letter
                # if a yellow turns into a green, remove it from the yellow list
                if letter in self.letter_lists['yellow']:
                    self.letter_lists['yellow'].remove(letter)
            # yellow matches
            elif letter in self.answer:
                print(f'{letter} is somewhere else in the answer')
                self.letter_lists['yellow'].add(letter)
                try:
                    self.letter_lists['yellow_position_history'][letter].append(i)
                except:
                    self.letter_lists['yellow_position_history'][letter] = [i]
            
            else:
                print(f'{letter} is not in the answer')
                self.letter_lists['grey'].add(letter)
        
        # checking if the game is won
        if list(self.letter_lists['green'].values()) == list(self.answer):
            self.game_won = True
            print(f'Game won in {self.guess_count} turns!')
        
        # checking if the game is lost
        elif (self.game_won == False) and (self.guess_count >= 5):
            self.game_lost = True
            print('Game over, guess limit reached')

        else:
            print('Guess evaluated')
    
    def submit_guess(self,word):
        word = word.lower()
        self.guesses[self.guess_count]=word
        self.current_round += 1
        self.guess_count += 1
        self.latest_guess = word
        print('Guess submitted')
        self.evaluate_guess(word)
        

g = {x+1:'' for x in range(5)}
g[1], g[3] = 'a','p'
list(g.values()) == list('apple')


game = Game('apple')
game.guesses
game.answer
game.submit_guess('peeps')
game.letter_lists
game.current_round
game.guess_count


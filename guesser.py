from wordle_data import import_wordle_data
import pandas as pd
import numpy as np

'''
To do:
- update generate_guess function to sort by last 2 or 3 letters; middle 3 letters
'''

class Guesser:
    def __init__(self) -> None:
        self.wordle_data = import_wordle_data()

    def generate_empty_letter_list(self):
    # Used for manually playing games of wordle
        return {
            'green':{x:'' for x in range(5)}, # empty dictionary with keys 1 through 5
            'yellow':set(), # going to be a set
            'yellow_position_history':{},
            'grey':set() # going to be a set
        }
    
    def generate_first_guess(self,n_top_letter_frequency_scores=20):
        '''
        Picks a random starting word from the top N of 5 letter words, ordered by the frequency with which the set of their letters occur in 5 letter words
        '''
        df = import_wordle_data().sort_values(by='letter_frequency_score',ascending=False).iloc[:n_top_letter_frequency_scores,:]
        return df.sample(1).index[0]
    
    def generate_options(self,letter_list_dictionary):
        # filters all 5 letter words to just the ones that fit with the previously guessed letters
        df_filtered = self.wordle_data.copy()
        dic = letter_list_dictionary
        green_dic = dic['green']
        grey_list, yellow_list = dic['grey'], dic['yellow']
        print(green_dic, grey_list, yellow_list)
        # need to work out how to exclude yellows in positions that have been guessed before
        # if the answer is 'pears' and i guess 'pump', the first P will go green and the 2nd will go grey. We want to make sure we don't exclude words that contain p.
        
        # 1. For every letter in your guess history, check if it's green.
        # 2. If a green letter exists, then filter the options for just those that match.
        # 3. If not, check if you can exclude because it's grey
        # 4. If not grey, check if you can exclude because it has a previously-guessed yellow
        # 5. If neither, check if it is a yellow match (and therefore should be included)
        # 6. Filter in the greens, filter out the greys and previous yellows, then filter for yellow matches
        for n in green_dic:
            letter = green_dic[n]
            print(n, letter)
            # if key == 0: # if this is the first iteration step, make a copy of the main dataframe
            #     df_filtered = df.copy() # df is the wordle_data dataframe imported
            if letter == '': # if no direct matching green letter, check if it matches the yellow letter list
                # for each word in the list, check if it contains a grey letter. Mark if it does and prepare to drop.
                df_filtered['grey_match_'+str(n)] = df_filtered[n].apply(lambda x: x in grey_list) # 
                # for each word in the list, check if it contains a yellow letter.
                df_filtered['yellow_match_'+str(n)] = df_filtered[n].apply(lambda x: x in yellow_list) # make a new column to flag these matches
                try:
                    df_filtered['yellow_matched_previously_'+str(n)] = df_filtered[n].apply(lambda x: x in dic['yellow_position_history'][n])
                except:
                    continue
            else:
                df_filtered = df_filtered.loc[df_filtered[n]==letter].copy() # filter the word list for just ones that match the greenlist
            
            print(df_filtered.shape)

        # get list of column names where we can identify yellow matches and exclude grey options
        match_cols_yellow = [x for (x) in df_filtered.columns if 'yellow_match' in str(x)] # what if yellow list is empty?
        match_cols_yellow_previously = [x for (x) in df_filtered.columns if 'yellow_matched_previously' in str(x)]
        match_cols_grey = [x for (x) in df_filtered.columns if 'grey_match' in str(x)]

        # exclude options that contain fewer yellow letters than we have (if we have them) and exclude options that contain grey letters
        if len(yellow_list) > 0:
            options_df = df_filtered.loc[np.sum(df_filtered[match_cols_yellow],axis=1)>=len(yellow_list)].copy()
        else:
            options_df = df_filtered.copy()

        # exclude options containing greys or previously-guessed yellows
        options_df = options_df.loc[~df_filtered[match_cols_grey].any(axis=1)].copy() # exclude options that contain grey letters
        options_df = options_df.loc[~df_filtered[match_cols_yellow_previously].any(axis=1)].copy()
        return options_df.sort_values(by='letter_frequency_score',ascending=False)

    def generate_enriched_options(self,letter_list_dictionary):
        options_df = self.generate_options(letter_list_dictionary)
        green_list = letter_list_dictionary['green']
        yellow_list = letter_list_dictionary['yellow']
        wordlist = pd.Series(options_df.index,name='wordlist')
        word_df = options_df[['word_frequency_rank']] # want to include word frequency
        # word_df = pd.DataFrame(index=wordlist)
        word_df['last_2_letters'] = wordlist.apply(lambda x: x[-2:]).values
        word_df['last_3_letters'] = wordlist.apply(lambda x: x[-3:]).values
        word_df['middle_3_letters'] = wordlist.apply(lambda x: x[1:4]).values
        word_df['unattempted_letters'] = wordlist.apply(lambda x: set(x).difference(set(list(green_list.values()) + list(yellow_list)))).values
        # word_df['count_unattempted_letters'] = pd.Series(word_df['unattempted_letters']).apply(lambda x: len(x)).values
        word_df['count_unattempted_letters'] = word_df['unattempted_letters'].apply(lambda x: len(x)).values
        
        word_df['last_2_letter_frequency'] = word_df[['last_2_letters']].merge(pd.DataFrame(word_df['last_2_letters'].value_counts(normalize=True)),left_on='last_2_letters',right_index=True).iloc[:,2]
        word_df['last_3_letter_frequency'] = word_df[['last_3_letters']].merge(pd.DataFrame(word_df['last_3_letters'].value_counts(normalize=True)),left_on='last_3_letters',right_index=True).iloc[:,2]
        word_df['middle_3_letter_frequency'] = word_df[['middle_3_letters']].merge(pd.DataFrame(word_df['middle_3_letters'].value_counts(normalize=True)),left_on='middle_3_letters',right_index=True).iloc[:,2]
        letter_freqs = pd.Series(
            [item for set in list(wordlist.apply(lambda x: set(x).difference(set(list(green_list.values()) + list(yellow_list))))) \
            for item in set]
        ).value_counts(normalize=True).to_dict()
        word_df['unattempted_letters_frequency_score'] = word_df['unattempted_letters'].apply(lambda x: sum([letter_freqs[letter] for letter in x]))
        return word_df

    def generate_guess(self,letter_list_dictionary,method=None,sample_n=1):
        options_df = self.generate_enriched_options(letter_list_dictionary)
        if len(options_df) == 0:
            print('No options found')
            return None
        elif method == 'letter_score':
            if len(options_df) <= 50:
                guess = options_df.sort_values(by='word_frequency_rank',ascending=False)[:sample_n].sample(1).index[0]
            else:
                guess = options_df.sort_values(by='letter_frequency_score',ascending=False)[:sample_n].sample(1).index[0]
            return guess
        elif method == 'letter_frequency':
            return options_df.sort_values(by='unattempted_letters_frequency_score',ascending=False)[:sample_n].sample(1).index[0]
        else:
            return options_df.sort_values(by=[method,'unattempted_letters_frequency_score'],ascending=[False,False])[:sample_n].sample(1).index[0]
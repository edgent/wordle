from wordle_data import import_wordle_data
import pandas as pd
import numpy as np

class Guesser:
    def __init__(self) -> None:
        pass
    
    def generate_first_guess(self,n_top_letter_frequency_scores=20):
            '''
            Picks a random starting word from the top N of 5 letter words, ordered by the frequency with which the set of their letters occur in 5 letter words
            '''
            df = import_wordle_data().sort_values(by='letter_frequency_score',ascending=False).iloc[:n_top_letter_frequency_scores,:]
            return df.sample(1).index[0]


    def generate_options(self,letter_list_dictionary):
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
        return options_df.sort_values(by='letter_frequency_score',ascending=False)

    def generate_guess(self,letter_list_dictionary,method='letter_score'):
        if method == 'letter_score':
            options_df = self.generate_options(letter_list_dictionary)
            guess = options_df.sort_values(by='letter_frequency_score',ascending=False).index[0]
            return guess
        else:
            return None
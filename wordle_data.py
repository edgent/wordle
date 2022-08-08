from wordfreq import word_frequency, top_n_list
import english_words
import pandas as pd
import scipy.stats as stats
import itertools
import numpy as np

# words in the 'english_words' package which shouldn't be used for guesses (generally proper nouns)
not_words = ['solon','somal','paula',"can't",'tracy','sarah','qatar','helen','perez',
'omaha','caleb','colby',"we'll",'damon','draco','stacy','alice',"don't",'benny','tyler']

# words missing from the 'english_words' package (generally from Wordle games where I wasn't able to generate a guess)
missing_words = ['tiara', 'gamer', 'homer', 'heist', 'fewer', 'trope', 'lowly', 'renew',
  'trove', 'humor', 'wrung', 'favor', 'rebus', 'using', 'masse', 'surer', 'finer', 'badly', 
  'fixer', 'duchy', 'pulpy', 'boozy', 'enema', 'jaunt', 'kebab', 'moult', 'labor', 'loopy', 
  'golem', 'goner', 'biome', 'wooer', 'flume', 'unmet', 'repay', 'sower', 'outdo', 'unfed', 
  'floss', 'batty', 'react', 'humph', 'sissy', 'rebut','unfit']

def generate_wordle_data():
    words = english_words.english_words_lower_set
    words_len5 = [word for word in words if len(word) == 5 and word not in not_words] + missing_words
    
    df = pd.DataFrame(columns=[x for x in range(5)]) # 5 columns for each letter in the answer
    for word in words_len5:
        df.loc[word] = list(word)

    words_len5_frequencies = pd.Series(words_len5).apply(lambda x: word_frequency(x,'en'))

    df['word_frequency_rank'] = words_len5_frequencies.apply(lambda x: stats.percentileofscore(words_len5_frequencies,x)).values

    letter_frequency_df = pd.Series(itertools.chain.from_iterable([list(set(x)) for x in df.index]),name='letter_frequency').value_counts()
    letter_frequency_dict = letter_frequency_df.to_dict()
    df['letter_frequency_score'] = np.nan
    for word in df.index:
        score = 0
        for letter in set(word):
            score += letter_frequency_dict[letter]
        df.loc[word,'letter_frequency_score']=score
    return df
    
def save_to_csv(dataframe):
    dataframe.to_csv('wordle_data')

def import_wordle_data():
    df = pd.read_csv('wordle_data',index_col=0)
    return df.rename(columns={str(x):x for x in range(5)})


# list(generate_wordle_data().index)
save_to_csv(generate_wordle_data())
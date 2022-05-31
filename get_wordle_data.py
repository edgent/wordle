from wordfreq import word_frequency, top_n_list
import english_words
import pandas as pd
import scipy.stats as stats
import itertools

def generate_csv():
    words = english_words.english_words_lower_set
    words_len5 = [word for word in words if len(word) == 5]
    
    df = pd.DataFrame(columns=[1,2,3,4,5])
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
    df.to_csv('wordle_data')

generate_csv()
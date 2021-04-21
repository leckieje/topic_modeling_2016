import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords, words
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

# generate stop words
custom_stops = ['https', 'rt', 'co', 'amp', 'via', 'go', 'get', 'said', 'say', 'news', 'new', 'make', 'want', 
                'trump', 'clinton', 'donald', 'donald trump', 'donaldtrump', 'says', 'hillary', 'hillaryclinton',
                'hillary clinton', 'realdonaldtrump', 'would', 'let', 'video', 'like']

# get random samples
def get_random_sample(df, num_samples):
    samp_idx = np.random.choice(range(len(df)), size=num_samples, replace=False)
    df_samp = df.iloc[samp_idx, :]
    return df_samp

# load and split data
def get_data(num_samples=50000, balanced=True, split=True):
    # load data
    legit = pd.read_csv('data/legit_tweets.csv', parse_dates = ['date'])
    troll = pd.read_csv('data/troll_tweets.csv', parse_dates = ['date'])
    legit['legit'] = 1

    # limit troll timeframe
    troll_summer = troll[(troll['date'] >= '2016-06-28') & (troll['date'] <= '2016-11-02')]

    # get samples
    if balanced:
        troll_samp = get_random_sample(troll_summer, int(num_samples/2))
        legit_samp = get_random_sample(legit, int(num_samples/2))
    elif num_samples > 0:
        troll_samp = get_random_sample(troll_summer, int(0.08 * num_samples))
        legit_samp = get_random_sample(legit, int((1 - 0.08) * num_samples))
    else:
        troll_samp = troll_summer
        legit_samp = legit

    # combine legit and troll tweets
    total_tweets = pd.concat([legit_samp.loc[:,['text','legit']], troll_samp.loc[:,['text','legit']]])
    total_tweets.reset_index(drop=True, inplace=True)

    # set X and y, split
    X = total_tweets['text']
    y = total_tweets['legit']

    if split:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y)
        
        return X_train, X_test, y_train, y_test
    
    else:
        return X, y

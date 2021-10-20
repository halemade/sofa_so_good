#preprocessing
import pandas as pd
import os
import json

#function that takes in a string and an ngram length, returns all ngrams
def generate_ngrams(s, n):
    s = str(s)
    tokens = [token for token in list(s) if token != "-"]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]

#function that takes in the list of tokens and counts how many times they occur
def freq_dist(token_list):
    unique_tokens = list(set(token_list))
    freq_dict = {unique_tokens[i]:0 for i in range(len(unique_tokens))}
    for item in token_list:
        for key in freq_dict:
            if item == key:
                freq_dict[key] += 1
    return freq_dict

#function that takes in a df and create columns for the ngrams. this function is written to create the 2/3/4 ngram cols but 
# is currently too computationally expensive need to proceed with just 2 ngrams for now

def add_ngram_cols(df,dfidstring):
    
    with open(dfidstring+"_ngram_2.json", "r") as read_file:
        ngram_2 = json.load(read_file)
        ngram_2 = {k: v for k, v in sorted(ngram_2.items(), key=lambda item: item[1],reverse=True)}
    ngram_2_dict = dict()
    for (key, value) in ngram_2.items():
        if value > 50:
            ngram_2_dict[key] = value

    with open(dfidstring+"_ngram_3.json", "r") as read_file:
        ngram_3 = json.load(read_file)
        ngram_3 = {k: v for k, v in sorted(ngram_3.items(), key=lambda item: item[1],reverse=True)}
    ngram_3_dict = dict()
    for (key, value) in ngram_3.items():
        if value > 50:
            ngram_3_dict[key] = value

    with open(dfidstring+"_ngram_4.json", "r") as read_file:
        ngram_4 = json.load(read_file)
        ngram_4 = {k: v for k, v in sorted(ngram_4.items(), key=lambda item: item[1],reverse=True)}
    ngram_4_dict = dict()
    for (key, value) in ngram_4.items():
        if value > 50:
            ngram_4_dict[key] = value
    
    keys_2 = list(ngram_2_dict.keys())
    keys_3 = list(ngram_3_dict.keys())
    keys_4 = list(ngram_4_dict.keys())
    
    #create a list of series and concat them all
    cat_copy = df['model_name_x']
    ngram_series_2 = []
    ngram_series_3 = []
    ngram_series_4 = []
    
    for key in keys_2:
        ngram_series_2.append(cat_copy.map(lambda x: key in str(x)))
    print('2grams mapped.')
    for key in keys_3:
        ngram_series_3.append(cat_copy.map(lambda x: key in str(x)))
    print('3grams mapped.')
    for key in keys_4:
        ngram_series_4.append(cat_copy.map(lambda x: key in str(x)))
    print('4grams mapped.')
    print(len(ngram_series_2),len(ngram_series_3),len(ngram_series_4))
        
    df_2 = pd.concat(ngram_series_2,axis=1,keys=keys_2)
    print('ngram 2 dataframe made.')
    df_3 = pd.concat(ngram_series_3, axis=1, keys = keys_3)
    print('ngram 3 dataframe made.')
    df_4 = pd.concat(ngram_series_4, axis=1, keys= keys_4)
    print('ngram 4 dataframe made.')
    
    final_df = pd.concat([df,df_2,df_3,df_4],axis=1)
    print('dataframe with ngrams created successfully.')
    return final_df
   
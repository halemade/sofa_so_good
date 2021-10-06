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
    cat_copy = df['piece_category']
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
        
    df_2 = pd.concat(ngram_series_2,axis=1,keys=keys_2)
    print('ngram 2 dataframe made.')
    df_3 = pd.concat(ngram_series_3, axis=1, keys = keys_3)
    print('ngram 3 dataframe made.')
    df_4 = pd.concat(ngram_series_4, axis=1, keys= keys_4)
    print('ngram 4 dataframe made.')
    
    final_df = pd.concat([df,df_2,df_3,df_4],axis=1)
    print('dataframe with ngrams created successfully.')
    return final_df
    
df_labels = ['df1','df2','df3','df4','df5','df6']
for index,df in enumerate(all_dfs):
#create a list of all categories
    cats = list(set(df['piece_category']))
    #create ngrams for all categories
    len_2_long = [generate_ngrams(x,2) for x in cats]
    len_3_long = [generate_ngrams(x,3) for x in cats]
    len_4_long = [generate_ngrams(x,4) for x in cats]
    #flatten lists
    len_2 = [item for sublist in len_2_long for item in sublist]
    len_3 = [item for sublist in len_3_long for item in sublist]
    len_4 = [item for sublist in len_4_long for item in sublist]
    #freq distributions of ngrams
    dict_2 = freq_dist(len_2)
    dict_3 = freq_dist(len_3)
    dict_4 = freq_dist(len_4)
    #write dictionaries to json
    with open(df_labels[index]+'_ngram_2.json', 'w') as fp:
        json.dump(dict_2, fp)
    with open(df_labels[index]+'_ngram_3.json', 'w') as fp:
        json.dump(dict_3, fp)
    with open(df_labels[index]+'_ngram_4.json', 'w') as fp:
        json.dump(dict_4, fp)

this_dir = os.listdir('./')
ngrams = []
for item in this_dir:
    if 'ngram' in item:
        ngrams.append(item)

prog_1 = add_ngram_cols(df1,'df1')
prog_2 = add_ngram_cols(df2,'df2')
prog_3 = add_ngram_cols(df3,'df3')
prog_4 = add_ngram_cols(df4,'df4')
prog_5 = add_ngram_cols(df5,'df5')
prog_6 = add_ngram_cols(df6,'df6')
programs = [prog_1,prog_2,prog_3,prog_4,prog_5,prog_6]
program_labels = ['prog_1','prog_2','prog_3','prog_4','prog_5','prog_6']
for ind,program in enumerate(programs):
    program.to_csv(program_labels[ind]+'.csv')
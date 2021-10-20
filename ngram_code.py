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
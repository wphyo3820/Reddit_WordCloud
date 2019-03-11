import pandas as pd
import numpy as np
import os
import json

def read_json_matrix(root, subreddit):
    result = {}
    for i in ["start", "one", "two"]:
        filepath = os.path.join(root, "data/{}/{}.json".format(i, subreddit))
        with open(filepath) as infile:
            result[i] = json.load(infile)
    return result

def convert_json_matrix(start, one, two):
    start_df = pd.DataFrame(list(start.items()), columns=["word", "count"])
    one_ngram_df = pd.DataFrame(one).fillna(0)
    two_ngram_df = pd.DataFrame(two).fillna(0)
    
    #divide by column sum
    start_df["prob"] = start_df["count"]/start_df["count"].sum(axis=0)
    one_ngram_df = one_ngram_df.divide(one_ngram_df.sum(axis=0))
    two_ngram_df = two_ngram_df.divide(two_ngram_df.sum(axis=0))
    return (start_df, one_ngram_df, two_ngram_df)

def generate_sentence(start_df, one_ngram_df, two_ngram_df, threshold, limit):
    curr = np.random.choice(start_df.word, 1, p=start_df.prob)[0]
    final_sentence = " ".join(curr.split(":"))
    while True:
        if len(final_sentence.split(" ")) == limit:
            break
        poss_vals = two_ngram_df.get(curr)
        if (poss_vals is None) or (len(poss_vals[poss_vals != 0]) <= threshold):
            curr_keyword = curr.split(":")[1]
            if curr_keyword not in list(one_ngram_df):
                break
            next_word = np.random.choice(list(one_ngram_df[curr_keyword].index), 1, p=one_ngram_df[curr_keyword].values)[0]
            final_sentence += " {}".format(next_word)
            curr = "{}:{}".format(curr_keyword, next_word)
        else:
            next_word = np.random.choice(list(two_ngram_df[curr].index), 1, p=two_ngram_df[curr].values)[0]
            final_sentence += " {}".format(next_word)
            curr = "{}:{}".format(curr.split(":")[1], next_word)
    return final_sentence
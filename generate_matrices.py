#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import nltk
import json
import re
import string
from collections import defaultdict

def decontract(phrase):
    # helper function to remove contractions
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def create_prob_matrices(subreddit, data):
    start_m = defaultdict(int)
    prob_m_1 = defaultdict(lambda: defaultdict(int))
    prob_m_2 = defaultdict(lambda: defaultdict(int))
	
	# limit to 1000 comments for faster runtimes
    for title in data[data.subreddit == subreddit].title:
		    # preprocessing
		    text = re.sub(r"http\S+", "", str(title)) # first remove hyperlinks
		    text = decontract(text) # second convert contractions into orginal phrases
		    text = text.translate(str.maketrans("", "", string.punctuation)) # remove punctuations
		    
		    # tokenization
		    words = nltk.word_tokenize(text)
		    words = [word.lower() for word in words if word.isalpha()]
		    
		    # structuring
		    if len(words) >= 2: 
		        start_m["{}:{}".format(words[0], words[1])] += 1
		        for i in range(len(words)):
		            if i < len(words) - 1:
		                prob_m_1[words[i]][words[i+1]] += 1
		            if i < len(words) - 2:
		                prob_m_2["{}:{}".format(words[i], words[i+1])][words[i+2]] += 1
    return (start_m, prob_m_1, prob_m_2)

if __name__ == "__main__":
    data = pd.read_csv("data/posts.csv")
    for subs in list(data.subreddit.unique()):
        s, one, two = create_prob_matrices(subs, data)
        ## save dictionaries to json
        with open("data/start/{}.json".format(subs), "w") as out:
            json.dump(s, out)
        with open("data/one/{}.json".format(subs), "w") as out:
            json.dump(one, out)
        with open("data/two/{}.json".format(subs), "w") as out:
            json.dump(two, out)
        print("Finished creating matrices for r/{}".format(subs))


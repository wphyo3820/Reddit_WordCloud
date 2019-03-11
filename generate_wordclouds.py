#!/usr/bin/env python
# coding: utf-8

from wordcloud import WordCloud
import pandas as pd

if __name__ == "__main__":
    posts = pd.read_csv("data/posts.csv")
    titles = posts.groupby("subreddit")["title"].apply(lambda x: " ".join(x))

    for i,t in enumerate(titles):
        wordcloud = WordCloud(font_path="fonts/GoogleSans-Medium.ttf", background_color="white", colormap="ocean", 
                            width=1000, height=400, max_words=400).generate(t)
        wordcloud.to_file(f"wordclouds/{titles.index[i]}.png")


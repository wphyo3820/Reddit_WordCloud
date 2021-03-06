#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import praw
import pandas as pd


def scrape_top_subreddits(url, limit):
    data = []
    for i in range(1, 100):
        response = requests.get(url + "/?page={}".format(i))
        content = BeautifulSoup(response.content, "html.parser")
        for c in content.find_all("div", attrs={"class": "span4 listing"}):
            if "Subscribers" == c.find("h3", attrs={"class": "listing-header"}).text:
                results = c.find_all(
                    "div", attrs={"data-target-filter": "sfw", "class": "listing-item"})
                for r in results:
                    data.append(r.get("data-target-subreddit"))
                    if len(data) == limit:
                        return pd.DataFrame({"subreddits": data})
    return None


def scrape_subreddit_data(reddit, subreddits):
    data = []
    for subr in subreddits:
        sub = reddit.subreddit(subr).top(limit=1000)
        data.extend([{"subreddit": subr, "id": s.id, "title": s.title,
                      "gilded": s.gilded, "score": s.score} for s in sub])
        print("Finished scraping r/{}".format(subr))
    return pd.DataFrame(data)


if __name__ == "__main__":
    reddit = praw.Reddit(client_id='JRRDQWr5Mn_8LA', client_secret='gmhoQTNiZhEp4hj08q7s_lb7Is0',
                         user_agent='Comment Extraction by /u/ivanchen9520')
    # STEP 1: get the top subreddits
    subreddits = scrape_top_subreddits("http://www.redditlist.com", 50)
    # STEP 2: get top posts from subreddits
    data = scrape_subreddit_data(reddit, subreddits.subreddits)
    # save dataframes
    subreddits.to_csv("data/subs.csv", index=False)
    data.to_csv("data/posts.csv", index=False)
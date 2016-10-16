import tweepy
import re
import time
import math
import pandas as pd
from watson_developer_cloud import AlchemyLanguageV1

def initAlchemy():
    al = AlchemyLanguageV1(api_key='ENTER-API-KEY')

    return al

def initTwitterApi():
    consumer_key = 'ENTER-CONSUMER-KEY'
    consumer_secret = 'ENTER_CONSUMER-SECRET'

    access_token = 'ENTER-ACCESS-TOKEN'
    access_token_secret = 'ENTER-ACCESS-TOKEN_SECRET'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api

'''This function is implemented to handle tweepy exception errors
because search is rate limited at 180 queries per 15 minute window by twitter'''

def limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError as error:
            print(repr(error))
            print("Twitter Request limit error reached sleeping for 15 minutes")
            time.sleep(16*60)
        except tweepy.RateLimitError:
            print("Rate Limit Error occurred Sleeping for 16 minutes")
            time.sleep(16*60)

def retrieveTweets(api, search, lim):
    if(lim == ""):
        lim = math.inf
    else:
        lim = int(lim)
    text = []
    for tweet in limit(tweepy.Cursor(api.search, q=search).items(limit = lim)):
        t = re.sub('\s+', ' ', tweet.text)
        text.append(t)

    data = {"Tweet":text,
            "Sentiment":"",
            "Score":""}

    dataFrame = pd.DataFrame(data, columns=["Tweet","Sentiment","Score"])

    return dataFrame

def analyze(al,dataFrame):
    sentiment = []
    score = []
    for i in range(0, dataFrame["Tweet"].__len__()):
        res = al.combined(text=dataFrame["Tweet"][i],
                          extract="doc-sentiment",
                          sentiment=1)
        sentiment.append(res["docSentiment"]["type"])
        if(res["docSentiment"]["type"] == "neutral"):
            score.append(0)
        else:
            score.append(res["docSentiment"]["score"])

    dataFrame["Sentiment"] = sentiment
    dataFrame["Score"] = score

    return dataFrame


def main():
    #Initialse Twitter Api
    api = initTwitterApi()

    #Retrieve tweets
    dataFrame = retrieveTweets(api,input("Enter the search query (e.g. #hillaryclinton ) : "), input("Enter limit for number of tweets to be searched or else just hit enter : "))

    #Initialise IBM Watson Alchemy Language Api
    al = initAlchemy()

    #Do Document Sentiment analysis
    dataFrame = analyze(al, dataFrame)

    #Save tweets, sentiment, and score data frame in csv file
    dataFrame.to_csv(input("Enter the name of the file (with .csv extension) : "))

if __name__ == '__main__':
    main()
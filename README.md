# Twitter-Sentiment-Analysis

## Overview

Python code for searching a query and finding all tweets with respect to it and analyzing the sentiment for that particlar tweet. All tweets along with it's sentiment is stored in a csv file. 

## Depedencies

* tweepy (http://www.tweepy.org/)
* IBM Watson AlchemyApi  (http://www.alchemyapi.com/)
* Pandas (http://pandas.pydata.org/)

## Run

After installing the dependencies download the sentiment_analysis.py paste the api key, consumer key, and access token along with their secrets and run it in the terminal

## Results

In light of recent us presedential election events i analyzed **#hillaryclinton** and **#donaldtrump** and it's results are in the files hillaryclinton.csv and donaldtrump.csv.

Just for fun i analysed the sentiment of **@sirajology** and to no suprise it was almost all positive :)

## Note

Since search is rate limited at 180 queries per 15 minute window by twitter i have set a function wherein if the error occurs the program sleeps for 15 minutes

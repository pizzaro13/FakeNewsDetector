#file for interpreting the data from different models

#use panads

import csv

allTweets = []

class tweet:
    def __init__(self, username, dateTime, numRetweets, tweetBody, hashtags, mentions):
        self.username = username
        self.dateTime = dateTime
        self.numRetweets = numRetweets
        self.tweetBody = tweetBody
        self.hashtags = hashtags
        self.mentions = mentions


def createTweets(fileToRead):
    with open(fileToRead) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            newTweet = tweet(row["Username"],row["Date"],row["Retweets"],row["Message"],row["Hashtags"],row["Mentions"])
            allTweets.append(newTweet)

#main
createTweets('tweets_results_0.csv')

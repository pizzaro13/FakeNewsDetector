#file for interpreting the data from different models

#use pandas

import csv
import datetime
import random

allTweets = []
listOfWeeks = []

class tweet:
    def __init__(self, username, dateTime, numRetweets, tweetBody, hashtags, mentions):
        self.username = username
        self.dateTime = dateTime
        self.numRetweets = numRetweets
        self.tweetBody = tweetBody
        self.hashtags = hashtags
        self.mentions = mentions
        self.week = 0

class cluster:
    def __init__(self, startingTweetBody):
        self.tweetList = [startingTweetBody]
        self.startingTweet = startingTweetBody
        self.clusterID = 0

class week:
    def __init__(self, weekNumber):
        self.clusterList = []
        self.weekNumber = weekNumber

def createTweets(fileToRead):
    with open(fileToRead) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            newTweet = tweet(row["Username"],row["Date"],row["Retweets"],row["Message"],row["Hashtags"],row["Mentions"])
            newTweet.dateTime = datetime.datetime.strptime(newTweet.dateTime, "%Y-%m-%d %H:%M:%S")
            newTweet.dateTime = newTweet.dateTime.date()
            newTweet.week = newTweet.dateTime.isocalendar()[1]
            allTweets.append(newTweet)

def createWeeks():
    counter = 1
    #53 weeks because it's a leap year
    while counter <= 53:
        newWeek = week(counter)
        listOfWeeks.append(newWeek)
        counter += 1

def createClusters(listTweets):
    for eachTweet in listTweets:
        weekIndex = eachTweet.week - 1
        clustersToCompare = listOfWeeks[weekIndex].clusterList
        foundCluster = False
        for currCluster in clustersToCompare:
            if compareTweets(currCluster.startingTweet, eachTweet.tweetBody):
                currCluster.tweetList.append(eachTweet)
                foundCluster = True
        if not foundCluster:
            newCluster = cluster(eachTweet.tweetBody)
            clustersToCompare.append(newCluster)

#return true it tweets are similar, false otherwise
def compareTweets(tweetBody1, tweetBody2):
    split1 = set(tweetBody1.split())
    split2 = set(tweetBody2.split())
    inCommon = split1
    inCommon = inCommon.intersection(split2)
    biggerTweet = max(len(split1),len(split2))
    comparison = float(len(inCommon))/float(biggerTweet)
    #if the intersection is at least 50% of the longer tweet
    if comparison >= .5:
        return True
    return False

def createClusterIDs():
    clustCount = 1
    for currWeek in listOfWeeks:
        for currCluster in currWeek.clusterList:
            if currCluster.clusterID == 0:
                break2 = False
                for currWeek2 in listOfWeeks:
                    #don't compare clusters from the same week
                    if currWeek == currWeek2:
                        continue
                    for currCluster2 in currWeek2.clusterList:
                        if currCluster2.clusterID != 0:
                            if compareTweets(currCluster.startingTweet, currCluster2.startingTweet):
                                currCluster.clusterID = currCluster2.clusterID
                                break2 = True
                                break
                    if break2:
                        break
                if not break2:
                    currCluster.clusterID = clustCount
                    clustCount += 1
#main
createTweets('tweets_results_0.csv')
createWeeks()
createClusters(allTweets)
createClusterIDs()
toWrite = open('Obama_Pledge_Allegiance_Clusters.json', 'w')
toWrite.write('{\n')
weekCounter = 0
toWrite.write('\t\"name\": \"obama pledge allegiance bans OR pledge OR allegiance\",\n')
toWrite.write('\t\"value\": 53,\n')
toWrite.write('\t\"children\": [\n')
for currWeek in listOfWeeks:
    toWrite.write('\t\t{\n')
    toWrite.write("\t\t\t\"week\": ")
    toWrite.write(str(weekCounter + 1))
    toWrite.write(",\n\t\t\t\"value\": ")
    toWrite.write(str(len(currWeek.clusterList)))
    toWrite.write(",\n\t\t\t\"children\": [\n")
    clusterCounter = 0
    for currCluster in currWeek.clusterList:
        toWrite.write("\t\t\t\t{\n\t\t\t\t\t\"name\": \"")
        toWrite.write(currCluster.startingTweet)
        toWrite.write("\",\n")
        toWrite.write("\t\t\t\t\t\"cluster\": ")
        toWrite.write(str(currCluster.clusterID))
        toWrite.write(",\n")
        toWrite.write("\t\t\t\t\t\"value\": ")
        toWrite.write(str(len(currCluster.tweetList)))
        toWrite.write("\n")

        clusterCounter += 1

        if clusterCounter == len(currWeek.clusterList):
            toWrite.write('\t\t\t\t}\n')
        else:
            toWrite.write('\t\t\t\t},\n')
    toWrite.write("\t\t\t]\n")
    weekCounter += 1
    if weekCounter == len(listOfWeeks):
        toWrite.write('\t\t}\n')
    else:
        toWrite.write('\t\t},\n')
toWrite.write('\t]\n')
toWrite.write('}')

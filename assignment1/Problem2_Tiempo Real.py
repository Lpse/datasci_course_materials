# -*- coding: cp1252 -*-
import sys
import re
import twitterstream


def lines(fp):
    print str(len(fp.readlines()))

def hw(line,tw,tu,suma):
    #   Function to print result in a readable format
    print "Line: ",line,"\n","TWEET: [",tw,"]"
    print "< Sentiment: ",suma," >"
    
    for k,v in sorted(tu.items()):
        print "<",u'{0}: {1}'.format(k,v),">"

    print "\n"

def CreateDictionary(fp,dict):   
    for line in fp:
        term, score  = line.split("\t")     # The file is tab-delimited. "\t" means "tab character"
        dict[term] = int(score)             # Convert the score to an integer.

    return dict

def checkListinString(list,string):
    #   Function to check if string has sentiment words
    if any(word in string.split() for word in list):
        return string
    else:
        return ""
    
def checkSentValue(str,dict,tuple):
    #   Function to find sentiment values
    tweet=set(str.split())                  # set of words in tweet
    tweet.intersection_update(list(dict))   # set of intersections
    for x in tweet:                         # set value from dictionary
        tuple[x]=int(dict.get(x))

    return tuple
        

def findStr(line,str,mode):
    #   Function to find the field to parse
    #   line:   line of twitterreq()
    #   str:    string to search
    #   mode:   search as initial or final string of the field
    #           mode    0:  initial
    #           mode    1:  final
    strOut=""
    i=line.find(str)
    strlen=len(str)
    if (i>=0):
            if(mode==0):
                i=i+strlen
                strOut=line[i:]

            if(mode==1):
                strOut=line[:i] 

    return strOut

def main():
    sent_file = open("AFINN-111.txt")
    tweet_file = open("twitterstream.py")

    print "Assigment1-PROBLEM2:\n"


    searchInitField="\"description\":\""    
    searchEndField="\",\"protected"
    parameters=[]
    url = "https://stream.twitter.com/1/statuses/sample.json"

    # Create dictionary from AFINN-111.txt
    AffinDict = {}
    SentimentsTuple={}
    AffinDict=CreateDictionary(sent_file,AffinDict)
    lineValue=int(0)
    suma=int(0)
    
    response=twitterstream.twitterreq(url,"GET",parameters)
    for line in response:
        # Cut the tweet
        lineValue+=1
        tweet=line.strip()
        tweet=findStr(tweet,searchInitField,0)
        tweet=findStr(tweet,searchEndField,1)
        suma=0
        # Select tweets in which sentiment words appear
        tweetReceived=checkListinString(AffinDict,tweet)
        SentimentsTuple.clear()
        if (tweetReceived==""):
            SentimentsTuple={'--':int(0)}
            tweetReceived=tweet
        else:
            # Check value of tweet in line and return values
            SentimentsTuple=checkSentValue(tweetReceived,AffinDict,SentimentsTuple)
            #   Function to compute total value of sentiment
            suma=int(sum(SentimentsTuple.itervalues()))
            
        hw(lineValue,tweetReceived,SentimentsTuple,suma)

    lines(sent_file)
    lines(tweet_file)
    

if __name__ == '__main__':
    main()

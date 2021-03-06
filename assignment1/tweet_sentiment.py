# -*- coding: cp1252 -*-
import sys
import re
import json

def lines(fp):
    # When reading is done completely, iterator is at the EOF --> This function returns "0 lines"
    print str(len(fp.readlines()))

def hw(line,tw,tu,suma):
    #   Function to print result in a readable format
    #print "Line: ",line,"\n","TWEET: [",tw,"]"
    #print "< Total Sentiment: ",suma," >"
    
    for k,v in sorted(tu.items()):
        print line," : <",u'{0}: {1}'.format(k,v),">"

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
    sent_file = open(sys.argv[1])   #   File AFINN-111.txt 
    tweet_file = open(sys.argv[2])  #   File Output.txt 

    searchInitField="\"description\":\""    
    searchEndField="\",\"protected"

    # Create dictionary from AFINN-111.txt
    AffinDict = {}
    AffinDict=CreateDictionary(sent_file,AffinDict)

    # Init aux variables
    SentimentsTuple={}
    lineValue=int(0)
    suma=int(0)

    # Read each line of the output.txt file
    while 1:
        tweet=tweet_file.readline()
        tweet=tweet.strip()
        if not tweet:
            break
        else:
            lineValue+=1
            tweet=findStr(tweet,searchInitField,0)
            tweet=findStr(tweet,searchEndField,1)
            suma=0
            # Select tweets in which sentiment words appear
            tweetReceived=checkListinString(AffinDict,tweet)
            SentimentsTuple.clear()
            if (tweetReceived==""):
                SentimentsTuple={'noSentiment':int(0)}
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

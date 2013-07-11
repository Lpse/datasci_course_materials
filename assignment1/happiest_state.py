# -*- coding: cp1252 -*-
import sys
from pprint import pprint
import operator
import json
import re

def lines(fp):
    # When reading is done completely, iterator is at the EOF --> This function returns "0 lines"
    print str(len(fp.readlines()))
    
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #Initialization
    scores = {}
    tweetScores = []
    tweetDict = {}
    StateTuple = {}
    StatesList = []
    FinalStateTuple = {}

    for line in sent_file:
        term, score  = line.split("\t")
        scores[term] = int(score)
   
    for line in tweet_file:
        data = json.loads(line)
        if 'text' in data:
                tweetScores.append(data['text'])

    for tweet in tweetScores:
        tweet = tweet.replace('\n',' ')
        i = 0
        words = tweet.encode('utf-8').split()
        k = 0
        while i < len(words):
            for key, value in scores.iteritems():
                if key == words[i]:
                    k = k + value
            i = i + 1
        tweetDict[tweet.encode('utf-8')] = float(k)

    for line in tweet_file:
        data = json.loads(line)
        d = 0
        for key, value in tweetDict.iteritems():
            
            try:
                
                if data['place']['country_code']=='US' and data['text'].encode('utf-8')==key:
                    st = data['place']['full_name']
                    p = 0
                    q = 0
                    for m in st:
                        if m == ",":
                            q = p
                        p = p + 1
                    #print st[q+2] + st[q+3]+"    "+str(value)
                    StateTuple[st[q+2] + st[q+3] +str(d)] = float(value)
                    StatesList.append(st[q+2] + st[q+3])
                d = d + 1
                     
            except:
                pass

    StatesList_new = list(set(StatesList))
    for w in StatesList_new:
        x = 0
        y = 0
        for key, value in StateTuple.iteritems():
            if w == key[:2]:
                x = x + float(value)
        FinalStateTuple[w] = x

    if (len(FinalStateTuple)>0):
        print max(FinalStateTuple, key = FinalStateTuple.get)
    
##    lines(sent_file)
##    lines(tweet_file)
    

if __name__ == '__main__':
    main()

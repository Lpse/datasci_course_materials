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
    tweet_file = open(sys.argv[1])

    #Initialization:
    scores = []
    TweetList = []
    output = {}
    topTenTuple3 = {}

    # Add file content to a list:
    for line in tweet_file:
        data = json.loads(line)
        if 'entities' in data:
            if 'hashtags' in data['entities']:
                for tag in data['entities']['hashtags']:
                    #print tag['text'].encode('utf-8')
                    scores.append(tag['text'].encode('utf-8'))
                    TweetList.append(tag['text'].encode('utf-8'))
    TweetList_new = list(set(TweetList))
    
    for item in TweetList_new:
        i = int(0)
        for item1 in scores:
            if item == item1:
                i+=1
        output[item] = float(i)
    topTenTuple3 = sorted(output.iteritems(),key=operator.itemgetter(1))
    
    b = int(0)
    for h in topTenTuple3:
        b+=1
    i = int(1)

    # Final list - Top-ten list
    while i < 11:
        out = ()
        out = topTenTuple3[b - i]
        print out[0] +'\t'+str(out[1])
        i+=1
    

if __name__ == '__main__':
    main()

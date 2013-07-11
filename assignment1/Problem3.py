# -*- coding: cp1252 -*-
import sys
import re
import json

def lines(fp):
    # When reading is done completely, iterator is at the EOF --> This function returns "0 lines"
    print str(len(fp.readlines()))

def hw(tu):
    #   Function to print result in a readable format
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

def AppendNewTerms(str,sum,senTuple):
    #   Function to return the tuple with new terms and values
    #   str --> tweetReceived
    #   sum --> suma
    #   senTuple --> SentimentsTuple
    termTuple={}
    str=str.split()
    auxsenTuple=list(senTuple)
    auxList=[]
    score=float(0)
    div=float(len(str)-len(auxsenTuple))

    # Find the non-match words:
    for i in range(len(str)):
        for j in range(len(auxsenTuple)):
            if str[i]==auxsenTuple[j]:
                auxList.append(int(0))
            else:
                auxList.append(int(1))
    for i in range(len(str)):
        if (auxList[i]==0):
            str[i]=""
            
    # Clean the final list
    str=filter(lambda x: len(x)>0, str)     

    # Compute initial-value of term (Other function will compute the final-value:
    # value(term)=[value(tweet)]/[(No.words in tweet)-(No.sentimental words in tweet)]
    if (div>0.0):
        score=float(sum/div)
    else:
        score=float(sum)
            
    termTuple=termTuple.fromkeys(str,score)
    return termTuple
    
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

def addterm(term, value, outdict):
    # Add an entry to the final dictionary unless the entry is alreadty there
    if outdict.has_key(term):
        outdict[term]=float(outdict[term])+float(value)
    else:
        outdict[term]=float(value)

    return outdict

def main():
    sent_file = open("AFINN-111.txt")   #   File AFINN-111.txt" --> sys.argv[1]
    tweet_file = open("datos.txt")  #   File Output.txt --> sys.argv[2]

    print "Assigment1-PROBLEM3:\n"

    searchInitField="\"description\":\""    
    searchEndField="\",\"protected"

    # Create dictionary from AFINN-111.txt
    AffinDict = {}
    AffinDict=CreateDictionary(sent_file,AffinDict)

    # Init aux variables
    SentimentsTuple={}      # Tuple of AFINN-term and its value
    NewTermsTuple={}        # Tuple of No-AFINN-terms and its value
    TweetTermsTuple={}      # Auxiliar Tuple of No-AFINN-terms for each tweet
    lineValue=int(0)
    suma=int(0)

    # Read each line of the output.txt file
    while 1:
        tweet=tweet_file.readline()
        tweet=tweet.strip()
        tweet.encode('utf-8')
        if not tweet:
            break
        else:
            lineValue+=1
            tweet=findStr(tweet,searchInitField,0)
            tweet=findStr(tweet,searchEndField,1)
            suma=float(0.0)
            # Select tweets in which sentiment words appear
            tweetReceived=checkListinString(AffinDict,tweet)
            SentimentsTuple.clear()
            if (tweetReceived==""):
                SentimentsTuple={'--':float(0)}
                tweetReceived=tweet
                suma=float(0.0)
            else:
                # Check value of tweet in line and return values
                SentimentsTuple=checkSentValue(tweetReceived,AffinDict,SentimentsTuple)
                #   Function to compute total value of sentiment
                suma=float(sum(SentimentsTuple.itervalues()))
                
            ##hw(lineValue,tweetReceived,SentimentsTuple,suma)

            # Compute terms of each tweet that are not defined in AFINN file
            TweetTermsTuple=AppendNewTerms(tweetReceived,suma,SentimentsTuple)

            # Compute terms
            for item in TweetTermsTuple:
                NewTermsTuple=addterm(item, TweetTermsTuple[item], NewTermsTuple)

    
    hw(NewTermsTuple)
    lines(sent_file)
    lines(tweet_file)
    

if __name__ == '__main__':
    main()

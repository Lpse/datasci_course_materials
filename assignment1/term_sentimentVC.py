import sys
import json
def main():
    #load the input new terms file into scores
    #sent_file = open(sys.argv[1])
    #scores = []
    #for line in sent_file:
        #scores.append(line.rstrip('\n'))
    #sent_file.close()
    #print scores
    #==========================================
    #load the file AFINN-111.txt into scores1
    AFIN = open("AFINN-111.txt")
    scores1 = {}
    for line in AFIN:
        term, score  = line.split("\t")
        scores1[term] = int(score)
    AFIN.close()
    #==========================================
    #load the output.json into scores2
    tweet_file = open("datos.txt")
    scores2 = []
    for line in tweet_file:
        data = json.loads(line)
        if 'lang' in data and 'text' in data:
            if data['lang'] == "en":
                scores2.append(data['text'])
    tweet_file.close()
    #==========================================
    #cross scores1 with scores2 to create tweets list scores3 and
    #at the same time, filling the list non_matched with the tweets
    #words that are not in the AFIN file
    scores3 = {}
    non_matched = ['Start']
    for tweet in scores2:
        tweet = tweet.replace('\n',' ')
        i = 0
        words = tweet.encode('utf-8').split()
        k = 0
        matched = False
        while i < len(words):
            for key, value in scores1.iteritems():
                if key == words[i]:
                    k = k + value
                    matched = True
            if matched == False:
                already_in = False
                for l in non_matched:
                    if words[i] == l:
                        already_in = True
                if already_in == False:
                    non_matched.append(words[i])
            matched = False
            i = i + 1
        scores3[tweet.encode('utf-8')] = float(k)
    #==========================================
    #open and loop through scores (out list of not scored terms),
    #then open and loop scores3 (the scored tweets list), we will then
    # split the tweets in words, and will take the first term in
    #scores and go through all the words in the tweet trying to find
    # a match. Whenever that match is found, we will then score the 
    # term and will pass to the next tweet, following the same process
    # until the tweet list is finished
    non_matched = list(set(non_matched))
    for term in non_matched:
        k = 0
        h = 0
        d = 0
        for key, value in scores3.iteritems():
            key = key.replace('\n',' ')
            i = 0
            words = key.split()
            while i < len(words):
                if term == words[i]:
                    k = k + value
                    h = h + 1
                    break
                i = i + 1
        if h == 0:    
            print term + '\t' + str(float(0))
        else:
            print term + '\t' + str(float(k/h))
if __name__ == '__main__':
    main()

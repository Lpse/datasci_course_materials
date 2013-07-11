import sys
import json


 
def main():
    print "Assigment1-PROBLEM4:\n"
    
    tweet_file = open("datos.txt","r")
    sc1=[]          # Aux variable to compute values
    sc2=[]          # Aux variable to compute values
    FileValues=[]   # Variable to get values from file

    # Function to load the file and build the list of values
    
    for lines in tweet_file:
        data=json.loads(lines)
        if 'lang' in data and 'text' in data:
            if data['lang']=="en":
                FileValues.append(data['text'])

    # Read tweets to split()
    for tw in FileValues:
        tw=tw.replace('\n',' ')
        str=tw.encode('utf-8').split()
        i=int(0)
        while i<len(str):
            sc1.append(str[i])
            i+=1


    sc2=sc1
    print sc2

    # Create dictionary as a container of final tuples
    freq={}
    index=int(1)
    for val2 in sc2:
        for val1 in sc1:
            if val2==val1:
                index+=1
        freq[val2]=float(index)
        print "< ",val2," : ",freq[val2]," >"
        

if __name__ == '__main__':
    main()

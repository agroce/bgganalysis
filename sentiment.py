import os
import time
from textblob import TextBlob
import sys
import scipy.stats
import pickle

with open("games.pickle") as f:
    games = pickle.load(f)

CUTOFF = 0
    
data = []
subdata = []

for (name,rank) in games:
    thisData = []
    thisSubdata = []
    if len(games[(name,rank)]) < CUTOFF:
        continue
    for (r,c) in games[(name,rank)]:
        if r == -1.0:
            continue
        s = TextBlob(c)
        try:
            data.append((r,s.sentiment.polarity))
            thisData.append((r,s.sentiment.polarity))
            subdata.append((r,s.sentiment.subjectivity))
            thisSubdata.append((r,s.sentiment.subjectivity))            
        except:
            pass
    print "#"*50
    print "#",rank,":",name,len(games[(name,rank)])
    thisRegress = scipy.stats.linregress(thisData)
    print "POLARITY R^2",(thisRegress.rvalue**2)
    thisSubRegress = scipy.stats.linregress(thisSubdata)
    print "SUBJECTIVITY R^2",(thisSubRegress.rvalue**2)    
    sys.stdout.flush()

print "*"*80

print "OVER ALL GAMES:"
    
print len(data)
            
regress = scipy.stats.linregress(data)

print "POLARITY R^2:",(regress.rvalue)**2

subRegress = scipy.stats.linregress(subdata)

print "SUBJECTIVITY R^2:",(subRegress.rvalue)**2

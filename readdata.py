import os
import time
from textblob import TextBlob
import sys
import scipy.stats

def getGames():
    games = []
    for f in os.listdir("data"):
        try:
            g = int(f.split(".txt")[0])
            games.append("data/"+f)
        except:
            pass
    return games

def normalize(word):
    n = ""
    for c in word.lower():
        if c.isalnum() or (c == "-"):
            n += c
    return n
        

games = {}
words = {}

CUTOFF = 30

for g in getGames():
    with open(g) as f:
        seenName = False
        seenRank = False
        seenRating = False
        comments = []
        for l in f:
            if (not seenName) and ("GAME:" in l):
                seenName = True
                name = l.split("GAME: ")[1][:-1]
            if (not seenRank) and ("RANK:" in l):
                seenRank = True
                rank = int(l.split("RANK: ")[1][:-1])
            if (seenName and seenRank):
                if (not seenRating) and ("RATING: " in l):
                    seenRating = True
                    if "N/A" not in l:
                        rating = float(l.split("RATING: ")[1][:-1])
                    else:
                        rating = -1.0
                    comment = ""
                elif seenRating:
                    if l == "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n":
                        comments.append((rating,comment))
                        seenRating = False
                    else:
                        comment += l
        if seenRating:
            comments.append((rating,comment))
        games[(name,rank)] = comments


        
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

import os
import time

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

for (name,rank) in sorted(games,key = lambda x:len(games[x])):
    print (name,rank),":",len(games[(name,rank)])
    for (r,c) in games[(name,rank)]:
        for w in c.split():
            wn = normalize(w)
            if wn not in words:
                words[wn] = 1
            else:
                words[wn] += 1

swords = sorted(words,key = lambda x:words[x])

for w in swords[-30:]:
    print w,words[w]

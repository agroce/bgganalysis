import urllib2
import xml.etree.ElementTree as ET
import os
import httplib
import random
import time

def getComments(gameNumber,reqRank):
    page = 1
    comments = []
    numComments = 1
    name = None
    rank = None
    print "READING DATA FOR GAME #",gameNumber
    while numComments != 0:
        didRead = False
        while not didRead:
            try:
                response = urllib2.urlopen('https://www.boardgamegeek.com/xmlapi/boardgame/'
                                        + str(gameNumber) + '&stats=1&comments=1&page=' + str(page))
                didRead = True
            except httplib.BadStatusLine:
                print "WAITING (1)..."
                time.sleep(30)
            except urllib2.HTTPError:
                print "WAITING (2)..."                
                time.sleep(30)

        html = response.read()
        try:
            root = ET.fromstring(html)
        except:
            return "PARSE ERROR"
        numComments = 0
        for child in root:
            for deepchild in child:
                if deepchild.tag == "comment":
                    comments.append(deepchild)
                    numComments += 1
                if deepchild.tag == "name" and (name == None):
                    a = deepchild.attrib
                    if "primary" in a:
                        name = deepchild.text
                        print "NAME:",name
                if deepchild.tag == "statistics" and (rank == None):
                    for statschild in deepchild:
                        if statschild.tag == "ratings":
                            for ratingschild in statschild:
                                if ratingschild.tag == "ranks":
                                    for rankschild in ratingschild:
                                        a = rankschild.attrib
                                        if a["name"] == "boardgame":
                                            try:
                                                rank = int(a["value"])
                                            except ValueError:
                                                print "NOT RANKED"
                                                return None
                                            print "RANK:",rank
                                            if rank > reqRank:
                                                print "GAME TOO LOW RANK"
                                                return None
        page += 1
    if rank == None:
        print "GAME NOT RANKED"
        return None
    return (name,rank,comments)

WORSTRANK = 5000

top20 = [174430, 161936, 182028, 12333, 167791, 187645, 120677, 169786, 193738, 173346, 84876,
              115746, 102794, 3076, 31260, 96848, 205637, 170216, 205059, 183394]
    
games = range(0,248000)
#random.shuffle(games)
gameData = []

#games = top20 + games

lowRank = []
for l in open ("data/lowrank.txt"):
    try:
        lowRank.append(int(l))
    except ValueError:
        pass

lowRankf = open("data/lowrank.txt",'a')
    
for game in games:
    if game in lowRank:
        continue
    if os.path.exists("data/"+str(game)+".txt"):
        print game,"ALREADY READ"
        continue
    g = getComments(game,WORSTRANK)
    time.sleep(0.8)
    if g == None:
        lowRankf.write(str(game)+"\n")
        lowRankf.flush()
        continue
    if g == "PARSE ERROR":
        print "PARSE ERROR!"
        continue
    outf = open("data/"+str(game)+".txt",'w')
    outf.write("*-"*40+"\n")
    outf.write("GAME: "+g[0].encode('utf-8')+"\n")
    outf.write("RANK: "+str(g[1])+"\n")    
    for c in g[2]:
        outf.write("=-"*20+"\n")
        a = c.attrib
        outf.write("RATING: "+a["rating"]+"\n")
        text = c.text.encode('utf-8')
        outf.write(text+"\n")
    outf.close()

lowRankf.close()

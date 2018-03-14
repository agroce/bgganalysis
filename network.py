import os
import time
from textblob import TextBlob
import sys
import scipy.stats
import pickle
from graphviz import Digraph
import math

with open("games.pickle") as f:
    games = pickle.load(f)

MCUTOFF = 2
ONLYCLOSEST = False
HOWMANY = 2

colonIgnore = ["Legacy","Magic","Lord of the Rings","Star Wars",
                   "Invasion", "Warhammer", "Arkham Horror", "Europe",
                   "The Card Game", "Escape", "Android", "Pandemic",
                   "The Board Game"]
    
for RANKCUTOFF in [200,250,300,350,400,450,500]:
    print "*" * 80
    print "ANALYZING FOR",RANKCUTOFF
    
    topN = filter(lambda x:x[1] <= RANKCUTOFF, games.keys())
    names = []
    alternatives = {}
    nodeMap = {}
    nameRankMap = {}
    nodes = set([])

    dot = Digraph(comment="",format='png')

    ALLINGRAPH=True

    gn = 0
    for (name,rank) in topN:
        names.append(name)
        gn += 1
        #dot.node(str(gn), (name + ":" + str(rank)).decode('utf-8').encode('ascii',errors='ignore'))
        nodeMap[name] = str(gn)
        nameRankMap[str(gn)] = (name, rank)
        if ALLINGRAPH:
            (nname,nrank) = nameRankMap[nodeMap[name]]
            ntext = str((nname + ": " + str(nrank))).decode('utf-8').encode('ascii',errors='ignore')
            dot.node(nodeMap[name], ntext)
            nodes.add(nodeMap[name])
    for name in names:
        alternatives[name] = []
        alternatives[name].append(name)
        if ":" in name:
            ns0 = name.split(":")[0]
            ns1 = name.split(":")[1]
            if ns0 not in names and ns0 not in colonIgnore:
                alternatives[name].append(ns0)
            if ns1 not in names:
                alternatives[name].append(ns1)
            alternatives[name].append(name.replace(":",""))
        if "(" in name:
            p0 = name.find(" (")
            p1 = name.find(")")
            nop = name[:p0] + name[p1+1:]
            if nop not in names:
                alternatives[name].append(nop)
        if "&" in name:
            alternatives[name].append(name.replace("&","and"))

    nodes = set()

    totalC = 0
    totalLen = 0
    
    for (name,rank) in sorted(topN,key=lambda x:x[1]):
        if rank > RANKCUTOFF:
            continue
        mentions = {}
        for (r,c) in games[(name,rank)]:
            totalC += 1
            totalLen += len(c)
            for n in names:
                if n == "Go":
                    continue # Too many false positives, hurts results
                if n == "Village" and "Dominion" in name:
                    continue # Avoid the card name mixup
                if n == "Nations" and "Imperial" in name:
                    continue # Talking about nations in game, not this game
                if (n.find("Imperial") == 0):
                    if "Star Wars" in name or "Descent" in name:
                        continue
                    if "Imperium" in name:
                        continue
                    if "Imperial Settlers" in name:
                        continue
                for s in alternatives[n]:
                    if " " + s + " " in c:
                        if n != name:
                            if n not in mentions:
                                mentions[n] = 1
                            else:
                                mentions[n] += 1
                        break
        print "="*50
        print (name,rank)
        nlinks = 0

        print totalC,"TOTAL COMMENTS"
        print totalLen,"TOTAL LENGTH"
        
        for n in sorted(mentions.keys(), key=lambda x:mentions[x], reverse=True):
            if mentions[n] < MCUTOFF:
                continue
            p = math.log(mentions[n]*10)
            print "  ",n,mentions[n]
            if nodeMap[name] not in nodes:
                nodes.add(nodeMap[name])
                (nname,nrank) = nameRankMap[nodeMap[name]]
                ntext = str((nname + ": " + str(nrank))).decode('utf-8').encode('ascii',errors='ignore')
                dot.node(nodeMap[name], ntext)
            if nodeMap[n] not in nodes:
                nodes.add(nodeMap[name])            
                (nname,nrank) = nameRankMap[nodeMap[n]]
                ntext = str((nname + ": " + str(nrank))).decode('utf-8').encode('ascii',errors='ignore')
                dot.node(nodeMap[n], ntext)
            dot.edge(nodeMap[name],nodeMap[n], penwidth=str(p))
            nlinks += 1
            if nlinks == HOWMANY:
                break
            if ONLYCLOSEST:
                break

    print "SAVING GRAPH FOR",RANKCUTOFF
    dot.render("top" + str(RANKCUTOFF) + "_2most",view=False)
                    


        

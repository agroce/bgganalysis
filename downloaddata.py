import urllib2
import xml.etree.ElementTree

response = urllib2.urlopen('https://www.boardgamegeek.com/xmlapi/boardgame/2536?&comments=1')
html = response.read()

print type(html)    

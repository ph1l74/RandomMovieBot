from urllib.request import Request, urlopen
import urllib
#from urllib2 import urlopen
from lxml import html

def getPic(posterURL):
    url = urlopen(posterURL)
    page = html.parse(url)
    e = page.getroot().find_class('poster')
    for i in e:
        string = html.tostring(i)
        string = string[string.find('src="')+5:string.find('" itemprop')]
        urllib.request.urlretrieve(string, "static/poster.jpg")
        print ("Pic for ", posterURL, " saved.")
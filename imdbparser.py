from urllib.request import Request, urlopen
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup as bs
import re

filmlist = {"Title" : [],
            "Year" : [],
            "Director" : [],
            "Tags" : [],
            "Number": []
            }

#userID = "56310167"
userID = "2831835"

#url='http://rss.imdb.com/user/ur' + userID + '/watchlist'
url = 'https://www.kinopoisk.ru/user/' + userID + '/movies/list/sort/default/vector/desc/perpage/200/'

def getList(URL):
    #pattern = re.compile(r"(tt[0-9]{7})")
    page = urlopen(URL).read()

    print (URL)

    if page:
        print(URL+ " opened")
    else:
        print("URL Opening failed")

    parsed_page = bs(page, "lxml")
    if page:
        print(URL+ " parsed")
    else:
        print("URL Parsed Failed")

    for item in parsed_page.find_all('a', 'name'):
        print (item)
    #listofitems =
    #print (listofitems)
    #for item in listofitems:
    #    string = str(etree.tostring(item))
        #search = re.search(pattern, string)
    #    i = 0
    #    print (string)
        #print(search.group())
        #while i < len(search):
        #    print (search.group(i))
        #    i+=1

        #string = string[string.find('tt'):string.find('tt')+9:]
        #if string not in filmlist["Number"]:
        #    filmlist["Number"].append(string)
        #print(filmlist["Number"])

getList(url)

#https://www.kinopoisk.ru/user/318061/list/1/filtr/all/sort/order/page/1/

#clearfix
from urllib.request import Request, urlopen
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

filmlist = {"Title" : [],
            "Year" : [],
            "Director" : [],
            "Tags" : [],
            "Number": []
            }

#userID = "2831835"

def getList(userID):
    filmList = {'Number': [], 'Title': []}
    driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    url = 'https://www.kinopoisk.ru/user/' + userID + '/movies/list/sort/default/vector/desc/perpage/200/'
    print(url)
    driver.get(url)
    page = driver.page_source
    parsed_page = bs(page, 'lxml')

    filmNumber = 0
    for item in parsed_page.find_all('div', 'info'):
        if item.find('a', 'name'):
            filmList["Number"].append(filmNumber)
            filmTitle = item.find('a', 'name').text
            filmList["Title"].append(filmTitle)
        filmNumber += 1
    filmNumber -= 1
    print(filmList['Title'])


        #item.find_all('')

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

#getList(userID)

#https://www.kinopoisk.ru/user/318061/list/1/filtr/all/sort/order/page/1/

#clearfix
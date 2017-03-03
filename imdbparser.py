import urllib.request
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def getList(URL):
    filmList = {'IMDB': []}
    filmCount = 0

    page = urllib.request.urlopen(URL)
    page_parsed = bs(page, 'lxml')

    for title_td in page_parsed.find_all('td', "titleColumn"):
        for title_link in title_td.find_all('a'):
            filmCount += 1
            title_link = title_link.get('href')
            title_pattern = re.compile('(tt\d{1,})')
            search = re.search(title_pattern, title_link)
            title = search.group()
            filmList['IMDB'].append(title)
    page = urllib.request.urlcleanup()
    return filmList, filmCount

def getListGenre(URL):
        filmList = {'IMDB': []}
        filmCount = 0

        page = urllib.request.urlopen(URL)
        page_parsed = bs(page, 'lxml')

        for title_td in page_parsed.find_all('td'):
            #print (title_td)
            for title_link in title_td.find_all('a'):
                filmCount += 1
                title_link = title_link.get('href')
                print(title_link)
                title_pattern = re.compile('(tt\d{1,})')
                search = re.search(title_pattern, title_link)
                title = search.groups()
                if title:
                    if title not in filmList['IMDB']:
                        filmList['IMDB'].append(title)
        page = urllib.request.urlcleanup()
        #print(filmList)
        #print(filmCount)
        return filmList, filmCount

#https://www.kinopoisk.ru/user/318061/list/1/filtr/all/sort/order/page/1/

#clearfix
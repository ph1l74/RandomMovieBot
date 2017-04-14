import urllib.request
from bs4 import BeautifulSoup as bs
import re

def get_list(URL):
    film_list = {'IMDB': []}
    film_count = 0

    page = urllib.request.urlopen(URL)
    page_parsed = bs(page, 'lxml')

    for title_td in page_parsed.find_all('td', "titleColumn"):
        for title_link in title_td.find_all('a'):
            film_count += 1
            title_link = title_link.get('href')
            title_pattern = re.compile('(tt\d{1,})')
            search = re.search(title_pattern, title_link)
            title = search.group()
            film_list['IMDB'].append(title)
    urllib.request.urlcleanup()
    return film_list, film_count

def get_list_genre(URL):
        film_list = {'IMDB': []}
        film_count = 0

        page = urllib.request.urlopen(URL)
        page_parsed = bs(page, 'lxml')

        for title_td in page_parsed.find_all('td'):
            #print (title_td)
            for title_link in title_td.find_all('a'):
                film_count += 1
                title_link = title_link.get('href')
                print(title_link)
                title_pattern = re.compile('(tt\d{1,})')
                search = re.search(title_pattern, title_link)
                title = search.groups()
                if title:
                    if title not in film_list['IMDB']:
                        film_list['IMDB'].append(title)
        urllib.request.urlcleanup()
        return film_list, film_count

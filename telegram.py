import telebot
import config
import random
import func
import csv
import urllib
import codecs
import re
from urllib.request import Request
import json

print("Modules imported")

bot = telebot.TeleBot(config.token)
bot

if bot:
    print("Bot started")

status = []

filmList = {"Number": [], "IMDB": []}

def fileOpen(filename):
    filmList = {"Number": [], "IMDB": []}
    ftpstream = urllib.request.urlopen(filename)
    filmListDR = csv.DictReader(codecs.iterdecode(ftpstream, "utf-8"), delimiter=',')
    filmNumber = 0
    for row in filmListDR:
        filmList["Number"].append(filmNumber)
        filmList["IMDB"].append(str(row['const']))
        filmNumber += 1
    filmNumber -= 1
    ftpstream = urllib.request.urlcleanup()
    print("Список успешно загружен\nЭлементов в списке: " + str(filmNumber))
    return filmList, filmNumber

def getInfo(title):
    jsonurl = "http://www.omdbapi.com/?i=" + title+ "&plot=short&r=json"
    response = urllib.request.urlopen(jsonurl)
    reader = codecs.getreader('utf-8')
    data = json.load(reader(response))
    filmTitle = data['Title']
    filmYear = data['Year']
    filmDirector = data['Director']
    filmGenre = data['Genre']
    filmCountry = data['Country']
    filmPlot = data['Plot']
    filmRuntime = data['Runtime']
    filmRating = data['imdbRating']
    filmScore = data['Metascore']
    filmURL = "http://www.imdb.com/title/" + str(data['imdbID'])
    filmPoster = data['Poster']
    return filmTitle, filmYear, filmDirector, filmGenre, filmCountry, filmPlot, filmRuntime, filmRating, filmScore, filmURL, filmPoster


def getRandom(filmList):
    randomFilm = random.choice(filmList["Number"])
    filmIMDB = str(filmList["IMDB"][randomFilm])
    return filmIMDB

@bot.message_handler(content_types='text')
def answer(message):
    global status, filmList
    setnull = False
    print("%s: %s: %s" % (message.chat.id, message.chat.first_name, message.text))
    if message.chat.id not in status:
        print ("New chat, id: %s" % message.chat.id)
    if message.chat.id in status:
        if message.text == "/setnull":
            print ("null set")
            setnull = True
        if message.text == "/random":
            filmIMDB = getRandom(filmList)
            filmTitle, filmYear, filmDirector, filmGenre, filmCountry, filmPlot, filmRuntime, filmRating, filmScore, filmURL, filmPoster = getInfo(filmIMDB)
            try:
                if filmScore == "N/A":
                    emoji = u'\U00002753'
                elif 0 < int(filmScore) < 20:
                    emoji = u'\U0001F232'
                elif 21 < int(filmScore) < 45:
                    emoji = u'\U0001F21A'
                elif 46 < int(filmScore) < 60:
                    emoji = u'\U0001F233'
                elif 61 < int(filmScore) < 80:
                    emoji = u'\U0001F22F'
                elif 81 < int(filmScore) < 100:
                    emoji = u'\U0001F4AF'
                answer1 = filmTitle + " (" + filmYear + ")\n" + filmDirector + "\n" + filmGenre + " / " + filmCountry
                answer2 = "\n\n" + filmPlot + "\n\n" + filmRuntime + " / " + filmRating + " / " + filmScore + " " + emoji
            except UnboundLocalError:
                pass
            answer = answer1+answer2
            keyboard = telebot.types.InlineKeyboardMarkup()

            if setnull:
                filmURL = False
                print(filmURL)
            try:
                keyboard.add(telebot.types.InlineKeyboardButton(text="Подбробнее о " + filmTitle, url=filmURL))
            except ValueError:
                print (filmURL)
            DLLink = filmTitle + " " + filmYear
            RuTracker = 'http://rutracker.org/forum/tracker.php?nm=' + re.sub(r' +', '%20', DLLink)
            PirateBay = "https://thepiratebay.org/search/" + re.sub(r' +', '%20', DLLink)
            RarBG = "https://rarbg.to/torrents.php?search=" + re.sub(r' +', '+', DLLink) + "&category%5B%5D=14&category%5B%5D=48&category%5B%5D=17&category%5B%5D=44&category%5B%5D=45&category%5B%5D=47&category%5B%5D=42&category%5B%5D=46"
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rutracker.org", url=RuTracker))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на piratebay.org", url=PirateBay))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rarbg.com", url=RarBG))
            poster = urllib.request.urlopen(filmPoster)
            bot.send_photo(message.chat.id, poster)
            bot.send_message(message.chat.id, answer, reply_markup=keyboard)
            bot.send_message(message.chat.id, "Не то? Нажимай на /random")

        else:
            bot.send_message(message.chat.id, "Я таких слов не знаю, извини")
    else:
        string = "Привет, " + str(message.chat.first_name) + ". Твой список еще не загружен." + "\nСкидывай мне его в *.csv, я пока подожду"
        bot.send_message(message.chat.id, string)

@bot.message_handler(content_types='document')
def handle_csv(message):
    global status,filmList
    if message.document.mime_type == "text/csv":
        file = message.document.file_id
        filepath = "https://api.telegram.org/file/bot" + config.token+"/" + bot.get_file(file).file_path
        filmList, filmNumber = fileOpen(filepath)
        if filmNumber % 10 == 1:
            string = "фильм"
        elif filmNumber % 10 == 2 or filmNumber % 10 == 3 or filmNumber % 10 == 4:
            string = "фильма"
        else:
            string = "фильмов"
        answer = 'В твоём списке ' + str(filmNumber) + " " + string
        if message.chat.id not in status:
            status.append(message.chat.id)
        print(status)
        #keyboard = telebot.types.InlineKeyboardMarkup()
        #keyboard.add(telebot.types.InlineKeyboardButton(text="/random"))
        bot.send_message(message.chat.id, answer)
        bot.send_message(message.chat.id, "Сейчас можешь воспользоваться командой /random , чтобы выбрать случайный фильм")
    else:
        type = message.document.mime_type
        bot.send_message(message.chat.id, "Это %s. Я такие файлы читать не умею. Скинь *.csv" %type)

if __name__ == '__main__':
    bot.polling(none_stop=True)


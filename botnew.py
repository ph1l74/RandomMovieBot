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
import imdbparser as imdb

print("Modules imported")

bot = telebot.TeleBot(config.token)

if bot:
    print("Bot started")

status = []

filmList = {}

urls = {'Top 250': 'http://www.imdb.com/chart/top',
        'Most Popular': 'http://www.imdb.com/chart/moviemeter',
        'Top English': 'http://www.imdb.com/chart/top-english-movies',
        'Top 10': 'http://www.imdb.com/year/',
        'Actions': 'http://www.imdb.com/genre/action',
        'Adventure': 'http://www.imdb.com/genre/adventure',
        'Animation': 'http://www.imdb.com/genre/animation',
        'Biography': 'http://www.imdb.com/genre/biography',
        'Comedy': 'http://www.imdb.com/genre/comedy',
        'Crime': 'http://www.imdb.com/genre/crime',
        'Documentary': 'http://www.imdb.com/genre/documentary',
        'Drama': 'http://www.imdb.com/genre/drama',
        'Family': 'http://www.imdb.com/genre/family',
        'Fantasy': 'http://www.imdb.com/genre/fantasy',
        'Film-Noir': 'http://www.imdb.com/genre/film_noir',
        'History': 'http://www.imdb.com/genre/history',
        'Horror': 'http://www.imdb.com/genre/horror',
        'Music': 'http://www.imdb.com/genre/music',
        'Musical': 'http://www.imdb.com/genre/music',
        'Mystery': 'http://www.imdb.com/genre/mystery',
        'Romance': 'http://www.imdb.com/genre/romance',
        'Sci-Fi': 'http://www.imdb.com/genre/sci_fi',
        'Sport': 'http://www.imdb.com/genre/sport',
        'Thriller': 'http://www.imdb.com/genre/thriller',
        'War': 'http://www.imdb.com/genre/war',
        'Western': 'http://www.imdb.com/genre/western'}

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
    filmIMDB = str(random.choice(filmList["IMDB"]))
    return filmIMDB

def sendFLStatus(filmCount, message):
    answer1 = 'Список успешно загружен.\nВ списке ' + str(filmCount) + " элементов."
    answer2 = '\nТеперь можете выбрать случайный фильмы командой /random'
    answer = answer1 + answer2
    bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types='text')
def answer(message):
    global filmList


    if "/random" in message.text:
        if filmList:
            filmIMDB = getRandom(filmList)
            filmTitle, filmYear, filmDirector, filmGenre, filmCountry, filmPlot, filmRuntime, filmRating, filmScore, filmURL, filmPoster = getInfo(
                filmIMDB)
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
                answer = answer1 + answer2
            except UnboundLocalError:
                answer1 = filmTitle + " (" + filmYear + ")\n" + filmDirector + "\n" + filmGenre + " / " + filmCountry
                answer2 = "\n\n" + filmPlot + "\n\n" + filmRuntime + " / " + filmRating + " / " + filmScore
                answer = answer1 + answer2
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="Подбробнее о " + filmTitle, url=filmURL))
            except ValueError:
                print(filmURL)
            DLLink = filmTitle + " " + filmYear
            RuTracker = 'http://rutracker.org/forum/tracker.php?nm=' + re.sub(r' +', '%20', DLLink)
            PirateBay = "https://thepiratebay.org/search/" + re.sub(r' +', '%20', DLLink)
            RarBG = "https://rarbg.to/torrents.php?search=" + re.sub(r' +', '+',
             DLLink) + "&category%5B%5D=14&category%5B%5D=48&category%5B%5D=17&category%5B%5D=44&category%5B%5D=45&category%5B%5D=47&category%5B%5D=42&category%5B%5D=46"
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rutracker.org", url=RuTracker))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на piratebay.org", url=PirateBay))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rarbg.com", url=RarBG))
            poster = urllib.request.urlopen(filmPoster)
            bot.send_photo(message.chat.id, poster)
            bot.send_message(message.chat.id, answer, reply_markup=keyboard)
            bot.send_message(message.chat.id, "Не то? Нажимай на /random")
            bot.send_message(message.chat.id, "Другой лист? Нажимай на /lists")
        else:
            if message.chat.first_name:
                answer1 = "Привет, " + str(message.chat.first_name) + ". Ты еще не выбрал список фильмов."
            else:
                answer1 = "Привет. Ты еще не выбрал список фильмов."
            answer2 = '\nВоспользуйся командой /start, чтобы узнать подробности.'
            answer = answer1 + answer2
            bot.send_message(message.chat.id, answer)
    if "/start" in message.text or "/lists" in message.text:
        if message.chat.first_name:
            answer1 = 'Привет, ' + message.chat.first_name + ". Выбери одну из следующих команд для выбора списка:\n"

        else:
            answer1 = 'Привет. Выбери одну из следующих команд для выбора списка:\n'

        file = open('greetings.txt', 'r')
        answerarray = []
        answer2 = ""
        for line in file:
            answer2 = answer2 + line
        file.close()
        answer = answer1 + answer2
        bot.send_message(message.chat.id, answer)
    if "/imdb250" in message.text:
        answer = 'Вы выбрали список "Топ 250 фильмов IMDB"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getList(urls['Top 250'])
        sendFLStatus(filmCount, message)
    if "/imdbmp" in message.text:
        answer = 'Вы выбрали список "Самые популярные фильмы IMDB"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getList(urls['Most Popular'])
        sendFLStatus(filmCount, message)
    if "/imdbeng" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы на Английском"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListge(urls['Top English'])
        sendFLStatus(filmCount, message)
    if "/gactions" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре экшн."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Actions'])
        sendFLStatus(filmCount, message)
    if "/ganimations" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре анимация."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Animation'])
        sendFLStatus(filmCount, message)
    if "/gadventure" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре приключения."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Adventure'])
        sendFLStatus(filmCount, message)
    if "/gbio" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре биографический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Biography'])
        sendFLStatus(filmCount, message)
    if "/gcomedy" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре комедия."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Comedy'])
        sendFLStatus(filmCount, message)
    if "/gcrime" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре криминал."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Crime'])
        sendFLStatus(filmCount, message)
    if "/gdoc" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре документальный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Documentary'])
        sendFLStatus(filmCount, message)
    if "/gdrama" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре драма."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Drama'])
        sendFLStatus(filmCount, message)
    if "/gfamily" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм для все семьи."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Family'])
        sendFLStatus(filmCount, message)
    if "/gfantasy" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фэнтези."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Fantasy'])
        sendFLStatus(filmCount, message)
    if "/gnoir" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм-нуар."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Film-Noir'])
        sendFLStatus(filmCount, message)
    if "/ghistory" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре исторический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['History'])
        sendFLStatus(filmCount, message)
    if "/ghorror" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре хоррор."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Horror'])
        sendFLStatus(filmCount, message)
    if "/gmusic" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре музыкальный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Music'])
        sendFLStatus(filmCount, message)
    if "/gmusic" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре мюзикл."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Musical'])
        sendFLStatus(filmCount, message)
    if "/gmystery" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре детектив"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Mystery'])
        sendFLStatus(filmCount, message)
    if "/gromance" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре романтический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Romance'])
        sendFLStatus(filmCount, message)
    if "/gscifi" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре научная фантастика."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Sci-Fi'])
        sendFLStatus(filmCount, message)
    if "/gsport" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре спортивный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Sport'])
        sendFLStatus(filmCount, message)
    if "/gthriller" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре триллер."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Thriller'])
        sendFLStatus(filmCount, message)
    if "/gwar" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм про войну."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['War'])
        sendFLStatus(filmCount, message)
    if "/gwestern" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре вестерн."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        filmList, filmCount = imdb.getListGenre(urls['Western'])
        sendFLStatus(filmCount, message)

@bot.message_handler(content_types='document')
def handle_csv(message):
    type = message.document.mime_type
    bot.send_message(message.chat.id, "Это %s. Я такие файлы читать не умею." %type)

if __name__ == '__main__':
    bot.polling(none_stop=True)


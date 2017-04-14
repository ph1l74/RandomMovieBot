import telebot
import config
import random
import datetime
import urllib
import codecs
import re
import json
import imdbparser as imdb
from urllib.request import Request

print("Modules imported")

# defining bot:

bot = telebot.TeleBot(config.token)

# list of clients:

clients = []

# default dictionary that will be filled:

film_list = {}

# date for logs:

now = datetime.datetime.now()
date = datetime.time(now.hour, now.minute, now.second)

# different URLs of film lists:

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

# defining funcs:


def get_info(title):
    # making URL for OMDB API request
    jsonurl = "http://www.omdbapi.com/?i=" + title + "&plot=short&r=json"
    # getting JSON-response
    response = urllib.request.urlopen(jsonurl)
    # decode response to UTF-8
    reader = codecs.getreader('utf-8')
    # getting data from decoded response
    data = json.load(reader(response))
    # writing info from data in variables
    film_title = data['Title']
    film_year = data['Year']
    film_dir = data['Director']
    film_genre = data['Genre']
    film_country = data['Country']
    film_plot = data['Plot']
    film_rt = data['Runtime']
    film_rating = data['imdbRating']
    film_score = data['Metascore']
    film_url = "http://www.imdb.com/title/" + str(data['imdbID'])
    film_img = data['Poster']
    return film_title, film_year, film_dir, film_genre, film_country, film_plot, film_rt, film_rating, film_score, \
           film_url, film_img


def get_random(film_list):
    # chosing random imdb-id from film_list
    film_imdb = str(random.choice(film_list["IMDB"]))
    return film_imdb


def send_fl_status(film_count, message):
    answer1 = 'Список успешно загружен.\nВ списке ' + str(film_count) + " элементов."
    answer2 = '\nТеперь можете выбрать случайный фильмы командой /random'
    answer = answer1 + answer2
    bot.send_message(message.chat.id, answer)

# message handler for text message:


@bot.message_handler(content_types='text')
def answer(message):
    global film_list, date
    emoji = u'\U00002753'

    if message.chat.id not in clients:
        clients.append(message.chat.id)
        print("New chat:" + str(message.chat.id))

    print(str(date) + ":" + str(message.chat.id) + ":" + str(message.chat.first_name) + ": " + str(message.text))

    if "/random" in message.text:
        if film_list:
            film_imdb = get_random(film_list)
            film_title, film_year, film_dir, film_genre, film_country, film_plot, film_rt, film_rating, film_score, \
                film_url, film_img = get_info(film_imdb)
            try:
                if film_score == "N/A":
                    emoji = u'\U00002753'
                elif 0 < int(film_score) < 20:
                    emoji = u'\U0001F232'
                elif 21 < int(film_score) < 45:
                    emoji = u'\U0001F21A'
                elif 46 < int(film_score) < 60:
                    emoji = u'\U0001F233'
                elif 61 < int(film_score) < 80:
                    emoji = u'\U0001F22F'
                elif 81 < int(film_score) < 100:
                    emoji = u'\U0001F4AF'
                answer1 = film_title + " (" + film_year + ")\n" + film_dir + "\n" + film_genre + " / " + film_country
                answer2 = "\n\n" + film_plot + "\n\n" + film_rt + " / " + film_rating + " / " + film_score + " " + emoji
                answer = answer1 + answer2
            except UnboundLocalError:
                answer1 = film_title + " (" + film_year + ")\n" + film_dir + "\n" + film_genre + " / " + film_country
                answer2 = "\n\n" + film_plot + "\n\n" + film_rt + " / " + film_rating + " / " + film_score
                answer = answer1 + answer2
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="Подбробнее о " + film_title, url=film_url))
            except ValueError:
                print(film_url)
            dll_link = film_title + " " + film_year
            rutracker = 'http://rutracker.org/forum/tracker.php?nm=' + re.sub(r' +', '%20', dll_link)
            piratebay = "https://thepiratebay.org/search/" + re.sub(r' +', '%20', dll_link)
            rarbg = "https://rarbg.to/torrents.php?search=" + re.sub(r' +', '+',
             dll_link) + "&category%5B%5D=14&category%5B%5D=48&category%5B%5D=17&category%5B%5D=44&category%5B%5D=45&category%5B%5D=47&category%5B%5D=42&category%5B%5D=46"
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rutracker.org", url=rutracker))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на piratebay.org", url=piratebay))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Искать на rarbg.com", url=rarbg))
            poster = urllib.request.urlopen(film_img)
            bot.send_photo(message.chat.id, poster)
            bot.send_message(message.chat.id, answer, reply_markup=keyboard)
            bot.send_message(message.chat.id, "Не то? Нажимай на /random")
            bot.send_message(message.chat.id, "Другой лист? Нажимай на /lists")
            print(str(date) + ":" + str(message.chat.id) + ":Bot: " + film_title + " (" + str(film_year) + ") " + "URL: " + film_url)
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
        film_list, film_count = imdb.get_list(urls['Top 250'])
        send_fl_status(film_count, message)
    if "/imdbmp" in message.text:
        answer = 'Вы выбрали список "Самые популярные фильмы IMDB"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list(urls['Most Popular'])
        send_fl_status(film_count, message)
    if "/imdbeng" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы на Английском"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list(urls['Top English'])
        send_fl_status(film_count, message)
    if "/gactions" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре экшн."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Actions'])
        send_fl_status(film_count, message)
    if "/ganimations" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре анимация."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Animation'])
        send_fl_status(film_count, message)
    if "/gadventure" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре приключения."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Adventure'])
        send_fl_status(film_count, message)
    if "/gbio" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре биографический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Biography'])
        send_fl_status(film_count, message)
    if "/gcomedy" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре комедия."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Comedy'])
        send_fl_status(film_count, message)
    if "/gcrime" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре криминал."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Crime'])
        send_fl_status(film_count, message)
    if "/gdoc" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре документальный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Documentary'])
        send_fl_status(film_count, message)
    if "/gdrama" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре драма."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Drama'])
        send_fl_status(film_count, message)
    if "/gfamily" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм для все семьи."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Family'])
        send_fl_status(film_count, message)
    if "/gfantasy" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фэнтези."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Fantasy'])
        send_fl_status(film_count, message)
    if "/gnoir" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм-нуар."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Film-Noir'])
        send_fl_status(film_count, message)
    if "/ghistory" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре исторический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['History'])
        send_fl_status(film_count, message)
    if "/ghorror" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре хоррор."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Horror'])
        send_fl_status(film_count, message)
    if "/gmusic" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре музыкальный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Music'])
        send_fl_status(film_count, message)
    if "/gmusic" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре мюзикл."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Musical'])
        send_fl_status(film_count, message)
    if "/gmystery" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре детектив"\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Mystery'])
        send_fl_status(film_count, message)
    if "/gromance" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре романтический фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Romance'])
        send_fl_status(film_count, message)
    if "/gscifi" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре научная фантастика."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Sci-Fi'])
        send_fl_status(film_count, message)
    if "/gsport" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре спортивный фильм."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Sport'])
        send_fl_status(film_count, message)
    if "/gthriller" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре триллер."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Thriller'])
        send_fl_status(film_count, message)
    if "/gwar" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре фильм про войну."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['War'])
        send_fl_status(film_count, message)
    if "/gwestern" in message.text:
        answer = 'Вы выбрали список "Лучшие фильмы в жанре вестерн."\nПодождите, пока список загрузится.'
        bot.send_message(message.chat.id, answer)
        film_list, film_count = imdb.get_list_genre(urls['Western'])
        send_fl_status(film_count, message)

# check for message doc type:


@bot.message_handler(content_types='document')
def handle_csv(message):
    bot.send_message(message.chat.id, "Я с файлами не работаю")

# starting bot:

if __name__ == '__main__':
    print("Bot started")
    bot.polling(none_stop=True)

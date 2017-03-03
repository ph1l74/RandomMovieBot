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
import kinoparser

print("Modules imported")

mode = {'Kinopoisk': False, 'IMDB': False}

bot = telebot.TeleBot(config.demo_token)

if bot:
    print("Bot started")

def kinopoiskParser(url):
    print("KP")

def imdbParser(url):
    print("IMDB")


@bot.message_handler(content_types='text')
def answer(message):
    if message.text == '/start':
        answer = "Привет, " + str(message.chat.first_name) + "! Введи сылку на свой аккаунт на Кинопоиске или IMDb"
        bot.send_message(message.chat.id, answer)
    elif "kinopoisk.ru/user/" in str(message.text):
        pattern = re.compile(r"(kinopoisk.ru/user/)(\d{1,})")
        search = re.search(pattern, message.text)
        kinoparser.getList(search.group(2))
    elif "imdb.com/user/ur" in str(message.text):
        pattern = re.compile(r"(imdb.com/user/ur)(\d{1,})")
        search = re.search(pattern, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)


import telebot
import config
import random

nikitabot = telebot.TeleBot(config.nikita_token)

phrases = ["Пошел нахуй, педрила, че ты мне пишешь?",
           "Я тебя не знаю, и знать не хочу ",
           "Ты на что намекаешь, паскуда?",
           "Ты -- пидор!",
           "В голосину со старинной дембельской песни.",
           "Мальчики похожи на качков.",
           "Бля, ты объебался опять чем-то?",
           "Я тебя не понимаю",
           "ТАЩЕМТА ГОДНО",
           "ДОРОГАЯ МОЯ СТОЛИЦА \nДОРОГОЙ МОЙ ФК СПАРТАК",
           "ООООООООООООООООО \nМОЯ ОБОРОНА",
           "Ебанистически тупой мудак",
           "Ай, бля, да что это я",
           "Хуесос. Какой же хуесос...",
           "Нет пути...",
           "Уезжают в родные края\nДембеля-дембеля-дембеля...",
           "Короче смотри, есть два стула...",
           "Жувебляди, миланопидоры, интердевочки, лациохуесосы, наполиопцщенцы. Ты кем будешь?",
           "Душа твоя — говно собачье, и все, что в тебе, блядь, есть — сплошное уродство."]

@nikitabot.message_handler(content_types='text')
def answer(message):
    answer = random.choice(phrases)
    print("From " + str(message.chat.username) + ": " + message.text)
    nikitabot.send_message(message.chat.id, answer)
    print("To " + str(message.chat.username) + ": " + answer)

@nikitabot.message_handler(content_types='document')
def answer(message):
    nikitabot.send_message(message.chat.id, "Нет")

if __name__ == '__main__':
        nikitabot.polling(none_stop=True)
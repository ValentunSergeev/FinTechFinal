import telegram
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from utils import load, clean_text, get_results
from constants import labels, common_requests, non_fin_words, cake, right_ans, wrong_ans
from collections import defaultdict
from threading import Thread, Lock
import time
import logging

TOKEN = "367594980:AAH7lIPlY51RHMyTqolXxCPMqn9KkH2E-M0"

user_states = {}
user_themes = {}
user_attempts = defaultdict(lambda: [0, 0]) # 0 - wrong theme number, 1 - wrong themes list
user_times = defaultdict(lambda: [0, True])  # time, is received

clf = load('saved_clf.pkl')
vect = load('vectorizer.pkl')

bot = telegram.Bot(token=TOKEN)


def predict(bot, update):
    chat_id = update.message.chat_id
    msg = ''
    if update.message.text.lower not in non_fin_words:  # TODO change check alg
        results = get_results(clf, vect, clean_text(update.message.text))  # TODO check if themes is empty
        user_themes[chat_id] = [i[0] for i in results]

        if results[0][1] / results[1][1] > 3:
            msg += "Вас интересует тема \"" + labels[int(results[0][0])] + "\". Да?"
            custom_keyboard = [["Да"], ["Нет"]]
            mode = "SINGLE"
        else:
            msg += "Пожалуйста, уточните, какая тема вас интересует(Введите номер или выбирите в списке)"
            custom_keyboard = [[str(i + 1) + '. ' + labels[int(results[i][0])]] for i in range(4)]
            custom_keyboard.append(["0. Никакая из этих тем не подходит"])
            mode = "MULTIPLE"

        user_times[chat_id] = [time.time(), False, mode]
        user_states[chat_id] = 'CHECK'

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text=msg, reply_markup=reply_markup)
    else:
        msg += cake
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)


def check_time():
    lock = Lock()
    while True:
        with lock:
            for chat_id, t in user_times.items():
                delta = round(time.time() - float(t[0]))
                if t[0] != 0:
                    if not t[1] and delta == 30:
                        if t[2] == "SINGLE":
                            bot.sendMessage(chat_id=chat_id, text="Мне нужен ваш ответ. Напишите \"да\" или \"нет\"")
                        else:
                            msg = "Я все еще хочу вам помочь. Уточните, какая тема вас интересует:\n"
                            for i in range(4):
                                msg += str(i + 1) + '. ' + labels[int(user_themes[chat_id][i])] + '\n'
                            msg += "0. Никакая из этих тем не подходит"
                            bot.sendMessage(chat_id=chat_id, text=msg)
                        user_times[chat_id][1] = True
                    if delta >= 210:
                        user_times[chat_id][0] = 0
                        user_states[chat_id] = 'PREDICT'
        time.sleep(1)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Привет! Я могу помочь вам с вопросами в финансовой области. Прсто спросите!")


def text(bot, update):
    chat_id = update.message.chat_id
    msg = ''

    if chat_id not in user_states:
        user_states[chat_id] = 'PREDICT'

    if user_states[chat_id] == 'PREDICT':
        predict(bot, update)
    else:
        if update.message.text.lower() in [str(i) for i in range(1, 5)] or update.message.text.lower() in right_ans \
                or update.message.text.lower()[3:] in [labels[int(user_themes[chat_id][i])].lower() for i in range(4)]:
            user_times[chat_id][0] = 0
            theme = user_themes.get(chat_id, [''])[0]

            msg += common_requests.get(theme, '')
            msg += common_requests.get(update.message.text.lower(), '')
            msg += "В ближайшее время на ваш запрос ответит оператор."

            bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=ReplyKeyboardRemove())

            user_states[chat_id] = 'PREDICT'

            user_themes[chat_id] = []  # TODO move to if
        elif update.message.text.lower()[3:] in wrong_ans:
            user_times[chat_id][0] = 0
            msg += "Не смогли определить тему вашего вопроса. Попробуйте перефразировать вопрос"

            bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=ReplyKeyboardRemove())
            user_states[chat_id] = 'PREDICT'  # TODO slice user_themes
        elif update.message.text.lower()[0] not in ['1', '2', '3', '4', '0']:
            predict(bot, update)
        else:
            if user_attempts[chat_id][0] == 2:
                msg = "ОК, похоже, мы оба запутались, давайте начнем заново :)"
                user_attempts[chat_id][0] = 0
                user_states[chat_id] = "PREDICT"
            else:
                msg += "Номер темы указан непрально."
                user_attempts[chat_id][0] += 1
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)


thread = Thread(target=check_time)
thread.start()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, text)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()

print("All components was successfully loaded.")

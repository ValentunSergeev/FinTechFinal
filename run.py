import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from utils import load, clean_text
from constants import labels, common_requests
import logging

TOKEN = "367594980:AAH7lIPlY51RHMyTqolXxCPMqn9KkH2E-M0"

user_states = {}
user_themes = {}

clf = load('saved_clf.pkl')
vect = load('vectorizer.pkl')


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Привет! Я могу помочь вам с вопросами в финансовой области. Прсто спросите!")


def text(bot, update):
    chat_id = update.message.chat_id
    msg = ''

    if chat_id not in user_states:
        user_states[chat_id] = 'PREDICT'

    if user_states[chat_id] == 'PREDICT':
        if True:  # TODO check if non-fin
            text = clean_text(update.message.text)
            theme = clf.predict(vect.transform([text]))

            answer = int(theme[0])
            user_themes[chat_id] = answer

            msg += "Вас интересует тема \"" + labels[answer] + "\". Да?"
            user_states[chat_id] = 'CHECK'

            custom_keyboard = [["Да"], ["Нет"]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
            bot.sendMessage(chat_id=chat_id, text=msg, reply_markup=reply_markup)
        else:
            msg += "Не похоже на фин текст. Попробуйте еще раз :)"
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    else:
        if update.message.text.lower() == 'нет':
            msg += "Не смогли определить тему вашего вопроса. Попробуйте перефразировать вопрос"
        else:
            theme = user_themes.get(chat_id, '')
            print(theme)
            msg += common_requests.get(theme, '')
            msg += "В ближайшее время на ваш запрос ответит оператор."

        bot.sendMessage(chat_id=update.message.chat_id, text=msg)

        user_themes[chat_id] = ''
        user_states[chat_id] = 'PREDICT'


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

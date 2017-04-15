from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import logging

TOKEN = "367594980:AAH7lIPlY51RHMyTqolXxCPMqn9KkH2E-M0"

user_states = {}


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def text(bot, update):
    chat_id = update.message.chat_id
    msg = ''

    if chat_id not in user_states:
        user_states[chat_id] = 'PREDICT'

    if user_states[chat_id] == 'PREDICT':
        if True:  # TODO check if
            # TODO predict logic
            msg = "Вас интересует <тема>. Да?"
            user_states[chat_id] = 'CHECK'
        else:
            msg = "Не похоже на фин текст. Попробуйте еще раз :)"
    else:
        if update.message.text == 'нет':
            msg = "Не смогли определить тему вашего вопроса. Попробуйте перефразировать вопрос"
        else:
            msg = "Окей" # TODO msg assignment from theme

        user_states[chat_id] = 'PREDICT'

    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, text)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()

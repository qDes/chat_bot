import logging
import os
import uuid

from dotenv import load_dotenv
from log_tools import TelegramLogsHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialog import fetch_dialogflow_answer


logger = logging.getLogger("chat_bot")


def start(bot, update):
    update.message.reply_text('Привет! Я бот помощник. Задавайте свои вопросы.')


def help(bot, update):
    update.message.reply_text('Help!')


def reply(bot, update):
    google_project_id = os.environ["GOOGLE_PROJECT_ID"]
    google_session_id = str(uuid.uuid4())
    language_code = "ru-RU"
    user_text = update.message.text
    reply, fallback = fetch_dialogflow_answer(google_project_id,
                                              google_session_id,
                                              user_text,
                                              language_code)
    update.message.reply_text(reply)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_token, chat_id))
    logger.info("start tg chat bot")
    updater = Updater(tg_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

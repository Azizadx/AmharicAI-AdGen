import telebot
from telebot import types
from config import TELEGRAM_TOKEN
from config import BASE_URL as BaseUrl

BOT_TOKEN = TELEGRAM_TOKEN
BASE_URL= BaseUrl

bot = telebot.TeleBot(BOT_TOKEN)

keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("About")
button2 = types.KeyboardButton("Help")
keyboard_markup.add(button1, button2)

def handle_start(message):
    bot.reply_to(message, "Hello! Welcome to AdBar", reply_markup=keyboard_markup)


def handle_message(message):
    if message.text == "About":
        bot.reply_to(message, "AiQEM is an African startup focused on AI and Blockchain business solutions")

def handle_message(message):
    if message.text == "Help":
        bot.reply_to(message, "Help is on the way.....")

def main():
    bot.polling()

if __name__ == "__main__":
    main()


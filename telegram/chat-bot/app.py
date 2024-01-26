import telebot
from telebot import types
from config import TELEGRAM_TOKEN
from config import BASE_URL as BaseUrl

BOT_TOKEN = TELEGRAM_TOKEN
BASE_URL = BaseUrl

bot = telebot.TeleBot(BOT_TOKEN)

keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("About")
button2 = types.KeyboardButton("Help")
keyboard_markup.add(button1, button2)

# Define inline keyboard
inline_keyboard = types.InlineKeyboardMarkup()
webapp_button = types.InlineKeyboardButton(text="Open Web App", url=BASE_URL)
inline_keyboard.add(webapp_button)

def handle_start(message):
    bot.reply_to(message, "Hello! Welcome to AdBar", reply_markup=keyboard_markup)

def handle_message(message):
    if message.text == "About":
        bot.reply_to(message, "AiQEM is an African startup focused on AI and Blockchain business solutions")
    elif message.text == "Help":
        bot.reply_to(message, "Help is on the way.....")
    elif message.text == "Open Web App":
        bot.reply_to(message, "Get Started:", reply_markup=inline_keyboard)

def main():
    bot.polling(none_stop=True, interval=10)  # Poll every 5 seconds

if __name__ == "__main__":
    main()

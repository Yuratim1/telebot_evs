import telebot
from telebot import types
import re
import requests
import inspect


bot = telebot.TeleBot("")

back_slash = "\n"
user_dict = {}

##################################### BOT ENTRY POINT START ######################################
@bot.message_handler(commands=['start'], chat_types=["private"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=True)
    regButton = types.KeyboardButton(text="Register \U0001F4C4", request_contact=False)
    searchButton = types.KeyboardButton(text="Search \U0001F50E")
    aboutButton = types.KeyboardButton(text="Premium \U0001F48E")
    premiumButton = types.KeyboardButton(text="About Us \U0001F4F0")
    markup.row(regButton)
    markup.row(searchButton)
    markup.row(aboutButton)
    markup.row(premiumButton)
    bot.send_message(message.from_user.id, "Choose an option below:", reply_markup = markup)
    print(message.from_user.id)
    print("message text->" + message.text)
##################################### BOT ENTRY POINT END ######################################
##################################### BOT MENU HANDLER START ######################################
@bot.message_handler(content_types=['text'])
def menu_handler(message):
    print(message)
    print(message.text)
    regSearch = re.split("\s", message.text, 1)
    print(regSearch)

    match regSearch[0]:
        case "Register":
            print("Register")
        case "Search":
            print("Search")
        case "Premium":
            print("Premium")
        case "About":
            print("AboutUs")

##################################### BOT MENU HANDLER END ######################################

bot.infinity_polling()
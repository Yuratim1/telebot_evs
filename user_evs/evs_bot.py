import telebot
from telebot import types
import re
from dataclasses import dataclass, field
from datetime import datetime
# import requests
# import inspect


bot = telebot.TeleBot("6236528384:AAEdxftW-3UsYIhEqrI3D7is9ecObwRZkWY")

back_slash = "\n"
user_dict = {}
categArray = ["SocialMedia", "Animals", "Theatre", "PermacultureFarming", "EventAssistance",
              "Education", "Sport", "RefugeeMigrants", "CultureArt", "DisabledPeople",
              "YoungPeople", "HealthCare", "SocialWork", "Environment", "SchoolKindergarten",
              "AwarnessRaisingCampaign"]

@dataclass
class Person:
    userid: int
    registerDate: int = 0
    premium: bool = False
    categoryselect: list[str] = field(init=False, default_factory=list)
    countryselect: list[str] = field(init=False, default_factory=list)


##################################### BOT ENTRY POINT START ######################################
@bot.message_handler(commands=['start'], chat_types=["private"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=False)
    regButton = types.KeyboardButton(text="Register \U0001F4C4", request_contact=False)
    searchButton = types.KeyboardButton(text="Sign In \U0001F50E")
    aboutButton = types.KeyboardButton(text="About Us \U0001F4F0")
    markup.row(regButton)
    markup.row(searchButton)
    markup.row(aboutButton)
    welcomeText = "Welcome to the EVS search project" \
                  " here you can search for available projects depending on your selection" \
                  " please register first so we know which countries and" \
                  " what projects you want to find "
    bot.send_message(message.from_user.id, welcomeText, reply_markup = markup)
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
            registration(message)
        case "Sign":
            print("Sign")
        case "About":
            print("AboutUs")

##################################### BOT MENU HANDLER END ######################################
##################################### BOT REGISTRATION START ######################################
def registration(message):
    print(message.from_user.id)
    print(message.date)
    # currentUserClass = Person(userid=message.from_user.id)
    
    
    keyboard = []
        
    for i, button in enumerate(categArray):
        keyboard.append([types.InlineKeyboardButton(button , callback_data=f"{button}")])

    reply_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.from_user.id, "Please choose the category you interested in", reply_markup = reply_markup)
    






##################################### ABOUT BUTTON START ######################################
def aboutUs(message):
    pass


##################################### ABOUT BUTTON END ######################################

bot.infinity_polling()
# if __name__ == "__main__":
#     start()
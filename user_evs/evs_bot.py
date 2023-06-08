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
countriesArray = ["Albania", "Austria", "Belgium", "Bosnia", "Bulgaria",
                  "Croatia", "Czech", "Denmark", "Estonia", "Finland", "France",
                  "Germany", "Greece", "Hungary", "Italy", "Latvia", "Lithuania", "Luxembourg",
                  "Malta", "Moldova", "Montenegro", "Netherlands", "Macedonia", "Norway",
                  "Poland", "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Spain",
                  "Sweden", "Switzerland", "Turkey"]

@dataclass
class Person:
    userid: int
    registerDate: int = 0
    premium: bool = False
    categoryselect: list[str] = field(init=False, default_factory=list)
    countryselect: list[str] = field(init=False, default_factory=list)

    @property
    def category_array(self):
        return self.categoryselect
    
    @category_array.setter
    def category_array(self, categ)
        self.categoryselect.append(categ)

    
    @property
    def country_array(self):
        return self.countryselect
    
    @country_array.setter
    def country_array(self, country):
        self.countryselect.append(country)

    # @property
    # def reg_date(self)
    #     return self.registerDate
    
    # @reg_date.setter
    # def reg_date(self, reg):
        



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
    keyboard = types.InlineKeyboardMarkup(row_width=3, )
    albania = types.InlineKeyboardButton('Albania', callback_data='Albania')
    austria = types.InlineKeyboardButton('Austria', callback_data='Austria')
    belgium = types.InlineKeyboardButton('Belgium', callback_data='Belgium')
    bosnia = types.InlineKeyboardButton('Bosnia and Herzegovina', callback_data='Bosnia')
    bulgaria = types.InlineKeyboardButton('Bulgaria', callback_data='Bulgaria')
    croatia = types.InlineKeyboardButton('Croatia', callback_data='Croatia')
    czech = types.InlineKeyboardButton('Czech Republic', callback_data='Czech')
    denmark = types.InlineKeyboardButton('Denmark', callback_data='Denmark')
    estonia = types.InlineKeyboardButton('Estonia', callback_data='Estonia')
    finland = types.InlineKeyboardButton('Finland', callback_data='Finland')
    france = types.InlineKeyboardButton('France', callback_data='France')
    germany = types.InlineKeyboardButton('Germany', callback_data='Germany')
    greece = types.InlineKeyboardButton('Greece', callback_data='Greece')
    hungary = types.InlineKeyboardButton('Hungary', callback_data='Hungary')
    italy = types.InlineKeyboardButton('Italy', callback_data='Italy')
    latvia = types.InlineKeyboardButton('Latvia', callback_data='Latvia')
    lithuania = types.InlineKeyboardButton('Lithuania', callback_data='Lithuania')
    luxembourg = types.InlineKeyboardButton('Luxembourg', callback_data='Luxembourg')
    malta = types.InlineKeyboardButton('Malta', callback_data='Malta')
    moldova = types.InlineKeyboardButton('Moldova', callback_data='Moldova')
    montenegro = types.InlineKeyboardButton('Montenegro', callback_data='Montenegro')
    netherlands = types.InlineKeyboardButton('Netherlands', callback_data='Netherlands')
    macedonia = types.InlineKeyboardButton('Macedonia', callback_data='Macedonia')
    norway = types.InlineKeyboardButton('Norway', callback_data='Norway')
    poland = types.InlineKeyboardButton('Poland', callback_data='Poland')
    portugal = types.InlineKeyboardButton('Portugal', callback_data='Portugal')
    romania = types.InlineKeyboardButton('Romania', callback_data='Romania')
    serbia = types.InlineKeyboardButton('Serbia', callback_data='Serbia')
    slovakia = types.InlineKeyboardButton('Slovakia', callback_data='Slovakia')
    spain = types.InlineKeyboardButton('Spain', callback_data='Spain')
    sweden = types.InlineKeyboardButton('Sweden', callback_data='Sweden')
    switzerland = types.InlineKeyboardButton('Switzerland', callback_data='Switzerland')
    turkey = types.InlineKeyboardButton('Turkey', callback_data='Turkey')
    keyboard.add(albania, austria, belgium)
    keyboard.add(bosnia, bulgaria)
    keyboard.add(croatia, czech)
    keyboard.add(denmark, estonia, finland)
    keyboard.add(france, germany, greece)
    keyboard.add(hungary, italy, latvia)
    keyboard.add(lithuania, luxembourg)
    keyboard.add(malta, moldova, montenegro)
    keyboard.add(netherlands, macedonia)
    keyboard.add(norway, poland, portugal)
    keyboard.add(romania, serbia, slovakia)
    keyboard.add(spain, sweden)
    keyboard.add(switzerland, turkey)
    country_text = "Choose a country in which the project will take place"
    bot.send_message(message.from_user.id, text=country_text, reply_markup=keyboard)
    print(message.text)
    print(message.id)

@bot.add_callback_query_handler(func= lambda message.text: )
def CategorySelect(message):
    print(message.text)
    print(message.id)

##################################### ABOUT BUTTON START ######################################
def aboutUs(message):
    pass

##################################### ABOUT BUTTON END ######################################

bot.infinity_polling()
# if __name__ == "__main__":
#     start()
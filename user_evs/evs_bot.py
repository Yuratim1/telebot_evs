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
categArray = ["Social Media", "Animals", "Theatre", "Permaculture Farming", "Event Assistance",
              "Education", "Sport", "Refugee/Migrants", "Culture/Art", "Disabled People",
              "Young People", "HealthCare", "Social Work", "Environment", "School/Kindergarten",
              "Awarness Raising Campaign"]
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
    def category_array(self, categ):
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

##################################### DB COMMIT NEW USER START ######################################
def db_commit():
    pass

##################################### DB COMMIT NEW USER END ######################################
##################################### BOT ENTRY POINT START ######################################
@bot.message_handler(commands=['start'], chat_types=["private"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, one_time_keyboard=True)
    regButton = types.KeyboardButton(text="Register \U0001F4C4", request_contact=False)
    searchButton = types.KeyboardButton(text="Sign In \U0001F50E")
    aboutButton = types.KeyboardButton(text="About Us \U0001F4F0")
    markup.row(regButton)
    markup.row(searchButton)
    markup.row(aboutButton)
    welcomeText = "Welcome to the EVS search project" \
                  " here you can search for available projects depending on your selection" \
                  " please register first so we know which countries and" \
                  " what projects you are interested in"
    bot.send_message(message.from_user.id, welcomeText, reply_markup = markup)
    # print(message.from_user.id)
    # print("message text->" + message.text)
##################################### BOT ENTRY POINT END ######################################
##################################### BOT MENU HANDLER START ######################################
@bot.message_handler(content_types=['text'])
def menu_handler(message):
    # print(message)
    # print(message.text)
    regSearch = re.split("\s", message.text, 1)
    print(regSearch)

    match regSearch[0]:
        case "Register":
            registrationStart(message)
        case "Sign":
            print("Sign")
        case "About":
            print("AboutUs")

##################################### BOT MENU HANDLER END ######################################
##################################### BOT REGISTRATION START ######################################
def registrationStart(message):

    CountryKeyboard = types.InlineKeyboardMarkup(row_width=4)
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
    CountryKeyboard.add(albania, austria, belgium, bosnia)
    CountryKeyboard.add(bulgaria, croatia, czech, denmark)
    CountryKeyboard.add(denmark, estonia, finland)
    CountryKeyboard.add(france, germany, greece)
    CountryKeyboard.add(hungary, italy, latvia)
    CountryKeyboard.add(lithuania, luxembourg)
    CountryKeyboard.add(malta, moldova, montenegro)
    CountryKeyboard.add(netherlands, macedonia)
    CountryKeyboard.add(norway, poland, portugal)
    CountryKeyboard.add(romania, serbia, slovakia)
    CountryKeyboard.add(spain, sweden)
    CountryKeyboard.add(switzerland, turkey)
    country_text = "Choose a country in which the project will take place:"
    bot.send_message(message.from_user.id, text=country_text, reply_markup=CountryKeyboard)
    # print(message.id)
    # print(message)
    # print(message.chat.id)
    

@bot.callback_query_handler(func= lambda message: message.data in countriesArray)
def CountrySelected(message):
    selected_country = message.data
    bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=f"Choose a country in which the project will take place:{back_slash}Country Selected -> {selected_country}",
        reply_markup=None
    )
    CategKeyboard = types.InlineKeyboardMarkup(row_width=3)
    socialmedia = types.InlineKeyboardButton('Social Media', callback_data='Social Media')
    animals = types.InlineKeyboardButton('Animals', callback_data='Animals')
    theatre = types.InlineKeyboardButton('Theatre', callback_data='Theatre')
    permaculturefarming = types.InlineKeyboardButton('Permaculture Farming', callback_data='Permaculture Farming')
    eventassistance = types.InlineKeyboardButton('Event Assistance', callback_data='Event Assistance')
    education = types.InlineKeyboardButton('Education', callback_data='Education')
    sport = types.InlineKeyboardButton('Sport', callback_data='Sport')
    refugeemigrants = types.InlineKeyboardButton('Refugee/Migrants', callback_data='Refugee/Migrants')
    cultureart = types.InlineKeyboardButton('Culture/Art', callback_data='Culture"/"Art')
    disabledpeople = types.InlineKeyboardButton('Disabled People', callback_data='Disabled People')
    youngpeople = types.InlineKeyboardButton('Young People', callback_data='Young People')
    healthcare = types.InlineKeyboardButton('Health Care', callback_data='Health Care')
    socialwork = types.InlineKeyboardButton('Social Work', callback_data='Social Work')
    environment = types.InlineKeyboardButton('Environment', callback_data='Environment')
    schoolkindergarten = types.InlineKeyboardButton('School/Kindergarten', callback_data='School/Kindergarten')
    awarnessraisingcampaign = types.InlineKeyboardButton('Awarness Raising Campaign', callback_data='Awarness Raising Campaign')

    CategKeyboard.add(socialmedia, animals, theatre)
    CategKeyboard.add(permaculturefarming, eventassistance)
    CategKeyboard.add(education, sport, refugeemigrants)
    CategKeyboard.add(cultureart, disabledpeople)
    CategKeyboard.add(youngpeople, healthcare)
    CategKeyboard.add(socialwork, environment)
    CategKeyboard.add(schoolkindergarten)
    CategKeyboard.add(awarnessraisingcampaign)

    categ_text = "Please choose the category you are interested in:"
    bot.send_message(message.from_user.id, text=categ_text, reply_markup=CategKeyboard)

@bot.callback_query_handler(func= lambda message: message.data in categArray)
def CategorySelected(message):
    selected_category = message.data

    confirmationKeyboard = types.InlineKeyboardMarkup(row_width=2)
    confirmKey = types.InlineKeyboardButton('Yes', callback_data='YES')
    declineKey = types.InlineKeyboardButton('No', callback_data='NO')
    confirmationKeyboard.add(confirmKey, declineKey)

    bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=f"Please choose the category you are interested in:{back_slash}Category Selected -> {selected_category}{back_slash}{back_slash}Is your selection correct?",
        reply_markup=confirmationKeyboard
    )

@bot.callback_query_handler(func= lambda message: message.data == "YES")
def submit_new_registration(message):
    print("Im in")
    db_commit()

@bot.callback_query_handler(func= lambda message: message.data == "NO")
def cancel_new_registration(message):
    start(message)

##################################### BOT REGISTRATION END ######################################
##################################### ABOUT BUTTON START ######################################
def aboutUs(message):
    pass

##################################### ABOUT BUTTON END ######################################

bot.infinity_polling()
# if __name__ == "__main__":
#     start()
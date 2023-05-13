import telebot
from telebot import types
import requests
import inspect


bot = telebot.TeleBot("")

back_slash = "\n"
user_dict = {}
# 
# ############################### CLASS START ####################################
# class UsrData:
#     def __init__(self, message):
#         self.user_id = message.from_user.id
#         self.j = 0
#         self.pos_array = []
#         self.pos_array_count = []
        
#     @property
#     def position_array(self):
#         return self.pos_array
        
#     @position_array.setter
#     def position_array(self, position):
#         self.pos_array.append(position)
#         return self.pos_array
        
#     @property
#     def position_array_count(self):
#         return self.pos_array_count
        
#     @position_array_count.setter
#     def position_array_count(self, position):
#         self.pos_array_count.append(position)
#         return self.pos_array_count
        
#     @property
#     def j_count(self):
#         return self.j
    
#     @j_count.setter
#     def j_count(self, count):
#         self.j = count
#         return self.j
    
#     def del_all(self):
#         self.pos_array.clear()
#         self.pos_array_count.clear()
#         self.j = 0
# ############################### CLASS END ######################################

# ############################### ASSIGNING / RETRIVING USER DATA/OBJECT START #######################
# def get_user_object(message):
#     if user_dict.get(message.from_user.id) != None:
#         return user_dict[message.from_user.id]
#     else:
#         new_obj = UsrData(message)
#         user_dict[new_obj.user_id] = new_obj
#         return new_obj
# ############################### ASSIGNING / RETRIVING USER DATA/OBJECT END #######################
##################################### BOT ENTRY POINT START ######################################
@bot.message_handler(commands=['start'], chat_types=["private"])
def start(message):
    # current_user = get_user_object(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, is_persistent=True)
    xrp_bt = types.KeyboardButton(text="XRP Price", request_contact=False)
    btc_bt = types.KeyboardButton(text="BTC Price")
    pos_bt = types.KeyboardButton(text="Positions")
    trend_bt = types.KeyboardButton(text="Trends")
    pl_bt = types.KeyboardButton(text="Profit/Loss")
    markup.row(xrp_bt, btc_bt, pos_bt)
    markup.row(pl_bt, trend_bt)
    bot.send_message(message.from_user.id, "Choose an option below:", reply_markup = markup)
##################################### BOT ENTRY POINT END ######################################

bot.infinity_polling()
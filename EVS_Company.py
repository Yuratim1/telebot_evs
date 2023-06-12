#!pip install python-telegram-bot-calendar
#from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

!pip install telebot
!pip install telegram
import telegram
import telebot
from telebot import types

from datetime import datetime

import pandas as pd

# Initialise the Bot
bot_token = "6024067411:AAHxQCR2E6VpfVL7rjq7wIHwkTkCYstpfRo"
bot       = telebot.TeleBot(bot_token)
# Global Variables 
user_dict     = {}
company_dict  = {}
project_dict  = {}

eu_countries  = [
    "\U0001F1E6\U0001F1F9 Austria",
    "\U0001F1E7\U0001F1EA Belgium",
    "\U0001F1E7\U0001F1EC Bulgaria",
    "\U0001F1ED\U0001F1F7 Croatia",
    "\U0001F1E8\U0001F1FE Cyprus",
    "\U0001F1E8\U0001F1FF Czech Republic",
    "\U0001F1E9\U0001F1F0 Denmark",
    "\U0001F1EA\U0001F1EA Estonia",
    "\U0001F1EB\U0001F1EE Finland", 
    "\U0001F1EB\U0001F1F7 France",
    "\U0001F1E9\U0001F1EA Germany",
    "\U0001F1EC\U0001F1F7 Greece",
    "\U0001F1ED\U0001F1FA Hungary",
    "\U0001F1EE\U0001F1EA Ireland",
    "\U0001F1EE\U0001F1F9 Italy",
    "\U0001F1F1\U0001F1FB Latvia",
    "\U0001F1F1\U0001F1F9 Lithuania",
    "\U0001F1F1\U0001F1FA Luxembourg",
    "\U0001F1F2\U0001F1F9 Malta",
    "\U0001F1F3\U0001F1F1 Netherlands",
    "\U0001F1F5\U0001F1F1 Poland",
    "\U0001F1F5\U0001F1F9 Portugal",
    "\U0001F1F8\U0001F1F0 Slovakia",
    "\U0001F1F8\U0001F1EE Slovenia",
    "\U0001F1EA\U0001F1F8 Spain",
    "\U0001F1F8\U0001F1EA Sweden",
]

class User:
    def __init__(self, user_id):
      self.id        = user_id

      # previous_state can must be a single string variable 
      self.previous_state = None

      # current_state can must be a single string variable
      self.current_state  = 'start'

      # current_state can must be a array of string variables
      self.next_state     = ['register', 'about us']

      self.registered     = False

      # Project ID counter, for ease of use.
      self.last_project_id = None

class Company:
    def __init__(self, company_id, company_name):
      self.id   = company_id
      self.name = company_name
      self.country         = None
      self.description     = None
      self.posted_projects = []

    def __repr__(self) -> str:
         return f"Company\n ID - {self.id}\n Name - {self.name}\n Country - {self.country}\n Description - {self.description}"

class Project:
    def __init__(self, project_id, project_name):
      self.id   = project_id
      self.name = project_name
      self.location        = None
      self.description     = None
      self.contact_details = None
      self.image_id        = None
      self.image_path      = None

# Additional Functions for Usability/Readability
def get_user(id):
    # Retrives or Creates a user's and its company's object from SQL.
    if id in user_dict.keys():
      return user_dict[id]
    else:
      user_dict[id] = User(id)
      return user_dict[id]


def sanitise_input(message, expected_type, state=None):
    if expected_type == 'text':
      if message.text:
        return True
      else:
        return False

    elif expected_type == 'image':
      if message.photo:
        return True
      else:
        return False



def print_pretty_dict(dictionary):
    df = pd.DataFrame.from_dict(dictionary.__dict__, orient='index')
    pd.set_option('display.max_rows', len(df))
    pd.set_option('display.max_columns', None)
    print(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    

##################################### BOT ENTRY POINT START ###################################
@bot.message_handler(commands=['start'], chat_types=["private"])
def start(message):
    user = get_user(message.from_user.id)

    if user.registered == False:
      user.current_state = 'start'
      user.next_state    = ['register', 'about us']

      markup           = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=True)
      register_button  = types.KeyboardButton(text="Register \U0001F4C4")
      about_button     = types.KeyboardButton(text="About Us \U0001F4F0")

      markup.row(about_button, register_button)
      welcome_text = "Welcome to ESC Project Hub" \
                    " here you can post your open positions for ESC projects." \
                    " Here you are able to advertise your projects using the form below."
      reply = bot.send_message(message.from_user.id, welcome_text, reply_markup = markup)


    elif user.registered == True:
      user.current_state = 'start'
      user.next_state    = ['main menu']
      main_menu(message)

    

##################################### BOT ENTRY POINT END ######################################

##################################### BOT MAIN MENU START ######################################
def main_menu(message):
    user = get_user(message.from_user.id)
    if ('main menu' in user.next_state) and (user.registered == True):
      user.previous_state = 'start'
      user.current_state  = 'main menu'
      user.next_state     = ['post new project', "view posted projects", 'profile', 'about us']

      markup           = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=True)
      profile_button   = types.KeyboardButton(text="Profile \U0001F4D3")
      about_button     = types.KeyboardButton(text="About Us \U0001F4F0")
      post_button      = types.KeyboardButton(text="Post New Project \U0001FAA7")
      premium_button   = types.KeyboardButton(text="Premium \U0001F381")
      
      markup.row(about_button, profile_button)
      markup.row(post_button)
      markup.row(premium_button)

      if user.last_project_id:
        view_button    = types.KeyboardButton(text="View Posted Projects \U0001F50D")
        markup.row(view_button)

      bot.send_message(message.from_user.id, 'Main Menu', reply_markup = markup)

    else:
      pass

##################################### BOT MAIN MENU END   ######################################


##################################### BOT PROJECT VIEWER START ###################################
@bot.message_handler(func=lambda message: message.text == "View Posted Projects \U0001F50D")
def view_posted_projects(message):
    user = get_user(message.from_user.id)
    if ("view posted projects" in user.next_state) and (user.registered == True):
      user.previous_state = user.current_state
      user.current_state  = "view posted projects"
      user.next_state     = ['view projects', 'main menu']

      markup           = types.InlineKeyboardMarkup(row_width=1)
      projects_objects = [types.InlineKeyboardButton(project_dict[message.from_user.id][project_id].name, callback_data='project selected:'+str(project_id)) for project_id in project_dict[message.from_user.id].keys()]
      markup.add(*projects_objects)

      reply = bot.send_message(message.from_user.id, "Select which project to view:", reply_markup=markup)

@bot.callback_query_handler(func=lambda message: message.data.startswith('project selected:'))
def view_a_project(message):
    user = get_user(message.from_user.id)
    if ('view projects' in user.next_state) and (user.registered == True):
      user.previous_state = user.current_state
      user.current_state  = 'view projects'
      user.next_state     = ['view projects', 'main menu']

      project_id = int(message.data.split(':')[1])
      response  = f"Name of Project: {project_dict[message.from_user.id][project_id].name}\n"
      response += f"Location: {project_dict[message.from_user.id][project_id].location}\n"
      response += f"Description: {project_dict[message.from_user.id][project_id].description}\n"
      response += f"Contact Details: {project_dict[message.from_user.id][project_id].contact_details}\n\n"

      reply     = bot.edit_message_reply_markup(chat_id=message.message.chat.id, 
                                        message_id=message.message.message_id,  reply_markup=None)

      if project_dict[message.from_user.id][project_id].image_id:
        bot.send_photo(message.from_user.id, photo=project_dict[message.from_user.id][project_id].image_id, caption=response, parse_mode='HTML')
      else:
        bot.send_message(message.from_user.id, response, parse_mode='HTML')

      main_menu(message)


##################################### BOT PROJECT VIEWER END ####################################

##################################### BOT PREMIUM START #########################################


def premium(message):
    premium_text = "Premium Service will provide you with more opportunities to post more projects and reach" \
                   "more clients."
    reply = bot.send_message(message.from_user.id, premium_text, reply_markup = None)


@bot.message_handler(func=lambda message: message.text == "Premium \U0001F381")
def buy_premium_service(message):
    # Create the keyboard markup
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Define the payment button
    #payment_button = types.InlineKeyboardButton('Buy Premium Service', pay=True, callback_data='pay for premium')
    #markup.add(payment_button)

    # Send the message to the user
    #reply = bot.send_message(message.from_user.id, 'To access the premium service, please click the button below to make a payment:',
    #                          reply_markup=markup)

    # Get the user's chat ID and the provider bot token
    chat_id        = message.chat.id
    provider_token = "284685063:TEST:ZmQxYWRiY2UwOTAz"
    # Generate a unique invoice ID
    invoice_id = 'premium_service_invoice_001'

    # Set the price and currency
    price = 9.99  # Example price in USD
    currency = 'USD'
    

    # Generate a unique payload for the payment provider
    payload = f'premium_service_{chat_id}'

    # Set the title and description of the premium service
    title = 'Premium Service'
    description = 'Unlock exclusive features with the premium service.'
    price_object = types.LabeledPrice(label=title, amount=int(price * 100))
    # Send the payment invoice to the user
    bot.send_invoice(chat_id=message.from_user.id, title=title, description=description,
                             invoice_payload=payload, provider_token=provider_token,
                             currency=currency, prices=[price_object],
                             start_parameter=invoice_id)


##################################### BOT PREMIUM END ###########################################

##################################### BOT REGISTRATION START ####################################
@bot.message_handler(func=lambda message: message.text == 'Register \U0001F4C4')
def register(message):
    user = get_user(message.from_user.id)
    if ('register' in user.next_state) and (user.registered == False):
      user.previous_state = 'start'
      user.current_state  = 'register'
      user.next_state     = ['get country', 'cancel registration']

      print(company_dict)

      # Reg form: 1.Name of Company, 2.Country, 3.Brief Description 
      cancellation_markup          = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=False)
      cancel_registration_button  = types.KeyboardButton(text="Cancel Registration \U0001F4C4")
      cancellation_markup.row(cancel_registration_button)

      reply = bot.send_message(message.from_user.id, "To register, please provide the following information:", reply_markup=cancellation_markup)
      reply = bot.send_message(message.from_user.id, "Enter the name of your company:")
      bot.register_next_step_handler(reply, get_country)
    else:
      pass

    

def get_country(message):
    user = get_user(message.from_user.id)
    if ('get country' in user.next_state) and (user.registered == False):
      user.previous_state = 'register'
      user.current_state  = 'get country'
      user.next_state     = ['get registration description', 'cancel registration']

      # Check for cancellation: 2 types of checks are needed here. 
      if check_for_cancellation(message):
        return cancel_registration(message)
      # Because this function does not rely on register new step handler, a wrapper must be used.
      @bot.message_handler(func=lambda message: cancel_registration(message) if message.text == 'Cancel Registeration \U0001F4C4' else None)
      def dummy_func(message):
        pass

      # Step 2 out of 4 
      # If user's first attempt at registration, create a new Company object, else use an existing one.
      # Each input from the user must be sanitised before passed on into the company object
      if sanitise_input(message, 'text'):
        if message.from_user.id in company_dict.keys():
          company_dict[message.from_user.id].name = message.text
        else:
          company_dict[message.from_user.id] = Company(message.from_user.id, message.text)

        markup = types.InlineKeyboardMarkup(row_width=3)
        country_button_objects = [types.InlineKeyboardButton(country, callback_data='country selected:'+country) for country in eu_countries]
        markup.add(*country_button_objects)

        reply = bot.send_message(message.from_user.id, "Enter your country:", reply_markup=markup)
      else:
        user.next_state = ['get country', 'cancel registration']
        response  = "The name of the company you have provided was not valid.\n"
        response += "Please only use text format for the name."
        reply = bot.send_message(message.from_user.id, response)
        reply = bot.send_message(message.from_user.id, "Enter the name of your company:")
        bot.register_next_step_handler(reply, get_country)

    else:
      pass
    
  
@bot.callback_query_handler(func=lambda message: message.data.startswith('country selected:'))
def get_registration_description(message):
    user = get_user(message.from_user.id)
    if ('get registration description' in user.next_state) and (user.registered == False):
      user.previous_state = 'get country'
      user.current_state  = 'get registration description'
      user.next_state     = ['registration description check', 'cancel registration']

      # Check for cancellation 
      if check_for_cancellation(message):
        return cancel_registration(message)

      # Step 3 out of 4 
      country   = message.data.split(':')[1]
      company_dict[message.from_user.id].country = country
      response  = "Country Selected\n\n"
      response += "Enter a brief description of your company:\n"
      response += "(No more than 250 characters)"
      reply     = bot.edit_message_text(text=response, chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=None)
      bot.register_next_step_handler(reply, registration_description_check)

    else:
      pass

def registration_description_check(message):
    user = get_user(message.from_user.id)
    if ('get registration description' or 'adjust company description' in user.next_state) and (user.registered == False):
      user.previous_state = user.current_state
      user.current_state  = 'registration description check'
      user.next_state     = ['registration details check', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_registration(message)

      # Check that the description was a text format
      # Check that the description meets length requirements
      if sanitise_input(message, 'text'):
        if len(message.text) <= 500:
          company_dict[message.from_user.id].description = message.text
          registration_details_check(message)
        else:
          response  = "Your description was too long\n"
          response += "Enter a shorter description of your company:"
          bot.send_message(message.from_user.id, response)
          bot.register_next_step_handler(message, registration_description_check)
      else:
        user.next_state = ['get registration description', 'cancel registration']
        
        response_one  = "The name of the company you have provided was not valid.\n"
        response_one += "Please only use text format for the name."
        reply = bot.send_message(message.from_user.id, response_one)

        response_two  = "Enter a brief description of your company:\n"
        response_two += "(No more than 250 characters)"
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, registration_description_check)
      
    else:
      pass

def registration_details_check(message):
    user = get_user(message.from_user.id)
    if ('registration details check' in user.next_state) and (user.registered == False):
      user.previous_state = 'registration description check'
      user.current_state  = 'registration details check'
      user.next_state     = ['finish registration', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_registration(message)
      # Because this function does not rely on register new step handler, a wrapper must be used to check for cancellation.
      @bot.message_handler(func=lambda message: cancel_registration(message) if message.text == 'Cancel Registeration \U0001F4C4' else None)
      def dummy_func(message):
        pass

      
      
      response  = f"Company Name: {company_dict[message.from_user.id].name}\n"
      response += f"Country: {company_dict[message.from_user.id].country}\n"
      response += f"Brief Description: {company_dict[message.from_user.id].description}\n\n"
      response += "<strong>Are all of the details correct?</strong>"

      markup     = types.InlineKeyboardMarkup(row_width=2)
      yes_button = types.InlineKeyboardButton('Yes', callback_data ='registration details are correct')
      no_button  = types.InlineKeyboardButton('No',  callback_data ='registration details are not correct')
      markup.add(yes_button, no_button)
      
      bot.send_message(message.from_user.id, response, reply_markup=markup, parse_mode='HTML')

    else:
      pass

@bot.callback_query_handler(func=lambda message: message.data == "registration details are correct" or message.data == 'registration details are not correct')
def finish_registration(message):
    user = get_user(message.from_user.id)
    if ('finish registration' in user.next_state) and (user.registered == False):
      user.previous_state = 'registration details check'
      user.current_state  = 'finish registration'
      user.next_state     = []

      if message.data == 'registration details are not correct':
        user.next_state.append('change registration details')
        user.next_state.append('cancel registration')

        # If the details that were provided are incorrect give an option to specify
        # which details to correct or start-over registration.
        markup                      = types.InlineKeyboardMarkup(row_width=1)
        company_name_button         = types.InlineKeyboardButton(text='Company Name', callback_data='Change Registration Details:Name')
        company_country_button      = types.InlineKeyboardButton(text='Company Country', callback_data='Change Registration Details:Country')
        company_description_button  = types.InlineKeyboardButton(text='Company Description', callback_data='Change Registration Details:Description')
        start_over_button           = types.InlineKeyboardButton(text='Start Over', callback_data='Change Registration Details:Start Over')
        markup.add(company_name_button, company_country_button, company_description_button)
        markup.add(start_over_button)
        bot.send_message(message.from_user.id, 'Which details would you like to adjust?', reply_markup=markup)
      elif message.data == 'registration details are correct':
        user.next_state.append('main menu')

        # Store the user information or perform any further processing here
        # You can access the company's information using company_dict[message.from_user.id]
        # For each registered user, there is an entry in user_dict, company_dict and project_dict
        user.registered = True

        response  = f"<b>Registration successful!</b>\n\n"
        response += f"Company Name: {company_dict[message.from_user.id].name}\n"
        response += f"Country: {company_dict[message.from_user.id].country}\n"
        response += f"Brief Description: {company_dict[message.from_user.id].description}\n"

        bot.send_message(message.from_user.id, response, parse_mode='HTML')

        print(company_dict[message.from_user.id])
        # Go to Main Menu after the registeration is complete
        main_menu(message)
      
    else:
      pass


@bot.callback_query_handler(func=lambda message: message.data.startswith('Change Registration Details:'))
def change_registration_details(message):
    user = get_user(message.from_user.id)
    if ('change registration details' in user.next_state) and (user.registered == False):
      user.previous_state = 'finish registration'
      user.current_state  = 'change registration details'
      user.next_state     = ['cancel registration']

      reply = bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=None)


      detail_to_change = message.data.split(':')[1]
      if detail_to_change == 'Name':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append('adjust company name')

        # Enables to change the name of company using 'adjust_company_name' function
        response = "Enter the correct company name:"
        reply    = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, adjust_company_name)

      elif detail_to_change == 'Country':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append('adjust company country')

        # Enables to change the company's country using 'adjust_company_country' function
        markup = types.InlineKeyboardMarkup(row_width=3)
        country_button_objects = [types.InlineKeyboardButton(country, callback_data='corrected country selected:'+country) for country in eu_countries]
        markup.add(*country_button_objects)

        bot.send_message(message.from_user.id, "Select the correct company country:", reply_markup=markup)

      elif detail_to_change == 'Description':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append('adjust company description')

        # Enables to change the company's description using 'registration_details_check' function
        response  = "Enter a corrected description of your company:\n"
        response += "(No more than 500 characters)"
        reply     = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, registration_description_check)

      elif detail_to_change == 'Start Over':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append('register')

        # Enables to start the registration process from the beginning
        # Deletes all previous registration records
        del company_dict[message.from_user.id]['company_name']
        del company_dict[message.from_user.id]['country']
        del company_dict[message.from_user.id]['description']
        register(message)

    else:
      pass

def adjust_company_name(message):
    user = get_user(message.from_user.id)
    if ('adjust company name' in user.next_state) and (user.registered == False):
      user.previous_state = 'change registration details'
      user.current_state  = 'adjust company name'
      user.next_state     = ['registration details check', 'cancel registration']

      if sanitise_input(message, 'text'):
        company_dict[message.from_user.id].name = message.text
        registration_details_check(message)
      else:
        user.next_state = ['adjust company name', 'cancel registration']
        
        response_one  = "The name of the company you have provided was not valid./n"
        response_one += "Please only use text format for the name."
        response_two  = "Enter the correct company name:"
        reply = bot.send_message(message.from_user.id, response_one)
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, adjust_company_name)
    else:
      pass

@bot.callback_query_handler(func=lambda message: message.data.startswith('corrected country selected:'))
def adjust_company_country(message):
    user = get_user(message.from_user.id)
    if ('adjust company country' in user.next_state) and (user.registered == False):
      user.previous_state = 'change registration details'
      user.current_state  = 'adjust company country'
      user.next_state     = ['registration details check', 'cancel registration']
      
      country   = message.data.split(':')[1]
      company_dict[message.from_user.id].country = country
      response  = "Country Selected"
      reply     = bot.edit_message_text(text=response, chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=None)

      registration_details_check(message)
    
    else:
      pass



##################################### BOT REGISTRATION END ################################






##################################### ABOUT BUTTON START ###################################
def about_us(message):
    pass
##################################### ABOUT BUTTON END #####################################






##################################### POST NEW PROJECT START ################################
@bot.message_handler(func=lambda message: message.text == "Post New Project \U0001FAA7")
def post_new_project(message):
    user = get_user(message.from_user.id)
    if ('post new project' in user.next_state) and (user.registered == True):
      user.previous_state = 'main menu'
      user.current_state  = 'post new project'
      user.next_state     = ['get new project location', 'cancel registration']

      # Cancellation Button MarkUp
      cancellation_markup          = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=0, is_persistent=False)
      cancel_registeration_button  = types.KeyboardButton(text="Cancel Post New Project \U0001F4C4")
      cancellation_markup.row(cancel_registeration_button)

      # Ask for Name of Project
      bot.send_message(message.from_user.id, "Enter the Name of the Project:", reply_markup=cancellation_markup)
      bot.register_next_step_handler(message, get_new_project_location)

    else:
      pass

def get_new_project_location(message):
    user = get_user(message.from_user.id)
    if ('get new project location' in user.next_state) and (user.registered == True):
      user.previous_state = 'post new project'
      user.current_state  = 'get new project location'
      user.next_state     = ['get new project description', 'cancel registration']

      # Check for cancellation 
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)

      # Store Project Name 
      # If user's first attempt at post new project, create a new dictionary and enter a newProject object,
      # else use an existing one. Each input from the user must be sanitised before passed on into the Project object
      if sanitise_input(message, 'text'):
        if message.from_user.id in project_dict.keys():
          # Generate and Store a new ID
          new_project_id       = user.last_project_id + 1
          user.last_project_id = new_project_id

          # Add new project object to the overall projects dictionary
          project_dict[message.from_user.id][new_project_id] = Project(new_project_id, message.text)
        else:
          # Generate and Store a new ID sequence, if no other Projects IDs were given out
          user.last_project_id = int(str(message.from_user.id) + str('001'))

          # Add new project object to the overall projects dictionary
          project_dict[message.from_user.id] = {user.last_project_id: Project(user.last_project_id, message.text)}

        # Step 3: Get Location
        bot.send_message(message.from_user.id, "Enter the Location (country):")
        bot.register_next_step_handler(message, get_new_project_description)

    else:
      pass

def get_new_project_description(message):
    user = get_user(message.from_user.id) 
    if ('get new project description' in user.next_state) and (user.registered == True):
      user.previous_state = 'get new project location'
      user.current_state  = 'get new project description'
      user.next_state     = ['new project description handler', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)

      print(project_dict)
      print(project_dict[message.from_user.id][user.last_project_id])

      # Store new project's location
      if sanitise_input(message, 'text'):
        project_dict[message.from_user.id][user.last_project_id].location = message.text
      

        # Step 5: Get Brief Description
        bot.send_message(message.from_user.id, "Enter a Brief Description (up to 200 characters):")
        bot.register_next_step_handler(message, new_project_desciption_handler)

      else:
        user.next_state = ['get country', 'cancel registration']
        response  = "The name of the company you have provided was not valid.\n"
        response += "Please only use text format for the name."
        reply = bot.send_message(message.from_user.id, response)
        reply = bot.send_message(message.from_user.id, "Enter the name of your company:")
        bot.register_next_step_handler(reply, get_country)

    else:
      pass

def new_project_desciption_handler(message):
    user = get_user(message.from_user.id)
    if ('new project description handler' in user.next_state) and (user.registered == True):
      user.previous_state = 'get new project description'
      user.current_state  = 'new project description handler'
      user.next_state     = ['new project contact details', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)

      # Store new project's description
      if sanitise_input(message, 'text'):
        # Step 5.5: Check for the length of the description. If it exceeds 200 characters prompt the user to try again.
        if len(message.text) <= 200:
          project_dict[message.from_user.id][user.last_project_id].description = message.text
          get_new_project_contact_details(message)
        else:
          bot.send_message(message.from_user.id, "The description should be no more than 200 characters. Please enter a shorter description:")
          bot.register_next_step_handler(message, new_project_desciption_handler)

    else:
      pass

def get_new_project_contact_details(message):
    user = get_user(message.from_user.id)
    if ('new project contact details' in user.next_state) and (user.registered == True):
      user.previous_state = 'new project description handler'
      user.current_state  = 'new project contact details'
      user.next_state     = ['get new project image', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)

      # Step 6: Get Contact Details
      bot.send_message(message.from_user.id, "Enter the Contact Details:")
      bot.register_next_step_handler(message, get_new_project_image)

    else:
      pass

def get_new_project_image(message):
    user = get_user(message.from_user.id)
    if ('get new project image' in user.next_state) and (user.registered == True):
      user.previous_state = 'new project contact details'
      user.current_state  = 'get new project image'
      user.next_state     = ['new project add image yes', 'new project add image no', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)


      # Store new project's contact details
      if sanitise_input(message, 'text'):
        project_dict[message.from_user.id][user.last_project_id].contact_details = message.text

        # Step 7: Ask if the user wants to add an image
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes_button = types.InlineKeyboardButton('Yes', callback_data='new project add image yes')
        no_button  = types.InlineKeyboardButton('No',  callback_data='new project add image no')
        markup.add(yes_button, no_button)

        reply = bot.send_message(message.from_user.id, "Would you like to add an image/poster?", reply_markup=markup)

    else:
      pass
       
@bot.callback_query_handler(func=lambda message: message.data == 'new project add image yes')
def new_project_add_image_yes(message):
    user = get_user(message.from_user.id)
    if ('new project add image yes' in user.next_state) and (user.registered == True):
      user.previous_state = 'get new project image'
      user.current_state  = 'new project add image yes'
      user.next_state     = ['new project save image', 'cancel registration']

      # Step 8: User wants to post an image
      reply = bot.send_message(message.from_user.id, "Please attach an image or poster for your project.")
      bot.register_next_step_handler(reply, new_project_save_image)

    else:
      pass

@bot.callback_query_handler(func=lambda message: message.data == 'new project add image no')
def new_project_add_image_no(message):
    user = get_user(message.from_user.id)
    if ('new project add image no' in user.next_state) and (user.registered == True):
      user.previous_state = 'get new project image'
      user.current_state  = 'new project add image no'
      user.next_state     = ['new project details check', 'cancel registration']

      # Step 8: User does not want to post an image
      #project_dict[message.from_user.id]['image'] = None
      new_project_details_check(message)

    else:
      pass

def new_project_save_image(message):
    user = get_user(message.from_user.id)
    if ('new project save image' in user.next_state) and (user.registered == True):
      user.previous_state = 'new project add image yes'
      user.current_state  = 'new project save image'
      user.next_state     = ['new project details check', 'cancel registration']
        
      # Check for cancellation
      if check_for_cancellation(message):
        return cancel_post_new_project(message, user)

      # Store new project's contact details
      if sanitise_input(message, 'image'):
        # Step 9: Save the attached image
        # Attached image is saved and processed here
        print_pretty_dict(message)
        photo_file_id   = message.photo[-1].file_id
        photo_file_path = bot.get_file(photo_file_id).file_path
        project_dict[message.from_user.id][user.last_project_id].image_id   = photo_file_id
        project_dict[message.from_user.id][user.last_project_id].image_path = photo_file_path
        # Proceed to finish registering the post
        new_project_details_check(message)
      else:
        reply = bot.send_message(message.from_user.id, "User input was invalid, please try again.")
        user.next_state = ['new project add image yes', 'cancel registration']
        new_project_add_image_yes(message)

    else:
      pass

def new_project_details_check(message):
    user = get_user(message.from_user.id)
    if ('new project details check' in user.next_state) and (user.registered == True):
      user.previous_state = user.current_state
      user.current_state  = 'new project details check'
      user.next_state     = ['new project finish post registration', 'cancel registration']

      # Check for cancellation
      if check_for_cancellation(message):
        cancel_post_new_project(message, user)
      # Because this function does not rely on register new step handler, a wrapper must be used to check for cancellation.
      @bot.message_handler(func=lambda message: cancel_post_new_project(message, user) if message.text == "Cancel Post New Project \U0001F4C4" else None)
      def dummy_func(message):
        pass

      
      
      response  = "<strong>Are all of the details correct?</strong>\n\n"
      response += f"Name of Project: {project_dict[message.from_user.id][user.last_project_id].name}\n"
      response += f"Location: {project_dict[message.from_user.id][user.last_project_id].location}\n"
      response += f"Description: {project_dict[message.from_user.id][user.last_project_id].description}\n"
      response += f"Contact Details: {project_dict[message.from_user.id][user.last_project_id].contact_details}\n\n"
      

      markup     = types.InlineKeyboardMarkup(row_width=2)
      yes_button = types.InlineKeyboardButton('Yes', callback_data ='new project details are correct')
      no_button  = types.InlineKeyboardButton('No',  callback_data ='new project details are not correct')
      markup.add(yes_button, no_button)

      if project_dict[message.from_user.id][user.last_project_id].image_id:
        bot.send_photo(message.from_user.id, photo=project_dict[message.from_user.id][user.last_project_id].image_id, caption=response, parse_mode='HTML', reply_markup=markup)
      else:
        bot.send_message(message.from_user.id, response, parse_mode='HTML', reply_markup=markup)

    else:
      pass



@bot.callback_query_handler(func=lambda message: message.data == "new project details are correct" or message.data == 'new project details are not correct')
def new_project_finish_post_registration(message):
    user = get_user(message.from_user.id)

    if ('new project finish post registration' in user.next_state) and (user.registered == True):
      user.previous_state = user.current_state
      user.current_state  = 'new project finish post registration'
      user.next_state     = []
      

      if message.data == 'new project details are not correct':
        user.next_state.append("adjust new project's details")
        user.next_state.append('cancel registration')
        # If the details that were provided are incorrect select
        # which details to correct or start-over registration.
        markup                         = types.InlineKeyboardMarkup(row_width=1)
        project_name_button            = types.InlineKeyboardButton(text="Project's Name", callback_data="Change New Project's Details:Name")
        project_location_button        = types.InlineKeyboardButton(text="Project's Location", callback_data="Change New Project's Details:Location")
        project_description_button     = types.InlineKeyboardButton(text="Project's Description", callback_data="Change New Project's Details:Description")
        project_contact_details_button = types.InlineKeyboardButton(text="Project's Contact Details", callback_data="Change New Project's Details:Contact Details")
        project_image_button           = types.InlineKeyboardButton(text="Project's Image", callback_data="Change New Project's Details:Image")
        start_over_button              = types.InlineKeyboardButton(text='Start Over', callback_data="Change New Project's Details:Start Over")
        markup.add(project_name_button, project_location_button, 
                   project_description_button, project_contact_details_button, project_image_button)
        markup.add(start_over_button)
        bot.send_message(message.from_user.id, 'Which details would you like to adjust?', reply_markup=markup)

      elif message.data == 'new project details are correct':
        user.next_state.append('main menu')

        # Step 10: Finish registering the post
        # Additional processing or storing the post information can be done here

        response  = "<b>Post registration successful!</b>\n\n"
        response += f"Name of Project: {project_dict[message.from_user.id][user.last_project_id].name}\n"
        response += f"Location: {project_dict[message.from_user.id][user.last_project_id].location}\n"
        response += f"Description: {project_dict[message.from_user.id][user.last_project_id].description}\n"
        response += f"Contact Details: {project_dict[message.from_user.id][user.last_project_id].contact_details}\n"
        if project_dict[message.from_user.id][user.last_project_id].image_id:
          response += "Image Attached\n\n"
          bot.send_photo(message.from_user.id, photo=project_dict[message.from_user.id][user.last_project_id].image_id, caption=response, parse_mode='HTML')
        else:
          bot.send_message(message.from_user.id, response, parse_mode='HTML')

        # Go to Main Menu after the post registration is complete
        main_menu(message)

@bot.callback_query_handler(func=lambda message: message.data.startswith("Change New Project's Details:"))
def change_new_project_details(message):
    user = get_user(message.from_user.id)
    if ("adjust new project's details" in user.next_state) and (user.registered == True):
      user.previous_state = 'new project finish post registration'
      user.current_state  = "change new project's details"
      user.next_state     = ['cancel registration']

      detail_to_change = message.data.split(':')[1]
      if detail_to_change == 'Name':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append("adjust new project's name")

        # Enables to change the name of company using 'adjust_company_name' function
        response = "Enter the correct project's name:"
        reply    = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, adjust_new_project_name)

      elif detail_to_change == 'Location':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append("adjust new project's location")

        # Enables to change the company's country using 'adjust_company_country' function
        response = "Enter the correct project's location:"
        reply = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, adjust_new_project_location)

      elif detail_to_change == 'Description':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append("adjust new project's description")

        # Enables to change the company's description using 'registration_details_check' function
        response  = "Enter a corrected description of your project:\n"
        response += "(No more than 250 characters)"
        reply     = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, adjust_new_project_description)

      elif detail_to_change == 'Contact Details':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append("adjust new project's contact details")

        # Enables to change the company's description using 'registration_details_check' function
        response  = "Enter the correct project's contact details:\n"
        reply     = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, adjust_new_project_contact_details)

      elif detail_to_change == 'Image':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append('new project save image')

        # Enables to change the company's description using 'registration_details_check' function
        response  = "Enter the correct project's image:\n"
        response += "Please attach an image or poster for your project."
        reply = bot.send_message(message.from_user.id, response)
        bot.register_next_step_handler(reply, new_project_save_image)

      elif detail_to_change == 'Start Over':
        # Add to user.next state another entry so the following function can allow access to itself.
        user.next_state.append("post new project")

        # Enables to start the registration process from the beginning
        # Deletes all previous registration records
        del project_dict[message.from_user.id][user.last_project_id]

        print(project_dict[message.from_user.id])
        response = "Starting the submission of a project over."
        reply    = bot.send_message(message.from_user.id, response)
        post_new_project(message)

    else:
      pass

def adjust_new_project_name(message):
    user = get_user(message.from_user.id)
    if ("adjust new project's name" in user.next_state) and (user.registered == True):
      user.previous_state = "change new project's details"
      user.current_state  = "adjust new project's name"
      user.next_state     = ['cancel registration']
      if sanitise_input(message, 'text'):
        user.next_state.append('new project details check')

        project_dict[message.from_user.id][user.last_project_id].name = message.text
        new_project_details_check(message)
      else:
        user.next_state.append("adjust new project's name")
        
        response_one  = "The name of the project you have provided was not valid./n"
        response_one += "Please only use text format for the name."
        response_two  = "Enter the correct project's name:"
        reply = bot.send_message(message.from_user.id, response_one)
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, adjust_company_name)

    else:
      pass

def adjust_new_project_location(message):
    user = get_user(message.from_user.id)
    if ("adjust new project's location" in user.next_state) and (user.registered == True):
      user.previous_state = "change new project's details"
      user.current_state  = "adjust new project's location"
      user.next_state     = ['cancel registration']
      if sanitise_input(message, 'text'):
        user.next_state.append('new project details check')

        project_dict[message.from_user.id][user.last_project_id].location = message.text
        new_project_details_check(message)
      else:
        user.next_state.append("adjust new project's location")
        
        response_one  = "The location of the project you have provided was not valid./n"
        response_one += "Please only use text format for the location."
        response_two  = "Enter the correct project's location:"
        reply = bot.send_message(message.from_user.id, response_one)
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, adjust_new_project_location)

    else:
      pass

def adjust_new_project_description(message):
    user = get_user(message.from_user.id)
    if ("adjust new project's description" in user.next_state) and (user.registered == True):
      user.previous_state = "change new project's details"
      user.current_state  = "adjust new project's description"
      user.next_state     = ['cancel registration']
      if sanitise_input(message, 'text'):
        user.next_state.append('new project details check')

        project_dict[message.from_user.id][user.last_project_id].description = message.text
        new_project_details_check(message)
      else:
        user.next_state.append("adjust new project's description")
        
        response_one  = "The description of the project you have provided was not valid./n"
        response_one += "Please only use text format for the description./n"
        response_one += "(No more than 250 characters)"
        response_two  = "Enter the correct project's description:"
        reply = bot.send_message(message.from_user.id, response_one)
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, adjust_new_project_description)

    else:
      pass

def adjust_new_project_contact_details(message):
    user = get_user(message.from_user.id)
    if ("adjust new project's contact details" in user.next_state) and (user.registered == True):
      user.previous_state = "change new project's details"
      user.current_state  = "adjust new project's contact details"
      user.next_state     = ['cancel registration']
      if sanitise_input(message, 'text'):
        user.next_state.append('new project details check')

        project_dict[message.from_user.id][user.last_project_id].contact_details = message.text
        new_project_details_check(message)
      else:
        user.next_state.append("adjust new project's contact details")
        
        response_one  = "The description of the project you have provided was not valid./n"
        response_one += "Please only use text format for the contact details./n"
        response_one += "(No more than 250 characters)"
        response_two  = "Enter the correct project's contact details:"
        reply = bot.send_message(message.from_user.id, response_one)
        reply = bot.send_message(message.from_user.id, response_two)
        bot.register_next_step_handler(reply, adjust_new_project_contact_details)

    else:
      pass
      




##################################### POST NEW PROJECT END ##################################

##################################### CANCELLATIONS START ############################
def check_for_cancellation(message) -> bool:
    if type(message) == types.Message:
      if message.text == 'Cancel Registration \U0001F4C4' or message.text == "Cancel Post New Project \U0001F4C4":
        return True
    elif type(message) == types.CallbackQuery:
      if message.data == 'Cancel Registration \U0001F4C4' or message.data == "Cancel Post New Project \U0001F4C4":
        return True
    else:
      return False
    
def cancel_registration(message):
    if message.from_user.id in company_dict.keys():
      del company_dict[message.from_user.id]
    start(message)

def cancel_post_new_project(message, user):
    user.next_state = ['main menu']
    if message.from_user.id in project_dict.keys():
      del project_dict[message.from_user.id][user.last_project_id]
    main_menu(message)
##################################### CANCELLATIONS END ##############################



bot.infinity_polling()

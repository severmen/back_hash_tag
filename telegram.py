import telebot
import pymongo
from telebot import types
import django
import os
from PIL import Image
#оповещения населения

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from city_departments.models import *

db_client = pymongo.MongoClient(host='localhost',
                                port=27000,
                                username= 'root',
                                password= 'example')

current_DB = db_client["hack_tag"]

collection_mongoDB = current_DB["public_alerts"]


client = telebot.TeleBot("2029631507:AAEwRx6qqVgaISvXtrq2EjPNu61cBG8AGkI")

def system_setings_user_answer(message):
    if message.text == "🔇Отключиться от сервиса":
        client.send_message(message.chat.id,"Вы отключены от сервиса") 
        collection_mongoDB.remove({"telegram_id":str(message.chat.id)})
    aplications(message)
    #send_header_informations(message)
      
def send_header_informations(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Получить помощь волонтёра"), 
        types.KeyboardButton("⚙️Системные настройки") )
    rmk.add(types.KeyboardButton("📢Сообщеть о проблеме"))
    rmk.add(types.KeyboardButton('🏭 Вызвать мастера из Управляющей Компании'))
    rmk.add(types.KeyboardButton("💰Прочие услуги"))



    message_text = "В случае какой либо важной информации информации, по выбранным категорям вам сражу же придёт уведомление если это касаеться вашего место жительства"
    
    return client.send_message(message.chat.id,message_text, reply_markup=rmk) 

@client.message_handler(content_types=['text'])
def aplications(message):
    if collection_mongoDB.count_documents({"telegram_id":str(message.chat.id)}) == 0:
        markup = types.ReplyKeyboardRemove(selective=False)
        message_text = "Извините, вы не зарегистрированный в системе 😕, но вы можете исправить по следующей ссылке http://rostelecom.com/ 😄"
        client.send_message(message.chat.id, message_text, reply_markup=markup)
    else:
        msg = send_header_informations(message)
        client.register_next_step_handler(msg, user_answer)

def user_answer(message):
    # markup = types.ReplyKeyboardRemove(selective = False)
    message_text = "Данный функционал в разработке :)"
    if message.text == "🏭 Вызвать мастера из Управляющей Компании":
        msg = client.send_message(message.chat.id, message_text)
    elif message.text == "⚙️Системные настройки":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🔇Отключиться от сервиса"),
            types.KeyboardButton("В главное меню") )
        message_text = "В данном разделе ты можешь изменять индивидульные парметры сервиса"
        msg = client.send_message(message.chat.id, message_text , reply_markup=markup)
        client.register_next_step_handler(msg, system_setings_user_answer)
    elif message.text == "📢Сообщеть о проблеме":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("В главное меню")) 
        message_text = "Кратко опишите ситуацию можете отправить одно видео и одну фотографию, yне забудьте пожалуйста сказать адресс"
        msg = client.send_message(message.chat.id, message_text, reply_markup=markup)
        client.register_next_step_handler(msg, new_event)
    elif message.text == "Получить помощь волонтёра":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("В главное меню")) 
        message_text = "Пожалуйста представьтесь"
        msg = client.send_message(message.chat.id, message_text, reply_markup=markup)
        help_informations = {
            'name':'',
            'situation':'',
            'adress':'',
        }
        client.register_next_step_handler(msg, need_volunteer_cheack_full_name, help_informations)
    elif message.text == "💰Прочие услуги":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Страхование"))
        markup.add(types.KeyboardButton("Вызов независимого специалиста"))
        markup.add(types.KeyboardButton("В главное меню"))

        message_text = "Вебрите необходимую услугу"
        msg = client.send_message(message.chat.id, message_text, reply_markup=markup)
        client.register_next_step_handler(msg, service_verification)
    else:        
        aplications(message)
def new_event(message):
    if message.text == "В главное меню":
        aplications(message)
    else:
        # chat_id = message.chat.id
        #
        # file_info = client.get_file(message.document.file_id)
        # downloaded_file = client.download_file(file_info.file_path)
        #
        # src = '/' + message.document.file_name;
        # with open(src, 'wb') as new_file:
        #     new_file.write(downloaded_file)
        #
        # client.reply_to(message, "Пожалуй, я сохраню это")
        # img = client.get_file(message.photo[-1].file_id)
        # a = client.download_file(img.file_path)
        # src = filepath + message.photo[0].file_id
        # with open(src, 'wb') as new_file:
        #     new_file.write(downloaded_file)
        new_message = HumanMessage(message = message.text)

        new_message.save()
        message_text ="Спасибо за информацию мы расмотрим его в ближайшее время"
        msg = client.send_message(message.chat.id, message_text)
        aplications(message)
def service_verification(message):
    message_text = "Данный функционал в разработке :)"
    if message.text == "Страхование":
        client.send_message(message.chat.id, "https://www.alfastrah.ru/individuals/?tag=MI_VZR_RUS&utm_source=yandex&utm_medium=cpc&utm_campaign=mi_ALS_VZR_BRAND_BROAD_Y_S_DM_RUS_yxprvzr&utm_content=pid%7C31126135170%7Crid%7C%7Ccid%7C60840897%7Cgid%7C4535608007%7Caid%7C10600196441%7Cadp%7Cno%7Cpos%7Cpremium1%7Csrc%7Csearch_none%7Cdvc%7Cdesktop%7Ccoef%7C0%7Cregion_name%7CУльяновск%7Cregion_id%7C195&utm_term=альфастрахование&yclid=5965507027731014006")
    elif message.text == "Вызов независимого специалиста":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Газовщик"))
        markup.add(types.KeyboardButton("Электрик"))
        markup.add(types.KeyboardButton("Сантехник"))
        msg = client.send_message(message.chat.id, "Выберите профиль", reply_markup=markup)
        client.register_next_step_handler(msg,cheack_profile)
    else:
        aplications(message)

def cheack_profile(message):
    client.send_message(message.chat.id, "Спасибо что пользуетесь нашим сервисом https://profi.ru/")
    aplications(message)

def need_volunteer_cheack_full_name(message,help_informations ):
    if message.text == "В главное меню":
        aplications(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("В главное меню"))
        message_text =  message.text + " кратко опишите ситуацию"
        help_informations['name'] = message.text
        msg = client.send_message(message.chat.id, message_text, reply_markup=markup)
        client.register_next_step_handler(msg, need_volunteer_cheack_situation, help_informations)
def need_volunteer_cheack_situation(message, help_informations):
    if message.text == "В главное меню":
        aplications(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("В главное меню")) 
        message_text = "Введите точный адресс"
        msg = client.send_message(message.chat.id, message_text, reply_markup=markup)
        help_informations['situation'] = message.text
        client.register_next_step_handler(msg, need_volunteer_cheack_adress, help_informations)
    
def need_volunteer_cheack_adress(message, help_informations):
    if message.text == "В главное меню":
        aplications(message)
    else:
        help_informations['adress']
        message_text = "Спасибо волонтёр свяжется с вами в ближайшее время"
        msg = client.send_message(message.chat.id, message_text)
        aplications(message)
client.polling(none_stop=True, interval=0)
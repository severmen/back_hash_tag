import os
import requests
from geopy import distance
import pymongo
import telebot
from telebot import types
from django.db.models import signals
from .models import Events, Volunteers

name_city_departament = {
    "горзас":"gas",
    "el": "Ульгэс",
    "CP": "МЧС",
    "Ульяновскводоканал":"water",
}
def mass_mailing(**kwargs):
    db_client = pymongo.MongoClient(host='localhost',
                                    port=27000,
                                    username='root',
                                    password='example')
    current_DB = db_client["hack_tag"]
    collection_mongoDB = current_DB["public_alerts"]
    client = telebot.TeleBot("2029631507:AAEwRx6qqVgaISvXtrq2EjPNu61cBG8AGkI")
    for one_result in collection_mongoDB.find({}):
        a = kwargs['instance'].User.first_name
        b = name_city_departament[a]
        if one_result[b] == "true":
            newport_ri = (float(kwargs['instance'].location.coords[1]), float(kwargs['instance'].location.coords[0]))
            cleveland_oh = (float(one_result['coord1']), float(one_result['coord2']))
            a = distance.distance(newport_ri, cleveland_oh)
            if a.meters < kwargs['instance'].radius:
                #это пока заглушка
                companу = "Ульяновскводоканала "
                text = "Новое уведомление по вашему месту жительства! "+companу +"сообщение от\r\n "
                text += kwargs['instance'].descriptions +"/r/n"
                text += "Проблему должны устранить к " + str(kwargs['instance'].date_of_creation.day) +" числу."
                text += "В "+ str(kwargs['instance'].date_of_creation.hour) + ":"+str(kwargs['instance'].date_of_creation.minute)
                client.send_message(one_result['telegram_id'], text)

            print("Минимальное растояние " + str(a.meters) + " метров")
            qa = 4
            pass

def volonter_mass_mailing(**kwargs):
    db_client = pymongo.MongoClient(host='localhost',
                                    port=27000,
                                    username='root',
                                    password='example')
    current_DB = db_client["hack_tag"]
    collection_mongoDB = current_DB["volonter"]
    client = telebot.TeleBot("2073510171:AAEi0fAmhxDrCUXPa9rupLiBpAtvjPFAoc4")
    for one_volonter in collection_mongoDB.find({}):
        text = "Внимание волонтёрам."+kwargs['instance'].Message
        text += " Волонтёры нужны до " + str(kwargs['instance'].datetime_need.day) + " числа."
        markup_inline = types.InlineKeyboardMarkup()
        item_help = types.InlineKeyboardButton(text = "Хочу помочь",
                                              callback_data="help_"+str(kwargs['instance'].id))

        markup_inline.add(item_help)
        client.send_message(one_volonter['telegram_id'], text, reply_markup = markup_inline)

signals.post_save.connect(receiver=volonter_mass_mailing, sender=Volunteers)
signals.post_save.connect(receiver=mass_mailing, sender=Events)
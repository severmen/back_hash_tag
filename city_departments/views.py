import pymongo

from geopy import distance
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Events
from datetime import datetime



import pytz
import telebot
from telebot import types


class NewUserRegistrations(APIView):
    def post(self, request, format=None):
        db_client = pymongo.MongoClient(host='localhost',
                                        port=27000,
                                        username='root',
                                        password='example')
        current_DB = db_client["hack_tag"]
        collection_mongoDB = current_DB["public_alerts"]
        collection_mongoDB.insert_one({
            "telegram_id": request.POST['id'],
            "gas": request.POST['gas'],
            "el": request.POST['el'],
            "CP": request.POST['CP'],
            "water": request.POST['water'],
            "coord1": request.POST['coord1'],
            "coord2": request.POST['coord2'],
        })
        def send_massage():
            nonlocal request
            client = telebot.TeleBot("2029631507:AAEwRx6qqVgaISvXtrq2EjPNu61cBG8AGkI")
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Начать пользоваться системой"))
            message_text = "Поздровляем с регистрацией!"
            client.send_message(request.POST['id'], message_text, reply_markup=rmk)
        send_massage()
        return Response({"sucsess":"ok"})

class NewVolonterRegistrations(APIView):
    def post(self, request, format=None):
        db_client = pymongo.MongoClient(host='localhost',
                                        port=27000,
                                        username='root',
                                        password='example')
        current_DB = db_client["hack_tag"]
        collection_mongoDB = current_DB["volonter"]
        collection_mongoDB.insert_one({
            "telegram_id": request.POST['id'],
        })
        def send_massage():
            nonlocal request
            client = telebot.TeleBot("2073510171:AAEi0fAmhxDrCUXPa9rupLiBpAtvjPFAoc4")
            message_text = "Поздровляем с регистрацией! \r\n в случае налии актульной информации мы оповещи вас в ближайше время"
            client.send_message(request.POST['id'], message_text)
            a = 5
        send_massage()
        return Response({"sucsess":"ok"})



class GetEvents(APIView):
    def post(self, request, format=None):
        utc = pytz.UTC
        result = []
        for one_event in Events.objects.all():
            if datetime.now().replace(tzinfo=utc) < one_event.end_date.replace(tzinfo=utc):
                newport_ri = (request.POST['w'],request.POST['s'])
                cleveland_oh = (one_event.location.coords[0], one_event.location.coords[1])
                distance_from_user = distance.distance(newport_ri, cleveland_oh)
                if distance_from_user.meters < one_event.radius:
                    result.append({
                        "name":one_event.name,
                        "decriptions": one_event.descriptions,
                        "end_date":{
                            "day": one_event.end_date.day,
                            "mounth": one_event.end_date.month,
                        }
                    })
        return Response(result)

from django.db import models
from django.contrib.auth.models import User

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from datetime import datetime

class Events(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Названия мероприятия")
    location = models.PointField(default=Point(48.39786528867364, 54.3186259381731), verbose_name="Локация")
    descriptions = models.TextField(max_length=1000, verbose_name="Описания мероприятия")
    radius = models.IntegerField(verbose_name="Радиус охвата события м.", )
    end_date = models.DateTimeField(blank=True, verbose_name="Дата и время оканчания мероприятия")
    date_of_creation = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата и время создания мероприятия")
    class Meta:
        verbose_name_plural = 'Мероприятии'
        verbose_name = 'Мероприятия'
        ordering = ['-name']

    def __str__(self):
        return self.name
class Volunteers(models.Model):
    Events = models.ForeignKey(Events, on_delete=models.CASCADE, verbose_name="Название мероприятия")
    Count = models.IntegerField(verbose_name="Нобходимое количество волонтёров")
    Message = models.TextField(verbose_name="Сообщение волонтёром")
    datetime_need = models.DateTimeField(verbose_name="До какого срока необходимы волонтёры")
    date_of_creation = models.DateTimeField(default=datetime.now,    verbose_name="Дата и время создания мероприятия")
    class Meta:
        verbose_name_plural = 'Волонтёры'
        verbose_name = 'Волонтёр'
        ordering = ['-Events']

    def __str__(self):
        return str(self.Events)

class Message(models.Model):
    '''
    тут можно отправлять Общую информацию незвисимо от ситуации
    '''
    Events = models.ForeignKey(Events, on_delete=models.CASCADE, verbose_name="Название мероприятия")
    header = models.CharField(max_length=400, verbose_name="Заголовок сообщения")
    title = models.TextField(verbose_name="Сообщение")
    date_of_creation = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата и время сообщения")

    class Meta:
        verbose_name_plural = 'Сообщении'
        verbose_name = 'Сообщения'
        ordering = ['-header']

    def __str__(self):
        return self.header

class HumanMessage(models.Model):
    message = models.TextField(verbose_name='Сообщение')
    date_of_creation = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата и время заявки")
    img = models.ImageField(null=True, verbose_name = 'Изображение')
    video = models.FileField(null=True, verbose_name='Видео')

    class Meta:
        verbose_name_plural = 'Сообщении от пользователей'
        verbose_name = 'Сообщения от пользователя'
        ordering = ['-message']

    def __str__(self):
        return self.message

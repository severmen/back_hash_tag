from django.contrib import admin

from django.forms import TextInput, Textarea , NumberInput
# from django.db import models
from django.contrib.gis.db import models
from .models import Events , Volunteers, Message, HumanMessage
from django.contrib.gis.forms import OSMWidget, OpenLayersWidget
from django.contrib.gis.admin import OSMGeoAdmin

class EventsAdmin(OSMGeoAdmin):
    list_display = ('name', 'location',)
    map_width = 600
    map_height = 400
    scale_text = False
    layerswitcher = False
    mouse_position = False
    modifiable = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
        models.IntegerField:{'widget': NumberInput(attrs={'style':'height:44px; width: 59px;'})}
    }
    map_template = 'gis2/admin/osm2.html'
    list_display = ('name', 'date_of_creation')
    fields = ('name', 'location','descriptions', 'radius', 'end_date')

    def save_model(self, request, obj, form, change):
        '''
        при сохраении компании функиция добавлет в качества автора
        авторизованного пользователя
        '''
        obj.User = request.user
        super(EventsAdmin, self).save_model(request, obj, form, change)


class MessageAdmin(admin.ModelAdmin):
    fields = ('header', 'title','Events' )
    list_display = ('header', 'date_of_creation')


class HumanMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'date_of_creation')


class VolunteersAdmin(admin.ModelAdmin):
    list_display = ('Events', 'Count', 'datetime_need', 'volunteers_recruited')
    fields = ('Events', 'Count','Message', 'datetime_need')
    def volunteers_recruited(self, obj):
        '''
        создём ещё одно поле для отопбражения
        количестов просмотров
        '''
        return '0'
        request = collection_mongoDB_statistics_serivice.find_one({"id": obj.id})
        return (request.get('count') if request != None else 0)

    volunteers_recruited.short_description = 'Волонтёров уже набрано'
admin.site.register(Message, MessageAdmin)
admin.site.register(HumanMessage, HumanMessageAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Volunteers, VolunteersAdmin)


# admin.site.register(Recipe)
# admin.register(Shop)
# @admin.register(Shop)
# class ShopAdmin(OSMGeoAdmin):
#     list_display = ('name', 'location',)


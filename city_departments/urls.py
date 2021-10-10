from django.urls import path, include, re_path
from .views import NewUserRegistrations, GetEvents , NewVolonterRegistrations
urlpatterns = [
    re_path(r'new_user_registrations/', NewUserRegistrations.as_view()),
    re_path(r'get_events/', GetEvents.as_view()),
    re_path(r'new_volonter_registrations/', NewVolonterRegistrations.as_view()),

]

from django.apps import AppConfig


class CityDepartmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_departments'

    def ready(self):
        import city_departments.signals

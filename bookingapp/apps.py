from django.apps import AppConfig


class BookingappConfig(AppConfig):
    name = 'bookingapp'


class LoadReceivers(AppConfig):
    name = 'bookingapp'

    def ready(self):
        from . import receivers
        

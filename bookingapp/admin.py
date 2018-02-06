from django.contrib import admin
from .models import Venue, Features, Room, Booking
# Register your models here.

admin.site.register(Venue)
admin.site.register(Features)
admin.site.register(Room)
admin.site.register(Booking)
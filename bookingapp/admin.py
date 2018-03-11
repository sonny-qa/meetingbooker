from django.contrib import admin
from .models import Venue, Features, Room, Booking
# Register your models here.

#admin.site.register(Venue)
#admin.site.register(Features)
#admin.site.register(Room)
admin.site.register(Booking)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name','address')

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('name','display_venue','seats','display_features')


#admin.site.register(Venue,VenueAdmin)

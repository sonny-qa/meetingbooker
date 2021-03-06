from django.contrib import admin
from .models import  Venue, Features, Room, Booking, Document, Location
# Register your models here.

#admin.site.register(Venue)
#admin.site.register(Features)
#admin.site.register(Room)
#admin.site.register(Booking)

class RoomInline(admin.TabularInline):
	model = Room



@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name','address','display_associated_rooms')
	inlines = [RoomInline]

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('name','display_venue','seats','display_features','owner')

@admin.register(Booking)
class Booking(admin.ModelAdmin):
	list_display = ('id','room','display_booking_venue','start_time','end_time','user')

@admin.register(Document)
class Document(admin.ModelAdmin):
	list_display = ('upload','room','uploaded_at',)

@admin.register(Location)
class Location(admin.ModelAdmin):
	list_display = ('venue','postcode','position','street','county','town','number')

#admin.site.register(Venue,VenueAdmin)

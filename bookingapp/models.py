import uuid
from django.urls import reverse #generate URL by reversing url pattern
from django.conf import settings
from django.db import models
# Create your models here.


class Venue(models.Model):
	"""
	Model representing a venue, i.e. a church, mosque etc.
	"""
	class Meta:
		permissions = (("can_edit_venue","Edit a venue details"),)
		
	name = models.CharField(max_length=200, help_text="Enter a venue name")
	address = models.CharField(max_length=200, help_text="Enter the address")
	

	def __str__(self):
		return self.name

	def display_associated_rooms(self):
		"""
		return the list of rooms associated with a venue
		"""
		return ', '.join([room.name for room in self.room_set.all()[:3]])

	display_associated_rooms.short_description = "Available Rooms"
class Features(models.Model):
	"""
	Model to represent the different room features, (e.g. wifi, projector etc.)
	"""
	name = models.CharField(max_length=200, help_text="Enter a feature")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Features"
		verbose_name_plural = "Features"

class Room(models.Model):

	"""
	Model representing a room within a venue
	"""
	name = models.CharField(max_length=200, help_text="Enter a room name")
	seats = models.IntegerField()
	features = models.ManyToManyField(Features, help_text="Select room features")
	venue = models.ForeignKey('Venue',on_delete=models.CASCADE)
	rate = models.DecimalField(max_digits=5, decimal_places=2)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		"""
		returns the url to access the detail of this room
		"""
		return reverse('room-detail',args=[str(self.id)])

	def display_venue(self):
		"""
		creates a string of the venue for display in admin
		"""

		return self.venue
	display_venue.short_description = 'Venue'

	def display_features(self):
		"""
		creates a string of the features for that particular room
		"""
		return  ', '.join([feature.name for feature in self.features.all()[:3]])
	display_features.short_description = 'Features'

class Booking(models.Model):
	"""
	Model representing a specific booking of a room within a venue
	each Booking will need a globally unique value - the Id
	"""

	id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique id for this booking for the entire system")
	start_time = models.DateTimeField(null=True,blank=True)
	end_time = models.DateTimeField(null=True,blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	room = models.ForeignKey('Room',on_delete=models.CASCADE)
	#venue = models.ForeignKey(Venue,on_delete=models.CASCADE)

	def display_booking_venue(self):
		"""
		function to look back up the venue for the belonging to the respective room
		we don't put a venue field on this model as it would be repeating
		venue belongs to a room and a booking belongs to a room
		"""
		return self.room.venue
	display_booking_venue.short_description = "Venue"







	def get_absolute_url(self):
		"""
		returns the url to access the detail of this booking
		"""
		return reverse('booking-detail',args=[str(self.id)])

class Document(models.Model):
	uploaded_at = models.DateTimeField(auto_now_add=True)
	upload = models.FileField()
	room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)


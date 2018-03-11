from django.db import models
import uuid
from django.urls import reverse #generate URL by reversing url pattern
from django.conf import settings
# Create your models here.


class Venue(models.Model):
	"""
	Model representing a venue, i.e. a church, mosque etc.
	"""

	name = models.CharField(max_length=200, help_text="Enter a venue name")
	address = models.CharField(max_length=200, help_text="Enter the address")


	def __str__(self):
		return self.name

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
	venue = models.ForeignKey('Venue',on_delete=models.CASCADE)

	def __str__(Self):
		return self.name

	def get_absolute_url(self):
		"""
		returns the url to access the detail of this booking
		"""
		return reverse('booking-detail',args=[str(self.id)])


from django.shortcuts import render
from .models import Venue, Features, Room, Booking
from django.views import generic
from django import forms

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import json as json
# Create your views here.
from django.core import serializers

import os
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
 

GOOGLE_API = get_env_variable('GOOGLE_API')




def index(request):

	num_venues = Venue.objects.all().count()
	num_rooms = Room.objects.all().count()

	return render(
		request,
		'index.html',
		context={'num_venues': num_venues,'num_rooms': num_rooms},

		)

# list of all rooms	
class RoomListView(generic.ListView):
	model = Room

class RoomDetailView(generic.DetailView):
    model = Room

def editVenue(request):
	#needs to return a list of venues 

	return render(
		request,
		'bookingapp/edit_venue.html',
		context={'GOOGLE_API':GOOGLE_API}
		)

def edit_all_venues(request):

	if request.method == 'POST':
		form = VenueSelectForm(request.POST)
		if form.is_valid():
			
			return HttpResponseRedirect(reverse('rooms') )  # does nothing, just trigger the validation

	else:
		form = VenueSelectForm()
		return render(request, 'bookingapp/venue_edit_all.html', {'form': form})




class VenueSelectForm(forms.Form):

	venue = forms.ChoiceField(choices=[('','---------')]+[(v.id, str(v)) for v in Venue.objects.all()]
		,label="Select a Venue to edit ")
	name = forms.CharField(max_length=30,label="Venue name")

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)
		self.fields['venue'].queryset = Venue.objects.none()

def LoadVenueDetails(request):

	venue_id = request.GET.get('venue')
	venue_details = Venue.objects.filter(id=venue_id)

	#return ("hello")
	data = serializers.serialize('json', venue_details, fields=('name','address', ))

	
	return HttpResponse(json.dumps(data),content_type="application/json")
	#return render(request,'bookingapp/venue_details.html',{'venue_details':venue_details})

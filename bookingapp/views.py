from django.shortcuts import render
from .models import Venue, Features, Room, Booking, Document
from django.views import generic
from django import forms
from django.forms import ModelForm, inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import json as json
# Create your views here.
from django.core import serializers
from django.contrib import messages

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import modelform_factory
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelMultipleChoiceField,ModelForm

from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver

import boto3
import botocore

from urllib.parse import urlparse


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



@login_required(login_url='../accounts/login')
@permission_required('bookingapp.can_edit_venue',login_url='../accounts/login')
def edit_all_venues(request):

	if request.method == 'POST':
		form = VenueSelectForm(request.POST)
		if form.is_valid():
			
			#save the updated data

			obj = Venue.objects.get(id=request.POST.get('venue'))
			obj.name = request.POST.get('name')
			obj.address = request.POST.get('address')
			obj.save()
	
			messages.add_message(request, messages.INFO, 'Saved')
			return render(request, 'bookingapp/venue_edit_all.html', {'form': form})
			#return HttpResponseRedirect(reverse('rooms') )  # does nothing, just trigger the validation

	else:
		form = VenueSelectForm()
		return render(request, 'bookingapp/venue_edit_all.html', {'form': form})




class VenueSelectForm(forms.Form):

	venue = forms.ChoiceField(choices=[('','---------')]+[(v.id, str(v)) for v in Venue.objects.all()]
		,label="Select a Venue to edit ")
	name = forms.CharField(max_length=30,label="Name")
	address = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':18}),label="Address")


def LoadVenueDetails(request):

	venue_id = request.GET.get('venue')
	venue_details = Venue.objects.filter(id=venue_id)


	print('sonny',venue_details.values())
	data = serializers.serialize('json', venue_details, fields=('name','address', 'id'))

	
	return HttpResponse(json.dumps(data),content_type="application/json")
	#return render(request,'bookingapp/venue_details.html',{'venue_details':venue_details})


#list of venues for editing rooms
class RoomListEdit(ListView):
	model = Room
	template_name = 'bookingapp/room_list_edit.html'


class RoomUpdate(UpdateView):
	
	model=Room	
	form_class =  modelform_factory(Room,
        widgets={"features": CheckboxSelectMultiple }, fields = ['name','venue','seats','rate','features'])
	
	template_name = 'bookingapp/room_update_form.html'
	success_url = reverse_lazy('rooms-list-edit')
	


#-------------------------------------------

class DocumentListView(ListView):
	model = Document
	template_name = 'bookingapp/document_form.html'


	def get_context_data(self, **kwargs):
		#pk = self.kwargs['pk']
		#print('pk',pk)
		context = super().get_context_data(**kwargs)
		#documents = Document.objects.filter(room_id=pk)
		#print('user',self.request.user.id,self.request.user)
		#print(Document.objects.filter(room__owner_id=3))
		#print('test',[(r.owner_id == self.request.user.id) for r in Room.objects.all()])
		documents = Document.objects.filter(room__owner_id=self.request.user.id)
		#print('docs',documents)
		#documents = Document.objects.all()
		context['documents'] = documents

		return context

class DocumentCreateView(CreateView):
	model = Document
	template_name = 'bookingapp/document_upload_form.html'
	fields = ['room','upload']
	fields_required = ['room','upload']
	success_url = reverse_lazy('rooms-images')



def DocumentDelete(request):
	AWS_ACCESS_KEY_ID  = get_env_variable('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY= get_env_variable('AWS_SECRET_ACCESS_KEY')

	session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
	#print('session',session)
	s3 = session.resource('s3')
	bucket = s3.Bucket('meetingbooker-static')
	doc_id = request.GET.get('doc_id')
	item = Document.objects.filter(id=doc_id)
	item_key = item[0].upload.url
	o = urlparse(item_key)
	print('netloc',o.netloc)
	print('path',o.path)
	path = o.path
	#bucket.object(item_key).delete()
	print('item...','https://'+ o.netloc + o.path)
	bucket.delete_objects(
    Delete={
        'Objects': [
            {
                'Key': str('https://'+o.netloc+o.path)
            }
        ]
    }
)

	s3.Object('meetingbooker-static', path[1:]).delete()
#https://meetingbooker-static.s3.amazonaws.com/media/IMG_4963_1_9BV4oXM.png and this media/IMG_4963_1_9BV4oXM.png
	for object in bucket.objects.all():
		#print('this',item_key,'and this',object.key)



		if str(item_key) in 'https://meetingbooker-static.s3.amazonaws.com/'+object.key:
			print('does it match',item_key == str('https://'+o.netloc+o.path))
			print('got it',object.key,'matches',item_key)
			#object.delete()
	
	
	
		
	
	#s3.Object('meetingbooker-static', item_key).delete()
	#Document.objects.filter(id=doc_id).delete()

	print('deleted?')


	return HttpResponse('ok')



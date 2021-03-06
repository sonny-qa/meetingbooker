from django.shortcuts import render
from .models import Venue, Features, Room, Booking, Document, Location
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
import django.dispatch

import os

from bookingapp.signals import *
from bookingapp.receivers import *



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
from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.contrib.gis.geos import GEOSGeometry  
from decimal import Decimal





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

def SaveVenueDetails(request):
	postcode = request.GET.get('postcode')
	lat = request.GET.get('lat')
	lng = request.GET.get('lng')
	venue_name = request.GET.get('venue_name')
	number = request.GET.get('number')
	street = request.GET.get('street')
	town = request.GET.get('town')
	county = request.GET.get('county')
	
	print('got postcode back...',lat,lng,venue_name)
	print('anything', Venue.objects.filter(name=venue_name).first())
	

	# check if the name being tried is already a match for venue instances
	if (Venue.objects.filter(name=venue_name).first()):
		return HttpResponse('name already exists')
	else:
		new_venue = Venue.objects.create(name=venue_name)
		new_venue.save()

		point = GEOSGeometry("POINT({0} {1})".format(Decimal(lng), Decimal(lat)))

		loc = Location(venue=new_venue,postcode=postcode,position=point,
			number=number, street=street, town=town, county=county)
		loc.save()
		return HttpResponse('created ok')

		
	

		# create a new instance of Venue

		# create a new instance of the address record


	# return error - name already in use

#list of venues for editing rooms
class RoomListEdit(ListView):
	model = Room
	template_name = 'bookingapp/room_list_edit.html'

class VenueListEdit(ListView):
	model = Venue
	template_name = 'bookingapp/venue_list_edit2.html'


class RoomUpdate(UpdateView):
	
	model=Room	
	form_class =  modelform_factory(Room,
        widgets={"features": CheckboxSelectMultiple }, fields = ['name','venue','seats','rate','features'])
	
	template_name = 'bookingapp/room_update_form.html'
	success_url = reverse_lazy('rooms-list-edit')
	
class RoomCreate(CreateView):
	model= Room
	form_class =  modelform_factory(Room,
        widgets={"features": CheckboxSelectMultiple }, fields = ['name','venue','seats','rate','features'])
	
	template_name = 'bookingapp/room_create_form.html'
	success_url = reverse_lazy('rooms-list-edit')
#-------------------------------------------

class DocumentListView(ListView):
	model = Document
	template_name = 'bookingapp/document_form.html'
	print('send signal')
	book_published.send(sender=Document, book='test', user='test2')

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

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class VenueAdd(CreateView):
	model = Venue
	template_name = 'bookingapp/venue_add.html'
	fields = ('name',)





	

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your meetingbooker account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def DocumentDelete(request):

	doc_id = request.GET.get('doc_id')
	
	item = Document.objects.filter(id=doc_id)
	#item_key = item[0].upload.url
	#o = urlparse(item_key)
	#get the path for required object
	#path = o.path
	#bucket.object(item_key).delete()
	
	#first delete model from DB
	print('deleting django obj',item)
	item.delete()

	#s3.Object('meetingbooker-static', path[1:]).delete()


	#return (render_to_response('bookingapp/document_form.html'))
	#return HttpResponse(status=200)
	#return HttpResponseRedirect('room-images')
	return JsonResponse({'id':"#"+doc_id},status=201)

@receiver(post_delete, sender=Document)
def aws_del(sender, instance,**kwargs):
	#signal handler
	#s3.Object('meetingbooker-static', path[1:]).delete()

	AWS_ACCESS_KEY_ID  = get_env_variable('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY= get_env_variable('AWS_SECRET_ACCESS_KEY')

	session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
	#print('session',session)
	s3 = session.resource('s3')
	bucket = s3.Bucket('meetingbooker-static')

	#get the url from instanc passed with signal

	o = urlparse(instance.upload.url)
	path = o.path
	s3.Object('meetingbooker-static', path[1:]).delete()
	
	print("Request finished! getting")

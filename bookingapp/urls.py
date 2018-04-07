from django.urls import path
from . import views
from django.conf.urls import include	
from django.conf.urls import url

urlpatterns = [
	path('', views.index, name='index'),
	path('rooms/', views.RoomListView.as_view(), name='rooms'),
	path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
	path('venue/edit-all',views.edit_all_venues,name="edit-all-venues"),
	path('ajax/load-venue-details/', views.LoadVenueDetails, name='load-venue-details'),
	path('accounts/', include('django.contrib.auth.urls')),


	path('edit-rooms/',views.RoomListEdit.as_view(), name="rooms-list-edit"),
	path('rooms-images/',views.DocumentListView.as_view(), name='rooms-images'),
	url(r'room/(?P<pk>[0-9]+)/$', views.RoomUpdate.as_view(), name='room-edit'),
	path('image-add/', views.DocumentCreateView.as_view(), name='image-add'),


]
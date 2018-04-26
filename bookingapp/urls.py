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
	path('edit-venues/',views.VenueListEdit.as_view(), name="venues-list-edit"),
	path('rooms-images/',views.DocumentListView.as_view(), name='rooms-images'),
	url(r'room/(?P<pk>[0-9]+)/$', views.RoomUpdate.as_view(), name='room-edit'),
	path('image-add/', views.DocumentCreateView.as_view(), name='image-add'),
	path('room-create/',views.RoomCreate.as_view(),name='room-create'),
	path('image-delete',views.DocumentDelete,name='delete-doc'),
	url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
	path('add-venue/',views.VenueAdd.as_view(), name="venue-add"),
	path('ajax/save-venue-details/', views.SaveVenueDetails, name='save-venue-details'),



]
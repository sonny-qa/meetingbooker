from django.urls import path
from . import views
from django.conf.urls import include	

urlpatterns = [
	path('', views.index, name='index'),
	path('rooms/', views.RoomListView.as_view(), name='rooms'),
	path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
	path('venue/edit-all',views.edit_all_venues,name="edit-all-venues"),
	path('ajax/load-venue-details/', views.LoadVenueDetails, name='load-venue-details'),
	path('accounts/', include('django.contrib.auth.urls')),
	
]
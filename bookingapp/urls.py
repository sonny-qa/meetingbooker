from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('rooms/', views.RoomListView.as_view(), name='rooms'),
	path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),

]
from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),

    # create room_form url
    path('createRoom/', views.createRoom, name='create-room'),
    path('updateRoom/<str:pk>', views.updateRoom, name='update-room'),
    path('deleteRoom/<str:pk>', views.deleteRoom, name='delete-room'),

]

from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),

    # create room_form url
    path('createRoom/', views.createRoom, name='create-room'),
    path('updateRoom/<str:pk>', views.updateRoom, name='update-room'),
    path('deleteRoom/<str:pk>', views.deleteRoom, name='delete-room'),
    path('deleteMessage/<str:pk>', views.deleteMessage, name='delete-message'),

    path('profile/<str:pk>', views.userProfile, name='user-profile'),
]

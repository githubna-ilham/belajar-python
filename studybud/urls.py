from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


# basic url
# def home(request):
#     return HttpResponse('Hello World!')

# def room(request):
#     return HttpResponse('room')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]

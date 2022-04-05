from multiprocessing import context
from django.shortcuts import redirect, render

from base.models import Room, Topic
from .forms import RoomForm
from django.db.models import Q


# from django.http import HttpResponse
# Create your views here.

# rooms = [
#     {'id': '1', 'name': 'Lets learn Django'},
#     {'id': '2', 'name': 'Lets learn Python'},
#     {'id': '3', 'name': 'Frondend development'},
# ]

# menampilkan semua data
# def home(request):
#     rooms = Room.objects.all()
#     topics = Topic.objects.all()

#     context = {'rooms': rooms, 'topics': topics}
#     return render(request, 'base/home.html', context)

# menampilkan semua data berdasarkan filter
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # search by 1 filter
    # rooms = Room.objects.filter(topic__name__icontains=q)

    # search by multifilter
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    # menghitung jumlah room yang tampil
    room_count = rooms.count()

    # menampilkan semua data topic
    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)
    # rooms = Room.objects.filter(topic__name__contains=q)

    # topics = Topic.objects.all()

    # context = {'rooms': rooms, 'topics': topics}
    # return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    # static data
    # room = None
    # for r in rooms:
    #     if r['id'] == pk:
    #         room = r

    context = {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # print in console the data
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    # context = {'room': room}
    return render(request, 'base/delete.html', {'obj': room})


# def topic(request):
#     topics = Topic.objects.all()
#     context = {'topics': topics}
#     return render(request, 'base/home.html', context)

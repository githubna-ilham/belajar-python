from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from base.models import Message, Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    context = {'pages': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'pages': page, 'form': form}
    return render(request, 'base/login_register.html', context)


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

    # menampilkan recent activities
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by(
        '-created')[:10]

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }

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

    # shown all messages data
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@ login_required(login_url='login')
def createRoom(request):

    form = RoomForm()
    if request.method == 'POST':
        # print in console the data
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/create-room.html', context)


@ login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not the host of this room')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@ login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not the host of this room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    # context = {'room': room}
    return render(request, 'base/delete.html', {'obj': room})


# def topic(request):
#     topics = Topic.objects.all()
#     context = {'topics': topics}
#     return render(request, 'base/home.html', context)

def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not the host of this room')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    # context = {'room': room}
    return render(request, 'base/delete.html', {'obj': message})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {'user': user, 'rooms': rooms,
               'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)

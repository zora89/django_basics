from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Something is off, No Records Found!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Some detail is incorrect, retry!')

    loginPage_data = {'page':page}
    return render(request, 'base/login_register.html', loginPage_data )

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'Error Occured in Registration!')




    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
        
    topic = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    


    home_data = {'rooms': rooms, 'topics': topic, 'room_count': room_count, 'room_messages':room_messages }
    return render(request, 'base/home.html', home_data )

def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect ('room', id=room.id)

    room_data = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', room_data)

def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    profile_data = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', profile_data)

@login_required(login_url="login")    
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect('home')

    create_data = {'form': form}
    
    return render(request, 'base/room_form.html', create_data)

@login_required(login_url="login") 
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Not Allowed!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    update_data = {'form': form}
    return render(request, 'base/room_form.html', update_data)

@login_required(login_url="login") 
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('Not Allowed!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url="login") 
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('Not Allowed!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})



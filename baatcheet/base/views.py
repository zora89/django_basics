from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, User
from .forms import RoomForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )
    topic = Topic.objects.all()
    user = User.objects.filter(
        Q(username__icontains=q)
    )

    home_data = {'rooms': rooms, 'topics': topic, 'users': user}
    return render(request, 'base/home.html', home_data )

def room(request, id):
    room = Room.objects.get(id=id)
    room_data = {'room': room}
    return render(request, 'base/room.html', room_data)
    
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

def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    update_data = {'form': form}
    return render(request, 'base/room_form.html', update_data)


def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})



from django.shortcuts import render
from .models import Room
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all()
    home_data = {'rooms': rooms}
    return render(request, 'base/home.html', home_data )

def room(request, id):
    room = Room.objects.get(id=id)
    room_data = {'room': room}
    return render(request, 'base/room.html', room_data)
    
def createRoom(request):
    form = RoomForm()
    create_data = {'form': form}
    
    return render(request, 'base/room_form.html', create_data)


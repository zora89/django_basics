from django.shortcuts import render


rooms = [
    {'id':1, 'name': "Lets Discuss Politics"},
    {'id':2, 'name': "Lets Discuss Science"},
    {'id':3, 'name': "Lets Discuss History"},
]


def home(request):
    home_data = {'rooms': rooms}
    return render(request, 'base/home.html', home_data )

def room(request, id):
    room = None
    for i in rooms:
        if i['id'] == int(id):
            room = i 
    room_data = {'room': room}
    return render(request, 'base/room.html', room_data)
    
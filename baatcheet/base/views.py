from django.shortcuts import render


rooms = [
    {'id':1, 'name': "Lets Discuss Politics"},
    {'id':2, 'name': "Lets Discuss Science"},
    {'id':3, 'name': "Lets Discuss History"},
]


def home(request):
    return render(request, 'home.html', {'rooms' : rooms})

def room(request):
    return render(request, 'room.html')
    
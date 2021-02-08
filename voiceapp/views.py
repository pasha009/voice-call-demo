from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import uuid

tem_user = {}  # user_id to room_id
tem_room = {}  # room_id to user_id

# not a view, just fetches id of user if known or creates new
def identifier(request):
    user_id = request.session.get("user_id", False)
    if not user_id or user_id not in tem_user:
        user_id = uuid.uuid1().hex
        request.session["user_id"] = user_id
        tem_user[user_id] = []
    return user_id
   
def index(request): 
    user_id = identifier(request)
    if request.method == "POST":
        room_id = str(uuid.uuid1().hex)[:5]
        tem_room[room_id] = [user_id,]
        tem_user[user_id].append(room_id)
    context = { 
        "id" : user_id, 
        "rooms": tem_user[user_id]
    }
    return render(request, "index.html", context) 

def call_view(request, room_id):
    user_id = identifier(request)
    if room_id not in tem_room:
        return HttpResponseNotFound("room not found")
    if user_id not in tem_room[room_id]:
        tem_room[room_id].append(user_id)
    context = {
        "id" : user_id,
        "users" : tem_room[room_id]
    }
    return render(request, "room.html", context)

##### TEST part

test_rooms = {}

def test_index(request):
    if request.method == "POST":
        room_id = str(uuid.uuid1().hex)[:5]
        test_rooms[room_id] = []
        return redirect('test_call_view', room_id=room_id)
    return render(request, "test_index.html")

def test_call_view(request, room_id):
    if room_id not in test_rooms:
        return HttpResponseNotFound("room not found")
    user_id = str(uuid.uuid1().hex)
    test_rooms[room_id].append(user_id)
    context = {
        "id" : user_id,
        "users" : test_rooms[room_id]
    }
    return render(request, "test_room.html", context)


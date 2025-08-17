from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from .models import Room, Message, Topic, User
from .forms import RoomForm
from django.contrib import messages


# view all rooms
def rooms(request):
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=search_query) |
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
        ).distinct().order_by('-updated_at')
    
    topics = Topic.objects.all()
    recent_activity = Message.objects.filter(Q(room__topic__name__icontains=search_query))[:5]
    # User = get_user_model() remove is pending
    top_hosted = User.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[:3]
    context = {'rooms': rooms, 'topics':topics, 'recent_activity': recent_activity, 'top_hosted': top_hosted}
    return render(request, 'base/rooms.html', context)


# pk is a parameter come from the url
def public_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_activity = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'recent_activity': recent_activity, 'topics': topics}
    return render(request, 'base/public_profile.html', context)


# view a room
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        message.save()
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


# create/update room
@login_required(login_url='user:login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        Room.objects.create(
            topic=topic,
            host=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.success(request, "Room created successfully.")
        return redirect('rooms')
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# update room
@login_required(login_url='user:login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        messages.error(request, "You are not authorized to update this room.")
        return redirect('rooms')

    if request.method == 'POST':
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, "Room updated successfully.")
        return redirect('rooms')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


# delete a room
@login_required(login_url='user:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here!")
    
    if request.method == 'POST':
        room.delete()
        return redirect('rooms')
    return render(request, 'base/delete.html',{'room':room})


# delete the message of a room
@login_required(login_url='user:login')
def deleteMessage(request, pk):
    if request.method == 'POST':
        userMessage = Message.objects.get(id=pk)
        if request.user != userMessage.user:
            return HttpResponse("Your are not allowed here!")

        userMessage.delete()
        messages.success(request, "Your message deleted successfully")
        if userMessage.room.message_set.exists():
            return redirect('room', pk=userMessage.room.id)
        else:
            userMessage.room.participants.remove(request.user)

    return redirect('rooms')
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room, Topic, Message


def login_page(request):
    page = 'login'
    err_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            err_message = "User does not exist!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                err_message = "Incorrect username or password!"

    context = {
        'page': page,
        'err_message': err_message,
    }
    return render(request, 'base/login_page.html', context)

def register_page(request):
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {
        'page' : page,
        'form' : form,
    }
    return render(request, 'base/login_page.html', context)

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect("home")

def home(request):

    rooms = Room.objects.all()
    room_count = rooms.count()
    topics = Topic.objects.all()
    messages = Message.objects.all().order_by('-created')

    q = request.GET.get('q') if request.GET.get('q') else ''

    if q:
        rooms = rooms.filter(Q(name__icontains=q) |
                             Q(topic__name__icontains=q)|
                             Q(host__username__icontains=q))
        messages = messages.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'messages' : messages,
        'room_count' : room_count,
    }
    return render(request, 'base/home.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_count = rooms.count()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user,
               'rooms' : rooms,
               'messages' : messages,
               'topics' : topics,
               'room_count' : room_count,}
    return render(request, 'base/profile.html', context)


def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")

    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    participant_count = participants.count()

    if request.method == 'POST':
        message_body = request.POST.get('msg_body')
        if message_body:
            message = Message(room=room, user=request.user, body=message_body)
            if request.user not in participants:
                room.participants.add(request.user)

            message.save()
            return redirect('room', pk=room.id)

    context = {
        'room': room,
        'messages': messages,
        'participants': participants,
        'participant_count': participant_count,
    }
    return render(request, 'base/room_page.html', context)

@login_required(login_url='login_page')
def create_room(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect("home")
    else:
        form = RoomForm()

    topics = Topic.objects.all()
    context = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login_page')
def edit_room(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user != room.host:
        return redirect('room', pk=pk)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=pk)

    else:
        form = RoomForm(instance=room)
        topics = Topic.objects.all()

    context = {
        'form': form,
        'topics': topics,
        'room' : room,
    }
    return render(request, "base/create_room.html", context)

@login_required(login_url='login_page')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect("home")
    context = {
        'obj': room,
    }
    return render(request, 'base/delete.html', context)

@login_required(login_url='login_page')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room

    if message.user != request.user:
        return redirect('room', room.id)

    if request.method == 'POST':
        message.delete()
        return redirect('room', room.id)

    context={
        'obj' : message
    }
    return render(request, 'base/delete.html', context)


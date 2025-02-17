from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
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
    topics = Topic.objects.all()

    q = request.GET.get('q') if request.GET.get('q') else ''

    if q:
        rooms = rooms.filter(Q(name__icontains=q) |
                             Q(topic__name__icontains=q)|
                             Q(host__username__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
    }
    return render(request, 'base/home.html', context)

@login_required(login_url='login_page')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            return redirect("home")
    else:
        form = RoomForm()

    context = {
        'form': form,
    }
    return render(request, 'base/create_room.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message_body = request.POST.get('msg_body')
        if message_body:
            message = Message(room=room, user=request.user, body=message_body)
            message.save()
            return redirect('room', pk=room.id)

    context = {
        'room': room,
        'messages': messages,
        'participants': participants,
    }
    return render(request, 'base/room_page.html', context)

@login_required(login_url='login_page')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.set([request.user])
            room.save()
            return redirect("home")
    else:
        form = RoomForm()
    context = {
        'form': form,
    }
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login_page')
def edit_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            return redirect("home")
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
    }
    return render(request, "base/create_room.html", context)

@login_required(login_url='login_page')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect("home")
    context = {
        'room': room,
    }
    return render(request, 'base/delete_room.html', context)

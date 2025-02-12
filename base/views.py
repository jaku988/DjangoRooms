from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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

    context = {
        'page': page,
        'err_message': err_message,
    }
    return render(request, 'base/login_page.html', context)


def register_page(request):
    page = 'register'

    context = {
        'page': page,
    }
    return render(request, 'base/login_page.html', context)

@login_required(login_url='login_page')
def logout_page(request):
    pass


#strona startowa aplikacji
def home(request):
    return render(request, 'base/home.html')

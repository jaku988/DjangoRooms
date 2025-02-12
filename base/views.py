from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        'page': page,
        'form' : form,
    }
    return render(request, 'base/login_page.html', context)

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect("home")


#strona startowa aplikacji
def home(request):
    return render(request, 'base/home.html')

from django.shortcuts import render




#strona startowa aplikacji
def home(request):
    return render(request, 'base/home.html')

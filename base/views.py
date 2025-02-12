from django.http import HttpResponse
from django.shortcuts import render




#strona startowa aplikacji
def home(request):
    return HttpResponse("<h1>Strona Startowa</h2>")

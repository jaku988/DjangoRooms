from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login-page', views.login_page, name='login'),
    path('register-page', views.register_page, name='register'),
    path('logout', views.logout_page, name='logout'),
]
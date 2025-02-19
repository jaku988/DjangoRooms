from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login-page', views.login_page, name='login'),
    path('register-page', views.register_page, name='register'),
    path('logout', views.logout_page, name='logout'),
    path('room<str:pk>', views.room, name='room'),
    path('create-room', views.create_room, name='create_room'),
    path('edit-room/<str:pk>', views.edit_room, name='edit_room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete_room'),
    path('delete-message/<str:pk>', views.delete_message, name='delete_message'),
]
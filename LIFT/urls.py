from django.contrib import admin
from django.urls import path
from .views import homeview, loginview
urlpatterns = [
    path('', homeview.index, name="index"),
    path('login', loginview.login, name="Login"),
    path('register', loginview.register, name="Register"),
]
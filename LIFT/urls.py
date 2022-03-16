from django.contrib import admin
from django.urls import path
from .views import homeview, loginview,bookview
urlpatterns = [
    path('', homeview.landing_page, name="landing"),
    path('index', homeview.index, name="HomePage"),
    path('login', loginview.signin, name="Login"),
    path('register', loginview.register, name="Register"),
    path('signout', loginview.signout, name="Logout"),
    path('booking',bookview.book, name= "bookRide")
]
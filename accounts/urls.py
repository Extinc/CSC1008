from django.contrib import admin
from django.urls import path
from. import views
urlpatterns = [
    path('', views.signin, name="login"),
    path('rindex', views.register, name="register"),
    path('signout', views.signout, name="signout"),
]
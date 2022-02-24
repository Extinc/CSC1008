from django.shortcuts import render
from django.http import HttpResponse
import requests


# Create your views here.
def Login(request):
    return render(request, 'login.html', {'title': "Login"})

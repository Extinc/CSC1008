from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from django.contrib.auth.decorators import login_required


# Create your views here.



def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        args = {}
        # MISSING USER AUTHENTICATION

        if user is not None:
            login(request, user)
            User.objects.filter(username=username).update(last_login=timezone.now())

            return redirect('HomePage')
        else:
            messages.error(request, "Username / Password Incorrect")

    return render(request, 'login.html', {'title': "Login"})


def register(request):
    if request.user.is_authenticated:
        return redirect('HomePage')
    else:
        if request.method == "POST":
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username")

            if len(username) > 10:
                messages.error(request, "Username must be under 10 characters")

            if pass1 != pass2:
                messages.error(request, "Passwords didn't match!")

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!")
            customergrp = Group.objects.get(name='customer')
            user = User.objects.create_user(username=username, email=email, password=pass1)
            user.first_name = fname
            user.last_name = lname

            user.save()
            user.groups.add(customergrp)
            messages.success(request, "Your Account has been successfully created")
            return redirect('Login')

        return render(request, 'register.html', {'title': "Register"})


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("landing")
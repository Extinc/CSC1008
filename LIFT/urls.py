from django.urls import path

from .codes import BookingFunctions
from .views import homeview, loginview
from .views import testview, api

urlpatterns = [
    path('', homeview.landing_page, name="landing"),
    path('index', homeview.index, name="HomePage"),
    path('test', testview.testpage, name="TestPage"),
    path('getInfo/', api.getInfo),
    path('getPrice/', api.getPrice),
    path('findnearest/', api.getNearest),  # API CALL FOR FINDING NEAREST POINT TO USER
    path('bookingsearch/', api.booking_search),  # API CALL FOR DO BOOKING SEARCH
    path('findDriver/', api.findDriver),
    path('get_addr/', api.get_address),
    path('endRide/', BookingFunctions.endRide),
    path('select_pickup/', testview.select_pickup),
    path('login', loginview.signin, name="Login"),
    path('register', loginview.register, name="Register"),
    path('signout', loginview.signout, name="Logout"),
]

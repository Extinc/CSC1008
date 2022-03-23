from django.urls import path
from .views import homeview, loginview, bookview, testview
from django.urls import path

from .views import homeview, loginview, bookview

urlpatterns = [
    path('', homeview.landing_page, name="landing"),
    path('index', homeview.index, name="HomePage"),
    path('test', testview.testpage, name="TestPage"),
    path('plot_route/', testview.plot_route),
    path('getInfo/', testview.getInfo),
    # path('showPrice/',testview.showPrice),
    path('select_pickup/', testview.select_pickup),
    path('get_addr/', homeview.get_address),
    path('login', loginview.signin, name="Login"),
    path('register', loginview.register, name="Register"),
    path('signout', loginview.signout, name="Logout"),
    path('booking', bookview.book, name="bookRide"),

]

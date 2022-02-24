from django.shortcuts import render
from django.http import HttpResponse
import requests


# Create your views here.
def index(request):
    response = requests.get(
        "https://developers.onemap.sg/commonapi/search?searchVal=revenue&returnGeom=Y&getAddrDetails=Y&pageNum=1")
    response1 = requests.get(
        "https://developers.onemap.sg/privateapi/popapi/getPlanningarea?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjgsInVzZXJfaWQiOjgsImVtYWlsIjoiY2xvc2Vkc3VwZXJhcGl1c2VyQHNsYS5nb3Yuc2ciLCJmb3JldmVyIjpmYWxzZSwiaXNzIjoiaHR0cDpcL1wvMTAuMC4zLjExOjgwODBcL2FwaVwvdjJcL3VzZXJcL3Nlc3Npb24iLCJpYXQiOjE0NjczNjA0NjEsImV4cCI6MTQ2Nzc5MjQ2MSwibmJmIjoxNDY3MzYwNDYxLCJqdGkiOiJjNzkwZjBhYjQwOTcwNzFhMWE4MDQ1YTFjNjRlM2M5MSJ9.Pp6zos_p_jjiChWsi2F7O-k-yxgr173QlXqeGc-rpWw&lat=1.3&lng=103.8")
    data = response.json();
    # data1 = response1.json();
    return render(request, 'index.html', {'title': "Home"})
    # return HttpResponse(data['results'][0]['LONGITUDE'])

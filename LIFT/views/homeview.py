from django.shortcuts import render
from django.http import HttpResponse
import requests

onemapdev_url = "https://developers.onemap.sg"
# Create your views here.
def index(request):
    # urls = onemapdev_url+ "/privateapi/popapi/getAllPlanningarea"
    urls = onemapdev_url+ "/commonapi/search"
    params = {}
    params['token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjg0NjUsInVzZXJfaWQiOjg0NjUsImVtYWlsIjoiYWxwaGF0b29uQGhvdG1haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjQ3MTUyMjAxLCJleHAiOjE2NDc1ODQyMDEsIm5iZiI6MTY0NzE1MjIwMSwianRpIjoiMTczN2Y3OWI2YjA3ZGMxZGY3MDczNTI4NDFjNTUxYzEifQ.r0LRxUefCvw7-Op_B1hzM4bFo3s5iFXeeNKiC9xfdk4'
    # params['lat'] = '1.3776586388017433'
    # params['returnGeom'] = 'Y'
    print(params)
    response = requests.get(urls, params=params)
    data = response.json()
    # data1 = response1.json();
    args = {}
    args['title'] = "Home"
    args['showcase'] = "HELLO WORLD"
    args['testdata'] = data
    print(args)
    if request.user.is_authenticated:
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)
    # return HttpResponse(data['results'][0]['LONGITUDE'])
from django.shortcuts import render
from django.http import HttpResponse
import requests
import classes.AcceptedRides


onemapdev_url = "https://developers.onemap.sg"
# Create your views here.
def book(request):
    

    

    return render(request, 'book.html')
   
       
    # return HttpResponse(data['results'][0]['LONGITUDE'])

def entryLocation(location):
    urls = onemapdev_url+ "/commonapi/search"
    params ={}
    params["searchVal"] = location
    params["returnGeom"] = "Y"
    params["getAddrDetails"] = "Y"
    response = requests.get(urls, params=params)
    return response.json()

def distanceCalculation(startLocation,endLocation):
    urls = onemapdev_url+ "/privateapi/routingsvc/route"
    params ={}
    params["start"] = startLocation
    params["end"] = endLocation
    params["routeType"] = "drive"
    params['token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjg0NjUsInVzZXJfaWQiOjg0NjUsImVtYWlsIjoiYWxwaGF0b29uQGhvdG1haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjQ3MTUyMjAxLCJleHAiOjE2NDc1ODQyMDEsIm5iZiI6MTY0NzE1MjIwMSwianRpIjoiMTczN2Y3OWI2YjA3ZGMxZGY3MDczNTI4NDFjNTUxYzEifQ.r0LRxUefCvw7-Op_B1hzM4bFo3s5iFXeeNKiC9xfdk4'
    response = requests.get(urls, params=params)
    return response.json()


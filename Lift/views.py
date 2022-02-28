from django.shortcuts import render
from django.http import HttpResponse
import requests

onemapdev_url = "https://developers.onemap.sg"
# Create your views here.
def index(request):
    urls = onemapdev_url+ "/privateapi/popapi/getAllPlanningarea"
    params = {}
    params['token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjg0NjUsInVzZXJfaWQiOjg0NjUsImVtYWlsIjoiYWxwaGF0b29uQGhvdG1haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjQ1OTQ1NjI5LCJleHAiOjE2NDYzNzc2MjksIm5iZiI6MTY0NTk0NTYyOSwianRpIjoiMmMyZjA1MjU0MTkwZDVkMTYyYTZkZDI1OGY1OGJiODAifQ._fQ4y6Od1uFnftfElyemT1yEiraOX-LX-5Ojy6NHJaY'
    params['lat'] = '1.3776586388017433'
    params['lng'] = '103.84874408446957'
    response = requests.get(urls, params=params)
    data = response.json();
    # data1 = response1.json();
    args = {}
    args['title'] = "Home"
    args['testdata'] = data
    if request.user.is_authenticated:
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)
    # return HttpResponse(data['results'][0]['LONGITUDE'])

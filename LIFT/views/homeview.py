from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from ..codes.Routes import roadedge_df
# Create your views here.
from ..models.models import PointInfo
from django.core import serializers

search_result = None

def landing_page(request):
    return render(request, 'landing.html')

@login_required(login_url='/login')
def index(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:
        print(roadedge_df)
        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)


def get_address(request):
    if request.method == "GET":
        # search = request.GET.get('search')
        searchval = request.GET['search']
        payload = []
        global search_result
        search_result = PointInfo.objects.all().filter(
            Q(BUILDINGNAME__startswith=searchval) | Q(ROAD__startswith=searchval) | Q(POSTALCODE__startswith=searchval))
        searchload = {}
        for search in search_result:
            if search.BUILDINGNAME != "" and search.BUILDINGNAME != "null":
                searchload[search.id] = search.BUILDINGNAME
                # payload.append(search.BUILDINGNAME)
            if search.BLOCK != "":
                if search.id not in searchload:
                    searchload[search.id] = search.BLOCK
                # payload.append(search.BLOCK)
            if search.POSTALCODE != "":
                if search.id not in searchload:
                    searchload[search.id] = search.POSTALCODE
                # payload.append(search.POSTALCODE)
        return JsonResponse(searchload, safe=False)

def getNearest(request):
    result = find_nearest(float(request.GET['lat']), float(request.GET['long'])).to_json(orient='records')
    return JsonResponse({'data': result})

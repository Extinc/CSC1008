from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from ..codes.Pathfinder import PathFinder
from ..codes.Routes import roadedge_df, find_nearest
# Create your views here.
from ..models.models import PointInfo

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
        search_result = PointInfo.objects.exclude(BUILDINGNAME__isnull=True).exclude(BUILDINGNAME__exact='').annotate(
            BUILDINGNAME_count=Count('BUILDINGNAME')).filter(
            Q(BUILDINGNAME__startswith=searchval) | Q(ROAD__startswith=searchval) | Q(POSTALCODE__startswith=searchval))
        searchload = {}
        for search in search_result:
            if search.BUILDINGNAME not in searchload.values():
                if search.BUILDINGNAME!= "" and search.BUILDINGNAME != "null":
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
    if request.method == "GET":
        result = find_nearest(float(request.GET['lat']), float(request.GET['long'])).to_json(orient='records')
        return JsonResponse({'data': result})


def booking_search(request):
    if request.method == "POST":
        startid = request.POST['starting']
        endid = request.POST['ending']
        pf = PathFinder()
        start = PointInfo.objects.get(id=startid)
        end = PointInfo.objects.get(id=endid)

        pf.find_path(start.lat, start.long, end.lat, end.long)
        geom = pf.generate_geojson('LineString')
        return JsonResponse(geom, safe=False)

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from ..codes.Routes import roadedge_df
# Create your views here.
from ..datastructure.Trie import Trie
from ..models.models import PointInfo

search_result = None
search_data = None

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
        global search_result, search_data
        if len(searchval) == 1:

            search_data = Trie()
            search_result = PointInfo.objects.all().filter(Q(BUILDINGNAME__startswith=searchval) | Q(ROAD__startswith=searchval) | Q(POSTALCODE__startswith=searchval))

            for search in search_result:
                if search.BUILDINGNAME != "":
                    search_data.insert(1, search.BUILDINGNAME)
                if search.ROAD != "":
                    search_data.insert(1,search.ROAD)
                if search.POSTALCODE != "":
                    search_data.insert(1, search.POSTALCODE)

        else:
            # global search_data
            # search_data.printAutoSuggestions(searchval)
            search_data.computetop5()
            print()
        return JsonResponse({'status': True, 'payload': payload})

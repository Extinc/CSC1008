from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
# Create your views here.
from ..models.models import PointInfo

search_result = None


def landing_page(request):
    return render(request, 'landing.html')


@login_required(login_url='/login')
def index(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:

        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)





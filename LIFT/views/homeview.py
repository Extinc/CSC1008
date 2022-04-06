from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
# Create your views here.
from ..models.models import PointInfo


@login_required(login_url='/login')
def index(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:

        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        lname = request.user.last_name
        args['fname'] = fname + " " + lname

        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)





from flask import Blueprint

# from wsgi import app
routes = Blueprint('routes', __name__, static_folder="static", template_folder="templates")

from .home import *
from .maps import *
from .user import *

from pickle import FALSE
from aryanwheels.settings.dev import SECRET_KEY
from .common import *


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = []
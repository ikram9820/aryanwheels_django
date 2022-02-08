import imp
from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-4d6w#q*q&j%2059kqunbsixgafc6*z&)#r77+bo27@k8t3ld46'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aryanwheels',
        'HOST':'localhost',
        'USER':'root',
        'PASSWORD':'root',
    }
}

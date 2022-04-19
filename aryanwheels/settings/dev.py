from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-4d6w#q*q&j%2059kqunbsixgafc6*z&)#r77+bo27@k8t3ld46'

ALLOWED_HOSTS = ['10.0.2.2','127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}

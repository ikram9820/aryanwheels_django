from django_filters.rest_framework import FilterSet
from . import models
class VehicleFilter(FilterSet):
    class Meta:
        model= models.Vehicles
        fields= {
            'owner_id': ['exact'],
            'price': ['gt','lt'],
        }

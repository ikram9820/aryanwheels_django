from django.contrib import admin
from django.http import HttpRequest
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models  

@admin.register(models.Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug':['model']
    }
    list_display= ['id','car_name','owner','price','vehicles_type']
    list_editable= ['price','vehicles_type']
    list_filter=['vehicles_type','posting_date']
    list_per_page= 10
    list_select_related= ['owner__user']
    search_fields= ['id','manufacturer','model','model_year']

    def car_name(self,vehicle):
        return f'{vehicle.manufacturer}, {vehicle.model} {vehicle.model_year}'

    # @admin.display(ordering='likes')
    # def like_rate(self,vehicle):
    #     if(vehicle.likes==None):
    #         return 'Low rated vehicle'
            
    #     if vehicle.likes <100:
    #         return 'Low rated vehicle'
    #     return 'High rated vehicle'

@admin.register(models.VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    pass







@admin.register(models.Seller)
class UserAdmin(admin.ModelAdmin):
    list_display= ['id','user','whatsapp_contact','city','country','vehicle_count']
    list_editable= ['whatsapp_contact','city']
    list_per_page= 10
    search_fields= ['user__first_name','user__last_name']

    @admin.display(ordering='vehicle_count')
    def vehicle_count(self,user):
        url = (reverse('admin:showroom_vehicles_changelist')
               + '?' + urlencode({'owner__id':str(user.id)})
               )
        return format_html('<a href="{}">{}</a>',url,user.vehicle_count)
         

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(vehicle_count= Count('vehicles'))
    




@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_select_related= ['user']

@admin.register(models.LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    list_select_related= ['like__user','vehicle']

from rest_framework import serializers

from . import models



class ImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return models.VehicleImage.objects.create(vehicle_id=self.context['vehicle_id'],**validated_data)

    class Meta:
        model= models.VehicleImage
        fields= ['id','image']



class VehiclesSerializer(serializers.ModelSerializer):

    # name = serializers.SerializerMethodField(method_name='car_name',read_only= True)
    id = serializers.IntegerField(read_only= True)
    owner= serializers.StringRelatedField(read_only=True)
    owner_id= serializers.IntegerField(read_only=True)
    posting_date=serializers.DateTimeField(read_only=True)
    
    # manufacturer = serializers.CharField(write_only=True)
    # model = serializers.CharField(write_only=True)
    # model_year = serializers.IntegerField(write_only=True)
    slug=serializers.SlugField(write_only=True)

    images= ImageSerializer(many= True,read_only=True)
    
    class Meta:
        model = models.Vehicles
        fields = ['id','owner_id','owner','manufacturer', 'model','slug','model_year', 'price',
                  'posting_date','distance_traveled','description','images']
  
    # def car_name(self,vehicle:models.Vehicles):
    #     return f'{vehicle.manufacturer}, {vehicle.model} {vehicle.model_year}'

    def create(self, validated_data):
        owner_id=self.context['owner_id']
        if(owner_id!=None):
            return models.Vehicles.objects.create(owner_id=owner_id,**validated_data)
        return None
 


# class SimpleVehicleSerializer(serializers.ModelSerializer):
#     images= ImageSerializer(read_only=True,many =True)
#     class Meta:
#         model= models.Vehicles
#         fields= ['id','model','model_year','price','posting_date','distance_traveled','color','description','likes','images']


class FollowSerializer(serializers.ModelSerializer):

    user_id= serializers.IntegerField(read_only=True)
    seller_id= serializers.IntegerField(read_only=True)
    class Meta:
        model= models.Follow
        fields= ['id','user_id','seller_id']

    def validate_seller_id(self,value):
        if not models.Seller.objects.filter(pk=value).exists():
            raise serializers.ValidationError("This user has no seller account")
        return value 

    def save(self, **kwargs):
        user= self.context['user_id']
        seller= self.context['seller_id']
        if not models.Seller.objects.filter(pk=seller).exists():
            raise serializers.ValidationError("This user has no seller account")
        try:
            follow= models.Follow.objects.get(user_id=user,seller_id=seller)
            follow.delete()
            self.instance= follow
        except models.Follow.DoesNotExist:
            self.instance= models.Follow.objects.create(user_id=user,seller_id=seller)

        return self.instance


class SellerSerializer(serializers.ModelSerializer):
    user= serializers.StringRelatedField(read_only=True)
    vehicles= VehiclesSerializer(read_only= True,many= True)
    post_count= serializers.IntegerField(source= 'vehicles.count',read_only= True)
    followers= serializers.IntegerField(source= 'following.count',read_only= True)
    class Meta:
        model = models.Seller
        fields = ['id','user', 'whatsapp_contact','address','city','country','post_count','followers','bio','vehicles',]

  

class LikedItemSerializer(serializers.ModelSerializer):
    vehicle= VehiclesSerializer(read_only=True)
    vehicle_id= serializers.IntegerField(write_only=True)
                                            
    class Meta:
        model= models.LikedItem
        fields=['id','vehicle_id','vehicle']


    def validate_vehicle_id(self,value):
        if not models.Vehicles.objects.filter(pk=value).exists():
            raise serializers.ValidationError('no vehicle is posted with this id')
        return value

    def save(self, **kwargs):
        like_id= self.context['like_id']
        vehicle_id= self.validated_data['vehicle_id']
        try:
            liked_item= models.LikedItem.objects.get(like_id=like_id,vehicle_id=vehicle_id)
            liked_item.delete()
            self.instance= liked_item
        except models.LikedItem.DoesNotExist:
            self.instance= models.LikedItem.objects.create(like_id=like_id,**self.validated_data)

        return self.instance



class LikeSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only= True)
    user_id= serializers.IntegerField(required=False)
    liked_at= serializers.DateTimeField(read_only=True)
    liked_item= LikedItemSerializer(many= True,read_only=True)
    
    class Meta:
        model= models.Like
        fields= ['id','user_id','liked_at','liked_item']
    


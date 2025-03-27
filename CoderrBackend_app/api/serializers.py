from django.forms import ValidationError
from rest_framework import serializers, status
from CoderrBackend_app import models
from CoderrBackend_app.models import UserProfile, Offer, OfferDetail, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Min
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email']
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    class Meta:
        model = UserProfile 
        fields = [ "user", "username", "first_name", "last_name", 'file', 'location', 'tel', 'description', 'working_hours', 'type', "email",'created_at']
    
    def update(self, instance, validated_data):        
        """Siehe Dokumentation in docs/serializers.md"""
        user_data = validated_data.pop('user', None)      
        if user_data:
            user = instance.user  
            user.first_name = self.initial_data.get('first_name', user.first_name)
            user.last_name = self.initial_data.get('last_name', user.last_name)
            user.email = self.initial_data.get('email', user.email)
            user.save() 
        
        return super().update(instance, validated_data)

class UserAuthTokenSerializer(serializers.Serializer):
  username = serializers.CharField(write_only=True)
  password = serializers.CharField(write_only=True)
  
  def validate(self, attrs):  
        """Siehe Dokumentation in docs/serializers.md"""
        username = attrs.get('username')         
        password = attrs.get('password')       
        user = User.objects.filter(username=username).first()
        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
                raise serializers.ValidationError('Invalid username or password')
        attrs['user'] = authenticated_user
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True) 
   
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password','repeated_password','type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self): 
        """Siehe Dokumentation in docs/serializers.md"""        
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        if pw != repeated_pw:
            raise serializers.ValidationError({'password': 'Password must match'})
        user = User(
        email=self.validated_data['email'],
        username=self.validated_data['username'] )
        user.set_password(pw)
        user.save()            
        type = self.validated_data['type']           
        UserProfile.objects.create(user=user, type=type)
        return user
        
        
class OfferDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)  
    delivery_time_in_days = serializers.IntegerField()
    class Meta:
        model = OfferDetail
        fields = '__all__'
        extra_kwargs = {'offer': {'required': False},  'id': {'required': False}}

  
class OfferSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True)
    class Meta:
        model = Offer
        fields = '__all__'
        extra_kwargs = {'image': {'required': False, 'allow_null': True},
                        'user': {'read_only': True}}
    
    def get_user_details(self, obj):
        """Siehe Dokumentation in docs/serializers.md"""    
        if self.context.get("view") == "retrieve":
            return None
        return {
            "first_name": obj.user.first_name,
            "last_name":obj.user.last_name,            
            "username": obj.user.username
        }          
      
    def get_min_price(self, obj):
        """Siehe Dokumentation in docs/serializers.md"""           
        return obj.details.aggregate(Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        """Siehe Dokumentation in docs/serializers.md"""         
        return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0
       
    
    def create(self, validated_data):
        """Siehe Dokumentation in docs/serializers.md"""        
        try: 
            details_data = validated_data.pop("details", [])             
            offer = Offer.objects.create(**validated_data)      
            for detail in details_data:
                revisions = detail.get('revisions')
                if revisions == 0 or revisions is None:
                    detail['revisions'] = 1  
                if not OfferDetail.objects.filter(offer=offer, title=detail['title']).exists():
                    OfferDetail.objects.create(offer=offer, **detail)     
            return offer
        except Exception as e:
            print(f"Error al crear oferta: {e}")  
            raise   
        
    def update(self, instance, validated_data):
        """Siehe Dokumentation in docs/serializers.md"""           
        details_data = validated_data.pop("details", [])           
        min_price = self.get_min_price(instance)
        min_delivery_time = self.get_min_delivery_time(instance)        
        self.update_offer(instance, validated_data, min_price, min_delivery_time)       
        self.update_offer_details(instance, details_data)
        min_price = self.get_min_price(instance)
        min_delivery_time = self.get_min_delivery_time(instance)
        if instance.min_price != min_price or instance.min_delivery_time != min_delivery_time:
            instance.min_price = min_price
            instance.min_delivery_time = min_delivery_time
            instance.save()
        return instance
  
    def update_offer(self, instance, validated_data, min_price, min_delivery_time):        
        """Siehe Dokumentation in docs/serializers.md"""        
        for attr, value in validated_data.items():            
                setattr(instance, attr, value)
        instance.min_price = min_price
        instance.min_delivery_time = min_delivery_time       
        instance.save()  
       
        
    def update_offer_details(self, instance, details_data):          
        """Siehe Dokumentation in docs/serializers.md"""
        existing_details = {detail.offer_type: detail for detail in OfferDetail.objects.filter(offer=instance)}       
        for detail_data in details_data:       
            offerType = detail_data.get('offer_type')   
            revisions = detail_data.get('revisions')  
            detail_data['revisions'] = 1 if revisions == 0 or revisions is None else revisions       
            if offerType in existing_details:
                detail_instance = existing_details[offerType]
                for attr, value in detail_data.items():
                    setattr(detail_instance, attr, value)                                        
                detail_instance.save()
            else:                
                OfferDetail.objects.create(offer=instance, **detail_data)      
     

class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.SerializerMethodField() 
    features = serializers.ListField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)
    class Meta:
        model = Order        
        fields = '__all__'   
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('offer_detail', None)  # Eliminar el campo 'offer_detail' de la representación
        return representation
    
    def get_price(self, obj):  # Asegurar que el método esté aquí
        """Devuelve el precio como número en lugar de string"""
        return float(obj.offer_detail.price) if obj.offer_detail else None
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ["reviewer"]
        
        
   
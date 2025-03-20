
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from CoderrBackend_app.api.serializers import UserProfileSerializer, UserAuthTokenSerializer, RegistrationSerializer, OfferSerializer, OfferDetailSerializer, OrderSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from CoderrBackend_app.models import UserProfile, Offer, OfferDetail, Order, Review
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerProfile, CanCreateReview, CanCreateOrder, CanCreateOffer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.db.models import Avg, Q
from rest_framework.pagination import PageNumberPagination
from CoderrBackend_app.filters import OfferFilter, ReviewFilter
from rest_framework.parsers import JSONParser

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer  
    permission_classes = [IsAuthenticated, IsOwnerProfile]          
 
    
class CustomerListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer').select_related('user')
    serializer_class = UserProfileSerializer
  
  
class BusinessListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business').select_related('user')
    serializer_class = UserProfileSerializer
       
    
class LoginView(ObtainAuthToken):
    serializer_class = UserAuthTokenSerializer

    def post(self, request, *args, **kwargs): 
        """Siehe Dokumentation in docs/views.md"""        
        username = request.data.get('username', None)
        password = request.data.get('password', None)      
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)            
        if username and not password:
            return self.guest_login(username)        
        return self.user_login(request)

    def success_response(self, user, token, message):
        """Siehe Dokumentation in docs/views.md"""        
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
            "message": message }, status=status.HTTP_200_OK)

    def error_response(self, error_message, status_code):
        """Siehe Dokumentation in docs/views.md"""        
        return Response({"error": error_message}, status=status_code)

    def guest_login(self, username):          
        """Siehe Dokumentation in docs/views.md"""        
        user = self.authenticate_or_create_user(username)
        token, _ = Token.objects.get_or_create(user=user)
        return self.success_response(user, token, "Login Successfully as Guest!")
        
    def user_login(self, request): 
        """Siehe Dokumentation in docs/views.md"""        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']    
            token, _ = Token.objects.get_or_create(user=user)
            return self.success_response(user, token, "Login Successfully!")
        return self.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_guest_type_from_username(self, username):       
        """Siehe Dokumentation in docs/views.md"""        
        if username.startswith("guest_"):       
            user_type = username.split("guest_")[1]           
            return user_type
        return None  
    
    def authenticate_or_create_user(self, username):        
        """Siehe Dokumentation in docs/views.md"""        
        user_type = self.get_guest_type_from_username(username)      
        if user_type is None:
            raise ValidationError("Invalid username format.")    
        user = self.get_or_create_guest_user(user_type)
        self.ensure_guest_profile(user, user_type)
        return user
    
    def get_or_create_guest_user(self, user_type): 
        """Siehe Dokumentation in docs/views.md"""        
        if user_type == 'customer':            
            user, created = User.objects.get_or_create(
                username="guest_customer", email="guest_customer@example.com", 
                defaults= {"first_name": "Guest", "last_name": "Customer"} )            
        elif user_type == 'business':
            user, created = User.objects.get_or_create(
            username="guest_business", email="guest_business@example.com",
            defaults={"first_name": "Guest", "last_name": "Business"} )      
        if created:
            user.set_password("guest_password") 
            user.save()    
        return user
          
    def ensure_guest_profile(self, user, user_type):
        """Siehe Dokumentation in docs/views.md"""                        
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        if user_profile.type != user_type:
            user_profile.type = user_type
            user_profile.save()                    
        
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Siehe Dokumentation in docs/views.md"""         
        serializer = RegistrationSerializer(data=request.data)       
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data= {"token": token.key,                  
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
                "message": "Successfully registered!"}            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

class OfferPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = 'page_size'
    max_page_size = 10


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CanCreateOffer]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter    
    
    def list(self, request, *args, **kwargs):
        """Siehe Dokumentation in docs/views.md"""
        offers = self.get_queryset()
        page = self.paginate_queryset(offers)
        data = []        
        for offer in page:                  
            details = [ {
            "id": detail.id, "url": f"/offerdetails/{detail.id}/"}for detail in offer.details.all() ]  
            offer_data = OfferSerializer(offer).data
            offer_data['details'] = details
            data.append(offer_data)
        return self.get_paginated_response(data)
       
    def get_queryset(self):    
        """Siehe Dokumentation in docs/views.md """
        queryset = Offer.objects.all() 
        user_id = self.request.query_params.get('creator_id')
        if user_id and self.request.user.is_authenticated:
            queryset = queryset.filter(user=user_id)
        params = self.request.query_params   
        filters = Q()
        if search := params.get('search'): filters |= Q(title__icontains=search) | Q(description__icontains=search)       
        if max_delivery_time := params.get('max_delivery_time'): filters &= Q(min_delivery_time__lte=max_delivery_time)
        if min_price := params.get('min_price'): filters &= Q(min_price__gte=min_price)   
        queryset = queryset.filter(filters)
        if ordering := params.get('ordering'): queryset = queryset.order_by(ordering)      
        return queryset    
        
    
    def perform_create(self, serializer, format=None):        
        """Siehe Dokumentation in docs/views.md"""       
        user = self.request.user 
        self.validate_user_permissions(user)
        details_data = self.get_validated_details()        
        min_price, min_delivery_time = self.calculate_min_values(details_data)        
        image = None  
        if serializer.is_valid():  
            offer = serializer.save(user=user,min_price=min_price, min_delivery_time=min_delivery_time, image=image)  
            self.create_or_update_offer_details(offer, details_data)
            return Response({"id": offer.id, "message": "Angebot erfolgreich erstellt"}, status=status.HTTP_201_CREATED) 
        raise ValidationError(serializer.errors)
    
    def perfom_update(self, serializer, format=None):                        
        """Siehe Dokumentation in docs/views.md"""
        details_data = self.get_validated_details()                
        offer = serializer.save()
        self.create_or_update_offer_details(offer, details_data)
        return Response({"id": offer.id, "message": "Angebot erfolgreich aktualisiert"}, status=status.HTTP_200_OK)
           
    def get_validated_details(self):
        """Siehe Dokumentation in docs/views.md"""        
        details_data = self.request.data.get("details", [])        
        if not isinstance(details_data, list):
            raise PermissionDenied({"error": "Das Feld 'details' muss eine Liste sein"})
        return details_data    
    
    def calculate_min_values(self, details_data):
        """Siehe Dokumentation in docs/views.md """         
        prices = [float(detail.get('price')) for detail in details_data if detail.get('price') is not None]
        delivery_times = [int(detail.get('delivery_time_in_days')) for detail in details_data if detail.get('delivery_time_in_days') is not None]           
        min_price = min(prices) if prices else 0.00
        min_delivery_time = min(delivery_times) if delivery_times else None       
        return min_price, min_delivery_time 
    
    def create_or_update_offer_details(self, offer, details_data):
        """Siehe Dokumentation in docs/views.md"""        
        for detail_data in details_data:
            existing_detail = OfferDetail.objects.filter(offer=offer, title=detail_data.get('title')).first()
            if existing_detail:
                for key, value in detail_data.items():
                    setattr(existing_detail, key, value)
                existing_detail.save()
            else:
                OfferDetail.objects.create(offer=offer, **detail_data)
        
    def validate_user_permissions(self, user):             
        """Siehe Dokumentation in docs/views.md"""        
        if not hasattr(user, 'profile') or user.profile.type != "business":
            raise ValidationError({"error":"Nur User vom type 'business' dürfen Angebote erstellen"})              

class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()  
    serializer_class = OfferDetailSerializer 
    permission_classes = [AllowAny]
   
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CanCreateOrder]
    
    def get_queryset(self):       
        """Siehe Dokumentation in docs/views.md"""        
        user = self.request.user        
        if user.is_staff:
            return Order.objects.all()  
        if user.is_authenticated:
            return Order.objects.filter(
                customer_user=user.profile ) | Order.objects.filter(business_user=user.profile) 
        return Order.objects.none()  
    
    def list(self, request, *args, **kwargs):
        """Siehe Dokumentation in docs/views.md"""        
        orders = self.get_queryset().select_related('offer_detail')  
        serialized_orders = OrderSerializer(orders, many=True).data  
        return Response(serialized_orders, status=200)
    
    def create(self,request, *args, **kwargs):        
        """Siehe Dokumentation in docs/views.md"""            
        offer_detail_id = self.get_offer_detail(request.data.get("offer_detail_id"))
        request_data = self.request_data(offer_detail_id,user=self.request.user)     
        serializer = self.get_serializer(data=request_data)        
        if not serializer.is_valid():
            print (f"ERROR: Invalid data en el serializer: {serializer.errors}")   
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def get_offer_detail(self, offer_detail_id):
        """Siehe Dokumentation in docs/views.md"""
        if not offer_detail_id:
            return Response({"error": "offer_detail_id is required"}, status=status.HTTP_400_BAD_REQUEST)        
        try:
            return OfferDetail.objects.get(id=offer_detail_id)           
        except OfferDetail.DoesNotExist:
            return Response({"error": "Invalid offer_detail ID"}, status=status.HTTP_404_NOT_FOUND)
                
    def request_data(self, offer_detail,user):    
        """Siehe Dokumentation in docs/views.md"""        
        return {
            "offer_detail": offer_detail.id,
            "customer_user" : self.request.user.id, 
            "business_user": offer_detail.offer.user.id, 
            "title":offer_detail.title,
            "revisions": offer_detail.revisions,
            "delivery_time_in_days":offer_detail.delivery_time_in_days,
            "price":offer_detail.price,
            "features":offer_detail.features,
            "offer_type":offer_detail.offer_type,
            "status":"in_progress"        }
            
    def Destroy(self, request, *args, **kwargs):
        """Siehe Dokumentation in docs/views.md"""            
        order = self.get_object()        
        if not request.user.is_staff:
            return Response({"error": "Sie haben keine Berechtigung, diese Bestellung zu löschen."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
   
class BusinessUserOrderCountView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, business_user_id, *args, **kwargs):        
        """Siehe Dokumentation in docs/views.md"""
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:            
            business_user = UserProfile.objects.get(id=business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        ongoing_orders_count = Order.objects.filter(business_user=business_user, status="in_progress").count()
        return Response({"order_count": ongoing_orders_count}, status=status.HTTP_200_OK)

class BusinessUserCompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, business_user_id, *args, **kwargs):        
        """Siehe Dokumentation in docs/views.md"""        
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:            
            business_user = UserProfile.objects.get(id=business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        completed_orders_count = Order.objects.filter(business_user=business_user, status="completed").count()
        return Response({"completed_order_count": completed_orders_count}, status=status.HTTP_200_OK)
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CanCreateReview]  
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
       
    def get_queryset(self):             
        """ Siehe Dokumentation in docs/views.md  """          
        queryset = Review.objects.all()          
        return queryset
       
    def perform_create(self, serializer):
        """ Saves the review with the requesting user as the reviewer. """        
        serializer.save(reviewer=self.request.user)
 
class StatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Siehe Dokumentation in docs/views.md"""
        review_count = Review.objects.count() 
        average_rating = Review.objects.aggregate(Avg("rating"))["rating__avg"] or 0 
        business_profile_count = UserProfile.objects.filter(type="business").count() 
        offer_count = Offer.objects.count()  
        data = {    "review_count": review_count,
                    "average_rating": round(average_rating, 1), 
                    "business_profile_count": business_profile_count,
                    "offer_count": offer_count        }
        return Response(data)
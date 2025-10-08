from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet,CustomerListView, BusinessListView, LoginView, RegistrationView, OfferViewSet, OfferDetailViewSet, OrderViewSet, ReviewViewSet,StatisticsView,BusinessUserOrderCountView, BusinessUserCompletedOrderCountView
router = DefaultRouter()
router.register(r'profile', UserProfileViewSet)
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profiles/customer/', CustomerListView.as_view(), name='customer-list'),
    path('profiles/business/', BusinessListView.as_view(), name='business-list'),
    path('base-info/', StatisticsView.as_view(), name='base-info'),
    path('order-count/<int:business_user_id>/', BusinessUserOrderCountView.as_view(), name='_order_count_business_user'),
    path('completed-order-count/<int:business_user_id>/', BusinessUserCompletedOrderCountView.as_view(), name='_completed_order_count_business_user'),

]


import django_filters
from django.db.models import Q
from .models import Offer, Review


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user', required=False)
    max_delivery_time = django_filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte', required=False)
    min_price = django_filters.NumberFilter(field_name='min_price', required=False)
    search = django_filters.CharFilter(method="filter_search", required=False)
    ordering = django_filters.OrderingFilter(fields=(
        ('min_price', 'min_price'),
        ('-min_price', '-min_price'),        
        ('updated_at', 'updated_at'),
        ('-updated_at', '-updated_at'),
    ))
    
    class Meta:
        model = Offer
        fields = ['creator_id', 'max_delivery_time', 'min_price', 'search']
    
    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
        return queryset

    
class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name='business_user', required=False)
    reviewer_id = django_filters.NumberFilter(field_name='reviewer', required=False)
    ordering = django_filters.OrderingFilter(fields=(
        ('updated_at', 'updated_at'),
        ('-updated_at', '-updated_at'),  
        ('rating', 'rating'), 
        ('-rating', '-rating'),
    ))
    
    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id' ]
import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Offer, Review


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user', required=False)
    max_delivery_time = django_filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte', required=False, method="validate_max_delivery_time")
    min_price = django_filters.NumberFilter(field_name='min_price', required=False, method="validate_min_price")
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
        """Searches for offers with a title or description containing the given value.
        If no value is given, returns the unfiltered queryset."""
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
        return queryset
    

    def validate_max_delivery_time(self, queryset, name, value):        
        """ Validates and filters the queryset based on the maximum delivery time. This function checks if the provided `value` for maximum delivery time is a valid integer.
        If the validation succeeds, it filters the queryset to include only offers with a minimum delivery time less than or equal to the specified `value`.
        **Args**:
            - queryset (QuerySet): The initial queryset of offers to be filtered.
            - name (str): The name of the filter field, not used in this method.
            - value (int or None): The maximum delivery time to filter offers by.
        **Returns**: - QuerySet: The filtered queryset based on the maximum delivery time.
        **Raises**:  - ValidationError: If the `value` is not a valid integer. """

        if value is not None:
                try:
                    value = int(value)
                    queryset = queryset.filter(min_delivery_time__lte=value)
                except ValueError:
                    raise ValidationError(f'max_delivery_time must be an integer, received: {value}')  
        return queryset
 
    def validate_min_price(self, queryset, name, value):        
        """Validates and filters the queryset based on the minimum price. This function checks if the provided `value` for minimum price is a valid number.
        If the validation succeeds, it filters the queryset to include only offers with a minimum price greater than or equal to the specified `value`.
        **Args**:
            - queryset (QuerySet): The initial queryset of offers to be filtered.
            - name (str): The name of the filter field, not used in this method.
            - value (number or None): The minimum price to filter offers by.
        **Returns**: - QuerySet: The filtered queryset based on the minimum price.
        **Raises**:  - ValidationError: If the `value` is not a valid number. """
        if value is not None:
            try:
                value = float(value) 
            except ValueError:
                raise ValidationError(f'min_price must be a number, received: {value}')  
            return queryset.filter(min_price__gte=value) 
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
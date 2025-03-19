from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=20)
    file = models.FileField(upload_to='images/', null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(max_length=50, null=True,blank=True, validators=[RegexValidator(regex=r'^\d{1,2}-\d{1,2}$')])
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.user.username == "Customer":
            self.user.email = ""
            self.user.set_unusable_password()
        elif self.user.username == "Business":
            self.user.email = ""
            self.user.set_unusable_password()
        else:
            if not self.user.email or not self.user.has_usable_password:
                raise ValidationError("Regular users must have an email and password.")
            super().save(*args, **kwargs)


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)   
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class OfferDetail(models.Model):   
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField() 
    offer_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')])
    
    def __str__(self):
        return f"{self.offer.title} - {self.title}"
    
class Order(models.Model):
    customer_user = models.ForeignKey(UserProfile, related_name="customer_orders", on_delete=models.CASCADE)
    business_user = models.ForeignKey(UserProfile, related_name="business_orders", on_delete=models.CASCADE)
    offer_detail = models.ForeignKey(OfferDetail, related_name="orders", on_delete=models.CASCADE, null=True, blank=True) # 🔗 Enlace a OfferDetail
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.customer_user and hasattr(self, 'request') and self.request.user.is_authenticated:
            self.customer_user = self.request.user.profile 
        if not self.business_user and self.offer_detail:
            self.business_user = self.offer_detail.offer.user  
        super().save(*args, **kwargs)
    
    def __str__(self):
       return f"Order: {self.offer_detail.title} - {self.customer_user}"
  
 
    
class Review(models.Model):
    business_user = models.ForeignKey(UserProfile, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    
    def can_create(self):
        return self.user.profile.type == "customer"
    def __str__(self):
        return f"{self.rating} - {self.business_user.user.username}"
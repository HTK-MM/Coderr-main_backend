from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from CoderrBackend_app.models import Review
from rest_framework.exceptions import ValidationError


class IsOwnerProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        """Siehe Dokumentation in docs/permissions.md"""          
        if request.method in permissions.SAFE_METHODS:  
            return request.user.is_authenticated         
        if obj.user == request.user:
            return True        
        raise PermissionDenied("You do not have permission to perform this action.")

class CanCreateReview(permissions.BasePermission):   
    def has_permission(self, request, view):       
        """Siehe Dokumentation in docs/permissions.md"""          
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated       
        if request.user.is_authenticated:
            user_type = getattr(request.user.profile, "type", None)
            business_id = request.data.get("business_user")           
            if user_type != "customer":
                return False            
            existing_review =  Review.objects.filter(reviewer=request.user, business_user=business_id).first()
            if existing_review:                
                raise ValidationError({"error":"Du hast bereit eine Bewertung für den Profil abgegeben."})
            return True
        return False 

    def has_object_permission(self, request, view, obj):       
        """Siehe Dokumentation in docs/permissions.md"""         
        if request.method in permissions.SAFE_METHODS:
            return True         
        return obj.reviewer == request.user 
    
    
class CanCreateOrder(permissions.BasePermission):
    def has_permission(self, request, view):        
        """Siehe Dokumentation in docs/permissions.md"""        
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated        
        if request.user.is_authenticated:
            user_type = getattr(request.user.profile, "type", None)            
            if request.method == "POST" and user_type == "customer":
                return True            
            if request.method == "PATCH" and user_type == "business":
                return True  
            if request.method == "DELETE":                
                return request.user.is_staff            
        return False 
    
    def has_object_permission(self, request, view, obj):         
        """Siehe Dokumentation in docs/permissions.md"""  
        if request.method == "GET":       
            if request.user.is_authenticated:
                if obj.customer_user == request.user.profile or obj.business_user == request.user.profile:
                    return True      
        if request.method == 'DELETE' and request.user.is_staff:
            return True        
        user_type = getattr(request.user.profile, "type", None)
        if request.method == "PATCH" and user_type == "business":
            if obj.business_user == request.user.profile:
                return True
            else:
                raise PermissionDenied("Sie haben keine Berechtigung um die Bestellung zu aktualisieren.")
        return False
       
class CanCreateOffer(permissions.BasePermission):
    def has_permission(self, request, view):       
        """Siehe Dokumentation in docs/permissions.md"""          
        if request.method in permissions.SAFE_METHODS:
            return True       
        if request.user.is_authenticated:
            user_type = getattr(request.user.profile, "type", None)           
            if request.method == "POST" and user_type == "business":
                return True      
            return user_type == "business"
        return False
          
    def has_object_permission(self, request, view, obj):        
        """Siehe Dokumentation in docs/permissions.md"""
        if request.method in permissions.SAFE_METHODS:
            return True 
        if request.method in ['PATCH', 'PUT', 'DELETE']: 
            return obj.user == request.user     
        return False
    
class CanViewOffer(permissions.BasePermission):   
    def has_permission(self, request, view):
        """Siehe Dokumentation in docs/permissions.md"""
        if request.method == 'GET':            
            if view.action == 'list':
                return True           
            elif view.action == 'retrieve':
                return request.user.is_authenticated
            return False 
        return True
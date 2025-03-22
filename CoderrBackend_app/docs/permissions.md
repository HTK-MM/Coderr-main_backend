# Permissions

## IsOwnerProfile

### def has_object_permission(self, request, view, obj): 
Check if the user is the owner of the profile to be modified.

## CanCreateReview

### def has_permission(self, request, view):       
Check if the user is a customer and has not already created a review for the business user.

### def has_object_permission(self, request, view, obj):
-   Check if the request user is the reviewer of the review
-   Only allow if the user is the reviewer of the review
  
## CanCreateOrder

### def has_permission(self, request, view):        
Check if the user is a customer, business or staff and allowed to create, update or delete an order.

### def has_object_permission(self, request, view, obj):         
Check if the user is a customer, business or staff and allowed to create, update or delete an order.
The rules are as follows:
-   GET: only allow if the user is the customer or business user of the order
-   DELETE: only allow if the user is staff
-   PATCH: only allow if the user is business     

## CanCreateOffer

### def has_permission(self, request, view):               
Check if the user is a business and allowed to create, update or delete an offer.
The rules are as follows:
-   GET: allow everyone
-   POST: only allow if the user is a business
-   PATCH: only allow if the user is a business
-   DELETE: only allow if the user is a business 
  
### def has_object_permission(self, request, view, obj):        
Determines whether the requesting user has object-level permissions for the specified object based on the request method.
SAFE_METHODS (e.g., GET) are always allowed. For PATCH, PUT, and DELETE requests, the user must be the owner of the object (i.e., `obj.user` must match `request.user`).
**Args:**
    - request: The HTTP request object.
    - view: The view that handles the request.
    - obj: The object for which permission is being checked.
**Returns:**
    - bool: True if the user has permission for the action, False otherwise. 
  
## CanViewOffer

### def has_permission(self, request, view):  
Check if the user is allowed to view the offer list or retrieve a specific offer.
**Args:**
    - request (Request): The request object containing the request data.
    - view (View): The view object containing the view's action.            
**Returns:**
    - bool: True if the user is allowed to view the offer list or retrieve a specific offer, False otherwise.
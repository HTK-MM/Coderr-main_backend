# Permissions

## IsOwnerProfile

### def has_object_permission(self, request, view, obj): 
Check if the user is the owner of the profile to be modified.

## CanCreateReview

### def has_permission(self, request, view):       
Check if the user is a customer and has not already created a review for the business user.

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
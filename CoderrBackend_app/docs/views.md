# Views

## LoginView

### def post(self, request, *args, **kwargs): 
Handles user login and guest login.
   -    If the 'username' is given and 'password' is not given, it will be considered as a guest login.
   -    If both 'username' and 'password' are given, it will be considered as a user login.
   **Args:**   request (Request): The request object containing the post data.
   **Returns:**    Response: A response object containing the authentication token or an error message.

### def success_response(self, user, token, message):
Generates a successful response for login and guest login.
    **Args:**
    -   user (User): The user instance.
    -   token (Token): The token instance.
    -   message (str): The message to be included in the response.
    **Returns:**
    -   Response: A response object with the authentication token and user information.

### def error_response(self, error_message, status_code):
Generates an error response for login and guest login.
    **Args:**  
    -    error_message (str): The error message to be included in the response.
    -    status_code (int): The HTTP status code for the response.
    **Returns:**     
    -   Response: A response object with the error message.

### def guest_login(self, username):          
Handles guest login.
-    If the 'username' is given and 'password' is not given, it will be considered as a guest login.
     The guest login will create a new user if the given username does not exist.
    **Args:**  
    -    username (str): The guest username.
    **Returns:**
    -    Response: A response object containing the authentication token and user information."""

###  def user_login(self, request): 
Handles user login.
    **Args:**  
    -   request (Request): The request containing the username and password.
    **Returns:**
    -    Response: A response object containing the authentication token and user information.
    -   Raises:     serializers.ValidationError: If the username or password is invalid.

### def get_guest_type_from_username(self, username):       
Returns the user type from the given username if it is a guest login.
-   If the username starts with 'guest_', it will be split and the second part will be returned as the user type.
    **Args:**   
    -   username (str): The username to be checked.
    **Returns:**    
    -   str or None: The user type if the username is a guest login, otherwise None.

### def authenticate_or_create_user(self, username):        
Authenticates or creates a guest user account based on the given username.
-   If the username is valid, the corresponding user account will be retrieved or created.
-   If the user account is created, the password will be set to "guest_password".
    **Args:** 
    -   username (str): The username to be authenticated.
    **Returns:**
    -   User: The created or retrieved guest user account.
    -   Raises:     ValidationError: If the username is invalid.

### def get_or_create_guest_user(self, user_type): 
Gets or creates a guest user account based on the given user type. If the user account does not exist, a new user account will be created with the given user type.
The username and email of the guest user will be set to "guest_{user_type}" and "guest_{user_type}@example.com". The first name and last name will be set to "Guest" and the user type respectively.
-   If the user account is created, the password will be set to "guest_password".
    **Args:**
    -   user_type (str): The user type of the guest user to be created.
    **Returns:**
    -   User: The created or retrieved guest user account."""

### def ensure_guest_profile(self, user, user_type):
Ensures the user profile has the given user type. If the user profile does not exist, it will be created.
-   If the user profile exists, its user type will be updated to the given user type.
    **Args:** 
    -   user (User): The user whose profile is to be ensured.
    -   user_type (str): The user type to be set for the user profile.



## RegistrationView

### def post(self, request):
Handles user registration. If the provided data is valid, a new user account is created, and a new authentication token is generated.
    **Args:**
    -   request (Request): The request containing the registration data.
    **Returns:**
    -   Response: A response object containing the authentication token, username, email, and user ID, or an error message.


## OfferViewSet

### def list(self, request, *args, **kwargs):
Retrieves a paginated list of offers.
This method fetches the offers from the database, paginates them according to the pagination settings, and serializes them into a list of dictionaries. Each offer dictionary contains offer details, including a URL for each of its associated offer details.
    **Args:**
    -   request (Request): The request object containing query parameters.
    -   *args: Additional arguments.
    -   **kwargs: Additional keyword arguments.
    **Returns:**
    -   Response: A paginated response containing serialized offer data.   

###  def get_queryset(self):      
Retrieves a queryset of offers based on the request parameters.        
If the user is authenticated and a 'creator_id' is present in the query parameters, it filters offers by the specified creator ID. Otherwise, it returns all offers.
This method also supports filtering by 'search', 'max_delivery_time', and 'min_price', and ordering by any of the model's fields.
**Returns:**    
    -   QuerySet: A queryset of Offer instances filtered by creator ID if specified, or all offers. """

### def perform_create(self, serializer, format=None):        
Creates a new Offer instance and its related OfferDetail instances. This method performs the following steps:
1.  Validates the user permissions.
2.  Retrieves the validated offer details.
3.  Calculates the minimum price and delivery time from the validated offer details.
4.  Creates a new Offer instance using the validated data.
5.  Creates or updates the related OfferDetail instances.
6.  Returns a response with the created Offer instance's ID and a success message.
    **Args:**
    -   serializer (OfferSerializer): The validated OfferSerializer instance.
    -   format (str): The format of the response. Defaults to None.
    **Returns:**
    -   Response: A response object containing the created Offer instance's ID and a success message.
    -   Raises:     ValidationError: If the serializer is invalid.

### def perfom_update(self, serializer, format=None):  
Updates an existing Offer instance and its related OfferDetail instances.
This method performs the following steps:
1. Retrieves the validated offer details.
2. Updates the existing Offer instance using the serializer.
3. Creates or updates the related OfferDetail instances.
4. Returns a response with the updated Offer instance's ID and a success message.
**Args:**
    - serializer (OfferSerializer): The validated OfferSerializer instance.
    - format (str): The format of the response. Defaults to None.
**Returns:**
    - Response: A response object containing the updated Offer instance's ID and a success message.
    - Raises: ValidationError: If the serializer is invalid.



### def get_validated_details(self):
Retrieves the validated offer details from the request data. This method checks if the 'details' field is present in the request data and if it is a list. If the field is missing or not a list, it raises a PermissionDenied exception.
    **Returns:**
    -   list: A list of dictionaries, each containing the details for an OfferDetail instance.

### def calculate_min_values(self, details_data):
Calculates the minimum price and delivery time from the validated offer details.
1.  Extracts the prices and delivery times from the validated offer details.
2.  Calculates the minimum price and delivery time.
3.  Returns the minimum price and delivery time as a tuple.
    **Args:**
    -   details_data (list): A list of dictionaries, each containing the details for an OfferDetail instance.
    **Returns:**
    -   tuple: A tuple containing the minimum price and delivery time. 

### def create_or_update_offer_details(self, offer, details_data):
Creates or updates the OfferDetail instances related to the given Offer instance. This method loops over the validated offer details and either creates a new OfferDetail instance or updates an existing one if a matching title is found.

### def validate_user_permissions(self, user):             
Validates that the given user is a business user. If the user is not a business user, raises a ValidationError with an appropriate error message.
    **Args:**
    -   user (User): The user to validate.
    **Raises:**     ValidationError: If the user is not a business user.


## OrderViewSet

### def get_queryset(self):       
Retrieves a queryset of orders based on the request user. If the user is staff, it returns all orders.
-   If the user is authenticated, it returns orders where the user is either the customer or business.
-   If the user is not authenticated, it returns an empty queryset.
    **Returns:**
    -   QuerySet: A queryset of Order instances filtered by user. 
       
### def list(self, request, *args, **kwargs):
Retrieves a list of orders for the authenticated user. If the user is staff, returns all orders.
Otherwise, returns orders where the user is either the customer or business. 
Returns a serialized response of the orders with a 200 status code.

### def create(self,request, *args, **kwargs):        
Creates a new Order instance from the given request data. The request data should contain the offer_detail_id.
The method performs the following steps:
1.  Retrieves the OfferDetail instance from the given offer_detail_id.
2.  Creates a new Order instance with the given request data.
3.  Validates the Order instance.
4.  If the validation fails, logs an error message.
5.  Creates the Order instance.
6.  Returns a response with the created Order instance and a 201 status code.
    **Args:**
    -   request (Request): The request containing the offer_detail_id.
    **Returns:**
    -   Response: A response object containing the created Order instance and a 201 status code.
    **Raises:**
    -   ValidationError: If the serializer is invalid. 

### def get_offer_detail(self, offer_detail_id):
Retrieves an OfferDetail instance based on the given offer_detail_id. This method checks if the provided offer_detail_id is valid and retrieves the corresponding OfferDetail instance.
-   If the offer_detail_id is not provided, it returns a 400 error response.
-   If the offer_detail_id does not correspond to any existing OfferDetail, it returns a 404 error response.    
    **Args:**   
    -   offer_detail_id (int): The ID of the OfferDetail to retrieve.    
    **Returns:**    
    -   OfferDetail: The retrieved OfferDetail instance if found.
    -   Response: A response object with an error message if the offer_detail_id is missing or invalid.

### def request_data(self, offer_detail,user):    
Prepares the request data for creating an Order instance.
    **Args:**
    -   offer_detail (OfferDetail): The OfferDetail instance to create an Order for.
    -   user (User): The authenticated user.
    **Returns:**
    -   dict: A dictionary containing the request data for creating an Order instance.  

### def Destroy(self, request, *args, **kwargs):
Destroys an existing Order instance. This method checks if the authenticated user is staff and if the order instance exists.
-   If the user is not staff, it returns a 403 error response with an error message.
-   If the order does not exist, it returns a 404 error response with an error message.
-   Otherwise, it deletes the order instance and returns a 204 response.
    **Args:**
    -   request (Request): The request object containing the order ID.
    **Returns:**
    -   Response: A response object with the deletion status.       


## BusinessUserOrderCountView

### def get(self, request, business_user_id, *args, **kwargs):        
Retrieves the count of ongoing orders for a specified business user.    
This method checks if the requesting user is authenticated. If not, it returns an unauthorized error response. It then attempts to retrieve the business user with the provided ID. If the business user is not found, it returns a not found error response. Otherwise, it counts and returns the number of orders that are in progress for the specified business user.    
    **Args:**
    -   request (Request): The request object containing the user and any additional data.
    -   business_user_id (int): The ID of the business user for whom the order count is to be retrieved.
    -   *args: Additional arguments.
    -   **kwargs: Additional keyword arguments.        
    **Returns:**
    -   Response: A response object containing the order count or an error message with the appropriate status code.

##  BusinessUserCompletedOrderCountView

### def get(self, request, business_user_id, *args, **kwargs):        
Retrieves the count of completed orders for a specified business user.    
This method checks if the requesting user is authenticated. If not, it returns an unauthorized error response. It then attempts to retrieve the business user with the provided ID. If the business user is not found, it returns a not found error response. Otherwise, it counts and returns the number of orders that were completed for the specified business user.    
    **Args:**
    -   request (Request): The request object containing the user and any additional data.
    -   business_user_id (int): The ID of the business user for whom the order count is to be retrieved.
    -   *args: Additional arguments.
    -   **kwargs: Additional keyword arguments.        
    **Returns:**
    -   Response: A response object containing the order count or an error message with the appropriate status code.

## ReviewViewSet

### def get_queryset(self): 
**Returns:**
    - A queryset of Review instances filtered by business_user_id and reviewer_id if specified, or all reviews.

## StatisticsView

### def get(self, request):
Retrieves statistical information about the reviews, average rating, business profiles, and offers. This method calculates the total number of reviews, the average review rating, the count of business profiles, and the count of offers. 
It returns this information in a JSON response with the corresponding keys: 'review_count', 'average_rating', 'business_profile_count', and 'offer_count'.    
    **Args:**
    -   request (Request): The request object.
    **Returns:**
    -   Response: A response containing the statistical data in JSON format.   


        
        
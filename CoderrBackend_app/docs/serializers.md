# Serializers

## UserProfileSerializer

### def update(self, instance, validated_data):        
Updates the user profile and the related user.
    **Args:**
    -   instance: The UserProfile instance to be updated.
    -   validated_data: A dictionary containing the validated data.
    **Returns:**
    -   The updated UserProfile instance. 

## UserAuthTokenSerializer

### def validate(self, attrs):  
Validate the provided username and password.
This method authenticates a user using the provided username and password. If the authentication is successful, the authenticated user is added to the attrs dictionary. If the authentication fails, a ValidationError is raised.
    **Args:**
    -   attrs (dict): A dictionary containing the username and password.
**Returns:**
    -    dict: The attrs dictionary with the authenticated user added.
**Raises:**
    -    serializers.ValidationError: If the username or password is invalid.

## RegistrationSerializer

### def save(self): 
Creates a new user and a related UserProfile instance.
    **Args:**
    -   validated_data (dict): A dictionary containing the validated data.
    **Returns:**
    -   The created User instance.
    **Raises:**
    -   serializers.ValidationError: If the passwords do not match.

## OfferSerializer

### def get_user_details(self, obj):
Retrieve user details for the associated offer.
    **Args:**
    -   obj: The Offer instance for which to retrieve user details.
    **Returns:**
    -   dict: A dictionary containing the user's first name, last name, and username.

### def get_min_price(self, obj):
Returns the minimum price of all the offer details for the associated offer.
-   If there are no offer details, returns 0.

### def get_min_delivery_time(self, obj):
Returns the minimum delivery time of all the offer details for the associated offer.
-   If there are no offer details, returns 0.

### def create(self, validated_data):
Creates a new Offer instance and its related OfferDetail instances.
    **Args:**   
    -   validated_data (dict): A dictionary containing the validated data.
    **Returns:**    
    -   The created Offer instance.
    **Raises:**
    -   serializers.ValidationError: If there is any error during the creation process.

### def update(self, instance, validated_data):
Updates an Offer instance and its related OfferDetail instances.
    **Args:**
    -   instance (Offer): The Offer instance to update.
    -   validated_data (dict): A dictionary containing the validated data.
    **Returns:**
    -   Offer: The updated Offer instance.

### def update_offer(self, instance, validated_data):        
Updates the attributes of an existing Offer instance.
    **Args:**
    -   instance (Offer): The Offer instance to be updated.
    -   validated_data (dict): A dictionary containing the new attribute values. 

### def update_offer_details(self, instance, details_data):            
Updates the OfferDetail instances related to an Offer.
    **Args:**
    -   instance (Offer): The Offer instance whose details are to be updated.
    -   details_data (list): A list of dictionaries, each containing data for an OfferDetail instance.
    **Behavior:**
    -   If an OfferDetail's 'id' is provided and exists, its attributes are updated.
    -   If 'revisions' is missing or zero, it is set to 1.
    -   If no 'id' is provided, a new OfferDetail instance is created with the provided data.  
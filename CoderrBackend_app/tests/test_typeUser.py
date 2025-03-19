from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from CoderrBackend_app.models import UserProfile
from rest_framework.authtoken.models import Token


class TypeUserTest(APITestCase):
    
    def setUp(self):       
        """Set up the test environment for TypeUserTest. This method creates a test user and their profile with a 'customer' type. It also generates an authentication token 
        for the user and initializes the API client. The method defines URLs for accessing customer and business profiles to be used in the tests."""
        self.user = User.objects.create_user(username='testuser', password='testpass', email="test@example.com")        
        self.user_profile = UserProfile.objects.create(user=self.user, type='customer')
        self.user_token = Token.objects.create(user=self.user)
       
        self.client = APIClient()
       
        self.customer_url = '/api/profiles/customer/'  
        self.business_url = '/api/profiles/business/'
    
    def test_get_customers_authenticated(self): 
        """Test that an authenticated user can retrieve a list of customers."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')       
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_business_authenticated(self):
        """Test that an authenticated user can retrieve a list of businesses."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}') 
        response = self.client.get(self.business_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_customers_unauthenticated(self):        
        """Test that an unauthenticated user cannot retrieve a list of customers. The test sends a GET request to the customer list URL without
        authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_business_unauthenticated(self):        
        """Test that an unauthenticated user cannot retrieve a list of businesses. The test sends a GET request to the business list URL without
        authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.get(self.business_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def tearDown(self):       
        """Clean up the test environment after each test case by deleting all instances of User and UserProfile to ensure no test data persists between tests."""        
        UserProfile.objects.all().delete()
        User.objects.all().delete()
       
   


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from CoderrBackend_app.models import UserProfile, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


     
        
class BusinessOrderCountTest(APITestCase):
    def setUp(self):
        """Set up the test environment by creating test users and their profiles. This method creates a customer user and a business user, along with their respective profiles and authentication tokens.
        It also creates sample orders with different statuses linked to these profiles. An API client is initialized for testing purposes."""

        self.customer_user = User.objects.create_user(username="testuser", password="testpassword",email="test@example.com")  
        self.customer_profile = UserProfile.objects.create(user=self.customer_user, type='customer') 
        self.customer_token = Token.objects.create(user=self.customer_user)    
        
        self.business_user = User.objects.create_user(username="businessuser", password="businesspassword",email="test@example.com")
        self.business_profile = UserProfile.objects.create(user=self.business_user, type='business')       
               
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="in_progress")
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="in_progress")
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="completed")
       
        self.client = APIClient()
        
        
    def test_orderCount_by_businessId (self):
        """Test that the order count for a specific business user is retrieved correctly. The test authenticates as a customer user, sends a GET request to the order count API endpoint
        with the business user's ID, and verifies that the response status code is 200 OK. It also checks that the response data matches the expected order count."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        url =  f"/api/order-count/{self.business_user.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "order_count": 3
        }
        self.assertEqual(response.data, expected_data)
    
    def test_orderCount_nonexistent_businessId(self):
        """Test that an authenticated customer user cannot retrieve the order count for a non-existent business user ID. The test authenticates as a customer user, 
        sends a GET request to the order count API endpoint with a non-existent business user ID, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        business_userId = 99999
        url = f"/api/order-count/{business_userId}/"  
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)         
    
    
class BusinessCompletedOrderCountTest(APITestCase):
    def setUp(self):
        """Set up the test environment by creating test users and their profiles. This method creates a customer user and a business user, along with their respective profiles and authentication tokens.
        It also creates sample orders with different statuses linked to these profiles. An API client is initialized for testing purposes."""
        self.customer_user = User.objects.create_user(username="testuser", password="testpassword",email="test@example.com")  
        self.customer_profile = UserProfile.objects.create(user=self.customer_user, type='customer') 
        self.customer_token = Token.objects.create(user=self.customer_user)    
        
        self.business_user = User.objects.create_user(username="businessuser", password="businesspassword",email="test@example.com")
        self.business_profile = UserProfile.objects.create(user=self.business_user, type='business')               
       
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="in_progress")
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="in_progress")
        Order.objects.create(customer_user=self.customer_profile, business_user=self.business_profile, status="completed")

        self.client = APIClient()
        
    def test_completed_orderCount_by_businessId(self):
        """Test that an authenticated customer user can retrieve the count of completed orders for a specific business user. The test authenticates as a customer user, 
        sends a GET request to the completed order count API endpoint with the business user's ID, and verifies that the response status code is 200 OK. 
        It also checks that the response data matches the expected completed order count."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        url =  f"/api/completed-order-count/{self.business_user.id}/" 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "completed_order_count": 1
        }
        self.assertEqual(response.data, expected_data)
    
    def test_completed_orderCount_nonexistent_businessId(self):
        """Test that an authenticated customer user cannot retrieve the count of completed orders for a non-existent business user ID. The test authenticates as a customer user, 
        sends a GET request to the completed order count API endpoint with a non-existent business user ID, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        business_userId = 99999
        url =  f"/api/completed-order-count/{business_userId}/"   
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  

    def tearDown(self):       
        """Clean up the test environment after each test case by deleting all instances of User, UserProfile, and Order to ensure no test data persists between tests."""
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Order.objects.all().delete()
        
    
    
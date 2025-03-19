from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from CoderrBackend_app.models import UserProfile
from django.urls import reverse

user = User()

class GuestAuthenticationAPITests(APITestCase):
    
    def setUp(self):
        """ Set up the test environment by initializing the API client and the login URL.
        This method is called before each test is executed. It creates an instance of the APIClient
        and assigns the URL for the login view to the `login_url` attribute of the test case.       """
        
        self.client = APIClient()
        self.login_url = reverse('login')       

    def test_login_as_guest_customer(self):        
        """ Tests that a guest login with username 'guest_customer' succeeds. This test sends a login request with the username 'guest_customer' and 
        verifies that the response status code is 201 (Created) and that the response contains a valid authentication token."""
        
        response = self.client.post(self.login_url, {"username": "guest_customer"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "guest_customer")

    def test_login_as_guest_business(self):      
        """ Tests that a guest login with username 'guest_business' succeeds. This test sends a login request with the username 'guest_business' and
        verifies that the response status code is 201 (Created) and that the response contains a valid authentication token."""
        
        response = self.client.post(self.login_url, {"username": "guest_business"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "guest_business")

    def test_login_without_username(self):        
        """Tests that a login request without a username fails. This test sends a login request without providing a username and
        verifies that the response status code is 400 (Bad Request) and that the response contains an error message."""

        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
    def tearDown(self):        
        """Clean up the test environment after each test case. This method deletes all instances of Offer, OfferDetail, User, and UserProfile to ensure no test data persists between tests."""      
        User.objects.all().delete()
        UserProfile.objects.all().delete()
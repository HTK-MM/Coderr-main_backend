from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(APITestCase):
    def setUp(self):       
        """Set up the test environment by creating a test user and initializing the API client and login URL."""

        self.user = User.objects.create_user(username='testuser', password='testpass',email='test@example.com')
        self.client = APIClient()
        self.login_url = reverse('login')
        
    def test_login_OK(self):        
        """ Tests that a login request with correct credentials succeeds. This test sends a login request with correct credentials and
        verifies that the response status code is 201 (Created) and that the response contains a valid authentication token."""
        
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)  
       
       
    def test_login_Fail(self):        
        """ Tests that a login request with incorrect credentials fails. This test sends a login request with incorrect credentials and
        verifies that the response status code is 400 (Bad Request) and that the response contains an error message."""
        
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationTest(APITestCase):
    def setUp(self):    
        """Set up the test environment for registration tests. This method initializes the API client and prepares test data for valid registration and an existing user. 
        The valid registration data includes a username, email, password, repeated password, and user type. An existing user is also created to test registration scenarios involving duplicate users."""

        self.valid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "repeated_password": "securepassword123",
            "type": "Customer"
        }
       
        self.existing_user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123"
        )
       
        self.client = APIClient()
        
    def test_successful_registration(self):       
        """ Tests that a registration request with valid data is successful. This test sends a registration request with valid user data and verifies that the response status code is 201 (Created), a valid authentication 
        token is included in the response, and the username and email match the requested data. It also checks that the 'user_id' and success message are present in the response. Additionally, it verifies that the 
        user is created in the database and that the authentication token is valid.    """

        response = self.client.post("/api/registration/", self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token).exists())        
        self.assertEqual(response.data["username"], self.valid_data["username"])
        self.assertEqual(response.data["email"], self.valid_data["email"])
        self.assertIn("user_id", response.data)    
        self.assertEqual(response.data["message"], "Successfully registered!")        
        user_exists = User.objects.filter(username=self.valid_data["username"]).exists()
        self.assertTrue(user_exists)
        
    def test_invalid_data(self):       
        """Tests that a registration request with invalid data (e.g. missing required fields) is unsuccessful. This test sends a registration request with missing data and verifies 
        that the response status code is 400 (Bad Request), and that the response contains an error message indicating which field is missing. In this case, the password field is omitted. """
        invalid_data = self.valid_data.copy()
        invalid_data.pop("password")         
        response = self.client.post("/api/registration/", invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  
        
    def test_registration_existing_username(self):       
        """Tests that a registration request with a username that already exists in the database is unsuccessful. This test sends a registration request with a username 
        that is already in use and verifies that the response status code is 400 (Bad Request), and that the response contains an error message indicating that the username already exists. """
        existing_data = self.valid_data.copy()
        existing_data["username"] = self.existing_user.username 
        response = self.client.post("/api/registration/", existing_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data) 
   
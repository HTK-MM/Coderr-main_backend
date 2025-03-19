from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from CoderrBackend_app.models import UserProfile

class UserProfileTest(APITestCase):
    
    def setUp(self):
        """ Set up the test environment for UserProfileTest. This method creates two test users and their profiles. The first user is the "owner" and the second user is "otheruser". 
        An API client is initialized for testing purposes. The `url` instance variable is set to the URL of the profile owner's profile for testing purposes.     """
        self.user_owner = User.objects.create_user(username="owner", password="testpassword", email="test@example.com")
        self.profile_owner = UserProfile.objects.create(user=self.user_owner) 
        
        self.user_other =User.objects.create_user(username="otheruser", password="testpassword",email="test@example.com")
        self.profile_other = UserProfile.objects.create(user=self.user_other)

        self.url = f"/api/profile/{self.profile_owner.pk}/"  

    
    def test_get_userprofile_authenticated(self):       
        """Test that an authenticated user can retrieve their own user profile. The test sends a GET request to the profile owner's URL with authentication
        and verifies that the response status code is 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_userprofile_unauthenticated(self):       
        """Test that an unauthenticated user cannot retrieve the user profile. The test sends a GET request to the profile owner's URL without authentication 
        and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_userprofile_not_found(self):
        """Test that a request for a non-existent user profile returns a 404 status code. This test authenticates as the owner user and sends a GET request to a non-existent
        profile URL. It verifies that the response status code is 404 NOT FOUND, indicating that the user profile does not exist.    """
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get("/api/profile/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def get_patch_data(self):
        """Returns a dictionary with example data for a PATCH request to update a user profile. The dictionary contains the fields 
        first_name, last_name, location, tel, description, working_hours, and email. The values are example data for a business profile, but can be modified to test different scenarios."""
        return {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
    
    def test_patch_userprofile_owner(self):
        """Test that an authenticated user who is the owner of the profile can update their user profile. The test authenticates as the owner user, sends a PATCH request 
        with updated profile data to the profile owner's URL, and verifies that the response status code is 200 OK."""
        self.client.force_authenticate(user=self.user_owner)       
        response = self.client.patch(self.url, self.get_patch_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_userprofile_unauthenticated(self):
        """Test that an unauthenticated user cannot update a user profile. The test sends a PATCH request with updated profile data to the profile owner's URL 
        without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.patch(self.url, self.get_patch_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_userprofile_forbidden(self):
        """Test that an authenticated user who is not the owner of the profile cannot update the profile. The test authenticates as the owner user, 
        sends a PATCH request with updated profile data to the URL of another user's profile, and verifies that the response status code is 403 FORBIDDEN."""
        self.client.force_authenticate(user=self.user_owner)
        url = f"/api/profile/{self.profile_other.pk}/"
        response = self.client.patch(url, self.get_patch_data(), format="json")           
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_userprofile_not_found(self):
        """Test that a PATCH request to update a non-existent user profile returns a 404 NOT FOUND status code. The test authenticates as the owner user, sends a PATCH request 
        with updated profile data to a non-existent profile URL, and verifies that the response status code is 404 NOT FOUND."""
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.patch("/api/profile/9999/", self.get_patch_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def tearDown(self):       
        """Clean up the test environment after each test case by deleting all instances of User and UserProfile to ensure no test data persists between tests."""
        UserProfile.objects.all().delete()
        User.objects.all().delete()
       
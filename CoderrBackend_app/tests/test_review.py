from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from CoderrBackend_app.models import UserProfile, Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ReviewTest(APITestCase):
    def setUp(self):        
        """Set up the test environment for ReviewTest. This method creates test users and their profiles for a customer and a business. 
        It also initializes the API client and sets up the review URL endpoint to be used in the tests."""
        self.customer = User.objects.create_user(username="customer_user", password="testpass",email="test@example.com")
        self.customer_profile = UserProfile.objects.create(user=self.customer, type='customer')
        self.customer_token = Token.objects.create(user=self.customer)
                
        self.business = User.objects.create_user(username="business_user", password="testpass",email="test@example.com")
        self.business_profile = UserProfile.objects.create(user=self.business, type='business') 
        self.business_token = Token.objects.create(user = self.business)   
               
        self.client = APIClient()           
        self.review_url = reverse('review-list') 
        
    def create_review(self):
        """Creates a test review for the customer and business user in the test environment. Returns the created review object."""
        return Review.objects.create(
            business_user=self.business_profile,
            rating=4,
            description="This is a test review",
            reviewer=self.customer   )
           
    def test_get_reviews(self):
        """Test that an authenticated customer user can retrieve a list of reviews. The test authenticates as a customer user, sends a GET request to the review URL,
        and verifies that the response status code is 200 OK."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reviews_unauthenticated(self):
        """Test that an unauthenticated user cannot retrieve a list of reviews. The test sends a GET request to the review URL 
        without authentication and verifies that the response status code is 401 UNAUTHORIZED."""        
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_as_customer(self):
        """Test that an authenticated customer user can create a review. The test authenticates as a customer user, sends a POST request with review data to the review URL, 
        and verifies that the response status code is 201 CREATED."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        data={"business_user":self.business_profile.id, "rating":4, "description":"Toll gemacht!" }
        response = self.client.post(self.review_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_review_unauthenticated(self):        
        """Test that an unauthenticated user cannot create a review. The test sends a POST request with review data to the review URL 
        without authentication and verifies that the response status code is 401 UNAUTHORIZED."""      
        data={ "business_user":self.business.id, "rating":4, "description":"Toll gemacht!" }
        response = self.client.post(self.review_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
     
    def test_duplicate_review(self):        
        """Test that a user cannot rate the same business_user twice. The test creates a first review (valid), then tries to create a second review for the same business_user and
        verifies that the response status code is 403 FORBIDDEN and that the response contains a message with the text "Du hast bereit eine Bewertung für den Profil abgegeben."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')        
        self.test_create_review_as_customer()        
        data = {"description": "Great service!", "rating": 5, "business_user": self.business_profile.id}        
        response = self.client.post(self.review_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Du hast bereit eine Bewertung für den Profil abgegeben.", str(response.data["detail"]))
      
    def test_update_review_as_creator(self):       
        """Test that the creator of a review can update it. The test authenticates as the customer user (review creator), sends a PATCH request with updated review data to the review detail URL, 
        and verifies that the response status code is 200 OK. It also verifies that the review rating is updated in the database."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        data = {"rating": 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating,2)
        
    def test_update_review_wrong_data(self):        
        """Test that an authenticated customer user who is the creator of a review cannot update the review with wrong data. The test authenticates as a customer user, 
        sends a PATCH request with the review ID and wrong data to the review detail URL, and verifies that the response status code is 400 BAD REQUEST."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        data = {"rating": "gut"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_review_unauthenticated(self):         
        """Test that an unauthenticated user cannot update a review. The test sends a PATCH request with the review ID and new data to the review detail URL 
        without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        data = {"rating": 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_review_as_business(self):
        """Test that an authenticated business user cannot update a review. The test authenticates as a business user, sends a PATCH request with the review ID and new data to the review detail URL, 
        and verifies that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        data = {"rating": 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_review_nonexistent(self):      
        """Test that attempting to update a non-existent review returns a 404 NOT FOUND. The test authenticates as a customer user, sends a PATCH request with a non-existent review ID to 
        the review detail URL, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        review_id = 9999
        url = reverse('review-detail', args=[review_id])
        data = {"rating": 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
    def test_delete_review(self):
        """Test that the creator of a review can delete it. The test authenticates as the customer user (review creator), sends a DELETE request to the review detail URL, 
        and verifies that the response status code is 204 NO CONTENT. It also confirms the review no longer exists in the database."""        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])       
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_review_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a review. The test sends a DELETE request to the review detail URL without authentication 
        and verifies that the response status code is 401 UNAUTHORIZED."""       
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_review_as_business(self):
        """Test that an authenticated business user cannot delete a review. The test authenticates as a business user, sends a DELETE request to the review detail URL, 
        and verifies that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        review = self.create_review()
        url = reverse('review-detail', args=[review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_review_nonexistent(self):
        """Test that attempting to delete a non-existent review returns a 404 NOT FOUND. The test authenticates as a customer user, sends a DELETE request with a non-existent review ID
        to the review detail URL, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        review_id= 9999
        url = reverse('reviews', args=[review_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def tearDown(self):
        """Clean up the test environment after each test case by deleting all instances of Review to ensure no test data persists between tests."""
        Review.objects.all().delete()
       
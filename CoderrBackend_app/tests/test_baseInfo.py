from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.db.models import Avg
from django.contrib.auth.models import User
from CoderrBackend_app.models import UserProfile, Offer, Review


class StatisticsViewTest ( APITestCase):
    def setUp(self):        
        """ Set up test environment for StatisticsViewTest. This method creates test users and user profiles for a customer and a business. It also authenticates the API client with a test user.    
        Additionally, it creates sample reviews and offers to be used in the tests for the statistics view. The reviews are linked to the business profile and are created with varying ratings. The offers 
        are associated with the business user.    """

        self.customer = User.objects.create(username="customer", password="testpass", email="test@example.com")
        self.customer_profile = UserProfile.objects.get_or_create(user=self.customer, type="customer")
        self.business = User.objects.create(username="business", password="testpass", email="test@example.com")
        self.business_profile = UserProfile.objects.get_or_create(user=self.business , type="business")  # Otro tipo de usuario
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass")               
        
        Review.objects.create(business_user=self.business.profile,rating=4, description="This is a test review", reviewer=self.customer )       
        Review.objects.create( business_user=self.business.profile, rating=5, description="This is a test review", reviewer=self.customer)
        
        Offer.objects.create( user= self.business, title="Test Offer # 1", image = None, description="This is a test offer #1", min_price=100.0 )
        Offer.objects.create( user=self.business, title="Test Offer #2", image = None, description="This is a test offer #2", min_price=100.0 )
       

    def test_statistics_view(self):
        """ This test case tests the API endpoint for retrieving statistical information about the system. It creates a test environment with sample reviews and offers, and then tests the GET request to the endpoint. 
        It verifies that the response status code is 200 OK and that the response data matches the expected data.
        The expected data is a JSON object with the following keys: 'review_count', 'average_rating', 'business_profile_count', and 'offer_count'. 
        The values of these keys are the actual counts and average of the relevant models in the test database.      """
        
        response = self.client.get("/api/base-info/")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        expected_data = {
            "review_count": Review.objects.count(),
            "average_rating": round(Review.objects.aggregate(Avg("rating"))["rating__avg"] or 0, 1),
            "business_profile_count": UserProfile.objects.filter(type="business").count(),
            "offer_count": Offer.objects.count(),        
            }
        
        self.assertEqual(response.data, expected_data)
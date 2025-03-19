from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from CoderrBackend_app.models import UserProfile, Offer, OfferDetail
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class OfferTest(APITestCase):
    def setUp(self):
        """ Set up test environment for OfferTest. This method creates test users and user profiles for a customer and a business. It also authenticates the API client with a test user.    
        Additionally, it creates sample offers and offers details to be used in the tests for the offer view. The offers are linked to the business profile and are created with varying details. The offers detail are associated with the business user. """
        
        self.business_user = User.objects.create_user(username='business_user', password='testpass',email="test@example.com")
        self.business_profile = UserProfile.objects.create(user=self.business_user, type='business')
        self.business_token = Token.objects.create(user=self.business_user)
      
        self.customer_user = User.objects.create_user(username='customer_user', password='testpass',email="test@example.com")
        self.customer_profile = UserProfile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)

        self.offer = Offer.objects.create( user=self.business_user, title="Test Offer", image = None, description="This is a test offer", min_price=100.0 )
        
        self.offerdetail =   [ OfferDetail.objects.create(offer=self.offer,title= "Basic Design", revisions=1, delivery_time_in_days= 2, price= "50.00", features=[], offer_type="basic"),
                                OfferDetail.objects.create(offer=self.offer,title= "Standard Design", revisions=3, delivery_time_in_days= 5, price= "150.00", features=[] ,offer_type="standard"),
                                OfferDetail.objects.create(offer=self.offer,title= "Premium Design", revisions=5, delivery_time_in_days= 9, price= "200.00", features=[], offer_type="premium")] 
        self.client = APIClient()       
        self.offer_url = reverse('offer-list')
        self.offer_detail_url = reverse('offer-detail', args=[self.offer.id])
        
    def test_get_list_offers(self):        
        """ Test that an unauthenticated user can retrieve a list of offers. The test will send a GET request to the offer list URL and verify that the response status code is 200 OK.  """        
        response = self.client.get(self.offer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_by_creator(self):       
        """ Test that an unauthenticated user can retrieve a list of offers filtered by creator. The test will send a GET request to the offer list URL with the creator_id parameter and verify that the response status code is 200 OK and there are results.  """
        url = f"{self.offer_url}?creator_id={self.business_user.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)  # Verificar que hay resultados
   
    def test_create_offer_as_business(self):        
        """Test that a business user can create a new offer with details. The test will authenticate as a business user, send a POST request with offer data to the offer URL, and verify that the response status code is 201 CREATED."""

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        data = {
            "title": "New Offer",
            "description": "A new test offer",
            "image" : None,
            "details": [{"title": "Basic Design", "revisions":1, "delivery_time_in_days": 2, "price": "50.00", "features":[], "offer_type": "basic" },
                        {"title": "Standard Design", "revisions":3, "delivery_time_in_days": 5, "price": "150.00", "features":[], "offer_type": "standard" },
                    {"title": "Premium Design", "revisions":5, "delivery_time_in_days": 9, "price": "200.00", "features":[] , "offer_type": "premium" }]
        }
        response = self.client.post(self.offer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_offer_unauthenticated(self):       
        """Test that an unauthenticated user cannot create offers. The test will send a POST request with offer data to the offer URL without authentication and verify that the response status code is 401 UNAUTHORIZED."""
        data = {
            "title": "No Auth Offer",
            "description": "Should not be allowed"
        }
        response = self.client.post(self.offer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_offer_as_customer(self):       
        """Test that a customer user cannot create offers. The test will authenticate as a customer user, send a POST request with offer data to the offer URL, and verify that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        data = {
           "title": "New Offer",
            "description": "A new test offer",
            "image" : None,
            "details": [{"title": "Basic Design", "revisions":1, "delivery_time_in_days": 2, "price": "50.00", "features":[], "offer_type": "basic" },
                        {"title": "Standard Design", "revisions":3, "delivery_time_in_days": 5, "price": "150.00", "features":[], "offer_type": "standard" },
                    {"title": "Premium Design", "revisions":5, "delivery_time_in_days": 9, "price": "200.00", "features":[] , "offer_type": "premium" }]
        }
        response = self.client.post(self.offer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_offer_by_id(self):       
        """Test that an authenticated user can filter offers by 'offer_id' in the URL. The test will authenticate as a customer user,
        send a GET request with the offer ID to the offer detail URL, and verify that the response status code is 200 OK. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')           
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_offer_by_id_user_unauthenticated(self):
        """Test that an unauthenticated user can filter offers by 'offer_id' in the URL. The test will send a GET request with the offer ID to the offer detail URL without authentication and verify that the response status code is 200 OK. """
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offer_by_id_nonexistent(self):
        """Test that an authenticated user cannot filter offers by a nonexistent 'offer_id' in the URL. The test will authenticate as a customer user,
        send a GET request with a nonexistent offer ID to the offer detail URL, and verify that the response status code is 404 NOT FOUND. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        nonexistent_id = 99999
        url = reverse('offer-detail', args=[nonexistent_id])     
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_offerdetails (self):
        """Test that an authenticated user can filter offers by 'offer_id' in the URL. The test will authenticate as a customer user,
        send a GET request with the offer ID to the offer detail URL, and verify that the response status code is 200 OK. """
        url = reverse('offerdetail-detail', args=[self.offerdetail[0].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_offerdetails (self):
        """Test that an authenticated user cannot retrieve an offer detail by a nonexistent 'offer detail ID' in the URL. The test will authenticate as a customer user,
        send a GET request with a nonexistent offer detail ID to the offer detail URL, and verify that the response status code is 404 NOT FOUND. """
        offerdetail_id = 9999
        url = reverse('offerdetail-detail', args=[offerdetail_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_offer_as_creator(self):       
        """Test that an authenticated user who is the creator of an offer can update the offer. The test will authenticate as the creator user,
        send a PATCH request with the offer ID to the offer detail URL, and verify that the response status code is 200 OK. The test will also retrieve the offer and verify that the title is updated."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')        
        data = {"title": "Updated Offer"}
        response = self.client.patch(self.offer_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, "Updated Offer")
        
    def test_update_offer_invalid_data(self):
        """Test that updating an offer with invalid data returns a 400 BAD REQUEST. This test authenticates as a business user, sends a PATCH request with invalid
        data to the offer detail URL, and verifies that the response status code is 400 BAD REQUEST."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')           
        # Datos inválidos
        invalid_data = {"title": "", "description": ""}      
        response = self.client.patch(self.offer_detail_url, invalid_data, format='json')    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_offer_as_unauthenticated(self):
        """Test that an unauthenticated user cannot update an offer. The test sends a PATCH request with the offer ID to the offer detail URL without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        data = {"title": "Updated Offer"}
        response = self.client.patch(self.offer_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_offer_as_customer(self):        
        """Test that an authenticated user who is a customer cannot update an offer. The test will authenticate as a customer user,
        send a PATCH request with the offer ID to the offer detail URL, and verify that the response status code is 403 FORBIDDEN. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')       
        data = {"title": "Unauthorized Update"}
        response = self.client.patch(self.offer_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_nonexistent_offer(self):
        """Test that attempting to update a non-existent offer returns a 404 NOT FOUND. 
        The test authenticates as a business user, sends a PATCH request with a non-existent offer ID to the offer detail URL, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')    
        nonexistent_id = 99999  # Un ID que no existe en la base de datos
        url = reverse('offer-detail', args=[nonexistent_id])  
        data = {"title": "Updated Offer"}
        response = self.client.patch(url, data, format='json')    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer_as_creator(self):        
        """Test that the creator of an offer can delete it. The test authenticates as the creator user, sends a DELETE request to the offer detail URL, and verifies that the response status code is 204 NO CONTENT."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')        
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_offer_unauthenticated_fails(self):        
        """Test that an unauthenticated user cannot delete an offer. The test sends a DELETE request to the offer detail URL without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_as_customer(self):
        """Test that a user who did not create an offer cannot delete it. The test authenticates as a customer user, sends a DELETE request to the offer detail URL, and verifies that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.delete(self.offer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_offer(self):        
        """Test that attempting to delete a nonexistent offer returns a 404 NOT FOUND. The test authenticates as a business user, sends a DELETE request to the offer detail URL with a non-existent offer ID, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')    
        nonexistent_id = 99999  # Un ID que no existe en la base de datos
        url = reverse('offer-detail', args=[nonexistent_id])  
        data = {"title": "Updated Offer"}
        response = self.client.patch(url, data, format='json')    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def tearDown(self):        
        """Clean up the test environment after each test case. This method deletes all instances of Offer, OfferDetail, User, and UserProfile to ensure no test data persists between tests."""
        Offer.objects.all().delete()
        OfferDetail.objects.all().delete()
        User.objects.all().delete()
        UserProfile.objects.all().delete()

    
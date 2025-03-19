from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from CoderrBackend_app.models import UserProfile,Offer, Order, OfferDetail
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class OrderTest(APITestCase):
    def setUp(self):
        """ Set up test environment for OrderTest. This method creates test users and user profiles for a customer, a business and a staff user. It also authenticates the API client with a test user.
        Additionally, it creates sample offers and offers details to be used in the tests for the order view. The offers are linked to the business profile and are created with varying details. The offers detail are associated with the business user.
        Finally, it creates a sample order with status "in_progress" to be used in the tests for the order view. The order is linked to the customer and the business user.       """
        
        self.staff = User.objects.create_user(username="staff_user", password="staffpassword",email="test@example.com", is_staff = True)
        self.staff_profile = UserProfile.objects.create(user = self.staff)
        self.staff_token = Token.objects.create(user=self.staff)
         
        self.customer = User.objects.create_user(username='customer_user', password='testpass',email="test@example.com")
        self.customer_profile = UserProfile.objects.create(user = self.customer, type='customer')
        self.customer_token = Token.objects.create(user=self.customer)
       
        self.business = User.objects.create_user(username='business_user', password='testpass',email="test@example.com")
        self.business_profile = UserProfile.objects.create(user = self.business, type='business')
        self.business_token = Token.objects.create(user=self.business)  
         
        self.offer = Offer.objects.create( user= self.business, title="Test Offer", image = None, description="This is a test offer", min_price=100.0 )
        
        self.offer_detail =   [ OfferDetail.objects.create(offer=self.offer,title= "Basic Design", revisions=1, delivery_time_in_days= 2, price= "50.00", features=[], offer_type="basic"),
                                OfferDetail.objects.create(offer=self.offer,title= "Standard Design", revisions=3, delivery_time_in_days= 5, price= "150.00", features=[] ,offer_type="standard"),
                                OfferDetail.objects.create(offer=self.offer,title= "Premium Design", revisions=5, delivery_time_in_days= 9, price= "200.00", features=[], offer_type="premium")] 
        
        self.order = Order.objects.create( customer_user=self.customer_profile, business_user=self.business_profile, status="in_progress", offer_detail_id = self.offer_detail[0].id )   
       
        self.client = APIClient()
        self.order_url = reverse('order-list')
        self.order_detail_url = reverse('order-detail', args=[self.order.id])
              
        
    def test_get_list_orders(self):
        """Test that a user can retrieve a list of orders if they are authenticated."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        response = self.client.get(self.order_url)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_list_orders_unauthenticated(self):      
        """Test that an unauthenticated user cannot retrieve a list of orders. 
        The test sends a GET request to the order list URL without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_detail_order(self):
        """Test that an authenticated customer user can retrieve the details of a specific order. 
        The test authenticates as a customer user, sends a GET request to the order detail URL, and verifies that the response status code is 200 OK."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_order_as_customer(self):        
        """Test that an authenticated customer user can create an order.
        The test authenticates as a customer user, sends a POST request with the offer_detail_id to the order list URL, and verifies that the response status code is 201 CREATED."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        data = {          
            "offer_detail_id":self.offer_detail[1].id     
        }        
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      
    def test_create_order_details_empty(self):       
        """Test that an authenticated customer user cannot create an order with empty data.
        The test authenticates as a customer user, sends a POST request with empty offer_detail_id to the order list URL, and verifies that the response status code is 400 BAD REQUEST."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        data = {          
           "offer_detail_id": ""
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_order_as_unauthenticated(self):
        """Test that an unauthenticated user cannot create an order.
        The test sends a POST request with the offer_detail_id to the order list URL without authentication and verifies that the response status code is 401 UNAUTHORIZED."""
        data = {            
            "offer_detail_id":self.offer_detail[1].id           
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_order_as_business(self):       
        """Test that an authenticated user who is a business user cannot create an order.
        The test authenticates as a business user, sends a POST request with the offer_detail_id to the order list URL, and verifies that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        data = {          
            "offer_detail_id":self.offer_detail[2].id, 
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_order_detailsId_nonexistent(self):
        """Test that an authenticated customer user cannot create an order with a nonexistent offer_detail_id.
        The test authenticates as a customer user, sends a POST request with a nonexistent offer_detail_id to the order list URL, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        data = {          
            "offer_detail_id":"999999", 
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_status_order(self):
        """Test that an authenticated user who is a business user can update the status of an order. The test authenticates as a business user, sends a PATCH request with the order ID and
        the new status to the order detail URL, and verifies that the response status code is 200 OK. The test will also retrieve the order and verify that the status is updated."""

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')         
        data = {            
            "status": "completed"           
        }
        response = self.client.patch(self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")
        
    def test_update_order_wrong_data(self):        
        """Test that an authenticated user who is a business user cannot update the details of an order with wrong data. The test authenticates as a business user, sends a PATCH request with the order ID 
        and wrong data to the order detail URL, and verifies that the response status code is 400 BAD REQUEST. The test will also verify that the order details are not updated."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')       
        data = { "offer_detail": 999  }
        response = self.client.patch(self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_order_unauthenticated(self): 
        """Test that an unauthenticated user cannot update the status of an order. The test sends a PATCH request with the order ID and 
        the new status to the order detail URL without authentication and verifies that the response status code is 401 UNAUTHORIZED. The test will also verify that the order status is not updated."""
        data = { "status": "completed"  }
        response = self.client.patch(self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_order_as_customer(self):
        """Test that an authenticated user who is a customer user cannot update the status of an order. The test authenticates as a customer user, sends a PATCH request with the order ID and
        the new status to the order detail URL, and verifies that the response status code is 403 FORBIDDEN. The test will also verify that the order status is not updated."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')      
        data = {            
            "offer_detail_id": self.offer_detail[1].id         
        }
        response = self.client.patch(self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_order_nonexistent(self):
        """Test that an authenticated business user cannot update a non-existent order.
        The test authenticates as a business user, sends a PATCH request with a non-existent order ID to the order detail URL, and verifies that the response status code is 404 NOT FOUND."""

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        order_id = 9999
        url = reverse('order-detail', args=[order_id])   
        data = {            
            "status": "completed"           
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_order (self):
        """Test that an authenticated staff user can delete an order. The test authenticates as a staff user, sends a DELETE request to the order detail URL,
        and verifies that the response status code is 204 NO CONTENT. It also confirms the order no longer exists in the database."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.staff_token.key}')        
        response = self.client.delete(self.order_detail_url)        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_order_unauthenticated(self):
        """Test that an unauthenticated user cannot delete an order. The test sends a DELETE request to the order detail URL without authentication
        and verifies that the response status code is 401 UNAUTHORIZED."""
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_order_as_business (self):
        """Test that an authenticated business user cannot delete an order. The test authenticates as a business user, 
        sends a DELETE request to the order detail URL, and verifies that the response status code is 403 FORBIDDEN."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.business_token.key}')        
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_nonexistent_order(self):        
        """Test that an authenticated staff user cannot delete a nonexistent order. The test authenticates as a staff user,
        sends a DELETE request to the order detail URL with a nonexistent order ID, and verifies that the response status code is 404 NOT FOUND."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.staff_token.key}')
        order_id = 9999
        url = reverse('order-detail', args=[order_id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def tearDown(self):       
        """Clean up the test environment after each test case by deleting all instances of UserProfile, User, Order, Offer, and OfferDetail to ensure no test data persists between tests."""
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        Order.objects.all().delete()
        Offer.objects.all().delete()
        OfferDetail.objects.all().delete()
 
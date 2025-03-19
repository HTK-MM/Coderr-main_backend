# Coderr Backend API

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/HTK-MM/Coderr-main_backend/blob/master/README.MD) [![de](https://img.shields.io/badge/lang-de-yellow.svg)](https://github.com/HTK-MM/Coderr-main_backend/blob/master/README.de.md)

## Description

The **Coderr** project is an API developed with Django and Django REST Framework to manage users, offers, orders, and reviews on a business platform.

## Technologies Used

- Python 3.x

- Django 5.1.6
  
- Django REST Framework 3.15.2

- SQLite 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HTK-MM/CoderrBackend/.git
    cd projekt
   ```

2. Create and activate a virtual environment:
    ````bash    
    python -m venv venv
       source venv/bin/activate  #On Windows: venv\Scripts\activate
    ````

3. Install dependencies:
    ````bash 
    pip install -r requirements.txt
    ````

4. Configure the database and apply migrations:
    ````bash 
    python manage.py migrate
    ````

5. Create a superuser (optional for accessing the admin panel):
    ````bash 
    python manage.py createsuperuser
    ````

6. Start the development server:
    ````bash 
    python manage.py runserver
    ````
7. Frontend Setup: In the file shared/scripts/config.js, modify:
   ````bash
   const GUEST_LOGINS = {
        customer : {
            username: 'guest_customer'
        },
        business : {
            username: 'guest_business'     
        }
    }
    ````

## API Endpoints

### :small_blue_diamond: Base Information

-   ````**GET /base-info/**```` - Retrieve statistical information

### :small_blue_diamond: Profile

-   ````**GET /profiles/customer/**```` - List all customer profiles
-   ````**GET /profiles/business/**```` - List all business profiles   
-   ````**GET /profile/<int:pk>**````    - Retrieve details of a specific user
-   ````**PATCH /profile/<int:pk>**````  - Update details of a specific user

### :small_blue_diamond: Authentication

- ````**POST /login/**```` - User Login

- ````**POST /registration/**```` -  User registration
  
### :small_blue_diamond: Offers

-   ````**GET /offers/**```` - Retrieve a list of offers with filtering and search options
-   ````**POST /offers/**```` - Create a new offer
-   ````**GET /offers/{id}**```` - Retrieve details of a specific offer
-   ````**PATCH /offers/{id}**```` - Update a specific offer
-   ````**DELETE /offers/{id}**```` - Delete a specific offer
-   ````**GET /offerdetails/{id}**```` - Retrieve details of a specific offer detail

### :small_blue_diamond: Orders

-    ````**GET /orders/**```` - Retrieve a list of orders for the logged-in user
-    ````**POST /orders/**```` - Create a new order for an offer.
-    ````**GET /orders/{id}**```` - Retrieve details of a specific order
-    ````**PATCH /orders/{id}**```` - Update the status of a specific order
-    ````**DELETE /orders/{id}**```` - Delete a specific order
-    ````**GET /order-count/<business_user_id>/**```` - Retrieve the number of orders for a business profile
-    ````**GET /completed-order-count/<business_user_id>/**```` - Retrieve the number of completed orders for a business profile


### :small_blue_diamond: Reviews

-    ````**GET /reviews/**```` - Retrieve a list of reviews
-    ````**POST /reviews/**```` - Create a new review   
-    ````**GET /reviews/{id}**```` - Retrieve details of a specific review    
-    ````**PATCH /reviews/{id}**```` - Update a specific review
-    ````**DELETE /reviews/{id}**```` -  Delete a specific review

## Tests

To run automated tests:
```bash
python manage.py test
````



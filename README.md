# Coderr

Coderr is a platform for freelancers like fiverr.

This repository contains the backend for the Coderr-Project. The Frontend is provided by the Developer Akademie and can be found here: https://github.com/Developer-Akademie-Backendkurs/project.Coderr

## Installation

Clone the repository to your computer via git bash.

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

A detailed guide to cloning a repository can be found [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)


## Usage
Open the project in your Code editor and open the Terminal for the project. 

Use the package manager [pip](https://pypi.org/project/pip/#files) to install the dependencies.

```bash
pip install -r requirements.txt
```

Then start a virtual environment and start the Backend:
```bash
#Start the virutal environment
.\env\Scripts\Activate

#Start the backend
python manage.py runserver
```

To use this project without the Frontend you need to have software like [Postman](https://www.postman.com/downloads/).

## Creating a user
To use the project you first have to create a user.

Endpoint: localhost/api/registration/

HTTP-Method: POST

Request body:
```python
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

### Login

If you want to check your data go visit the endpoint localhost/api/login/.

Here you use the POST-Method and send the request body with your information:
```python
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

## Profiles
Here you can view a profile or edit your own. You can also get a list of all the available business users or customer users.

### View profiles
If you are not sure what your user id is go to Login and enter your data. Your id will be in the response data.

Endpoint: localhost/api/profile/{your_user_id}/

HTTP-Method: GET

Permissions: You need to be authenticated

### Editing your own profile
If you want to edit your profile you can do this here. This will only work for your own profile.
The request body should include all fields that you want to update. If you want to empty a field add it to the request body and leave it as an empty string.

Endpoint: localhost/api/profile/{your_user_id}/

HTTP-Method: PATCH

Permission: You need to be authenticated and can only edit YOUR OWN profile

Request body:
```python
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "email": "new_email@business.de"
}
```

### View all available business/customer users
Endpoints for business users: localhost/api/profiles/business/
Endpoints for customer users: localhost/api/profiles/customer/

HTTP-Method: GET

Permissions: You need to be authenticated

## Offers
In this section you can read all about creating, reading, updating and deleting offers.

### Reading offers (list)
Endpoint: localhost/api/offers/

HTTP-Method: GET

You may filter the offers by different query parameters. Here is a list of the available filters:
```python
#Filters the offers by the creator with the given id
creator_id (Datatype: integer)

#Filtering by a minimum price
min_price (Datatype: float)

#Filtering by delivery time, less or equal to the given value
max_delivery_time (Datatype: integer)

#Sorting the order by either updated_at or min_price
ordering (Datatype: string)

#Sorting offers which include a specific string in their title/description
search (Datatype: string)

#How many results may be shown at once
page_size (Datatype: integer)
```

### Creating offers
Endpoint: localhost/api/offers/

HTTP-Method: POST

Permissions: You need to be authenticated and of type business to create offers

Request body:
```python
{
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Visitenkarte"
      ],
      "offer_type": "basic"
    },
    {
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

**NOTE:** When posting and offer you need to have at least 3 details. 

### Reading offers (single)
Here you get a detailed view of a single offer.

Endpoint: localhost/api/offers/{offer_id}/

HTTP-Method: GET

### Updating a single offer
Endpoint: localhost/api/offers/{offer_id}/

HTTP-Method: PATCH

Permissions: You need to be authenticated and the creator of the offer to patch.

Request body (contains all the fields that you want to update):
```python
{
  "title": "Updated Grafikdesign-Paket",
  "details": [
    {
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    }
  ]
}
```
**NOTE:** offer_type need to be provided to identify the detail.

### Delete a single offer
Endpoint: localhost/api/offers/{offer_id}/

HTTP-Method: DELETE

Permissions: You need to be authenticated and the creator of the offer to delete it.

### Reading a single offer detail
Here you can see all the detailed information of a offer-detail.

Endpoint: localhost/api/offerdetails/{offer_detail_id}/

HTTP-Method: GET

Permissions: You need to be authenticated

## Orders
In this section you can read all about creating, reading, updating and deleting orders.

### Reading orders (list)
Here you can get a list of all available orders that you have created or are adressed at you if you are a business user.

Endpoint: localhost/api/orders/

HTTP-Method: GET

Permissions: You need to be authenticated

### Creating orders
Here you can create a new order based on the Details of an offer.

Endpoint: localhost/api/orders/

HTTP-Method: POST

Permissions: You need to be authenticated and of type customer to create a new order.

Request body:
```python
{
  "offer_detail_id": 1
}
```

### Updating an order
Here you can **update the status** of an order.

Endpoint: localhost/api/orders/{order_id}/

HTTP-Method: PATCH

Permissions: You need to be authenticated and be of type business to update an order.

Request body:
```python
{
  "status": "completed"
}
```
**NOTE:** Allowed values for status are "in_progress", "completed" and "cancelled".

### Deleting an order
Endpoint: localhost/api/orders/{order_id}/

HTTP-Method: DELETE

Permissions: You need to be authenticated and of type admin/staff to delete an order.

### Business user information
Here you can see information about the orders of a business user.

#### Orders in progress
See how many orders with the status "in_progress" a business user has.

Endpoint: localhost/api/order-count/{business_user_id}/

HTTP-Method: GET

Permissions: You need to be authenticated

#### Orders completed
Here you can see how many orders a business user has "completed".

Endpoint: localhost/api/completed-order-count/{business_user_id}/

HTTP-Method: GET

Permissions: You need to be authenticated

## Reviews
In this section you can read all about creating, reading, updating and deleting reviews.

### Reading reviews
Here you can see all the reviews given by users.

Endpoint: localhost/api/reviews/

HTTP-Method: GET

Permissions: You need to be authenticated

Query Parameters to modify search results:
```python
#Filter the results for a specific business user
business_user_id (Datatype: integer)

#Filter the results for a specific reviewer
reviewer_id (Datatype: integer)

#Customize the ordering of the results. Possible values are "updated_at" and "rating"
ordering (Datatype: string)
```

### Creating a review
Endpoint: localhost/api/reviews/

HTTP-Method: POST

Permissions: You need to be authenticated and of type customer

Request body:
```python
{
  "business_user": 123,
  "rating": 4,
  "description": "Alles war toll!"
}
```

### Updating a review
Here you can update the rating and description of a review.

Endpoint: localhost/api/reviews/{review_id}/

HTTP-Method: PATCH

Permissions: You need to be authenticated and the creator of the review to update it.

Request body:
```python
{
  "rating": 5,
  "description": "Noch besser als erwartet!"
}
```

### Deleting a review
Endpoint: localhost/api/review/{review_id}/

HTTP-Method: DELETE

Permissions: You need to be authenticated and the creator of the review to delete it.

## App Information
Here you can get a information abou the app like how many reviews there are or the average rating.

Endpoint: localhost/api/base-info/

HTTP-Method: GET

## Contributing

It is not intended to contribute to this repository.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# Pizza Restaurants API

A Flask RESTful API for managing pizza restaurants and their menu items, with a React frontend.

## Features

- RESTful API endpoints for managing restaurants and pizzas
- SQLite database with SQLAlchemy ORM
- React frontend for interacting with the API
- Full test coverage with pytest

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: React
- **Database**: SQLite
- **Testing**: pytest

## Setup

1. Clone the repository
2. Install dependencies:

```bash
# Install Python dependencies
pipenv install
pipenv shell

# Install Node.js dependencies
npm install --prefix client
```

## Running the Application

### Backend

```bash
# Start the Flask server on port 5555
python server/app.py
```

### Frontend

```bash
# Start the React development server on port 4000
npm start --prefix client
```

## API Endpoints

### Restaurants

- `GET /restaurants` - List all restaurants
- `GET /restaurants/<int:id>` - Get a specific restaurant with its pizzas
- `DELETE /restaurants/<int:id>` - Delete a restaurant

### Pizzas

- `GET /pizzas` - List all available pizzas

### Restaurant Pizzas

- `POST /restaurant_pizzas` - Create a new restaurant-pizza association

## Testing

Run the test suite with:

```bash
pytest -x
```

## Database Schema

### Restaurant
- id: Integer (Primary Key)
- name: String
- address: String

### Pizza
- id: Integer (Primary Key)
- name: String
- ingredients: String

### RestaurantPizza
- id: Integer (Primary Key)
- price: Integer (1-30)
- pizza_id: Integer (Foreign Key)
- restaurant_id: Integer (Foreign Key)

```sh
npm start --prefix client
```

You are not being assessed on React, and you don't have to update any of the
React code; the frontend code is available just so that you can test out the
behavior of your API in a realistic setting.

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Core Deliverables

All of the deliverables are graded for the code challenge.

### Models

You will implement an API for the following data model:

![domain diagram](https://curriculum-content.s3.amazonaws.com/6130/code-challenge-1/domain.png)

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db migrate
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

- A `Restaurant` has many `Pizza`s through `RestaurantPizza`
- A `Pizza` has many `Restaurant`s through `RestaurantPizza`
- A `RestaurantPizza` belongs to a `Restaurant` and belongs to a `Pizza`

Update `server/models.py` to establish the model relationships. Since a
`RestaurantPizza` belongs to a `Restaurant` and a `Pizza`, configure the model
to cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

### Validations

Add validations to the `RestaurantPizza` model:

- must have a `price` between 1 and 30

### Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using to_dict() (don't forget the comma if specifying a
single field).

NOTE: If you choose to implement a Flask-RESTful app, you need to add code to
instantiate the `Api` class in server/app.py.

#### GET /restaurants

Return JSON data in the format below:

```json
[
  {
    "address": "address1",
    "id": 1,
    "name": "Karen's Pizza Shack"
  },
  {
    "address": "address2",
    "id": 2,
    "name": "Sanjay's Pizza"
  },
  {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  }
]
```

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using `to_dict()` (don't forget the comma if specifying
a single field).

#### GET /restaurants/<int:id>

If the `Restaurant` exists, return JSON data in the format below:

```json
{
  "address": "address1",
  "id": 1,
  "name": "Karen's Pizza Shack",
  "restaurant_pizzas": [
    {
      "id": 1,
      "pizza": {
        "id": 1,
        "ingredients": "Dough, Tomato Sauce, Cheese",
        "name": "Emma"
      },
      "pizza_id": 1,
      "price": 1,
      "restaurant_id": 1
    }
  ]
}
```

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### DELETE /restaurants/<int:id>

If the `Restaurant` exists, it should be removed from the database, along with
any `RestaurantPizza`s that are associated with it (a `RestaurantPizza` belongs
to a `Restaurant`). If you did not set up your models to cascade deletes, you
need to delete associated `RestaurantPizza`s before the `Restaurant` can be
deleted.

After deleting the `Restaurant`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Restaurant` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Restaurant not found"
}
```

#### GET /pizzas

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  {
    "id": 2,
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni",
    "name": "Geri"
  },
  {
    "id": 3,
    "ingredients": "Dough, Sauce, Ricotta, Red peppers, Mustard",
    "name": "Melanie"
  }
]
```

#### POST /restaurant_pizzas

This route should create a new `RestaurantPizza` that is associated with an
existing `Pizza` and `Restaurant`. It should accept an object with the following
properties in the body of the request:

```json
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is created successfully, send back a response with the
data related to the `RestaurantPizza`:

```json
{
  "id": 4,
  "pizza": {
    "id": 1,
    "ingredients": "Dough, Tomato Sauce, Cheese",
    "name": "Emma"
  },
  "pizza_id": 1,
  "price": 5,
  "restaurant": {
    "address": "address3",
    "id": 3,
    "name": "Kiki's Pizza"
  },
  "restaurant_id": 3
}
```

If the `RestaurantPizza` is **not** created successfully due to a validation
error, return the following JSON data, along with the appropriate HTTP status
code:

```json
{
  "errors": ["validation errors"]
}
```

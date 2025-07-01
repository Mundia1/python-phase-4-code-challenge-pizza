#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Enable CORS
CORS(app, resources={"*": {"origins": ["http://localhost:4000", "http://127.0.0.1:4000"]}})

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return "<h1>Pizza Restaurants API</h1>"

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response([restaurant.to_dict() for restaurant in restaurants], 200)

# GET /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)
    
    # Include restaurant_pizzas with nested pizza data
    restaurant_dict = restaurant.to_dict()
    restaurant_dict['restaurant_pizzas'] = [rp.to_dict() for rp in restaurant.restaurant_pizzas]
    return make_response(restaurant_dict, 200)

# DELETE /restaurants/<int:id>
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)
    
    # The cascade='all, delete-orphan' in the relationship will handle the deletion of related RestaurantPizzas
    db.session.delete(restaurant)
    db.session.commit()
    return make_response('', 204)

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response([pizza.to_dict() for pizza in pizzas], 200)

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['price', 'pizza_id', 'restaurant_id']
        for field in required_fields:
            if field not in data:
                return make_response({"errors": [f"{field} is required"]}, 400)
        
        # Check if pizza and restaurant exist
        pizza = Pizza.query.get(data['pizza_id'])
        restaurant = Restaurant.query.get(data['restaurant_id'])
        
        if not pizza or not restaurant:
            return make_response({"error": "Pizza or Restaurant not found"}, 404)
        
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            # Return the expected response format
            return make_response({
                'id': restaurant_pizza.id,
                'price': restaurant_pizza.price,
                'pizza_id': restaurant_pizza.pizza_id,
                'pizza': {
                    'id': restaurant_pizza.pizza.id,
                    'name': restaurant_pizza.pizza.name,
                    'ingredients': restaurant_pizza.pizza.ingredients
                },
                'restaurant_id': restaurant_pizza.restaurant_id,
                'restaurant': {
                    'id': restaurant_pizza.restaurant.id,
                    'name': restaurant_pizza.restaurant.name,
                    'address': restaurant_pizza.restaurant.address
                }
            }, 201)
            
        except ValueError:
            db.session.rollback()
            return make_response({"errors": ["validation errors"]}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({"errors": ["Validation errors"]}, 400)

if __name__ == "__main__":
    app.run(port=5555, debug=True)

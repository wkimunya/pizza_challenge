#!/usr/bin/env python3

from flask import Flask, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate
from app import db
from app import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in restaurants]
    return jsonify(restaurant_list)

# Route to create a new restaurant
@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_restaurant = Restaurant(name=data['name'], address=data.get('address'))
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant created successfully', 'id': new_restaurant.id}), 201

# Route to get a specific restaurant by ID
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        pizzas = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in restaurant.pizzas]
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': pizzas
        }
        return jsonify(restaurant_data)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

# Route to delete a specific restaurant by ID
@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({}), 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

# Route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas]
    return jsonify(pizza_list)

# Route to create a new RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    errors = validate_restaurant_pizza_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']
    price = data['price']

    pizza = Pizza.query.get(pizza_id)
    if not pizza:
        return jsonify({'error': 'Pizza not found'}), 404

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    new_restaurant_pizza = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=price)
    db.session.add(new_restaurant_pizza)
    db.session.commit()

    return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 201

def validate_restaurant_pizza_data(data):
    errors = []

    if 'price' not in data:
        errors.append('Price is required')
    if 'pizza_id' not in data:
        errors.append('Pizza ID is required')
    if 'restaurant_id' not in data:
        errors.append('Restaurant ID is required')

    return errors

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5555)


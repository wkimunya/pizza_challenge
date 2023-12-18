from flask import Flask, request, jsonify
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': restaurant.id, 'name': restaurant.name} for restaurant in restaurants]
    return jsonify({'restaurants': restaurant_list})

# Route to create a new restaurant
@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_restaurant = Restaurant(name=data['name'])
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant created successfully', 'id': new_restaurant.id}), 201

# Route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = [{'id': pizza.id, 'name': pizza.name} for pizza in pizzas]
    return jsonify({'pizzas': pizza_list})

# Route to create a new pizza
@app.route('/pizzas', methods=['POST'])
def create_pizza():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_pizza = Pizza(name=data['name'])
    db.session.add(new_pizza)
    db.session.commit()

    return jsonify({'message': 'Pizza created successfully', 'id': new_pizza.id}), 201

# # Route to get all restaurant-pizza combinations with prices
# @app.route('/restaurant_pizzas', methods=['GET'])
# def get_restaurant_pizzas():
#     restaurant_pizzas = RestaurantPizza.query.all()
#     response_data = []

#     for rp in restaurant_pizzas:
#         restaurant_data = {'restaurant_id': rp.restaurant.id, 'restaurant_name': rp.restaurant.name}
#         pizza_data = {'pizza_id': rp.pizza.id, 'pizza_name': rp.pizza.name, 'price': rp.price}
#         response_data.append({'restaurant': restaurant_data, 'pizza': pizza_data})

#     return jsonify({'restaurant_pizzas': response_data})

# # Route to create a new restaurant-pizza combination with price
# @app.route('/restaurant_pizzas', methods=['POST'])
# def create_restaurant_pizza():
#     data = request.get_json()

#     if 'restaurant_id' not in data or 'pizza_id' not in data or 'price' not in data:
#         return jsonify({'error': 'Restaurant ID, Pizza ID, and Price are required'}), 400

#     restaurant = Restaurant.query.get(data['restaurant_id'])
#     pizza = Pizza.query.get(data['pizza_id'])

#     if not restaurant or not pizza:
#         return jsonify({'error': 'Invalid Restaurant ID or Pizza ID'}), 400

#     new_restaurant_pizza = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=data['price'])
#     db.session.add(new_restaurant_pizza)
#     db.session.commit()

#     return jsonify({'message': 'Restaurant-pizza combination created successfully', 'id': new_restaurant_pizza.id}), 201

# if __name__ == '__main__':
#     app.run(port=5555)

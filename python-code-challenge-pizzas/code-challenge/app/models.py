from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')

# class Pizza(db.Model):
#     __tablename__ = 'pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

#     restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')

# class RestaurantPizza(db.Model):
#     __tablename__ = 'restaurant_pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
#     pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

#     restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
#     pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

from app import create_app, db
from models import Restaurant, Pizza, RestaurantPizza

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()

    # Add seed data
    restaurant1 = Restaurant(name='Italian Delight')
    restaurant2 = Restaurant(name='Pizza Palace')
    pizza1 = Pizza(name='Margherita')
    pizza2 = Pizza(name='Pepperoni')
    
    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2])
    db.session.commit()

    # Establish relationships through RestaurantPizza
    restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1)
    restaurant_pizza2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2)
    restaurant_pizza3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza1)
    
    db.session.add_all([restaurant_pizza1, restaurant_pizza2, restaurant_pizza3])
    db.session.commit()

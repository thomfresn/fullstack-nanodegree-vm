from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheezePizza = MenuItem(name = "Margarita", description = "La famosa Margarita", course = "Entree", price = "8.99€", restaurant = myFirstRestaurant)
session.add(cheezePizza)
session.commit()

#import Flask module
from flask import Flask
app = Flask (__name__)

#import SQLAlchemy module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#decorator
@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ""
    for item in items:
        output += item.name
        output += "</br>"
        output += item.description
        output += "</br>"
        output += item.price
        output += "</br>"

        output += "</br>"
        output += "</br>"
    return output

#prevent from running the application if file is imported as module
if __name__ == '__main__':
    #reload the server each time the code changes
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

#import Flask module
from flask import Flask, render_template, request, redirect, url_for

#import SQLAlchemy module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask (__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#decorator
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItemName = request.form['name']
        newMenuItem = MenuItem(name = newMenuItemName,restaurant_id = restaurant_id)
        session.add(newMenuItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editmenuitem.html', restaurant_id = restaurant_id)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deletemenuitem.html', restaurant_id = restaurant_id)

#prevent from running the application if file is imported as module
if __name__ == '__main__':
    #reload the server each time the code changes
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

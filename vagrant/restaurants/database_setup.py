#Configuration of SQLAlchemy (http://www.sqlalchemy.org/)
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    #Table definition
    __tablename__ = 'restaurant'
    #Mappers definition
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    #Table definition
    __tablename__ = 'menu_item'
    #Mappers definition
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integere, ForeignKey('restaurant.id'))
    Restaurant = relationship(Restaurant)

##### end of the file ##########

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

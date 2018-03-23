from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import *
 
engine = create_engine('postgres://uj_bqjmybOXas_Mv:m8agBAD_K2C_F2Hc@10.11.241.30:50407/o1WjFon9QaFP2rIV')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

newCategory = Categories(name = 'Web Developer')
session.add(newCategory)
session.commit()

newCategory = Categories(name = 'Machine Learning Engineer')
session.add(newCategory)
session.commit()

newCategory = Categories(name = 'Software Developer')
session.add(newCategory)
session.commit()

newCategory = Categories(name = 'Android Developer')
session.add(newCategory)
session.commit()

newCategory = Categories(name = 'iOs Developer')
session.add(newCategory)
session.commit()

newCategory = Categories(name = 'DevOps')
session.add(newCategory)
session.commit()

print "Added items!"
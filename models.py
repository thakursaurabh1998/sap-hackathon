import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from sqlalchemy.orm import relationship

Base = declarative_base()

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))

class User(Base):
	__tablename__  = 'user'

	firstname = Column(String(100))
	lastname = Column(String(100))
	password = Column(String(12), nullable = False)
	usertype = Column(String(30), nullable=False)
	gender = Column(String(10))
	id = Column(Integer,primary_key=True)
	email = Column(String(80), nullable=False)

class Application(Base):
	__tablename__ = 'application'

	id = Column(Integer, primary_key=True)
	userid = Column(Integer, ForeignKey('user.id'))

	user = relationship(User)

class EmployeeJob(Base):
	__tablename__ = 'jobs'

	id = Column(Integer, primary_key=True)
	location = Column(String)
	experience = Column(Integer, nullable=False)
	status = Column(String, nullable=False)
	jobtype = Column(String)
	packagerequired = Column(String)
	requirements = Column(String)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

class RecruitJob(Base):
	__tablename__ = 'recruitjob'

	id = Column(Integer,primary_key=True)
	companyname = Column(String)
	location = Column(String)
	experience = Column(Integer, nullable=False)
	status = Column(String, nullable=False)
	jobtype = Column(String)
	requirements=Column(String)
	packagerequired = Column(String)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


engine = create_engine('postgres://qC0rjfgm1SWPL2A8:EnhqVlbeSDilYcJV@10.11.241.10:35179/F2L_FiOuppSA-Xiy')
# engine = create_engine('postgresql://jh_db:helloworld@localhost/sap')

Base.metadata.create_all(engine)

"""
This is my first python application that is being deployed on SAP Cloud Platform in the Cloud Foundry environment
"""
from flask import Flask
import os
from flask import jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, EmployeeJob, RecruitJob, Categories
import json
from flask import request, redirect, url_for
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc, asc
import datetime
import requests

app = Flask(__name__)

port = int(os.getenv("PORT", 9009))

# engine = create_engine('postgres://qC0rjfgm1SWPL2A8:EnhqVlbeSDilYcJV@10.11.241.10:35179/F2L_FiOuppSA-Xiy')
engine = create_engine('postgresql://jh_db:helloworld@localhost/sap')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		password = request.form['password']
		gender = request.form['gender']
		usertype = request.form['type']
		email = request.form['email']
		newUser = User(
			firstname=firstname,
			lastname=lastname,
			password=password,
			gender=gender,
			usertype=usertype,
			email=email)
		session.add(newUser)
		session.commit()
		index = email.find('@')
		email = email[:index]
		if usertype=='recruiter':
			return redirect(url_for('recruit',email=email))
		else:
			return redirect(url_for('employee',email=email))
	if request.method == 'GET':
		return render_template('register.html')

@app.route('/recruit/<string:email>',methods=['GET','POST'])
def recruit(email):
	if request.method == 'GET':
		return render_template('recruiter.html',email=email)

@app.route('/recruit',methods=['GET','POST'])
def saverecdata():
	if request.method == 'POST':
		companyname = request.form['companyname']
		location = request.form['location']
		experience = request.form['experience']
		requirements = request.form['requirements']
		status = request.form['status']
		jobtype = request.form['jobtype']
		package = request.form['package']
		email = request.form['email'] + '@gmail.com'
		requirements = request.form['requirements']
		uid = session.query(User).filter_by(email=email).first()
		newData = RecruitJob(
			companyname=companyname,
			location=location,
			experience=experience,
			requirements=requirements,
			status=status,
			jobtype=jobtype,
			packagerequired=package,
			user_id= uid.id)
		session.add(newData)
		session.commit()
		return redirect(url_for('recruitersavailable',id=uid.id))

@app.route('/getjob/<string:email>',methods=['GET','POST'])
def employee(email):
	if request.method == 'GET':
		return render_template('employee.html',email=email)

@app.route('/getjob',methods=['GET','POST'])
def saveempdata():
	if request.method == 'POST':
		location = request.form['location']
		experience = request.form['experience']
		status = request.form['status']
		requirements = request.form['requirements']
		jobtype = request.form['jobtype']
		package = request.form['package']
		email = request.form['email'] + '@gmail.com'
		uid = session.query(User).filter_by(email=email).first()
		newData = EmployeeJob(
			location=location,
			experience=experience,
			requirements=requirements,
			status=status,
			jobtype=jobtype,
			packagerequired=package,
			user_id= uid.id)
		session.add(newData)
		session.commit()
		return redirect(url_for('employeeavailable',id=uid.id))


@app.route('/check',methods=['GET','POST'])
def checkLogin():
	if request.method == 'POST':
		username = request.form['loginusername']
		correctpass = session.query(User).filter_by(email=username).first()
		password = request.form['loginpassword']
		if correctpass.password==password:
			if correctpass.usertype=='recruiter':
				return redirect(url_for('recruitersavailable',id=correctpass.id))
			elif correctpass.usertype=='employee':
				return redirect(url_for('employeeavailable',id=correctpass.id))
		else:
			return "<script>alert('Password not correct')</script>"


@app.route('/recruiters_available/<int:id>')
def recruitersavailable(id):
	recruiterinfo = session.query(RecruitJob).filter_by(user_id=id).first()
	matching = session.query(EmployeeJob,User).filter(User.id==EmployeeJob.user_id).filter_by(requirements=recruiterinfo.requirements).all()
	print recruiterinfo.requirements
	return render_template('matchreq.html',matching=matching)

@app.route('/employee_available/<int:id>')
def employeeavailable(id):
	recruiterinfo = session.query(EmployeeJob).filter_by(user_id=id).first()
	matching = session.query(RecruitJob,User).filter(User.id==RecruitJob.user_id).filter_by(requirements=recruiterinfo.requirements).all()
	return render_template('matchemp.html',matching=matching)

@app.route('/itemAdd',methods=['GET','POST'])
def itemAdd():
	if request.method == 'GET':
		items = session.query(Categories).all()
		return render_template('take.html', items=items)
	elif request.method == 'POST':
		category = request.form['category']
		newCategory = Categories(name=category)
		session.add(newCategory)
		session.commit()
		return redirect(url_for('itemAdd'))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=port)
    # app.debug=True
    app.run(host='0.0.0.0', port=5000)
#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
user_routes.py

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps

#Modules
from flask_app import db, app
from models import User, Msg
from user_create import *


class Registration_form(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])#<h1>Registration</h1>
	submit = SubmitField('register')

class Login_form(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('login')

def admin_login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None or "user_id" not in session:
			return redirect(url_for("dashboard_forbidden"))
		elif user_read(session['user_id']).type != "admin":
			return redirect(url_for("dashboard_forbidden"))
		return f(*args, **kwargs)
	return decorated_function

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			return redirect(url_for("login_wtf"))
		return f(*args, **kwargs)
	return decorated_function
	
	
@app.route("/registration_wtf", methods=('GET', 'POST'))
def registration_wtf():
	
	#besser weg https://stackoverflow.com/questions/13585663/flask-wtfform-flash-does-not-display-errors
	
	form = Registration_form()#if "GET", create form to send to template
	if form.validate_on_submit():

		name = form.username.data 
		password = form.password.data
		confirmation = form.password2.data
		error = None
		
		if User.query.filter_by(name = name).first():
			error = 'user name already registered.'
			flash(error)
			print(error)
			
		if len(password) < 8:
			error = 'password must be at least 8 characters long.'
			flash(error)
			print(error)
		
		if password != confirmation:
			error = 'password and confirmation password must match.'
			flash(error)
			print(error)
			
		if error:
			return render_template('auth/registration_wtf.html', form=form)

		result = user_create(name, generate_password_hash(password))
		
		if result:
			flash(result)
			print(result)
			return redirect(url_for('login_wtf'))
		

	return render_template('auth/registration_wtf.html', form=form)
	

#Login_wtf 
@app.route("/login_wtf", methods=('GET', 'POST'))
def login_wtf():

	form = Login_form()#if "GET", create form to send to template
	if form.validate_on_submit():

		name = form.username.data
		password = form.password.data
		error = None
		
		user = User.query.filter_by(name = name).first()#first or else you get an iterator
		
		if not user:
			error = 'User not found.'
			print(error)
			flash(error)
		
		#not check_password_hash(user.password, password)
		elif not check_password_hash(user.password, password):
			error = 'User name or password False.'
			print(error)
			flash(error)

		if not error:
			session.clear()
			session['user_id'] = user.id
			#user.online = True
			#with just dashboard() I get an onscreen error Badrequest
			return redirect(url_for('index'))
		
	return render_template('auth/login_wtf.html', form=form)
	
@app.route("/logout")
def logout():
	#user_id = session.get('user_id')
	#user = User.query.get(id)
	#user.online = False
	
	session.clear()
	return redirect(url_for('index'))
	
#This is cool (if calls the following function
#before every request. and there is a bp version.

@app.before_request
def load_logged_in_user():
	#I think I needed "get()" instead of just session['key']
	#for the case that session doesn't have a user_id yet?
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_read(user_id)
		
@app.route("/user_read")
def user_read(id):
	user = User.query.get(id)
	return user
	
@app.route("/user_delete")
@login_required
def user_delete():
	print(session['user_id'])
	user = User.query.get(session['user_id'])
	db.session.delete(user)
	db.session.commit()
	print('User deleted!')
	return redirect(url_for('logout'))
	

@app.route("/user_delete_by_id/<int:id>")
@admin_login_required
def user_delete_by_id(id):

	if id == session['user_id']:
		print("Please use the User options to delete your own account.")
		return redirect(request.referrer)
		
	#user = User.query.get(id)
	user = db.session.query(User).get(id)
	name = user.name
	db.session.delete(user)
	db.session.commit()
	print('User ' + name + ' deleted!')
	return redirect(request.referrer)

# -*- coding: utf-8 -*-

"""
msg_routes.py

"""

#Built-in/Generic
import datetime
import random
#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

from sqlalchemy import or_, and_

from functools import wraps

#Modules
from flask_app import db, app 
from models import User, Msg 
from user_routes import *


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
	
@app.route("/msg_create")#, methods=('GET', 'POST')) 
@login_required
def msg_create(): 

#-->
#if request.method == 'POST': 
		
		#title = request.form['new_msg'] 
	title = request.args.get('new_msg', "Leer", type=str)
	print(title)
	if check_msg_exists(title): 
		print('A msg with this name already exists') 
		return redirect(url_for('dashboard')) 

	user = user_read(session['user_id'])
	
	new_current_msg = Msg(title=title, parent_user=user.id, type="waiting") 
		
		#This needs to be here before the change/choose function calls 
		#because they query for this msg and then update current 
	db.session.add(new_current_msg) 
	db.session.commit() 


	print('Msg *'+new_current_msg.title+'* for user with id: *'+str(session['user_id'])+'* created!') 
	#flash('Msg *'+new_current_msg.title+'* for user with id: *'+str(session['user_id'])+'* created!') 
	
	
	num_users = db.session.query(User).count()
	num_msgs = db.session.query(Msg).count()
	
	user = user_read(session['user_id'])
	msgs = Msg.query.filter_by(parent_user = user.id)
	json = jsonify(result = render_template('auth/index_container.html', msgs=msgs, \
	num_users=num_users, num_msgs=num_msgs))
	
	#after you query all the whatever, render the "micro-template", return json 
	#json = jsonify(result = render_template('auth/index.html', msgs=msgs))
	return json
	
	#return redirect(request.referrer) 
	
@app.route("/msg_show") 
def msg_show(): 
	
	if "user_id" in session:
		user = user_read(session['user_id'])
		msgs = db.session.query(Msg).filter(and_(Msg.type=="live", Msg.parent_user != user.id))
	else:
		msgs = db.session.query(Msg).filter(Msg.type=="live")
		
	msgs_length = msgs.count()
	if msgs_length == 0:
		msg = "Surprisingly we have no new messages at this time!\
		We are working hard to add some but in the mean time we \
		hope you have a wonderful day!"
		
		json = jsonify(result=msg)
		print(json)
		return json
	else:
		index = random.randint(0, msgs_length-1)
		msg = msgs[index].title
		#msgs[index].readers += 1
		
		json = jsonify(result=msg)
		print(json)
		return json
	#return redirect(request.referrer) 
	
@app.route("/msg_update/<int:id>", methods=('GET', 'POST')) 
@login_required
def msg_update(id):
	
	if request.method == 'POST': 
		 
		new_title = request.form['msg_title_change_input'] 
		if check_msg_exists(new_title): 
			flash('A msg with this name already exists') 
			return redirect(url_for('dashboard')) 

		msg = db.session.query(Msg).get(id) 
		old_title = msg.title 
		msg.title = new_title 
		db.session.commit() 
		
		print('Msg title from !'+old_title+'! to *'+msg.title+'* changed!') 
	return redirect(url_for('dashboard')) 

@app.route("/msg_delete/<int:id>")
@admin_login_required
def msg_delete(id):
	msg = db.session.query(Msg).get(id)
	db.session.delete(msg)
	db.session.commit()
	print('Msg *' + msg.title + '* Deleted!')
	return redirect( request.referrer)

@app.route("/msg_set_to_waiting/<int:id>")
@admin_login_required
def msg_set_to_waiting(id):
	msg = db.session.query(Msg).get(id)
	#db.session.delete(msg)
	msg.type = "waiting"
	db.session.commit()
	print('Msg *' + msg.title + '* is now waiting!')
	return redirect(request.referrer)
	
@app.route("/msg_set_to_live/<int:id>")
@admin_login_required
def msg_set_to_live(id):
	msg = db.session.query(Msg).get(id)
	#db.session.delete(msg)
	msg.type = "live"
	db.session.commit()
	print('Msg *' + msg.title + '* is now live!')
	return redirect(request.referrer)
	
@app.route("/msg_set_to_reported/<int:id>")
@admin_login_required
def msg_set_to_reported(id):
	msg = db.session.query(Msg).get(id)
	#db.session.delete(msg)
	msg.type = "reported"
	db.session.commit()
	print('Msg *' + msg.title + '* is now reported!')
	return redirect(request.referrer)
	
@app.route("/msg_liked/<int:id>")
@login_required
def msg_liked(id):
	msg = db.session.query(Msg).get(id)
	#db.session.delete(msg)
	msg.likes += 1
	db.session.commit()
	print('Msg *' + msg.title + '* liked!')
	return redirect(request.referrer)
	
@app.route("/check_msg_exists/<string:title>/")
def check_msg_exists(title):
	return db.session.query(Msg).filter_by(title=title, parent_user=session["user_id"]).first()


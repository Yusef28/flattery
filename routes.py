#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
routes.py: All Routes 

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from sqlalchemy import or_

#Modules
from flask_app import db, app

from models import User, Msg

import msg_routes, user_routes

from functools import wraps

#for some reason I need to also import all from each of these. 
#especially list_routes for find all from list
from msg_routes import *
from user_routes import *

#needs to be above all functions that use it???
def admin_login_required(f):

	@wraps(f)
	def decorated_function():
		if g.user is None or "user_id" not in session:
			return redirect(url_for("dashboard_forbidden"))
		elif user_read(session['user_id']).type != "admin":
			return redirect(url_for("dashboard_forbidden"))
		return f()
	return decorated_function
	
	
@app.route("/get_msgs_and_current_msg")
def get_msgs_and_current_msg():
	user = user_read(session['user_id'])
	
	
	msgs = Msg.query.all()
	#current_msg = find_current_msg(msgs)
	return msgs, None#, current_msg
	
@app.route("/")
def index():
	num_users = db.session.query(User).count()
	num_msgs = db.session.query(Msg).count()
	if 'user_id' not in session or not user_read(session['user_id']):
		return render_template('auth/index.html', num_users=num_users, num_msgs=num_msgs)
	else:
		msgs, current_msg = get_msgs_and_current_msg()
		return render_template('auth/index.html', msgs=msgs, current_msg=current_msg, 
		num_users=num_users, num_msgs=num_msgs)

#Messages @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/dashboard_show_msgs")
@admin_login_required
def dashboard_show_msgs():
	#get all msgs for the user
	
	msgs, current_msg = get_msgs_and_current_msg()
	return render_template('list/dashboard_msgs.html', msgs=msgs)
	

@app.route("/dashboard_show_live_msgs")
@admin_login_required
def dashboard_show_live_msgs():
	#get all msgs for the user
	
	msgs = db.session.query(Msg).filter(Msg.type=="live")
	return render_template('list/dashboard_msgs.html', msgs=msgs)
	
@app.route("/dashboard_show_waiting_msgs")
@admin_login_required
def dashboard_show_waiting_msgs():
	#get all msgs for the user
	
	msgs = db.session.query(Msg).filter(Msg.type=="waiting")
	return render_template('list/dashboard_msgs.html', msgs=msgs)
	
@app.route("/dashboard_show_reported_msgs")
@admin_login_required
def dashboard_show_reported_msgs():
	#get all msgs for the user
	
	msgs = db.session.query(Msg).filter(Msg.type=="reported")
	return render_template('list/dashboard_msgs.html', msgs=msgs)
	
	
#Users $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


@app.route("/dashboard_show_all_users")
@admin_login_required
def dashboard_show_all_users():
	
	users = User.query.all()
	title = "All Users"
	return render_template('list/dashboard_users.html', users=users, title=title)
	
@app.route("/dashboard_show_online_users")
@admin_login_required
def dashboard_show_online_users():
	
	users = db.session.query(User).filter(User.online==True)
	title = "Online Users"
	return render_template('list/dashboard_users.html', users=users, title=title)
	
@app.route("/dashboard_show_admin_users")
@admin_login_required
def dashboard_show_admin_users():
	
	users = db.session.query(User).filter(User.type=="admin")
	title = "Admin Users"
	return render_template('list/dashboard_users.html', users=users, title=title)
	
@app.route("/dashboard_show_premium_users")
@admin_login_required
def dashboard_show_premium_users():
	
	users = db.session.query(User).filter(User.type=="premium")
	title = "Premium Users"
	return render_template('list/dashboard_users.html', users=users, title=title)

@app.route("/dashboard_show_reported_users")
@admin_login_required
def dashboard_show_reported_users():
	
	users = db.session.query(User).filter(User.type=="reported")
	title = "Reported Users"
	return render_template('list/dashboard_users.html', users=users, title=title)

@app.route("/dashboard_show_banned_users")
@admin_login_required
def dashboard_show_banned_users():
	
	users = db.session.query(User).filter(User.type=="banned")
	title = "Banned Users"
	return render_template('list/dashboard_users.html', users=users, title=title)
	

# Main ########################################################################################


	
@app.route("/dashboard_forbidden")
def dashboard_forbidden():
	
	return render_template('list/forbidden.html')
	
@app.route("/dashboard_error_404")
def dashboard_error_404():
	
	return render_template('list/error_404.html')

@app.route("/dashboard")
@admin_login_required
def dashboard():
	
	#get all msgs for the user
	msgs, current_msg = get_msgs_and_current_msg()
	
	#if not current_msg:
	#-->
	return render_template('list/dashboard_msgs.html', msgs=msgs)
	
	#current, completed, deleted = [], [], []
	#tasks = Task.query.filter_by(parent_list=current_msg.id)
	#tasks = sorted(list(tasks), key=lambda x:(
	#-x.important,
	#x.state=="deleted",
	#x.state=="current",
	#x.state=="completed",
	#x.id))
	
	#for task in tasks:
	#	if task.state == "current":
	#		current.append(task)
	#	elif task.state == "completed":
	#		completed.append(task)
	#	else:
	#		deleted.append(task)
			
	#current = sorted(current, key=lambda x:(-x.important, x.sort_value))
	
	#return render_template('list/dashboard_filter_all.html', 
	#msgs=msgs, 
	#current=current, 
	#filter="All")
	
#find the list with current=True
#@app.route("/find_current_msg")
#def find_current_msg(msgs):#
#	for msg in msgs:
#		if msg.current == True:
#			return msg
#	return None
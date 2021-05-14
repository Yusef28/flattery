import os
import datetime

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
	

import routes, errors
from flask_app import db, app
from models import User, Msg
from user_routes import *
from user_create import *
from msg_routes import *

def admin_login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None or "user_id" not in session:
			return redirect(url_for("dashboard_forbidden"))
		elif user_read(session['user_id']).type != "admin":
			return redirect(url_for("dashboard_forbidden"))
		return f(*args, **kwargs)
	return decorated_function

@app.route("/add_compliments")
@admin_login_required
def add_compliments():

	user = user_read(session['user_id'])
	
	with open('compliment.txt', 'r', encoding="utf8") as compliments: 
		for c in compliments.readlines():
			
			title = c
			print(title)
			
			if check_msg_exists(title): 
				print('A msg with this name already exists') 
			else:
				new_current_msg = Msg(title=title, parent_user=user.id, type="live") 
				db.session.add(new_current_msg)
				db.session.commit()
				print('Msg *'+new_current_msg.title+'* for user with id: *'+str(session['user_id'])+'* created!') 
		


'''
class Config(object):
	
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USER_TLS = os.environ.get('MAIL_USER_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['flatteryteam@gmail.com']
	
'''





#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

#
"""
app.py: 
"""

#D DEVELOPMENT
#Built-in/Generic Imports
import datetime
import os 

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/flatterytest1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

#Modules
import routes, errors
from models import User, Msg

import logging
from logging.handlers import SMTPHandler
import config
import os

'''
app.config.update(
	MAIL_SERVER = os.environ.get('MAIL_SERVER'),
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25),
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None,
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
	ADMINS = ['flatteryteam@gmail.com']
	
)


if not app.debug:
	if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
		auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
	secure = None
	if app.config['MAIL_USE_TLS']:
		secure = ()
	mail_handler = SMTPHandler(
		mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
		fromaddr='no-reply@' + app.config['MAIL_SERVER'],
		toaddrs=app.config['ADMINS'], subject='Microblog Failure',
		credentials=auth, secure=secure)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)
	
'''


#P PRODUCTION
'''
#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

#
"""
app.py:
"""

#Built-in/Generic Imports
import datetime

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="flattery",
	password="FlatB1ll123",
	hostname="flattery.mysql.pythonanywhere-services.com",
	databasename="flattery$flatteryapp",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'StArFox64'

db = SQLAlchemy(app)

#Modules
import routes, errors
from models import User, Msg

import logging
from logging.handlers import SMTPHandler
import config
import os
'''


'''
app.config.update(
	MAIL_SERVER = os.environ.get('MAIL_SERVER'),
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25),
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None,
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
	ADMINS = ['flatteryteam@gmail.com']
)


if not app.debug:
	if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
		auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
	secure = None
	if app.config['MAIL_USE_TLS']:
		secure = ()
	mail_handler = SMTPHandler(
		mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
		fromaddr='no-reply@' + app.config['MAIL_SERVER'],
		toaddrs=app.config['ADMINS'], subject='Microblog Failure',
		credentials=auth, secure=secure)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)
	
'''

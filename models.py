#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
models.py: All Models
"""

#Built-ins/Generic
import datetime

#Libs
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from sqlalchemy.orm import relationship

#fur datum
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Date
#Modules
from flask_app import db

class User(db.Model):

	__tablename__ = "users"

	#Autoincrement has costs https://sqlite.org/autoinc.html
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=True, default=None)
	password = db.Column(db.String(200), nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	
	msgs = relationship("Msg", cascade="all, delete")
	
	time_zone = db.Column(db.String(80), unique=True, nullable=True, default=None)#must check if None
	list_count = db.Column(db.Integer, nullable=False, default=0) #not used
	last_active = db.Column(DateTime(timezone=True), server_default=func.now()) #and then update?
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	online = db.Column(Boolean, unique=False, default=False)
	
	#change this to status and update code?
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")#alpha, beta, basic, premium, anon, admin
	
	banned = db.Column(Boolean, unique=False, default=False)
	ban_severity = db.Column(db.Integer, nullable=False, default=0) #0,1,2 1=30 day, 2=life
	banned_until = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	#banned_from = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None (use func.now in code?)
	
class Msg(db.Model):

	__tablename__ = "msgs"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	parent_user = Column(Integer, ForeignKey('users.id'), nullable=False)
	#parent_user_name but careful if I allow name changing...
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	
	# ################################### new task Columns #######################################
	
	#Count Columns
	all_count = db.Column(db.Integer, nullable=False, default=0) #This will be the number of people who receive your message
	important_count = db.Column(db.Integer, nullable=False, default=0)
	deleted_count = db.Column(db.Integer, nullable=False, default=0)
	completed_count = db.Column(db.Integer, nullable=False, default=0)
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	
	#new 14-12-2020
	
	#sorting
	#sort_value = db.Column(db.Integer, nullable=False)#a value must be assigned at creation!!
	#sorted_by = db.Column(db.String(4056), unique=False, nullable=True, default=None)
	
	#type columns
	tags = db.Column(db.String(4056), unique=False, nullable=False, default="")
	categories = db.Column(db.String(4056), unique=False, nullable=False, default="")
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")#statuses:waiting, live, reported
	
	#social columns
	likes = db.Column(db.Integer, nullable=False, default=0)
	#like_users
	#readers int (number of people that have seen a message
	#goodness int ration likes/readers or just calculate as needed
	
	reported = db.Column(Boolean, unique=False, nullable=False, default=False)
	reported_by = db.Column(db.Integer, nullable=True, default=None)#User ID here

	#Time columns
	recycle_period_days = db.Column(db.Integer, nullable=False, default=7)
	
	#color columns
	color = db.Column(db.String(80), unique=False, nullable=True, default=None)#must check if none
	

#this is for admin tasks?or blog posts?
class Admin(db.Model):

	__tablename__ = "admin"
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=True, default='')
	body = db.Column(db.String(8000), nullable=True, default='')
	
	#smaller sizes so that it works in pythonanywheere without error 1118
	link = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	foto_link = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	signature = db.Column(db.String(200), unique=False, nullable=True, default="Yusef")
	
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	pinned = db.Column(Boolean, unique=False, default=False)
	deleted = db.Column(Boolean, unique=False, default=False)
	
	#sort_order = Column(Integer, nullable=False)#a value must be assigned at creation!!!
	
	#type columns
	tags = db.Column(db.String(1000), unique=False, nullable=False, default="")
	categories = db.Column(db.String(1000), unique=False, nullable=False, default="")
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")
	
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	
	
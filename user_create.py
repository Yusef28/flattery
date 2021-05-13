#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
user_create.py

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

#Modules
from flask_app import db, app
from models import User, Msg


@app.route("/user_create")
def user_create(name, password):

	user = User(name=name, password=password)
	db.session.add(user)
	db.session.commit()
	
	print('User *'+user.name+'* created!')
	return True
	





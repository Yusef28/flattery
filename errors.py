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

from flask_app import app, db
@app.errorhandler(404)
def not_found_error(error):
	return render_template('list/error_404.html'),404
	
@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('list/error_500.html'), 500
	
	

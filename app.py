#pip install flask
#pip install flask_sqlalchemy

from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create flask app instance 
app = Flask(__name__)

#create sqlite database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import flask_whooshalchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY']= '54534534545345hjb45j34h54h5bhjbjj344545'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['WHOOSH_BASE'] = '/site.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#print('12')


from Snap import routes
from Snap.routes import socketio

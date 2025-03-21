from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book


#Initializing the flask.
app = Flask(__name__)

#Setting the Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'


#Used to connect the Flask app to the flask-sqlalchemy code.
db.init_app(app)


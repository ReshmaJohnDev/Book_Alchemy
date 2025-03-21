from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Book
import os


#Initializing the flask.
app = Flask(__name__)

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'library.sqlite')

#Setting the Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


#Used to connect the Flask app to the flask-sqlalchemy code.
db.init_app(app)


# Create the tables if they don't already exist
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)



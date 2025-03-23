from flask_sqlalchemy import session

from data_models import Book,Author
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_


authors = session.query(Author).all()
return authors

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import foreign

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    author_birth_date = Column(Date)
    author_date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(id = {self.author_id}, name = {self.author_name})"


class Book(db.Model):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String)
    book_title = Column(String)
    book_publication_year = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.author_id') )

    def __repr__(self):
        return f"Book(id = {self.book_id}, title = {self.book_title})"






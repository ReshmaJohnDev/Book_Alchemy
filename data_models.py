from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an Author in the database.
    """
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String, unique=True)
    author_birth_date = db.Column(db.Date)
    author_date_of_death = db.Column(db.Date)

    def __repr__(self):
        """
        Returns a string representation of the Author object.
        """
        return f"Author(id = {self.author_id}, author_name = {self.author_name})"


class Book(db.Model):
    """
    Represents a Book in the database.
    """
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_isbn = db.Column(db.String)
    book_title = db.Column(db.String,unique=True)
    book_publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id') )

    # Define the relationship with the Author model
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        """
        Returns a string representation of the Author object.
        """
        return f"Book(id = {self.book_id}, title = {self.book_title})"
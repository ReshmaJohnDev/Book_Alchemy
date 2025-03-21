from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    author_birth_date = Column(Date)
    author_date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(id = {self.author_id}, name = {self.author_name})"






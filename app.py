import os
import requests
from datetime import datetime
from flask import Flask, render_template,request, redirect, url_for, flash
from data_models import db,Author, Book
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session


API_URL = 'https://www.googleapis.com/books/v1/volumes'
#Initializing the flask.
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure, random 24-byte key

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'library.sqlite')

#Setting the Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'


#Used to connect the Flask app to the flask-sqlalchemy code.
db.init_app(app)


# Create the tables if they don't already exist
with app.app_context():
    db.create_all()


@app.route('/')
def home_page():

    #Default criteria
    sort_by = request.args.get('sort_by', None)
    books_query = Book.query
    if sort_by == 'author':
        books_query = books_query.join(Author).order_by(Author.author_name)
    elif sort_by == 'title':
        books_query = books_query.join(Author).order_by(Book.book_title)

    books = books_query.all()

    book_details = []

    for book in books:
        # Call the Google Books API using the ISBN for each book
        isbn = book.book_isbn.replace('-', '')
        response = requests.get(f'{API_URL}?q=isbn:{isbn}')
        if response.status_code == 200:
            books_data = response.json().get('items', [])
            if books_data:
                book_info = books_data[0]['volumeInfo']
                book_image_url = book_info.get('imageLinks', {}).get('thumbnail', None)
            else:
                book_image_url = None
        else:
            book_image_url = None

        book_details.append({
            'title': book.book_title,
            'author': book.author.author_name,
            'publication_year': book.book_publication_year,
            'image_url': book_image_url
        })
    return render_template('home.html', book_details= book_details, sort_by= sort_by)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        authors = Author.query.all()
        author_name = request.form.get('author_name')
        author_birth_date= request.form.get('author_birth')
        author_death_date = request.form.get('author_death')

        # Convert string dates to datetime.date objects
        author_birth_date = datetime.strptime(author_birth_date, '%Y-%m-%d').date()
        death_date = None
        if author_death_date:
            # If the death date is provided, convert it as well
            death_date = datetime.strptime(author_death_date, '%Y-%m-%d').date()

        new_author = Author(
            author_name=author_name,
            author_birth_date=author_birth_date,
            author_date_of_death=death_date
        )

        db.session.add(new_author)
        db.session.commit()
        flash('Author successfully added!', 'success')
        return redirect(url_for('home_page'))

    return render_template('add_author.html')
#
#
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        author_id = request.form.get('author_id')
        book_isbn = request.form.get('book_isbn')
        book_title= request.form.get('book_title')
        book_publication_year = request.form.get('book_publication_year')

        new_book = Book(
            book_isbn = book_isbn,
            book_title = book_title,
            book_publication_year = book_publication_year,
            author_id  = author_id
        )

        db.session.add(new_book)
        db.session.commit()
        flash('Book successfully added!', 'success')
        return redirect(url_for('home_page'))

    return render_template('add_book.html',authors = authors )


if __name__ == '__main__':
    app.run(debug=True)



import os
import requests
from datetime import datetime
from flask import Flask, render_template,request, redirect, url_for, flash
from data_models import db,Author, Book


#API to get book’s cover image
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

def fetch_book_image(isbn):
    try:
        isbn = isbn.replace('-', '')  # Remove hyphens for standardization
        response = requests.get(f'{API_URL}?q=isbn:{isbn}')
        if response.status_code == 200:
            books_data = response.json().get('items', [])
            if books_data:
                book_info = books_data[0]['volumeInfo']
                book_image_url = book_info.get('imageLinks', {}).get('thumbnail', None)
                return book_image_url
            else:
                return None
    except requests.RequestException as e:
        print(f"Error fetching book image: {e}")
        return None


@app.route('/',methods=['GET', 'POST'])
def home_page():
    """
    Home page that allows users to search and sort books by title or author.
    """
    search_query = ''
    sort_by = request.args.get('sort_by', None)
    books = []
    try:
        if request.method == 'POST':
            search_query = request.form.get('search_query', '')  # Get the search query from the form
            if search_query:
                books = Book.query.filter(Book.book_title.ilike(f'%{search_query}%')).all()
        # For GET Request
        else:
            if sort_by == 'author':
                books = Book.query.join(Author).order_by(Author.author_name).all()
            elif sort_by == 'title':
                books = Book.query.order_by(Book.book_title).all()
            else:
                books = Book.query.all()

        book_details = []
        for book in books:
            # Call the Google Books API using the ISBN for each book
            book_image_url = fetch_book_image(book.book_isbn)
            book_details.append({
                'book': book,
                'image_url': book_image_url
            })
        return render_template('home.html', book_details=book_details, sort_by=sort_by, search_query=search_query)
    except Exception as e:
        print(f"Error in home_page route: {e}")
        return render_template('home.html', book_details=[], sort_by=sort_by, search_query=search_query)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Route for adding a new author.
    """
    try:
        if request.method == 'POST':
            author_name = request.form.get('author_name')
            author_birth_date = request.form.get('author_birth')
            author_death_date = request.form.get('author_death')

            # Convert string dates to datetime.date objects
            author_birth_date = datetime.strptime(author_birth_date, '%Y-%m-%d').date()
            death_date = None
            if author_death_date:
                # Convert the death date , if provided
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

    except Exception as e:
        print(f"Error in add_author route: {e}")
        flash('An error occurred while adding the author.'
              ' Please try again later.', 'error')
        return redirect(url_for('home_page'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Route for adding a new Book.
    """
    try:
        authors = Author.query.all()
        if request.method == 'POST':
            author_id = request.form.get('author_id')
            book_isbn = request.form.get('book_isbn')
            book_title = request.form.get('book_title')
            book_publication_year = request.form.get('book_publication_year')

            new_book = Book(
                book_isbn=book_isbn,
                book_title=book_title,
                book_publication_year=book_publication_year,
                author_id=author_id
            )

            db.session.add(new_book)
            db.session.commit()
            flash('Book successfully added!', 'success')
            return redirect(url_for('home_page'))

        return render_template('add_book.html', authors=authors)

    except Exception as e:
        print(f"Error in add_book route: {e}")
        flash('An error occurred while adding the book.'
              ' Please try again later.', 'error')
        return redirect(url_for('home_page'))


@app.route('/book/<int:book_id>/delete', methods=['GET', 'POST'])
def delete_book(book_id):
    """
     Routing that deletes a book from the homepage. If the book’s author doesn’t have any other books
     in the  library, it deletes the author from your database.
    """
    try:
        if request.method == 'POST':
            book = Book.query.get_or_404(book_id)
            author = Author.query.get_or_404(book.author_id)
            print(author)
            # Delete the user selected book
            db.session.delete(book)
            db.session.commit()

            remaining_books = Book.query.filter_by(author_id=author.author_id).all()
            if not remaining_books:
                db.session.delete(author)
                db.session.commit()

            flash('Book successfully deleted!', 'success')
            return redirect(url_for('home_page'))

    except Exception as e:
        print(f"Error in delete_book route: {e}")
        flash('An error occurred while deleting the book. Please try again later.', 'error')
        return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)


Book Alchemy
A simple web application to manage books and authors, built using Flask and SQLAlchemy. This app allows users to add, delete, and search books, and also manage authors with detailed information.

Features
Search Books: Search for books by title.
Sort Books: Sort books by author name or title.
Add Authors: Add new authors with their birth and death dates.
Add Books: Add new books with ISBN, title, publication year, and associate them with authors.
Delete Books: Delete books and automatically remove authors who no longer have any books associated with them.

Technologies Used
Flask: Micro web framework for Python.

SQLAlchemy: ORM for interacting with the database.

SQLite: Database to store authors and books information.

Requests: To fetch book data from the Google Books API for book covers.

Installation
Prerequisites
Python 3.x

Pip (Python package installer)

Steps to Run Locally
Clone the repository:

bash
Copy code
git clone https://github.com/ReshmaJohnDev/Book_Alchemy.git
cd Book_Alchemy
Install the required dependencies:



text
Copy code
FLASK_APP=app.py
FLASK_ENV=development
Initialize the database (this will create the necessary tables):

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the application:

bash
Copy code
flask run
Open your browser and visit http://127.0.0.1:5000/.

File Structure
bash
Copy code
/library-management-system
│
├── /data                   # Folder containing the SQLite database
├── /templates              # HTML templates for rendering views
│   ├── home.html           # Homepage with book and author management
│   ├── add_author.html     # Page to add new authors
│   ├── add_book.html       # Page to add new books
│
├── /static                 # Folder containing static assets like CSS/JS
├── app.py                  # Main Flask application file
├── data_models.py          # SQLAlchemy models for Authors and Books
├── requirements.txt        # Python dependencies file
└── README.md               # Project documentation
Usage
Home Page: Displays a list of all books and authors. You can sort the books by title or author name, and search for books by title.

Add Author: Navigate to /add_author to add a new author. You must enter the author's name, birth date, and (optional) death date.

Add Book: Navigate to /add_book to add a new book. You need to provide the book's ISBN, title, publication year, and select an author for the book.

Delete Book: You can delete a book from the homepage. If the deleted book was the last one by an author, the author will also be deleted from the system.
The application fetches book cover images from the Google Books API using the ISBN. When a book is added, the system queries the API to retrieve the cover image.





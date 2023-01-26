from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'book': 'info'}

@api.route('/books', methods = ['POST'])
@token_required
def add_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    release_date = request.json['release_date']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    book = Book(title, author, length, release_date, isbn, user_token = user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.length = request.json['length']
    book.release_date = request.json['release_date']
    book.isbn = request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def remove_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
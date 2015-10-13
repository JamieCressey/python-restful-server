from flask import Blueprint
from flask_restful import Api, Resource, abort, reqparse
from RestfulServer.data.models import Book, db
from RestfulServer.middleware import authenticate
from datetime import datetime

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class BooksApi(Resource):
	method_decorators = [authenticate]
	def get(self):
		_books = []
		books = Book.query.all()
		for book in books:
			_books.append(book.as_dict())

		return _books

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('title', type=str, help='Title of the book', required = True)
		parser.add_argument('author', type=str, help='Author of the book')
		parser.add_argument('release_date', type=str, help='Release date of the book')
		args = parser.parse_args()

		book = Book(args.title, args.author)

		if args.release_date:
			book.release_date = datetime.strptime(args.release_date, '%d/%m/%Y')

		db.session.add(book)
		db.session.commit()

		book = Book.query.filter_by(title=args.title).first()

		return book.as_dict()
		

class BookApi(Resource):
	def get(self, title):
		book = Book.query.filter_by(title=title).first()
		if book:
			return book.as_dict()
		else:
			abort(404)

	def put(self, title):
		parser = reqparse.RequestParser()
		parser.add_argument('author', type=str, help='Author of the book')
		parser.add_argument('release_date', type=str, help='Release date of the book')
		args = parser.parse_args()

		book = Book.query.filter_by(title=title).first()
		if book:
			if args.author:
				book.author = args.author
			if args.release_date:
				try:
					book.release_date = datetime.strptime(args.release_date, '%d/%m/%Y')
				except:
					return {
						'error': 'invalid release_date: DD/MM/YYYY'
					}, 500

			db.session.commit()

			return Book.query.filter_by(title=title).first().as_dict()
		else:
			abort(404)

	def delete(self, title):
		book = Book.query.filter_by(title=title).first()
		if book:
			db.session.delete(book)
			db.session.commit()
			return {
				'message': 'Book deleted'
			}
		else:
			abort(404)

api.add_resource(BooksApi, '/books/')
api.add_resource(BookApi, '/book/<string:title>/')

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	author = db.Column(db.String(120))
	release_date = db.Column(db.DateTime)

	def __init__(self, title, author, release_date=None):
		self.title = title
		self.author = author
		self.release_date = release_date

	def __repr__(self):
		return '<Book %r>' % (self.title)

	def as_dict(self):
		from datetime import datetime

		_dict = {}
		for c in self.__table__.columns:
			_val = getattr(self, c.name)
			if isinstance(_val, datetime):
				_val = _val.strftime('%d/%m/%Y') 

			_dict[c.name] = _val

		return _dict

class Credential(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(120))
	secret = db.Column(db.String(120))
	nonce = db.Column(db.Integer)

	def __init__(self, key, secret, nonce=0):
		self.key = key
		self.secret = secret
		self.nonce = nonce

	def __repr__(self):
		return '<Credential>'

	def as_dict(self):
       		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

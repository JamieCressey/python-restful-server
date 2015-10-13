from flask_restful import abort
from flask_limiter import Limiter
from flask import request
from RestfulServer.data.models import Credential, db
from functools import wraps

limiter = Limiter()

def authenticate(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		from base64 import b64encode
		from hashlib import sha256
		from hmac import new

		if not getattr(func, 'authenticated', True):
			return func(*args, **kwargs)

		_headers = {}
		_headers['key'] = request.headers.get('X-Authentication-Key')
		_headers['sig'] = request.headers.get('X-Authentication-Signature')
		_headers['nonce'] = request.headers.get('X-Authentication-Nonce')

		for h in _headers:
			if not h:
				abort(401)

		print _headers['nonce']

		creds = Credential.query.filter_by(key=_headers['key']).first()

		if not creds:
			abort(401)

		print creds.nonce

		if _headers['nonce'] < creds.nonce:
			abort(401)

		_sig = b64encode(new(str(creds.secret),
			  msg=str(_headers['nonce']),
			  digestmod=sha256).digest())

		if _sig != _headers['sig']:
			abort(401)
	
		creds.nonce = _headers['nonce']
		db.session.commit()
		
		return func(*args, **kwargs)

		abort(401)
	return wrapper

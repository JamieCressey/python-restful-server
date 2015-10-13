#!/usr/bin/env python
from RestfulServer import app
from RestfulServer.data.models import db, Book, Credential

with app.app_context():
	db.drop_all()
	db.create_all()

	test_creds = Credential('#your_api_key', '#your_api_secret')

	db.session.add(test_creds)
	db.session.commit()

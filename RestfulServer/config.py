import os

class BaseConfig(object):
	DEBUG = False
	TESTING = False
	# sqlite :memory: identifier is the default if no filepath is present
	SQLALCHEMY_DATABASE_URI = 'sqlite:///restful.db'
	RATELIMIT_GLOBAL = "200 per day, 60 per hour"
	RATELIMIT_HEADERS_ENABLED = True

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	TESTING = True

class TestingConfig(BaseConfig):
	DEBUG = False
	TESTING = True

config = {
	"development": "RestfulServer.config.DevelopmentConfig",
	"testing": "RestfulServer.config.TestingConfig"
}


def configure_app(app):
	config_name = os.getenv('FLAKS_CONFIGURATION', 'development')
	app.config.from_object(config[config_name])
	app.config.from_pyfile('config.cfg', silent=True)

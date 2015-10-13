from flask import Flask
from utils import get_instance_folder_path
from RestfulServer.api.controllers import api_bp
from RestfulServer.config import configure_app
from RestfulServer.middleware import limiter
from RestfulServer.data.models import db

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True)

configure_app(app)
db.init_app(app)
limiter.init_app(app)

app.register_blueprint(api_bp)

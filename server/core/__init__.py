from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app(app_name="MAP_API"):
	app = Flask(app_name)
	app.config.from_object('core.config.BaseConfig')
	cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
	cors.init_app(app)

	from core.api import api
	app.register_blueprint(api, url_prefix="/api")

	from core.models import db
	db.init_app(app)
	migrate.init_app(app,db)
	
	return app
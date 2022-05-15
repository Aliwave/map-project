from ntpath import join
from pickle import TRUE
from posixpath import dirname
from dotenv import load_dotenv
import os



class BaseConfig(object):
	FLASK_DEBUG = 1
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/pythontest'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'the quick brown fox jumps over the lazy   dog'
	#SESSION_TYPE = "filesystem"
	UPLOAD_FOLDER = os.path.dirname(os.path.dirname(__file__))+"/uploads/"
	ALLOWED_EXTENSIONS = {'geojson', 'csv','xlsx'}
	FLASK_ENV ='development'
	DEVELOPMENT = True
	DEBUG= True
	dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
	load_dotenv(dotenv_path)
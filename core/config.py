from ntpath import join
from dotenv import load_dotenv
import os

class BaseConfig(object):
	UPLOAD_FOLDER = os.path.dirname(os.path.dirname(__file__))+"/uploads/"
	ALLOWED_EXTENSIONS = {'xlsx'}
	SESSION_TYPE = 'filesystem'
	SESSION_COOKIE_SECURE=True
	dotenv_path = join(os.path.dirname(__file__), '.env')
	load_dotenv(dotenv_path)
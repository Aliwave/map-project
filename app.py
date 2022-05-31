from re import template
from flask import Flask, jsonify, request, session, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
# from flask_caching import Cache
from core.models import DBUpload, DefaultData, DataGetter
from random import randint
import json
import uuid
from urllib.request import Request
import os
import pandas as pd


app = Flask(__name__,
						static_folder="./dist/static",
						template_folder="./dist")
app.config.from_object('core.config.BaseConfig')
Session(app)
# cache = Cache(app)
# cache.init_app(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors.init_app(app)

#queslist = DefaultData.getDefaultQues(session.sid)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/uploaddb', methods=['POST'])
def upload_file():
	file = DBUpload(request)#,session.get('username')
	filename = file.saveFile(session.sid)
	queslist = file.getQuestions()
	return jsonify({"msg":session.sid,"queslist":queslist})

@app.route('/api/geojson', methods=['GET'])
def maptest():
	return jsonify(DefaultData.getDefaultGeoJson().to_json())

@app.route('/api/regions', methods=['GET'])
def getReglist():
	# mainlist["geojson"] = r1.to_json()
	# #mainlist["reg_list"] = reg_list
	return jsonify(DefaultData.getDefaultReg())

@app.route('/api/questions', methods=['GET'])
def getQuestions():
	#queslist = DefaultData.getDefaultQues(session.sid)
	# if(len(queslist) != 0):
	# 	return jsonify(list(queslist[:,0]))
	return jsonify(DefaultData.getDefaultQues(session.sid))

@app.route('/api/data', methods=['POST'])
def getData():
	requestdata = request.get_json()
	data = DataGetter(session.sid)
	return data.getData(requestdata)
	#return session.sid

@app.route('/api/dataCrit', methods=['POST'])
def getCritData():
	requestdata = request.get_json()
	data = DataGetter(session.sid)
	return data.getCritData(requestdata)

@app.route('/api/session',methods=['GET'])
def getSession():
	return session.sid

@app.route('/api/session1',methods=['GET'])
def getSession1():
	return session.sid

# @app.route('/api/test',methods=['GET'])
# @cache.cached()
# def test():
# 	number = randint(1,1000)
# 	cache.set('number1',pd.read_json(os.path.dirname(__file__)+"/uploads/remaster.json",orient="split").to_json(orient="split"))
# 	rb = cache.get('number1')
# 	return f'{rb}'

# @app.route('/api/test1',methods=['GET'])
# def test1():
	
# 	testdict = {}
# 	for k in cache.cache._cache:
# 		testdict[k] = cache.get(k)
# 	return testdict

@app.route('/hello/<string:name>/')
def say_hello(name):
	response = { 'msg': 'Hello{}'.format(name)}
	return jsonify(response)

# @app.shell_context_processor
# def shell():
# 	return {"db":db, "UserTable":UserTable}
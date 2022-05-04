from flask import Blueprint, jsonify, request, session
import pandas as pd
import json
from core.models import User, DBUpload, DefaultData
import uuid


api = Blueprint('api', __name__)
queslist = DefaultData.getDefaultQues()

@api.route('/uploaddb', methods=['POST'])
def upload_file():
	file = DBUpload(request)#,session.get('username')
	filename = file.saveFile()
	queslist = file.getQuestions()
	return jsonify({"msg":session['username']+' '+str(session['visits']),"queslist":list(queslist[:,0])})

@api.route('/geojson', methods=['GET'])
def maptest():
	return jsonify(DefaultData.getDefaultGeoJson().to_json())

@api.route('/regions', methods=['GET'])
def getReglist():
	# mainlist["geojson"] = r1.to_json()
	# #mainlist["reg_list"] = reg_list
	return jsonify(DefaultData.getDefaultReg())

@api.route('/questions', methods=['GET'])
def getQuestions():
	# if(len(queslist) != 0):
	# 	return jsonify(list(queslist[:,0]))
	return jsonify(DefaultData.getDefaultQues())


@api.route('hello/<string:name>/')
def say_hello(name):
	response = { 'msg': 'Hello{}'.format(name)}
	return jsonify(response)

# @api.route("/")
# def index():
#     if 'visits' in session:
#         session['visits'] = session.get('visits') + 1  # обновление данных сессии
#     else:
#         session['visits'] = 1  # запись данных в сессию
 
#     return f"<h1>Main Page</h1>Число просмотров: {session['visits']}"
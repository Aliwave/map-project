import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import re
import numpy as np
import os
from werkzeug.utils import secure_filename
from core.config import BaseConfig
from flask import jsonify
import geopandas as gpd
from io import StringIO
import uuid

db = SQLAlchemy()

#Миграции
class UserTable(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)

	def to_dict(self):
		return dict(id=self.id,
								name=self.name)

#Модели
class User:
	def __init__(self, name):
		self.name = name
	def get_name(self):
		print(self.name)

class DBUpload:
	def __init__(self, request, username="test"):
		self.request = request
		self.file = request.files['file']
		self.filename = self.file.filename
		self.username = username
		print(self.username)

	def saveFile(self):
		try:

			if(self.request.method == 'POST'):
				if self.file and self.allowed_file(self.filename):
					#filename = secure_filename(self.file.filename)
					temp = pd.read_excel(self.file)
					with open(os.path.join(BaseConfig.UPLOAD_FOLDER, self.username+'.json'), 'w') as f: 
						f.write(temp.to_json(orient="split"))
					self.filename = os.path.join(BaseConfig.UPLOAD_FOLDER, self.username+'.json')
		except BaseException as e:
				print(e)
				#self.file.save(os.path.join(BaseConfig.UPLOAD_FOLDER, "maindb."+filename.rsplit('.', 1)[1].lower()))
				#filename = os.path.join(BaseConfig.UPLOAD_FOLDER, "maindb."+filename.rsplit('.', 1)[1].lower())


	def getQuestions(self):
		table1 = pd.read_json(self.filename,orient="split")
		table1 = table1.fillna("")
		tpl = "\d+\W\s.*"
		ques = [] 
		for j in range(0,len(table1.axes[1])):
			for i in range(0,50):
				if re.match(tpl, str(table1.iat[i,j])) is not None:
					ques.append([table1.iat[i,j],i,j])
		queslist = np.array(ques)
		return queslist
	
	def allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in BaseConfig.ALLOWED_EXTENSIONS

class DefaultData:
	__regions = [
	"Вся область",
	"ЗАТО Первомайский",
	"Свечинский район",
	"Кикнурский район",
	"Сунский район",
	"Опаринский район",
	"Подосиновский район",
	"Пижанский район",
	"Оричевский район",
	"Кумёнский район",
	"г. Котельнич",#"городской округ Котельнич"
	"Орловский район",
	"Даровской район",
	"Верхошижемский район",
	"Верхнекамский район",
	"Афанасьевский район",
	"г. Киров",#"городской округ Киров",
	"Юрьянский район",
	"Белохолуницкий район",
	"Котельничский район",
	"Арбажский район",
	"Тужинский район",
	"г. Вятские Поляны",#"городской округ Вятские Поляны"
	"г. Кирово-Чепецк",#"городской округ Кирово-Чепецк"
	"г. Слободской",#"городской округ Слободской"
	"Советский район",
	"Омутнинский район",
	"Унинский район",
	"Богородский район",
	"Зуевский район",
	"Фалёнский район",
	"Немский район",
	"Кильмезский район",
	"Лебяжский район",
	"Уржумский район",
	"Нолинский район",
	"Санчурский район",
	"Нагорский район",
	"Мурашинский район",
	"Лузский район",
	"Яранский район",
	"Малмыжский район",
	"Вятскополянский район",
	"Шабалинский район",
	"Слободской район",
	"Кирово-Чепецкий район"
	]
	__path = "E:\\University\\MagaDiplom\\map_project_2_main\\server\\uploads\\maindb.json"
	__geojson = gpd.read_file("E:\\University\\MagaDiplom\\map_project_2_main\\server\\backend\\regions.geojson", encoding="utf-8")
	@staticmethod
	def getDefaultQues():
		table1 = pd.read_json(DefaultData.__path,orient="split")
		table1 = table1.fillna("")
		tpl = "\d+\W\s.*"
		ques = [] 
		for j in range(0,len(table1.axes[1])):
			for i in range(0,50):
				if re.match(tpl, str(table1.iat[i,j])) is not None:
					ques.append([table1.iat[i,j],i,j])
		queslist = np.array(ques)
		return list(queslist[:,0])

	@staticmethod
	def getDefaultReg():
		return DefaultData.__regions
	
	@staticmethod
	def getDefaultGeoJson():
		return DefaultData.__geojson
	



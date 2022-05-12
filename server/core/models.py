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
import json

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
	"Орический район",
	"Куменский район",
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
	__path = os.path.dirname(os.path.dirname(__file__))+"\\uploads\\remaster.json"
	__geojson = gpd.read_file(os.path.dirname(os.path.dirname(__file__))+"\\backend\\regions.geojson", encoding="utf-8")
	__maintable = pd.read_json(__path,orient="split")
	
	@staticmethod
	def getDefaultQues():
		# table1 = pd.read_json(DefaultData.__path,orient="split")
		# table1 = table1.fillna("")
		# tpl = "\d+\W\s.*"
		# ques = [] 
		# for j in range(0,len(table1.axes[1])):
		# 	for i in range(0,50):
		# 		if re.match(tpl, str(table1.iat[i,j])) is not None:
		# 			ques.append([table1.iat[i,j],i,j])
		# queslist = np.array(ques)
		# return list(queslist[:,0])
		maintable = DefaultData.__maintable
		queslist = list(maintable)
		queslist[3] = re.sub(r'(\s\/\/\s.*)','',queslist[3])
		for i in range(0,len(queslist)-1):
			queslist[i] = re.sub(r'(\s\/\/\s.*)','',queslist[i])
		queslist = sorted(set(queslist), key=lambda d: queslist.index(d))
		return queslist

	@staticmethod
	def getDefaultReg():
		return DefaultData.__regions
	
	@staticmethod
	def getDefaultGeoJson():
		return DefaultData.__geojson

class DataGetter:
	__path = os.path.dirname(os.path.dirname(__file__))+"\\uploads\\remaster.json"
	__maintable = ""
	__regions = []
	__questions = []
	__temp = ""

	def __init__(self,request):
		self.__maintable = pd.read_json(self.__path,orient="split")
		self.__questions = request['selectedQuestions']
		self.__regions = request['selectedRegions']
	
	def _findData(self,ques,reg=""):
		temp = self.__maintable.copy()
		if(reg != ""):
			temp = temp[temp['48. Где проживаете?'] == reg['region']]
		#поиск по вопросу
		mainfilter = temp.filter(like=ques) #нахождение кол-ва ответов в столбцах
		mainfilter = mainfilter.loc[:,~mainfilter.columns.duplicated()] #убираем дубликаты
		if("//" not in mainfilter.columns[0]):#проверка на множественный вопрос
			restable = pd.DataFrame(
				mainfilter
				.replace(to_replace=r'Другое:.*', value='Другое', regex=True)
				.value_counts(dropna=True).to_frame()) #обработка вопросов с единственный столбцом ответов
			#replace - замена по регулярному выражению
			restable = restable.reset_index()
			restable.columns = ['name','data'] #именование в зависимости от требований графики для единичного вопроса
			name = restable['name'].to_list()
			data = restable['data'].to_list()
		else: #обработка вопросов с несколькими столбцами ответов
			restable = pd.DataFrame()
			for i in mainfilter.columns:
				jj = mainfilter.filter(like=i)
				if(jj.iloc[0][0]== 0 or pd.isna(jj.iloc[0][0]) or jj.iloc[0][0]==1):
					restable1 = pd.DataFrame(jj
					.replace(to_replace=r'[^0].*', value="1.0", regex=True)
					.value_counts(dropna=True).sort_index(ascending=False).to_frame()) #dropna=True если надо убирать пустые значения
				else:
					restable1 = pd.DataFrame(jj.value_counts(dropna=True).sort_index(ascending=False).to_frame())
				restable1 = restable1.reset_index()
				if(restable1.iat[0,0] == 0):
					restable1 = pd.DataFrame({
						'name': [1.0],
						'column':[0]
					})
				restable1.columns = ['values',i[i.find("//")+3:]]
				#print(restable1)
				restable = pd.concat([restable,restable1],axis=1)
				restable = restable.loc[:,~restable.columns.duplicated()]
				name = restable.columns.to_list()
				name.pop(0)
				data = []
				print(restable)
				if(restable.to_numpy()[0][0] == 1):
					data = pd.Series(restable.loc[restable["values"].values == 1.0].to_numpy()[0]).to_list()
					data.pop(0)
				else: 
					data = [0]
		mydict = {
			"labels":name,
			"data":data
		}
		return mydict
	
	def getData(self):
		answer = []
		tempdict = dict()
		for ques in self.__questions:
			tempdict['question'] = ques
			tempregdata = []
			for reg in self.__regions:
				tempregdict = dict()
				if(reg['region'] == 'Вся область'):
					tempregdict['name'] = 'Вся область'
					regdata = self._findData(ques)
				else:
					tempregdict['name'] = reg['region']
					regdata = self._findData(ques,reg)
				tempregdict['labels'] = regdata['labels']
				tempregdict['data'] = regdata['data']
				tempregdata.append(tempregdict)
				tempregdict = dict()
			tempdict['regions']=tempregdata
			answer.append(tempdict)
			tempdict = dict()
		return json.dumps(answer,indent=4,ensure_ascii=False)
	
	



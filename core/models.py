import pandas as pd
import re
import os
from werkzeug.utils import secure_filename
from core.config import BaseConfig
import geopandas as gpd
import json
from flask import jsonify

class DBUpload:
	def __init__(self, request):
		self.request = request
		self.file = request.files['file']
		self.filename = secure_filename(self.file.filename)

	def saveFile(self,sessionid):
		try:
			if(self.request.method == 'POST'):
				if self.file and self.allowed_file(self.filename):
					temp = pd.read_excel(self.file, header=0)
					with open(os.path.join(BaseConfig.UPLOAD_FOLDER, sessionid+'.json'), 'w') as f: 
						f.write(temp.to_json(orient="split"))
					self.filename = os.path.join(BaseConfig.UPLOAD_FOLDER, sessionid+'.json')
		except BaseException as e:
				print(e)

	def getQuestions(self):
		maintable = pd.read_json(self.filename,orient="split")
		queslist = list(maintable)
		for i in range(0,len(queslist)):
			queslist[i] = re.sub(r'(\s\/\/\s.*)','',queslist[i])
		queslist = sorted(set(queslist), key=lambda d: queslist.index(d))
		queslist.pop(queslist.index("Где проживаете?"))
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
	"Куменский район",
	"г. Котельнич",
	"Орловский район",
	"Даровской район",
	"Верхошижемский район",
	"Верхнекамский район",
	"Афанасьевский район",
	"г. Киров",
	"Юрьянский район",
	"Белохолуницкий район",
	"Котельничский район",
	"Арбажский район",
	"Тужинский район",
	"г. Вятские Поляны",
	"г. Кирово-Чепецк",
	"г. Слободской",
	"Советский район",
	"Омутнинский район",
	"Унинский район",
	"Богородский район",
	"Зуевский район",
	"Фаленский район",
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
	__path = os.path.dirname(os.path.dirname(__file__))+"/uploads/default.json"
	__geojson = gpd.read_file(os.path.dirname(os.path.dirname(__file__))+"/static/regions.geojson", encoding="utf-8")
	__maintable = pd.read_json(__path,orient="split")
	
	@staticmethod
	def getDefaultQues(sessionid="none"):
		if(os.path.exists(os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json")):
			DefaultData.__maintable = pd.read_json(os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json",orient="split")
			DefaultData.__path = os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json"
		else:
			DefaultData.__maintable = pd.read_json(DefaultData.__path,orient="split")
		maintable = DefaultData.__maintable
		queslist = list(maintable)
		for i in range(0,len(queslist)):
			queslist[i] = re.sub(r'(\s\/\/\s.*)','',queslist[i])
		queslist = sorted(set(queslist), key=lambda d: queslist.index(d))
		queslist.pop(queslist.index("Где проживаете?"))
		return jsonify(queslist)

	@staticmethod
	def getDefaultReg():
		return jsonify(DefaultData.__regions)
	
	@staticmethod
	def getDefaultGeoJson():
		return jsonify(DefaultData.__geojson.to_json())

class DataGetter:
	__path = os.path.dirname(os.path.dirname(__file__))+"/uploads/default.json"
	__maintable = ""

	def __init__(self,sessionid="none"):
		if(os.path.exists(os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json")):
			self.__maintable = pd.read_json(os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json",orient="split")
			self.__path = os.path.dirname(os.path.dirname(__file__))+"/uploads/"+sessionid+".json"
		else:
			self.__maintable = pd.read_json(self.__path,orient="split")
	
	def _findData(self,ques,reg=""):
		temp = self.__maintable.copy()
		if(reg != ""):
			temp = temp[temp['Где проживаете?'] == reg['region']]#фильтрация по району
		mainfilter = temp.filter(like=ques) #поиск по вопросу
		mainfilter = mainfilter.loc[:,~mainfilter.columns.duplicated()] #убираем дубликаты
		if("//" not in mainfilter.columns[0]):#проверка на множественный вопрос
			#обработка вопросов с единственный столбцом ответов
			restable = pd.DataFrame(
				mainfilter
				.replace(to_replace=r'Другое:.*', value='Другое', regex=True)#replace - замена по регулярному выражению
				.value_counts(dropna=True).to_frame())#value_counts - подсчет количества непустых значений
			if(not restable.empty): #проверка полученной таблицы на наличие данных
				restable = restable.reset_index()
				restable.columns = ['name','data'] #именование в зависимости от требований графики для единичного вопроса
				name = restable['name'].to_list()
				data = restable['data'].to_list()
			else:
				name = ["Нет данных"]
				data = [0]
		else: 
			#обработка вопросов с несколькими столбцами ответов
			name = []
			restable = pd.DataFrame()
			for i in mainfilter.columns: #проход по всем столбцам
				tempcolumn = mainfilter.filter(like=i) #преобразование каждого столбца в отдельную таблицу
				if(not tempcolumn.empty): #проверка на пустоту
					restable1 = pd.DataFrame(tempcolumn
					.replace(to_replace=r'[^0].*', value="1.0", regex=True)
					.value_counts(dropna=True).sort_index(ascending=False).to_frame())
					if( not restable1.empty):
						restable1 = restable1.reset_index()
						if(restable1.iat[0,0] == 0):
							restable1 = pd.DataFrame({
								'name': [1.0],
								'column':[0]
							})
						restable1.columns = ['values',i[i.find("//")+3:]]
						restable = pd.concat([restable,restable1],axis=1)
						restable = restable.loc[:,~restable.columns.duplicated()]
						name = restable.columns.to_list()
						name.pop(0)
						data = []
						if(restable.to_numpy()[0][0] == 1):
							data = pd.Series(restable.loc[restable["values"].values == 1.0].to_numpy()[0]).to_list()
							data.pop(0)
						else: 
							data = [0]
					else:
						if(len(name)== 0):
							name = ["Нет данных"]
							data = [0]
				else:
					if(len(name)== 0):
						name = ["Нет данных"]
						data = [0]
		mydict = {
			"labels":name,
			"data":data
		}
		return mydict
	
	def getData(self,request):
		questions = request['selectedQuestions']
		regions = request['selectedRegions']
		answer = dict()
		tempdata = dict()
		for reg in regions:
			tempregdict = dict()
			if(reg['region'] == 'Вся область'):
				regdata = self._findData(questions[-1])
			else:
				regdata = self._findData(questions[-1],reg)
			tempregdict['labels'] = regdata['labels']
			tempregdict['data'] = regdata['data']
			tempdata[reg['region']] = tempregdict
			tempregdict = dict()
		answer[questions[-1]]=tempdata
		jsondata = json.dumps(tempdata,indent=0,ensure_ascii=True,sort_keys=False)
		return jsondata

	def getCritData(self,request):
		questions = request['selectedQuestions']
		regions = request['selectedRegions']
		data = dict()
		for reg in regions:
			if(reg['region'] == 'Вся область'):
				continue
			temp = self.__maintable.copy()
			temp = temp[temp['Где проживаете?'] == reg['region']]
			fullcount = len(temp)
			if(fullcount == 0):
				data[reg['region']] = 0
				continue
			for element in questions:
				mainfilter = temp.filter(like=element) #нахождение кол-ва ответов в столбцах
				mainfilter = mainfilter.loc[:,~mainfilter.columns.duplicated()]
				if("//" not in mainfilter.columns[0]):
					temp = temp[temp[element].isin(questions[element])]
				else:
					for i in questions[element]:
						temp = temp[temp[element+" // "+i] == 1]
			data[reg['region']] = round((len(temp)/fullcount)*100)
		jsondata = json.dumps(data,indent=0,ensure_ascii=True,sort_keys=False)
		return jsondata

	# def getSelectedData(self):
	# 	answer = []
	# 	tempdict = dict()
	# 	for ques in self.__questions:
	# 		tempdict['question'] = ques
	# 		tempregdata = []
	# 		for reg in self.__regions:
	# 			tempregdict = dict()
	# 			if(reg['region'] == 'Вся область'):
	# 				tempregdict['name'] = 'Вся область'
	# 				regdata = self._findData(ques)
	# 			else:
	# 				tempregdict['name'] = reg['region']
	# 				regdata = self._findData(ques,reg)
	# 			tempregdict['labels'] = regdata['labels']
	# 			tempregdict['data'] = regdata['data']
	# 			tempregdata.append(tempregdict)
	# 			tempregdict = dict()
	# 		tempdict['regions']=tempregdata
	# 		answer.append(tempdict)
	# 		tempdict = dict()
	# 		return json.dumps(answer,indent=4,ensure_ascii=False)
	

	

	
	



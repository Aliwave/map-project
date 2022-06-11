from flask import Flask, jsonify, request, session, render_template
from flask_cors import CORS
from flask_session import Session
from core.models import DBUpload, DefaultData, DataGetter


app = Flask(__name__,
						static_folder="./dist/static",
						template_folder="./dist")
app.config.from_object('core.config.BaseConfig')
Session(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/uploaddb', methods=['POST'])
def upload_file():
	file = DBUpload(request)
	filename = file.saveFile(session.sid)
	queslist = file.getQuestions()
	return jsonify({"queslist":queslist})

@app.route('/api/geojson', methods=['GET'])
def getGeojson():
	return DefaultData.getDefaultGeoJson()

@app.route('/api/regions', methods=['GET'])
def getReglist():
	return DefaultData.getDefaultReg()

@app.route('/api/questions', methods=['GET'])
def getQuestions():
	return DefaultData.getDefaultQues(session.sid)

@app.route('/api/data', methods=['POST'])
def getData():
	requestdata = request.get_json()
	data = DataGetter(session.sid)
	return data.getData(requestdata)

@app.route('/api/dataCrit', methods=['POST'])
def getCritData():
	requestdata = request.get_json()
	data = DataGetter(session.sid)
	return data.getCritData(requestdata)
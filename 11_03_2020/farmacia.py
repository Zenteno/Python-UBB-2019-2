import requests
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
	url = "https://farmanet.minsal.cl/index.php/ws/getLocales"
	r  =  requests.get(url)
	diccionario = {}
	for objeto in r.json():
		llave_region = f"region_{objeto['fk_region']}" 
		if llave_region not in diccionario:
			diccionario[llave_region] = []
		if objeto["comuna_nombre"] not in diccionario[llave_region]:
			diccionario[llave_region].append(objeto["comuna_nombre"])
	return render_template('plantilla.html', regiones=diccionario)

@app.route('/farmaciasJson')
def farmacias_json():
	url = "https://farmanet.minsal.cl/index.php/ws/getLocales"
	r  =  requests.get(url)
	return jsonify(r.json())


@app.route('/farmacias')
def farmacias():
	url = "https://farmanet.minsal.cl/index.php/ws/getLocales"
	r  =  requests.get(url)
	ciudad = request.args.get('ciudad', default = "", type = str)
	farmacia = request.args.get('farmacia', default = "", type = str)
	farmacias_ = r.json()
	
	if ciudad!="":
		farmacias_ = [f for f in farmacias_ if f["comuna_nombre"].upper()==ciudad.upper()]
		#farmacias_ = filter(lambda x: x["comuna_nombre"].upper()==ciudad.upper(), farmacias_)
	if farmacia!="":
		farmacias_ = [f for f in farmacias_ if f["local_nombre"].upper()==farmacia.upper()]
		#farmacias_ = filter(lambda x: x["local_nombre"].upper()==farmacia.upper(), farmacias_)
	return render_template("farmacias.html",farmacies = farmacias_)

if __name__ == "__main__":
	app.run(debug=True)
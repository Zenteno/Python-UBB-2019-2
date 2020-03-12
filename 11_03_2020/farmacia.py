import requests
import json
from flask import Flask, render_template, jsonify

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
	return render_template("farmacias.html",farmacies = r.json())

if __name__ == "__main__":
	app.run(debug=True)
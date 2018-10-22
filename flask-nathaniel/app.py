from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('main.html')

@app.route('/locations')
def locations_page():
	return "Location Data Here"

@app.route('/PMIdata')
def pmi_page():
	return "PMI Data Here"
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('main.html')

@app.route('/locations')
def locations_page():
	return render_template('locations.html')

@app.route('/PMIdata')
def pmi_page():
	return render_template('PMIdata.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
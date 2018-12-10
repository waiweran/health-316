import sys
from flask import Flask, render_template, request
import map_plot as plot
import psycopg2
import hashlib
import database as db

app = Flask(__name__)

plots = dict()

@app.route('/top_diseases')
def top_diseases():
    tt = db.getPopular()
    tt = tt[:10]
    tod = db.getPopularToday()
    tod = tod[:10]
    tt = [val[0] + ": " + str(val[1]) + " searches" for val in tt]
    return render_template('top_diseases.html', topten = tt, today = tod)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/locations')
def conditions_page():
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute("SELECT condition_name.name FROM condition_name")
    return render_template('conditionlist.html', condition_name = c)
    conn.commit()
    c.close()
    conn.close()

@app.route('/locations/<condition_name>', methods=['GET', 'POST'])
def locations_page(condition_name):
    Gender='None'
    Race='None'
    if request.method == 'POST':  # this block is only entered when the form is submitted
        AgeRange = request.form.get('AgeRange')
        Gender = request.form.get('gender')
        Race = request.form.get('race')
    db.updateHistory(condition_name)
    datatypes = db.getDataTypes(condition_name)
    y = db.getDataYears(condition_name, datatypes[0])
    g = db.getDataGenders(condition_name, datatypes[0])
    r = db.getDataRaces(condition_name, datatypes[0])
    if Gender == 'None':
        Gender = g[0]
    if Race == 'None':
        Race = r[0]
    locations, values = db.getMapData(condition_name, datatypes[0], y[0], gender=Gender, race_ethnicity=Race)
    plot_html = plot.make_states_plot(locations, values, locations, datatypes[0], condition_name)
    plot_link = hashlib.md5(plot_html.encode()).hexdigest()
    plots[plot_link] = plot_html
    return render_template('locations.html', plot_link = plot_link, condition_name = condition_name, genders = g, races=r)

@app.route('/PMIdata')
def pmi_page():
    return render_template('PMIdata.html')

@app.route('/map_function/<plot_id>')
def map_function(plot_id):
    return plots[plot_id]

if __name__ == "__main__":
    app.run(host='0.0.0.0')

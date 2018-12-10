import sys
from flask import Flask, render_template, request
import map_plot as plot
import psycopg2
import hashlib
import database as db

app = Flask(__name__)

plots = dict()

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/top_diseases')
def top_diseases():
    tt = db.getPopular()
    tt = tt[:10]
    tt = [val[0] + ": " + str(val[1]) + " searches" for val in tt]
    return render_template('top_diseases.html', topten = tt)

@app.route('/blog_form')
def blog_form():
    return render_template('blog_form.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

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

@app.route('/locations/<condition_name>')
def locations_page(condition_name):
    db.updateHistory(condition_name)
    datatypes = db.getDataTypes(condition_name)
    y = db.getDataYears(condition_name, datatypes[0])
    g = db.getDataGenders(condition_name,datatypes[0])
    r = db.getDataRaces(condition_name,datatypes[0])
    locations, values = db.getMapData(condition_name, datatypes[0], y[0])
    plot_html = plot.make_states_plot(locations, values, locations, 'Scale', 'Plot')
    plot_link = hashlib.md5(plot_html.encode()).hexdigest()
    plots[plot_link] = plot_html

    return render_template('locations.html', plot_link = plot_link, genders = g, races=r)

@app.route('/PMIdata')
def pmi_page():
    return render_template('PMIdata.html')

@app.route('/map_function/<plot_id>')
def map_function(plot_id):
    return plots[plot_id]

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():

    if request.method == 'GET':  # this block is only entered when the form is submitted
        conditionName = request.form.get('conditionName', 'None')
    Agerange = request.form.get('AgeRange')

    return '''<h1> The condition name you entered is: **{}**. Your selected GDP value is **{}**. Your selected AI value is **{}**. Your selected Pop value is **{}**.  {} people died in the US in 2016 from your disease'''.format(conditionName, GDPrange, AIrange, Poprange, mortality)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

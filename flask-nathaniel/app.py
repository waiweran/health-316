import sys
sys.path.append("..")
from flask import Flask, render_template, request
from utilities import map_plot as plot
import psycopg2
import database as db

app = Flask(__name__)


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
    datatypes = db.getDataTypes(condition_name)
    print("Data Types: " + str(datatypes))
    return render_template('locations.html')

@app.route('/PMIdata')
def pmi_page():
    return render_template('PMIdata.html')

@app.route('/mapfunction')
def map_function():
    return plot.make_states_plot(["NC", "SC"], [2, 3], ["A", "B"], "Hi", "Lo")

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():

    if request.method == 'GET':  # this block is only entered when the form is submitted
        conditionName = request.form.get('conditionName', 'None')
    Agerange = request.form.get('AgeRange')

    return '''<h1> The condition name you entered is: **{}**. Your selected GDP value is **{}**. Your selected AI value is **{}**. Your selected Pop value is **{}**.  {} people died in the US in 2016 from your disease'''.format(conditionName, GDPrange, AIrange, Poprange, mortality)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

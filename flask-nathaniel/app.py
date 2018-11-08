from flask import Flask, render_template, request

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


@app.route('/process_data', methods=['GET', 'POST'])
def process_data():

    if request.method == 'POST':  # this block is only entered when the form is submitted
        conditionName = request.form.get('conditionName', 'None')
    GDPrange = request.form.get('GDPrange')
    AIrange = request.form.get('AIrange')
    Poprange = request.form.get('Poprange')
    return '''<h1> The condition name you entered is: **{}**. Your selected GDP value is **{}**. Your selected AI value is **{}**. Your selected Pop value is **{}**'''.format(conditionName, GDPrange, AIrange, Poprange)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

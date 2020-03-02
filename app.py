from flask import Flask, render_template, redirect, url_for, request
from forms import RecordForm
from records import Record
import os
import uuid
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['CSRF_ENABLED'] = True

RECORDS = []

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', data=RECORDS)

@app.route('/add', methods=('GET', 'POST'))
def add():
    form = RecordForm()
    if form.validate_on_submit():
        record = Record()
        record.id = uuid.uuid4()
        record.value = request.form['value']
        record.timestamp = datetime.now()
        RECORDS.append(record)
        return redirect(url_for('home'))
    return render_template('add.html', form=form)
    
@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    index = 0
    for i, j in enumerate(RECORDS):
        if j.id == id:
            index = i
            break
    RECORDS.pop(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

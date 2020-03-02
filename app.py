from flask import Flask, render_template, redirect, url_for, request
from forms import RecordForm
from records import Record
import os
import uuid
from datetime import datetime
import numpy as np
from scipy.stats import shapiro
from statsmodels.tsa.stattools import adfuller

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['CSRF_ENABLED'] = True

RECORDS = []

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', data=RECORDS)

@app.route('/add', methods=['GET', 'POST'])
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

@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    index = 0
    for i, j in enumerate(RECORDS):
        if str(j.id) == id:
            index = i
            break
    RECORDS.pop(index)
    return redirect(url_for('home'))

@app.route('/retrieve/<string:id>', methods=['GET', 'POST'])
def retrieve(id):
    record = None
    for item in RECORDS:
        if str(item.id) == id:
            record = item
            break
    return render_template('retrieve.html', id=id, data=record)

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    form = RecordForm()
    if form.validate_on_submit():
        for item in RECORDS:
            if str(item.id) == id:
                item.value = request.form['value']
                item.timestamp = datetime.now()
                break
        return redirect(url_for('home'))
    return render_template('edit.html', id=id, form=form)

@app.route('/statistics', methods=['GET'])
def statistics():
    count = len(RECORDS)
    records = []
    for item in RECORDS:
        records.append(item.value)
    records = np.array(records).astype(np.float)
    print(records)
    mean = np.mean(records)
    variance = np.var(records)
    if len(records) > 2:
        is_gaussian_shapiro = shapiro_test(records)
        confidence_interval = confidence_interval_95(mean, np.std(records), count)
    else:
        is_gaussian_shapiro = False
        confidence_interval = None
    if len(records) > 29:
        stationarity = ADF_test(records)
    else:
        stationarity = False
    return render_template('statistics.html', count=count, mean=mean, variance=variance,\
                           is_gaussian=is_gaussian_shapiro, confidence_interval=confidence_interval,\
                           statoinarity=stationarity)

def shapiro_test(array):
    _, p = shapiro(array)
    alpha = 0.05
    if p > alpha:
        return True
    else:
        return False

def confidence_interval_95(mean, sd, count):
    interval = []
    se = sd / np.sqrt(count)
    lower = mean - 1.96 * se
    upper = mean + 1.96 * se
    interval.append(lower)
    interval.append(upper)
    return interval

def ADF_test(array):
    adfTest = adfuller(array, autolag='AIC')
    if adfTest[1] < 0.05:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)

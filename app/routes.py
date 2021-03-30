from app import app
from flask import render_template
import os

@app.route('/')
@app.route('/home')
def home():
    title='Welcome'

    return render_template("index.html", title=title)

@app.route('/index')
def index():

    return render_template('index.html', message="Changing Data")

@app.route('/query_results')
def query_results():
    
    results = {}

    make = 'ford'

    return render_template('query_results.html',make=make)
   


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import yaml, os
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'deez nuts'

# DB configs
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

#main route
@app.route('/')
def homepage():
    return render_template('homepage.html')

#sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer_login WHERE email = %s', (email,))
        customer_login = cursor.fetchone()
        if customer_login:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not email or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO customer_login VALUES (NULL, %s, %s)', (password, email))
            mysql.connection.commit()
            msg = "You have successfully registered!"
    elif request.method == 'POST':
        msg = 'Please fill the form!'
    return render_template('SignUp.html', msg = msg)

#login
@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM customer_login WHERE email = %s AND password = %s', (email, password,))
        customer_login = cur.fetchone()
        if customer_login:
            session['loggedin'] = True
            session['id'] = customer_login['id']
            session['email'] = customer_login['email']
            return render_template('homepageLoggedIn.html')
        else:
            msg = 'Wrong email/password'
    return render_template('LogIn.html', msg=msg)

@app.route('/homepageloggedIn')
def homepagelogged():
    return render_template('homepageLoggedIn.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('LogIn'))

#contact
@app.route('/contact')
def contact():
    return render_template('homepageLoggedIn.html.html')

#about
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

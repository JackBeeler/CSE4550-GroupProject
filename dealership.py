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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
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
            cursor.execute('INSERT INTO customer_login VALUES (NULL, %s, %s, %s)', (email, password, email))
            mysql.connection.commit()
            msg = "You have successfully registered!"
    elif request.method == 'POST':
        msg = 'Please fill the form!'
    return render_template('SignUp.html', msg = msg)

#login
@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM customer_login WHERE username = %s AND password = %s', (username, password,))
        customer_login = cur.fetchone()
        if customer_login:
            session['loggedin'] = True
            session['customer_id'] = customer_login['customer_id']
            session['username'] = customer_login['username']
            msg = 'Success'
            return render_template('homepageLoggedIn.html', msg = msg)
       // else:
            //msg = 'Wrong username/password'
    //return render_template('LogIn.html', msg=msg)


//@app.route('/employeelogin', methods=['GET', 'POST'])
//def employeelogin():
    //msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM employee_login WHERE username = %s and password = %s', (username, password,))
        employeelogin = cur.fetchone()
        if employeelogin:
            session['loggedin'] = True
            session['employee_id'] = employeelogin['employee_id']
            session['username'] = employeelogin['username']
            return redirect(url_for('homepagelogged'))
        else: 
            msg = "Wrong username/password"
    return render_template('login.html', msg=msg)


@app.route('/homepageloggedIn')
def homepagelogged():
    return render_template('homepageLoggedIn.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('customer_id', None)
    session.pop('username', None)   
    return redirect(url_for('login'))

#contact
@app.route('/contact')
def contact():
    return render_template('Contact Us.html')

#about
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/searchresults')
def searchresults():
    return render_template('SearchResults.html')

@app.route('/vehiclelisting')
def vehiclelisting():
    return render_template('VehicleListing.html')


if __name__ == '__main__':
    
    app.run(debug=True)

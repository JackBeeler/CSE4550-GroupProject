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
    if 'username' in session:
        username2 = session['username']
        return render_template('homepageLoggedIn.html', homepageusername = username2)
    else:
        return render_template('homepage.html')

#sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
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
            cursor.execute('INSERT INTO customer_login VALUES (NULL, %s, %s, %s)', (email, password, username))
            cursor.execute('INSERT INTO customer (customer_photo) VALUES (default)')
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
        else:
            # Check if the person is an employee trying to log in
           # msg = 'Wrong username/password'
           cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute('SELECT * FROM employee_login WHERE username = %s and password = %s', (username, password,))
        employeelogin = cur1.fetchone()
        if employeelogin:
            session['loggedin'] = True
            session['employee_id'] = employeelogin['employee_id']
            session['username'] = employeelogin['username']
            return redirect(url_for('homepagelogged'))
        else: 
            msg = "Wrong username/password"
    return render_template('LogIn.html', msg=msg)




@app.route('/homepageloggedIn')
def homepagelogged():
    if 'username' in session:  
        username1 = session['username']  
    
    
    return render_template('homepageLoggedIn.html', homepageusername = username1)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('customer_id', None)
    session.pop('username', None)   
    return redirect(url_for('login'))

#contact
@app.route('/contact')
def contact():
    if 'username' in session:
        username3 = session['username']
        return render_template('Contact Us.html',homepageusername = username3)    
    else:
        return render_template('Contact Us.html')
    

#about
@app.route('/about')
def about():
    if 'username' in session:  
        username4 = session['username']
        return render_template('about.html', homepageusername = username4)
    else:
        return render_template('about.html')
        
        
@app.route('/hatchbacks')
def searchresultshatchbacks():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE body_style = "hatchback"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)   
        
@app.route('/sedans')
def searchresultsedan():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE body_style = "sedan"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)   
    
    
@app.route('/convertables')
def searchresultsconvertable():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE body_style = "convertable"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    @app.route('/coupes')
def searchresultscoupe():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE body_style = "coupe"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
        
@app.route('/searchresults')
def searchresults():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
     
    

@app.route('/vehiclelisting')
def vehiclelisting():
    if 'username' in session:  
        username6 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username6)
    else:
        return render_template('VehicleListing.html')
            
     
    

@app.route('/favorites')
def favorites():
     if 'username' in session:  
        username6 = session['username'] 
        return render_template('favorites.html',homepageusername = username6)
     else:
        return render_template('SignUp.html')
     


if __name__ == '__main__':
    
    app.run(debug=True)

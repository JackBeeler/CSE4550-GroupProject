from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import yaml, os
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = '1234'

# DB configs
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)



#main route
@app.route('/', methods=['GET', 'POST'])
def homepage():
     
     if 'username'  in session:
         username2 = session['username']
     
         if request.method == 'POST' and 'search' in request.form:
          Search = request.form['search']
          cursor = mysql.connection.cursor()
          cursor.execute('SELECT * FROM inventory WHERE make like %s OR model like %s OR color like %s OR year like %s', (Search, Search, Search, Search,))
          data1= cursor.fetchall()
          numRows = cursor.rowcount
          
          if data1:
               return render_template('SearchResults.html', data = data1, numRows=numRows, homepageusername = username2)
     else:
          if request.method == 'POST' and 'search' in request.form:
           Search = request.form['search']
           cursor = mysql.connection.cursor()
           cursor.execute('SELECT * FROM inventory WHERE make like %s OR model like %s OR color like %s OR year like %s', (Search, Search, Search, Search,))
           data1= cursor.fetchall()
           numRows = cursor.rowcount
          
          
           if data1:
               return render_template('SearchResults.html', data = data1, numRows=numRows)
    
     
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
            session['isUser'] = 'true'
            msg = 'Success'
            return redirect(url_for('homepagelogged', msg=msg,))
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
             session['isEmployee'] = 'true'
             
             return redirect(url_for('homepagelogged', msg=msg,))
            else: 
             msg = "Wrong username/password"
    return render_template('LogIn.html', msg=msg)




@app.route('/homepageloggedIn', methods=['GET','POST'])
def homepagelogged():
   if 'username'  in session:
         username2 = session['username']
         if request.method == 'POST' and 'search' in request.form:
               Search = request.form['search']
               cursor = mysql.connection.cursor()
               cursor.execute('SELECT * FROM inventory WHERE make like %s OR model like %s OR color like %s OR year like %s', (Search, Search, Search, Search,))
               data1= cursor.fetchall()
               numRows = cursor.rowcount
               if data1:
                    return render_template('SearchResults.html',  data=data1, numRows=numRows, homepageusername = username2 )
    
     
   if 'username' in session:
         username2 = session['username']
         return render_template('homepageLoggedIn.html', homepageusername = username2)
   else:
         return render_template('homepage.html')



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
        
 #BELOW THIS LIME IS THE LINKING TO EACH VEHICLE'S INDIVIDUAL LISTING PAGE 

@app.route('/1000001')
def searchresults1000001():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000001"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        if session['isUser'] == 'True':
          return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
        elif session['isEmployee'] == 'True':
          return render_template('employeeVehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)
     
     
@app.route('/1000002')
def searchresults1000002():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000002"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)     
     
@app.route('/1000003')
def searchresults1000003():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000003"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)
     
@app.route('/1000004')
def searchresults1000004():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000004"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000005')
def searchresults1000005():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000005"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000006')
def searchresults1000006():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000006"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000007')
def searchresults1000007():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000007"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000008')
def searchresults1000008():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000008"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000009')
def searchresults1000009():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000009"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000010')
def searchresults1000010():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000010"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000011')
def searchresults1000011():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000011"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000012')
def searchresults1000012():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000012"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000013')
def searchresults1000013():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000013"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000014')
def searchresults1000014():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000014"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000015')
def searchresults1000015():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000015"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000016')
def searchresults1000016():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000016"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000017')
def searchresults1000017():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000017"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000018')
def searchresults1000018():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000018"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000019')
def searchresults1000019():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000019"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000020')
def searchresults1000020():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000020"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000021')
def searchresults1000021():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000021"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000022')
def searchresults1000022():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000022"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000023')
def searchresults1000023():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000023"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000024')
def searchresults1000024():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000024"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000025')
def searchresults1000025():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000025"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000026')
def searchresults1000026():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000026"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000027')
def searchresults1000027():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000027"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000028')
def searchresults1000028():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000028"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

@app.route('/1000029')
def searchresults1000029():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000029"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)


@app.route('/1000030')
def searchresults1000030():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE vin = "1000030"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('VehicleListing.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('VehicleListing.html', data=data, numRows=numRows)

     
#ABOVE THIS LINE IS THE LINKING TO EACH VECHICLE'S INDIVIDUAL LISTING PAGE     
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
    
    
@app.route('/nissans')
def searchresultsnissans():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "nissan"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
@app.route('/kia')
def searchresultskia():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "kia"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    
@app.route('/honda')
def searchresultshonda():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "honda"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
@app.route('/volkswagon')
def searchresultsvolkswagon():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "volkswagen"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
   
@app.route('/chevrolet')
def searchresultschevrolet():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "chevrolet"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)

    
    
@app.route('/toyota')
def searchresultstoyota():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "toyota"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    
@app.route('/ford')
def searchresultsford():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "ford"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    
@app.route('/sentra')
def searchresultssentra():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "sentra"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
    
@app.route('/optima')
def searchresultsoptima():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "optima"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    
@app.route('/crz')
def searchresultscrz():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "crz"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
@app.route('/accord')
def searchresultsaccord():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "accord"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)     
    
    
@app.route('/jetta')
def searchresultsjetta():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "jetta"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)     
    
    
   
@app.route('/auris')
def searchresultsauris():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "auris"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows) 
    
    
    
@app.route('/beetle')
def searchresultsbeetle():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "beetle"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows) 
    
    
    
@app.route('/corolla')
def searchresultscorolla():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "corolla"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)   
    
    
@app.route('/malibu')
def searchresultsmalibu():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "malibu"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)     
    
    
    
@app.route('/civic')
def searchresultscivic():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "civic"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
    
@app.route('/taurus')
def searchresultstaurus():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "taurus"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
@app.route('/mustang')
def searchresultsmustang():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "mustang"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
@app.route('/cruze')
def searchresultscruze():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "cruze"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
@app.route('/volt')
def searchresultsvolt():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "volt"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
@app.route('/fiesta')
def searchresultsfiesta():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "fiesta"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
    
@app.route('/focus')
def searchresultsfocus():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "focus"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
    
@app.route('/soul')
def searchresultssoul():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "soul"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
    
@app.route('/juke')
def searchresultsjuke():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "juke"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/aventador')
def searchresultsaventador():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "aventador"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
@app.route('/yaris')
def searchresultsyaris():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "yaris"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
  
    
    
@app.route('/prius')
def searchresultsprius():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "prius"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)  
    
    
    
@app.route('/camry')
def searchresultscamry():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE model = "camry"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)       
    
    
    
@app.route('/lamborghini')
def searchresultslamborghini():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE make = "lamborghini"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
    
    
@app.route('/price8000')
def searchresultsprice8000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE our_price < 8000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)  
    
    
@app.route('/price15000')
def searchresultsprice15000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE our_price < 15000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)        
    
    
@app.route('/price20000')
def searchresultsprice20000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE our_price < 20000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/price25000')
def searchresultsprice25000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE our_price < 25000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/black')
def searchresultsblack():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "black"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
@app.route('/blue')
def searchresultsblue():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "blue"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)
    
    
@app.route('/grey')
def searchresultsgrey():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "grey"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/silver')
def searchresultssilver():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "silver"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/white')
def searchresultswhite():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "white"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/green')
def searchresultsgreen():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "green"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/red')
def searchresultsred():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE color = "red"')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
    
@app.route('/miles35000')
def searchresultsmiles35000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE mileage < 35000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)   
    
    
    
@app.route('/miles40000')
def searchresultsmiles40000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE mileage < 65000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
    
    
@app.route('/miles50000')
def searchresultsmiles50000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE mileage < 50000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
                       
                   
              
@app.route('/miles65000')
def searchresultsmiles65000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE mileage < 65000')
    data = cursor.fetchall()
    numRows = cursor.rowcount

    if 'username' in session:  
        username5 = session['username'] 
        return render_template('SearchResults.html',homepageusername = username5, data=data, numRows=numRows)
    else:
        return render_template('SearchResults.html', data=data, numRows=numRows)    
                       
                   
@app.route('/miles75000')
def searchresultsmiles75000():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory  WHERE mileage < 75000')
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
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM customer_login WHERE username = %s', (username6,))
        customer_login = cur.fetchone()
        if customer_login:
            CustomerID = customer_login['customer_id']
            msg = ''
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM jackfavorites WHERE id = %s ', (CustomerID,))
            data = cursor.fetchall()
            if data:
               numRows = cursor.rowcount
               return  render_template('favorites.html',homepageusername = username6, msg = msg, data=data, numRows = numRows)
            else: 
               msg = "You have no favorites"
               return render_template('favorites.html',homepageusername = username6, msg = msg, data=data, numRows=0)
                    
        else:
            # Check if the person is an employee EMPLOYEEE FAVORITES THEN NEEDS TO HAVE POST TO EDII/ADD VEHICLES ALSO
            cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur1.execute('SELECT * FROM employee_login WHERE username = %s',(username6,))
            employee_login = cur1.fetchone()
            if employee_login:
               EmployeeID = employee_login['employee_id']
               msg = ''
               cursor = mysql.connection.cursor()
               cursor.execute('SELECT * FROM jackfavorites WHERE id = %s ', (EmployeeID,))
               data = cursor.fetchall()          
               if data:
                  numRows = cursor.rowcount
                  return render_template('favorites.html',homepageusername = username6, msg = msg, data=data, numRows=numRows)
               else: 
                    msg = "You have no favorites"
                    return render_template('favorites.html',homepageusername = username6, msg = msg, data=data, numRows=0)
     
        
     else:
        return render_template('SignUp.html')








     


if __name__ == '__main__':
    
    app.run(debug=True)

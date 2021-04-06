from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml, os

app = Flask(__name__)

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
@app.route('/signup')
def signup():
    return render_template('SignUp.html')

#login
@app.route('/logIn')
def login():
    return render_template('logIn.html')

#contact
@app.route('/contact')
def contact():
    return render_template('Contact Us.html')

#about
@app.route('/about')
def about():
    return render_template('about.html')


#test route for database display
#@app.route('/users')
#def users():
#    cur = mysql.connection.cursor()
#    resultValue = cur.execute("SELECT * FROM customer")
#    if resultValue > 0:
#        customerDetails = cur.fetchall()
#        return render_template('users.html', customerDetails = customerDetails)


if __name__ == '__main__':
    app.run(debug=True)

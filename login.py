from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__, template_folder='./template')
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'skincare'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        
        # Check if the user exists in the database
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM userinfo WHERE Email=%s AND Password=%s", (Email, Password))
        user = mycursor.fetchone()  # Fetch one matching record
        
        if user:
            # Successful login, store user information in session and redirect to main page
            session['logged_in'] = True
            session['user_id'] = user[0]  # Assuming the first column is user ID
            
            # Redirect to the main page
            return redirect(url_for('home'))
        else:
            # Login failed, show an error message
            flash('Invalid Email or Password', 'danger')
            return render_template('login.html')
        
        mycursor.close()
        
    return render_template('login.html')

@app.route('/mainpage')
def home():
    if 'logged_in' in session:
        return render_template('mainpage.html')
    else:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session and log the user out
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

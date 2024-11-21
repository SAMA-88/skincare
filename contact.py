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

@app.route('/', methods=['POST' , 'GET'])
def contact():
    if request.method == 'POST':
            id = session.get('id')
            name = request.form.get('name')  
            email = request.form.get('email') 
            message = request.form.get('message') 

            
            
            mycursor = mysql.connection.cursor()
            
            mycursor.execute('INSERT INTO contactus (id,name,message,email ) VALUES (%s,%s,%s,%s)',
                                 (id,name,message,email))
            mysql.connection.commit()
            mycursor.close()
            flash('- Your Message sent successfully, Thank You', 'success')
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request 
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="./template")

# Configuring MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'skincare'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        details = request.form
        FirstName = details['FirstName']
        LastName = details['LastName']
        Phone = details['Phone']  # No space in the 'Phone' key
        Email = details['Email']
        Password = details['Password']
        Address = details['Address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO userinfo (FirstName, LastName, Phone, Email, Password, Address) VALUES (%s, %s, %s, %s, %s, %s)", (FirstName, LastName, Phone, Email, Password, Address))
        mysql.connection.commit()
        cur.close()
        return render_template("login.html")

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True, port=7000)
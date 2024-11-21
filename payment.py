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
def cart():
    if request.method == 'POST':
        CardName = request.form['CardName']
        productID = request.form.get('productID')
        CardNumber = request.form.get('CardNumber')
        expirymonth = request.form.get('expirymonth')
        expiryyear = request.form.get('expiryyear')
        CVV = request.form.get('CVV')

        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        try:
            expirymonth = int(expirymonth)
            expiryyear = int(expiryyear)
        except ValueError:
            flash('Invalid expiry date format. Please use valid numbers for month and year.', 'danger')
            return render_template('payment.html')

        # Check if the card is expired
        if (expiryyear < current_year) or (expiryyear == current_year and expirymonth < current_month):
            flash('Card has expired', 'danger')
            return render_template('payment.html')

        # Fetch product price
        cur = mysql.connection.cursor()
        cur.execute('SELECT price FROM Product WHERE productID = %s', (productID,))
        result = cur.fetchone()
        
        if result is None:
            flash('Product not found', 'danger')
            cur.close()
            return render_template('payment.html')

        product_price_db = result[0]

        Date = datetime.now()
        cur.execute('INSERT INTO order_n (customerID, order_date) VALUES (%s, %s, %s)',
                    (session['user_id'], Date))
        
        orderID = cur.lastrowid

        cur.execute('INSERT INTO payments ( orderID, Amount, Date, CardName, CardNumber, CVV) VALUES ( %s, %s, %s, %s, %s, %s)',
                    ( orderID, product_price_db, Date, CardName, CardNumber, CVV))
        mysql.connection.commit()

        payment_id = cur.lastrowid

        cur.execute('UPDATE order_n SET PaymentID = %s WHERE orderID = %s', (payment_id, orderID))
        mysql.connection.commit()

        cur.close()

        flash('Payment successful and order placed!', 'success')
        return render_template('payment.html')  

    return render_template('/payment.html')

if __name__ == '__main__':
    app.run(debug=True)

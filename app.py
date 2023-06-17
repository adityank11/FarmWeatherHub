from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'bc1b4821629db5b2b2a41084a2dd4649aa8f4aef9e4724de029397ad9a176afa'

db = mysql.connector.connect(host='localhost', database='stormfactor', user='root', password='Aditya!@#$12')
cursor = db.cursor()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/displayfarmers')
def display_farmers():
    q1 = "SELECT * FROM FARMERS"
    cursor.execute(q1)
    table_data = cursor.fetchall()
    return render_template('table.html', table_data=table_data)


@app.route('/insert', methods=['GET', 'POST'])
def farmer_registration():
    if request.method == 'POST':
        aadharID = request.form.get('aadharID')
        password = request.form.get('password')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        age = request.form.get('age')
        landid = request.form.get('landid')
        city = request.form.get('city')
        soiltype = request.form.get('soiltype')
        # Check if the aadharID is unique
        cursor.execute("SELECT aadharID FROM farmers WHERE aadharID = %s", (aadharID,))
        if cursor.fetchone() is not None:
            return "Error: Aadhar ID already exists."
        query1 = "INSERT INTO farmers (aadharID, password, phone, gender, fname, lname, age) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values1 = (aadharID, password, phone, gender, fname, lname, age)
        cursor.execute(query1, values1)
        query2 = "INSERT INTO land (landid, city, soiltype, aadharid) VALUES (%s, %s, %s, %s)"
        values2 = (landid, city, soiltype, aadharID)
        cursor.execute(query2, values2)
        db.commit()
        return "Registration successful"
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        aadharID = request.form['aadharID']
        password = request.form['password']
        cursor.execute("SELECT * FROM farmers WHERE aadharID = %s AND password = %s", (aadharID, password))
        farmer = cursor.fetchone()
        if farmer:
            session['farmer_id'] = aadharID
            cursor.execute("SELECT * FROM land WHERE aadharid = %s", (aadharID,))
            lands = cursor.fetchall()
            return render_template('profile.html', lands=lands)
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')


@app.route('/logout')
def farmer_logout():
    if 'farmer_id' in session:
        session.pop('farmer_id', None)
    return redirect(url_for('farmer_login'))


if __name__ == '__main__':
    app.run(debug=True)



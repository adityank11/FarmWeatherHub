from flask import Flask, render_template,request,redirect, url_for,session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# storm/Scripts/Activate.ps1

db = mysql.connector.connect(host='localhost',database='stormfactor',user='root',password='Aditya!@#$12')


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/displayfarmers')
def display_farmers():
    cursor = db.cursor()
    q1 = "SELECT * FROM FARMERS"
    cursor.execute(q1)
    table_data = cursor.fetchall()
    return render_template('table.html', table_data=table_data)


@app.route('/insert', methods=['GET','POST'])
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

      cursor = db.cursor()
      # Check if the aadharID is unique
      cursor.execute("SELECT aadharID FROM farmers WHERE aadharID = %s", (aadharID,))
      if cursor.fetchone() is not None:
         return "Error: Aadhar ID already exists."
      query1 = "INSERT INTO farmers (aadharID, password, phone, gender, fname, lname, age) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      values1 = (aadharID, password, phone, gender, fname, lname, age)
      cursor.execute(query1, values1)
      query2 = "INSERT INTO land (landid, city, soiltype, aadharid) VALUES (%s, %s, %s, %s)"
      values2=(landid,city, soiltype,aadharID)
      cursor.execute(query2, values2)
      db.commit()
      return "Registration successful"
   return redirect(url_for('display_farmers'))



# main driver function
if __name__ == '__main__':
    app.run(debug=True)


import logging
from flask import Flask, jsonify, request
import mysql.connector

connection = mysql.connector.connect(host ='localhost',
                                         database='Employee',
                                         user='root',
                                         password='junaid')

app = Flask(__name__)

def CreateCursor():
    return connection.cursor()

@app.route('/', methods = ['GET'])
def home():
    return jsonify ('HOME PAGE')


@app.route('/add', methods = ['POST'])
def add_record():
    """Add New Record in Database"""
    if request.method == 'POST':
        data = request.json

        EmpId = data["EmpId"]
        FirstName = data["FirstName"]
        LastName = data["LastName"]
        Address = data["Address"]
        City = data["City"]
        Pin = data["Pin"]

        qry = "INSERT INTO Details VALUES (%s,%s,%s,%s,%s,%s)"
        val = (EmpId,FirstName,LastName,Address,City,Pin)
        
        mycursor = CreateCursor()
    
        mycursor.execute(qry,val)

        connection.commit()
        return jsonify("Succesfull")

@app.route('/delete/<id>', methods = ['GET'])
def delete(id):
    """Delete Record of Specified EmpId"""
    if request.method == 'GET':
        mycursor = CreateCursor()
        
        mycursor.execute("Delete FROM Details WHERE EmpId = {}".format(id))
        connection.commit()
    return jsonify("Succecfully Deleted")

@app.route('/info/<id>', methods =['GET'])
def fetch(id):
    """Displays Employee Info of Specified EmpId"""
    if request.method == 'GET':
        mycursor = CreateCursor()
        mycursor.execute("SELECT * FROM Details WHERE EmpId ={}".format(id))
        #Fetching record and returns Tuple
        record = mycursor.fetchall()
        connection.commit()
        
        EmpId,FirstName,LastName,Address,City,Pin = record[0]
        data = {}
        data["EmpId"] = EmpId
        data["FirstName"] = FirstName
        data["LastName"] = LastName
        data["Address"] = Address
        data["City"]   = City
        data["Pin"] = Pin
        connection.commit()

        return data


if __name__=='__main__':
  app.run(debug=True)

from models import Employee
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from db_services import execute,closeConnection,commitConnection
from validations import validateEmployeeData

#insert employee details into employee table
@app.route('/employee', methods=['POST'])
def createEmployee(id=None):
    try:
        json = request.json
        print(json)
        name = json['name']
        skills = json['skills']
        designation = json['designation']
        print(designation)
        proj_id = json['proj_id']
        employee = Employee(id, name, skills, designation,proj_id  )
        if name and skills and designation and proj_id and request.method == 'POST':
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO employee(name, skills, designation,proj_id ) VALUES( %s, %s, %s,%s)"
            bindData = (employee.name, employee.skills, employee.designation,employee.proj_id)
            execute(sqlQuery, bindData)
            # conn.commit()
            commitConnection()
            response = jsonify('employee added successfully!')
            response._code = 200
            return response
        else:   
            return showMessage()
    except KeyError as e:
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        return jsonify('something went wrong..!!')

#view all employee details
@app.route('/employee', methods=['GET'])
def getEmployee():
    try:       
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM employee")
        empRows = cursor.fetchall()
        conn.commit()
        respone = jsonify(empRows)
        respone._code = 200
        return respone
    except Exception as e:
        print(e)

#update employee details
@app.route('/employee/<id>', methods=['PUT'])
def updateEmployee(id):
    try:
        json = request.json
        print(json)
        name = json['name']
        skills = json['skills']
        designation = json['designation']
        proj_id = json['proj_id']
        employee = Employee(id, name, skills, designation,proj_id )
        print(employee.id)
        if id and name and skills and designation and  proj_id  and request.method == 'PUT':
            query = "SELECT name FROM employee WHERE id=%s"
            bindData = employee.id
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('employee does not exist')
                return response
            elif data == 1:
                sqlQuery = "UPDATE employee SET name= %s, skills= %s, designation= %s, proj_id= %s WHERE id=%s "
                bindData = (employee.name, employee.skills, employee.designation, employee.proj_id,employee.id)
                execute(sqlQuery, bindData)
                commitConnection()
                respone = jsonify('employee updated successfully!')
                respone._code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except KeyError:
        return jsonify('Some Columns are missing or Mispelled the Column name')

#delete employee details
@app.route('/employee/<id>', methods=['DELETE'])
def deleteEmployee(id, name=None, skills=None,  designation=None, proj_id=None):
    try:
        employee = Employee(id, name, skills, designation,proj_id )
        sqlQuery = "SELECT name FROM employee WHERE id =%s"
        bindData = employee.id
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            commitConnection()
            response = jsonify('employee does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM employee WHERE id =%s"
            bindData = employee.id
            data = execute(sqlQuery, bindData)
            print(data)
            commitConnection()
            respone = jsonify(' employee deleted successfully!')
            respone._code = 200
            return respone
    except Exception as e:
            print(e)
# error handling
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone._code = 404
    return respone
  
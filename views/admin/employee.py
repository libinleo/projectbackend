from models import Employee
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
import uuid
from db_services import execute,closeConnection,commitConnection
from validations import validateEmployeeData

#insert employee details into employee table
@app.route('/employee', methods=['POST'])
def createEmployee():
    try:
        json = request.json
        print(json)
        emp_id= uuid.uuid4()
        name = json['name']
        skills = json['skills']
        designation_id = json['designation_id']
        proj_id = json['proj_id']       
        employee = Employee(emp_id, name, skills, designation_id, proj_id)
        if name and skills and designation_id and proj_id and request.method == 'POST':
            sqlQuery = "INSERT INTO employee(emp_id,name, skills, designation_id, proj_id) VALUES( %s, %s, %s,%s,%s)"
            bindData = (employee.emp_id,employee.name, employee.skills, employee.designation_id, employee.proj_id)
            execute(sqlQuery, bindData)           
            commitConnection()
            response = jsonify('Employee added successfully!')
            response.status_code = 200
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
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

#update employee details
@app.route('/employee/<emp_id>', methods=['PUT'])
def updateEmployee(emp_id):
    try:
        json = request.json
        print(json)
        name = json['name']
        skills = json['skills']
        designation_id = json['designation_id']
        proj_id = json['proj_id']
        employee = Employee(emp_id, name, skills, designation_id, proj_id )
        print(employee.emp_id)
        if emp_id and name and skills and designation_id and proj_id  and request.method == 'PUT':
            query = "SELECT name FROM employee WHERE emp_id=%s"
            bindData = employee.emp_id
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('Employee does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE employee SET name= %s, skills= %s, designation_id= %s, proj_id= %s WHERE emp_id=%s "
                bindData = (employee.name, employee.skills, employee.designation_id, employee.proj_id, employee.emp_id)
                execute(sqlQuery, bindData)
                commitConnection()
                respone = jsonify('Employee updated successfully!')
                respone.status_code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except KeyError:
        return jsonify('Some Columns are missing or Mispelled the Column name')

#delete employee details
@app.route('/employee/<emp_id>', methods=['DELETE'])
def deleteEmployee(emp_id, name=None, skills=None,  designation_id=None, proj_id=None):
    try:
        employee = Employee(emp_id, name, skills, designation_id, proj_id )
        sqlQuery = "SELECT name FROM employee WHERE emp_id =%s"
        bindData = employee.emp_id
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            commitConnection()
            response = jsonify('Employee does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM employee WHERE emp_id =%s"
            bindData = employee.emp_id
            data = execute(sqlQuery, bindData)
            print(data)
            commitConnection()
            respone = jsonify(' Employee deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)
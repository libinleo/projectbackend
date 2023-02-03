from models import Project
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
import uuid
from db_services import execute,closeConnection,commitConnection
from validations import validateProjectData

#insert project details into project table
@app.route('/project', methods=['POST'])
def createProject(id=None):
    try:
        json = request.json
        print(json)
        name = json['name']
        vertical = json['vertical']
        start_date = json['start_date']
        department = json['department']
        allocation = json['allocation']
        project = Project(id, name, vertical, start_date, department, allocation)
        if name and vertical and start_date and department and allocation and request.method == 'POST':
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO project(name, vertical, start_date, department, allocation) VALUES( %s, %s, %s,%s,%s)"
            bindData = (project.name, project.vertical, project.start_date, project.department, project.allocation)
            execute(sqlQuery, bindData)
            # conn.commit()
            commitConnection()
            response = jsonify('project added successfully!')
            response.allocation_code = 200
            return response
        else:   
            return showMessage()
    except KeyError as e:
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        return jsonify('something went wrong..!!')

#view all project details
@app.route('/project', methods=['GET'])
def getProject():
    try:       
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM project")
        empRows = cursor.fetchall()
        conn.commit()
        respone = jsonify(empRows)
        respone.allocation_code = 200
        return respone
    except Exception as e:
        print(e)

#update project details
@app.route('/project/<id>', methods=['PUT'])
def updateProject(id):
    try:
        json = request.json
        print(json)
        name = json['name']
        vertical = json['vertical']
        start_date = json['start_date']
        department = json['department']
        allocation = json['allocation']
        project = Project(id, name, vertical, start_date, department,allocation )
        print(project.id)
        if id and name and vertical and start_date and department and allocation  and request.method == 'PUT':
            query = "SELECT name FROM project WHERE id=%s"
            bindData = project.id
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('project does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE project SET name= %s, vertical= %s, start_date= %s, department= %s,allocation= %s WHERE id=%s "
                bindData = (project.name, project.vertical, project.start_date, project.department,project.allocation, project.id)
                execute(sqlQuery, bindData)
                commitConnection()
                respone = jsonify('Project updated successfully!')
                respone.allocation_code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except KeyError:
        return jsonify('Some Columns are missing or Mispelled the Column name')

#delete project details
@app.route('/project/<id>', methods=['DELETE'])
def deleteProject(id, name=None, vertical=None,  start_date=None, department=None,allocation=None):
    try:
        project = Project(id, name, vertical, start_date, department, allocation)
        sqlQuery = "SELECT name FROM project WHERE id =%s"
        bindData = project.id
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            commitConnection()
            response = jsonify('project does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM project WHERE id =%s"
            bindData = project.id
            data = execute(sqlQuery, bindData)
            print(data)
            commitConnection()
            respone = jsonify(' project deleted successfully!')
            respone.allocation_code = 200
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
    respone.allocation_code = 404
    return respone
  
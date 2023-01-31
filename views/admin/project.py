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
def createProject():
    try:
        json = request.json
        print(json)
        proj_id= uuid.uuid4()
        name = json['name']
        vertical = json['vertical']
        start_date = json['start_date']
        department = json['department'] 
        status = json['status']     
        project = Project(proj_id, name, vertical, start_date, department,status)
        if name and vertical and start_date and department and status and request.method == 'POST':
            sqlQuery = "INSERT INTO project(proj_id,name, vertical, start_date, department,status) VALUES( %s, %s, %s,%s,%s,%s)"
            bindData = (project.proj_id,project.name, project.vertical, project.start_date, project.department,project.status)
            execute(sqlQuery, bindData)           
            commitConnection()
            response = jsonify('project added successfully!')
            response.status_code = 200
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
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

#update project details
@app.route('/project/<proj_id>', methods=['PUT'])
def updateproject(proj_id):
    try:
        json = request.json
        print(json)
        name = json['name']
        vertical = json['vertical']
        start_date = json['start_date']
        department = json['department']
        status = json['status']
        project = Project(proj_id, name, vertical, start_date, department,status )
        print(project.proj_id)
        if proj_id and name and vertical and start_date and department and status  and request.method == 'PUT':
            query = "SELECT name FROM project WHERE proj_id=%s"
            bindData = project.proj_id
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('project does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE project SET name= %s, vertical= %s, start_date= %s, department= %s,status= %s WHERE proj_id=%s "
                bindData = (project.name, project.vertical, project.start_date, project.department,project.status, project.proj_id)
                execute(sqlQuery, bindData)
                commitConnection()
                respone = jsonify('Project updated successfully!')
                respone.status_code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except KeyError:
        return jsonify('Some Columns are missing or Mispelled the Column name')

#delete project details
@app.route('/project/<proj_id>', methods=['DELETE'])
def deleteproject(proj_id, name=None, vertical=None,  start_date=None, department=None,status=None):
    try:
        project = Project(proj_id, name, vertical, start_date, department, status)
        sqlQuery = "SELECT name FROM project WHERE proj_id =%s"
        bindData = project.proj_id
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            commitConnection()
            response = jsonify('project does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM project WHERE proj_id =%s"
            bindData = project.proj_id
            data = execute(sqlQuery, bindData)
            print(data)
            commitConnection()
            respone = jsonify(' project deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)
from models import Project
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from services.db_services import execute,closeConnection,commitConnection
from services.jwt import tocken_required
from services.logger import *
from validations import validateProjectData

#insert project details into project table
@app.route('/project', methods=['POST'])
@tocken_required
def createProject(id=None):
    try:
        json = request.json
        print(json)
        name = json['name']
        start_date = json['start_date']
        department = json['department']
        managerid =json['managerid']
        validation_error = validateProjectData(name,start_date,department,managerid)
        if validation_error:
            return validation_error
        project = Project(id, name,  start_date, department,managerid)
        if name and start_date and department and managerid and request.method == 'POST':
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO project(name,  start_date, department, managerid) VALUES( %s, %s, %s,%s)"
            bindData = (project.name, project.start_date, project.department, project.managerid)
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
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong  id , which is not in table..!!!')
    except Exception as e :
        return jsonify('something went wrong..!!')

#view all project details
@app.route('/project', methods=['GET'])
@tocken_required
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
        return jsonify("error")

#update project details
@app.route('/project/<id>', methods=['PUT'])
@tocken_required
def updateProject(id):
    try:
        json = request.json
        print(json)
        name = json['name']
        start_date = json['start_date']
        department = json['department']
        managerid = json['managerid']
        project = Project(id, name,  start_date, department,managerid )
        print(project.id)
        if id and name and start_date and department and managerid  and request.method == 'PUT':
            query = "SELECT name FROM project WHERE id=%s"
            bindData = project.id
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('project does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE project SET name= %s, start_date= %s, department= %s,managerid= %s WHERE id=%s "
                bindData = (project.name, project.start_date, project.department,project.managerid, project.id)
                execute(sqlQuery, bindData)
                commitConnection()
                respone = jsonify('Project updated successfully!')
                respone.allocation_code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong id , which is not in table..!!!')
    except Exception as e:
        return jsonify('some error')

#delete project details
@app.route('/project/<id>', methods=['DELETE'])
@tocken_required
def deleteProject(id, name=None,  start_date=None, department=None,managerid=None):
    try:
        project = Project(id, name,  start_date, department, managerid)
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
  
#   def demo(id, name, vertical, start_date, department,allocation, request):
#         if not name or not vertical or not start_date or not department or not allocation:
#         response = make_response(jsonify({'message': 'All fields are required'}))
#         response.status_code = 400
#         return response

#     project = Project(id, name, vertical, start_date, department,allocation)
#     if request.method == 'POST':
#         sqlQuery = "INSERT INTO project(name, vertical, start_date, department,allocation) VALUES( %s, %s, %s,%s,%s)"
#         bindData = (project.name, project.vertical, project.department, project.start_date,project.allocation)
#         try:
#             execute(sqlQuery, bindData)
#             commitConnection()
#         except pymysql.err.IntegrityError as e:
#             logger.error(f"IntegrityError: {e}")
#             # return jsonify({'message': 'project already exists with the same name'})
        
#         response = jsonify({'message': 'project added successfully!'})
#         response.status_code = 200
#         return response

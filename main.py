import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request
import uuid
import bcrypt
from flask_jwt_extended import  create_access_token

#Admin-Login
@app.route('/loginadmin', methods=['POST'])
def login():
    try:
        json = request.json
        username = json['username']
        password = json['password']        
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="SELECT name FROM adminlogin WHERE username= '%s' and password='%s'" % (username, password)
            data=cursor.execute(sqlQuery)
            print(data)
            if data==1:
                access_token = create_access_token(identity=username)
                conn.commit()
                return jsonify(message='Login Successful', access_token=access_token),200
            else:
                conn.commit()
                return jsonify('Wrong Credentials... Check Username and Password'), 401
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        cursor.close()
        conn.close()

#Admin-insert employee details into employee table
class CreateEmployee:
    def __init__(self, mydb):
        self.mydb = mydb
    def create_employee(self,emp_id, name, skills,designation_id_id,proj_id):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO employee(emp_id,name, skills,designation_id_id,proj_id) VALUES(%s,%s, %s,%s, %s)", (emp_id,name, skills,designation_id_id,proj_id))
                    conn.commit()
            return jsonify({'message': 'Employee details added successfully!'})
        except pymysql.err.IntegrityError as e:
            return jsonify({'error': 'Duplicate entry or foreign key errror'}), 409
        except Exception as e:
            print(e)
            return jsonify({'error': 'Internal server error'}), 500
@app.route('/employee', methods=['POST'])
def createEmployee():
    json_data = request.json
    emp_id= uuid.uuid4()
    name = json_data.get('name')
    skills = json_data.get('skills') 
    designation_id = json_data.get('designation_id_id')
    proj_id = json_data.get('proj_id')   
    if not all([name, skills]):
        return jsonify({'error': 'Missing required parameters in JSON object'}), 400
    create_emp = CreateEmployee(mydb)
    return create_emp.create_employee(emp_id,name,skills,designation_id,proj_id)

#Admin-View all datas in the employee table
class GetEmployee:
    def __init__(self, mydb):
        self.mydb = mydb
    def get_employee(self):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT * FROM employee")
                    emp_rows = cursor.fetchall()
                    respone = jsonify(emp_rows)
                    respone.status_code = 200
                    return respone
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500
get_emp = GetEmployee(mydb)
@app.route('/employee', methods =['GET'])
def getEmployee():
    return get_emp.get_employee()

#Admin-Update specific employee details in table
class UpdateEmployee:
    def __init__(self, mydb):
        self.mydb = mydb        
    def update_employee(self, emp_id, data):
        try:
            name = data['name']
            skills = data['skills']
            designation_id= data['designation_id']
            proj_id=data['proj_id']
            if emp_id and name and skills and designation_id and proj_id and request.method  == 'PUT':   
                sqlQuery = ("UPDATE employee SET name= %s, skills= %s, designation_id= %s,proj_id= %s WHERE emp_id=%s")
                bindData = ( name, skills, designation_id,proj_id,emp_id)
                conn = self.mydb.connect()
                cursor = conn.cursor()
                cursor.execute(sqlQuery,bindData)
                conn.commit()
                respone = jsonify('Employee updated successfully!')
                respone.status_code = 200
                return respone
            else:
                return jsonify({"error":"Invalid Request"}), 400
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500
        except Exception as e: 
            print("Error: ", e)
            return jsonify({"error": "Internal server error"}), 500
        finally:
            cursor.close()
            conn.close()
update_emp = UpdateEmployee(mydb)
@app.route('/employee/<emp_id>', methods=['PUT'])
def updateEmployee(emp_id):
    data = request.json
    return update_emp.update_employee(emp_id, data)

#Admin-Delete specific employee details from the table
class DeleteEmployee:
    def __init__(self, db):
        self.conn = db.connect()
        self.cursor = self.conn.cursor()        
    def delete_employee(self,emp_id):
        try:
            self.cursor.execute("SELECT emp_id FROM employee WHERE emp_id =%s",(emp_id))
            if self.cursor.rowcount == 0:
                return jsonify(message="Employee not found"), 404
            self.cursor.execute("DELETE FROM employee WHERE emp_id =%s",(emp_id))
            self.conn.commit()
            respone = jsonify(message='Employee deleted successfully!')
            respone.status_code = 200
            return respone
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()
delete_emp = DeleteEmployee(mydb)
@app.route('/employee/<emp_id>', methods=['DELETE'])
def deleteEmployee(emp_id):
    return delete_emp.delete_employee(emp_id)

#Admin-Inserting project details in the table
class CreateProject:
    def __init__(self, mydb):
        self.mydb = mydb
    def create_project(self,proj_id, name, vertical, start_date,department,status):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO project(proj_id,name,vertical, start_date, department,status) VALUES(%s,%s, %s, %s,%s, %s)", (proj_id,name,vertical, start_date, department,status))
                    conn.commit()
            return jsonify({'message': 'Project details added successfully!'})
        except pymysql.err.IntegrityError as e:
            return jsonify({'error': 'Duplicate entry'}), 409
        except Exception as e:
            print(e)
            return jsonify({'error': 'Internal server error'}), 500
@app.route('/project', methods=['POST'])
def createProject():
    json_data = request.json
    proj_id= uuid.uuid4()
    name = json_data.get('name')
    vertical = json_data.get('vertical') 
    start_date = json_data.get('start_date') 
    department = json_data.get('department')
    status = json_data.get('status')  
    if not all([name, vertical, start_date,department,status]):
        return jsonify({'error': 'Missing required parameters in JSON object'}), 400
    create_proj = CreateProject(mydb)
    return create_proj.create_project(proj_id,name, vertical, start_date,department,status)

#Admin-Getting all project details that are asssigned to manager
class GetProject:
    def __init__(self, mydb):
        self.mydb = mydb
    def get_project(self):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT * FROM project")
                    emp_rows = cursor.fetchall()
                    respone = jsonify(emp_rows)
                    respone.status_code = 200
                    return respone
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500
get_proj = GetProject(mydb)
@app.route('/project', methods =['GET'])
def getProject():
    return get_proj.get_project()

#Admin-Reassigning/updating specific project details
class UpdateProject:
    def __init__(self, mydb):
        self.mydb = mydb        
    def update_project(self, proj_id, data):
        try:
            name = data['name']
            vertical = data['vertical']
            start_date= data['start_date']
            department = data['department']
            status= data['status']
            if proj_id and name and vertical and start_date and department and status and  request.method  == 'PUT':   
                sqlQuery = ("UPDATE project SET name= %s, vertical= %s, start_date= %s,department= %s,status= %s WHERE proj_id=%s")
                bindData = ( name, vertical, start_date,department,status,proj_id)
                conn = self.mydb.connect()
                cursor = conn.cursor()
                cursor.execute(sqlQuery,bindData)
                conn.commit()
                respone = jsonify('Project details updated successfully!')
                respone.status_code = 200
                return respone
            else:
                return jsonify({"error":"Invalid Request"}), 400
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500
        except Exception as e: 
            print("Error: ", e)
            return jsonify({"error": "Internal server error"}), 500
        finally:
            cursor.close()
            conn.close()
update_proj = UpdateProject(mydb)
@app.route('/project/<proj_id>', methods=['PUT'])
def updateProject(proj_id):
    data = request.json
    return update_proj.update_project(proj_id, data)

#Admin-Deleting project details
@app.route('/project/<proj_id>', methods=['DELETE'])
def deleteProject(proj_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project WHERE proj_id =%s",(proj_id))
        conn.commit()
        respone = jsonify('Project deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()       
#Manager-Login
@app.route('/loginmanager', methods=['POST'])
def loginManager():
    try:
        json = request.json
        username = json['username']
        password = json['password']       
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="SELECT name FROM employee WHERE username= '%s' and password='%s' and designation_id='manager'" % (username, password)
            data=cursor.execute(sqlQuery)
            print(data)
            if data==1:
                access_token = create_access_token(identity=username)
                conn.commit()
                return jsonify(message=' Manager Verified Login Successful', access_token=access_token),200
            else:
                conn.commit()
                return jsonify('Invalid credentials for manager... Access Denied!'), 401
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return manager_login_invalid_credentials
    finally:
        cursor.close()
        conn.close()               
#Error Showing
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
#Error handling
def manager_login_invalid_credentials(e):
    return jsonify({'status': 'error',
                    'reason': '''Invalid credentials for manager... Access Denied!''' % request.base_url,
                    'code': 404}), 404
# def hash_password(password):
#     password = password.encode('utf-8')
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password, salt)
#     print(hashed_password.decode("utf-8"))
#     return hashed_password.decode('utf-8')    
if __name__ == "__main__":
    app.run()
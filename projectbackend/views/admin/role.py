from models import Role
from flask import jsonify
from flask import request
from app import app
import pymysql
from config import mydb
from db_services import execute,closeConnection,commitConnection
@app.route('/role', methods=['POST'])
def addRole(id=None):
    try:
        json = request.json
        role = json['role']
        roleobj = Role(id, role)
        if role and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO role(role) VALUES( %s)"
            bindData = roleobj.role
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Role is added successfully')
            response.status_code = 200
            return response
        else:
            return "something went wrong"
    except KeyError:
        return jsonify('key error, one value is missing')
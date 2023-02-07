import json
import bcrypt
from models.models import User
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
# from db_services import execute,closeConnection,commitConnection

        
@app.route('/manager', methods=['GET'])
# @tocken_required
def getmanager():
    try:       
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT fullname FROM user where roleid='2'")
        empRows = cursor.fetchall()
        conn.commit()
        respone = jsonify(empRows)
        respone.allocation_code = 200
        return respone
    except Exception as e:
        print(e)
        return jsonify("error")

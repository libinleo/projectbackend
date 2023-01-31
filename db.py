from socket import fromshare
import mysql.connector
from app import app
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "myproject"
)
#Admin login table
mydb_Create_Table_Query = """CREATE TABLE adminlogin
( id int(50) not null,
  name varchar(50) not null,
  username varchar(50) not null,
  password varchar(50) not null,
  CONSTRAINT admin_pk PRIMARY KEY (id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Admin login Table created successfully ")

#Employee designation table
mydb_Create_Table_Query = """CREATE TABLE designation
( designation_id int(50)  null,
  designation varchar(50)  null,
  CONSTRAINT admin_pk PRIMARY KEY (designation_id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Designation Table created successfully ")

#Admin employee Table
mydb_Create_Table_Query = """CREATE TABLE employee
( emp_id int(50) not null PRIMARY KEY,
  name varchar(50) not null,
  skills varchar(50) not null,
  designation_id int(50) not null,
  username  varchar(50) null,
  password  varchar(50)  null,
  proj_id int(50) not null,
  FOREIGN KEY(designation_id) REFERENCES designation(designation_id),
  FOREIGN KEY(proj_id) REFERENCES project(proj_id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Employee Details Table created successfully ")

#Admin Project Table
mydb_Create_Table_Query = """CREATE TABLE project
( proj_id int(50) not null,
  name varchar(50) not null,
  vertical varchar(50) not null,
  start_date varchar(50) not null,
  department varchar(50) not null,
  status varchar(50) not null, 
  CONSTRAINT project_pk PRIMARY KEY (proj_id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Project Table created successfully ")
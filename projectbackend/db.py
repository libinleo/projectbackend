from socket import fromshare
import mysql.connector
from app import app
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "myproject"
)
#Role table
mydb_Create_Table_Query = """CREATE TABLE role
( id int(50) not null auto_increment,
  role varchar(50) not null,
  CONSTRAINT admin_pk PRIMARY KEY (id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Role Table created successfully ")

#User table
mydb_Create_Table_Query = """CREATE TABLE user
( id int(50) not null auto_increment,
  fullname varchar(50) not  null,
  username varchar(50) not  null,
  password varchar(50) not  null,
  role_id int(50) not  null,
  CONSTRAINT admin_pk PRIMARY KEY (id),
  FOREIGN KEY(role_id) REFERENCES role(id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("User Table created successfully ")

#Admin Project Table
mydb_Create_Table_Query = """CREATE TABLE project
( id int(50) not null auto_increment,
  name varchar(50) not null,
  vertical varchar(50) not null,
  start_date varchar(50) not null,
  department varchar(50) not null,
  allocation varchar(50) not null, 
  CONSTRAINT project_pk PRIMARY KEY (id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Project Table created successfully ")

#Manager Employee Table
mydb_Create_Table_Query = """CREATE TABLE employee
( id int(50) not null auto_increment PRIMARY KEY,
  name varchar(50) not null,
  skills varchar(50) not null,
  designation varchar(50) not null,
  proj_id int(50) not null,
  FOREIGN KEY(proj_id) REFERENCES project(id)
)"""
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print("Manager Employee Details Table created successfully ")






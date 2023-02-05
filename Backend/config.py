from app import app
from flaskext.mysql import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
mydb = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['JWT_SECRET_KEY'] = '51f174a913f749dfbd7674fe690770c7'
mydb.init_app(app)
jwt = JWTManager(app)
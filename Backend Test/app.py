# import os
# from flask import Flask
# from flask_cors import CORS
# app = Flask(__name__)
# app.secret_key = "super secret key"
# app.secret_key=os.urandom(24)
# CORS(app)

import bcrypt
from flask import Flask
import bcrypt
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
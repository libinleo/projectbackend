from app import app
from views.manager.employee import *
from views.auth import *
from views.admin.project import *
from views.admin.role import *
from services.logger import *


if __name__ == "__main__":  
    app.run(debug=True)
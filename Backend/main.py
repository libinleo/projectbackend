from app import app
from services.manager.employee import *
from services.auth import *
from services.admin.project import *
from services.admin.role import *
from services.admin.user import *
from services.manager.projectname import *
from services.logger import *


if __name__ == "__main__":  
    app.run(debug=True)
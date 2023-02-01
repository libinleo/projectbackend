from app import app
from views.manager.employee import *
from views.manager.user import *
from views.admin.project import *
from views.admin.role import *

if __name__ == "__main__":  
    app.run(debug=True)
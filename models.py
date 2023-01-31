class Employee:
    def __init__(self,emp_id:str, name:str, skills:str,designation_id:str,username:str,password:str,proj_id:str ):
        self.emp_id=emp_id
        self.name=name
        self.skills=skills
        self.designation_id=designation_id
        self.proj_id=proj_id
        self.username=username
        self.password=password

class Designation:
    def __init__(self,designation_id:str,designation:str ):
        self.designation_id=designation_id
        self.designation=designation

class AdminLogin:
    def __init__(self,id:str,name:str,username:str,password:str ):
        self.id=id
        self.name=name
        self.username=username
        self.password=password

class Project:
    def __init__(self,proj_id:str, name:str, vertical:str,start_date:str,department:str,status:str ):
        self.proj_id=proj_id
        self.name=name
        self.vertical=vertical
        self.start_date=start_date
        self.department=department
        self.status=status
        

      
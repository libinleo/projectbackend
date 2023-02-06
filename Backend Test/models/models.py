class Role:
    def __init__(self,id:int, role:str ):
        self.id=id
        self.role=role

class User:
    def __init__(self,id:int,fullname:str,username:int,password:str,roleid:int ):
        self.id=id
        self.fullname=fullname
        self.username=username
        self.password=password
        self.roleid=roleid

class Project:
    def __init__(self,id:int,name:str,start_date:str,department:str,manager:str ):
        self.id=id
        self.name=name
        self.start_date=start_date
        self.department=department
        self.manager=manager

class Employee:
    def __init__(self,id:int, name:str, skills:str,designation:str,project:str ):
        self.id=id
        self.name=name
        self.skills=skills
        self.designation=designation
        self.project=project
        
        

      
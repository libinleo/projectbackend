class Role:
    def __init__(self,id:int, role:str ):
        self.id=id
        self.role=role

class User:
    def __init__(self,id:int,fullname:str,username:int,password:str,role_id:int ):
        self.id=id
        self.fullname=fullname
        self.username=username
        self.password=password
        self.role_id=role_id

class Project:
    def __init__(self,id:int,name:str,vertical:str,start_date:str,department:str,allocation:str ):
        self.id=id
        self.name=name
        self.start_date=start_date
        self.department=department
        self.allocation=allocation
        self.vertical=vertical

class Employee:
    def __init__(self,id:int, name:str, skills:str,designation:str,proj_id:int ):
        self.id=id
        self.name=name
        self.skills=skills
        self.designation=designation
        self.proj_id=proj_id
        
        

      
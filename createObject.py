import json
from datetime import datetime
from nameko.standalone.rpc import ClusterRpcProxy

config = {"AMQP_URI":"amqp://guest:guest@127.0.0.1:5672//"}

class project:
    def __init__(self, projectname = None, organization=None,description=None, members=None):
        self.projectname = projectname
        self.organization = organization
        self.description = description
        self.timestamp = str(datetime.now())
        #user management members with Fk one to many relationship
        self.members = members 
        self.putinDB()
    def getproject(self,projectID = None):
        with ClusterRpcProxy(config) as rpc:
            if projectID:
                projects = rpc.mongodb_service.getproject(projectID)
                return json.dumps(projects)
            else:
                projects = rpc.mongodb_service.getproject(self.last_project)
                return json.dumps(projects)


    def getprojects(self):
        with ClusterRpcProxy(config) as rpc:
            projects = rpc.mongodb_service.getprojects()
            return json.dumps(projects)
    
    def putinDB(self):
        print(self.__dict__)
        with ClusterRpcProxy(config) as rpc:
            project = rpc.mongodb_service.insertproject(self.__dict__)
            self.last_project = project
            print('from put in db',project)

class mongoDB:
    def __init__(self,**entries):
        self.__dict__.update(entries)
        with ClusterRpcProxy(config) as rpc:
            mongodb = rpc.mongodb_service.initialise(self.__dict__)
    def getdetails(self):
        return json.dumps(self.__dict__)

class aws_key:
    def __init__(self,projectID,**entries):
        if bool(entries):
            self.__dict__.update(entries)
            self.putinDB(projectID)
    def getaws_key(self,projectID):
        with ClusterRpcProxy(config) as rpc:
            aws_key = rpc.mongodb_service.getawskey(projectID)
            return json.dumps(aws_key)
    def putinDB(self,projectID):
        with ClusterRpcProxy(config) as rpc:
            aws_key = rpc.mongodb_service.insertawskey(projectID,self.__dict__)
            return json.dumps(aws_key)

class instance:
    def __init__(self,projectID,**entries):
        self.__dict__.update(entries)
        if bool(entries)
            self.putinDB(projectID)
    def getinstances(self,projectID):
        with ClusterRpcProxy(config) as rpc:
            instance =  rpc.mongodb_service.getinstances(projectID)
            return json.dumps(instance)
    def putinDB(self,projectID):
        with ClusterRpcProxy(config) as rpc:
            instance = rpc.mongodb_service.insertinstances(projectID,self.__dict__)
            return json.dumps(instance)

from nameko.rpc import rpc
from pymongo import MongoClient




class MongoDBService:
    name = "mongodb_service"
    
    @rpc
    def initialise(self,mongoDB):
        print("initialiser: request",mongoDB)
        client = MongoClient(mongoDB["mongoDBurl"])
        global db
        db = client[mongoDB["mongoDBdatabase"]]
        
    @rpc
    def insertproject(self,dicttoinsert):
        print("insertproject: request",dicttoinsert)
        collection = db['project']
        post_id = collection.insert_one(dicttoinsert).inserted_id
        return str(post_id)
    @rpc
    def getprojects(self):
        print("getprojects:")
        projects = []
        collection = db['project']
        for project in collection.find():
            projects.append(project)
        return json.dumps(projects)

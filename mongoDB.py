from nameko.rpc import rpc
from pymongo import MongoClient
import json
from bson.objectid import ObjectId


class MongoDBService:
    name = "mongodb_service"
    client = MongoClient("mongodb://localhost:27017/")
    db = client["terraform-database"]
    @rpc
    def initialise(self,mongoDB):
        print("initialiser: request",mongoDB)
        self.client = MongoClient(mongoDB["mongoDBurl"])
        self.db = self.client[mongoDB["mongoDBdatabase"]]
        
    @rpc
    def insertproject(self,dicttoinsert):
        print("insertproject: request",dicttoinsert)
        collection = self.db['project']
        post_id = collection.insert_one(dicttoinsert).inserted_id
        return str(post_id)
    @rpc
    def getproject(self,projectID):
        print("getproject:",projectID)
        collection = self.db['project']
        document = collection.find_one({'_id': ObjectId(projectID)})
        document['_id'] = str(document['_id'])
        return str(document)
    @rpc
    def getprojects(self):
        print("getprojects:")
        projects = []
        collection = self.db['project']
        for project in collection.find():
            projects.append(project)
        return str(projects)
    @rpc
    def insertawskey(self,projectID,dicttoinsert):
        print("insertawskey: request",dicttoinsert)
        collection_aws = self.db['awskeys']
        collection_project = self.db['project']
        post_id =  collection_aws.insert_one(dicttoinsert).inserted_id
        collection_project.update({'_id':ObjectId(projectID)},{'$set':{'aws_key':post_id}})
        return str(post_id)
    @rpc
    def getawskey(self,projectID):
        print("getawskey: request",projectID)
        collection_project = self.db['project']
        collection_aws = self.db['awskeys']
        document = collection_project.find_one({'_id': ObjectId(projectID)})
        awskeyID = document['aws_key']
        document = collection_aws.find_one({'_id': awskeyID})
        print(document)
        document['_id'] = str(document['_id'])
        return str(document)
    @rpc
    def insertinstances(self,projectID,dicttoinsert):
        print("insertawskey: request",dicttoinsert)
        collection_instance = self.db['instance']
        collection_project = self.db['project']
        for instance in dicttoinsert['instances']:
            post_id =  collection_instance.insert_one(dicttoinsert).inserted_id
            collection_project.update({'_id':ObjectId(projectID)},{'$push':{'instances':post_id}})
        return "done"
    @rpc
    def getawskey(self,projectID):
        print("getawskey: request",projectID)
        collection_project = self.db['project']
        collection_instance = self.db['instance']
        document = collection_project.find_one({'_id': ObjectId(projectID)})
        instances = document['instances']
        instances_tosend = []
        for instance in instances:
            document = collection_instance.find_one({'_id': instance})
            print(document)
            document['_id'] = str(document['_id'])
            instances_tosend.append(document)
        return str(instances_tosend)


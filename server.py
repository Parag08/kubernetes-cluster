from flask import Flask, render_template, request, url_for
from createObject import project, mongoDB,aws_key,instance
import json
import utility
app = Flask(__name__)

Deploy = {}

@app.route("/intialise/",methods=['POST'])
def intialiseMongoDB():
    try:
        global mongo 
        mongo = mongoDB(**request.json)
        return mongo.getdetails()
    except Exception as inst:
        print(inst)
        return "please provide mongoDBurl, mongoDBdatabase"

@app.route("/intialise/",methods=['GET'])
def getMongoDB():
    try:
        return mongo.getdetails()
    except Exception as inst:
        return "mongodb not initialised"
        

@app.route("/project/",methods=['POST'])
def addproject():
    try:
        projectname=request.json["projectname"]
        description=request.json["description"]
        organization=request.json["organization"]
        members=request.json["members"]
        p = project(projectname,description,members,organization)
        projectDict = json.loads(p.getproject())
        return json.dumps(projectDict)
    except Exception as inst:
        print(inst)
        return "error in request: is missing please check input json"

@app.route("/project/",methods=['GET'])
def getprojects():
    try:
        p = project()
        return json.loads(p.getprojects())
    except Exception as inst:
        print inst
        return "make sure database is initialised"
    
@app.route("/project/<projectID>",methods=['GET'])
def getproject(projectID):
    try:
        p = project()
        return json.loads(p.getproject(projectID))
    except Exception as inst:
        print inst
        return "make sure database is initialised"

@app.route("/aws_key/<projectID>",methods=['POST'])
def addaws_key(projectID):
    awskey = aws_key(projectID,**request.json)
    return awskey.getaws_key(projectID)

@app.route("/aws_key/<projectID>",methods=['GET'])
def getaws_key(projectID):
    awskey = aws_key(projectID)
    return awskey.getaws_key(projectID)

@app.route("/instances/<projectID>",methods=['POST'])
def addinstance(projectID):
    instanceObj = instance(projectID,**request.json)
    return instanceObj.getinstances(projectID)

@app.route("/instances/<projectID>",methods=['GET'])
def getinstance(projectID):
    instanceObj = instance(projectID)
    return instanceObj.getinstances(projectID)

@app.route("/deploy/<projectID>",methods=['GET'])
def deployproject(projectID):
    p = project()
    awskey = aws_key(projectID)
    instanceObj = instance(projectID)
    projectDict = json.loads(p.getproject(projectID))
    awsDict = json.loads(awskey.getaws_key(projectID))
    instanceDict =  json.loads(instanceObj.getinstances(projectID))
    utility.deploy(projectDict,awsDict,instanceDict)
    return "deployment started"

if __name__ == "__main__":
    app.run(
        port=8000
    )
